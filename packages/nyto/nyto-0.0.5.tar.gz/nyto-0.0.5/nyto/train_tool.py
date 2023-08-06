
from nyto import net_tool
from nyto import pool_tool
import numpy as np
import random

def _net_random_normal(net_ref, tag_set=None):
	def random_mod(mod):
		if type(mod)==np.ndarray:
			return np.random.standard_normal(size=mod.shape)
		return np.random.standard_normal()

	if tag_set is None:
		return net_ref.apply(random_mod)
	return net_ref.tag[tag_set].apply(random_mod)

def _net_random(net_ref, tag_set=None):

	def random_mod(mod):
		if type(mod)==np.ndarray:
			return np.random.random(size=mod.shape)
		return np.random.random()

	if tag_set is None:
		return net_ref.apply(random_mod)
	return net_ref.tag[tag_set].apply(random_mod)

def _net_norm(net_ref, tag_set=None):

	total=0
	def sum_func(mod):
		nonlocal total
		if type(mod)==np.ndarray:
			total+=np.sum(np.square(mod)); return
		total+=mod**2

	if tag_set is None:
		net_ref.apply(sum_func)
		return np.sqrt(total)

	net_ref.tag[tag_set].apply(sum_func)
	return np.sqrt(total)

def _net_unitization(net_ref, tag_set=None):
	norm=_net_norm(net_ref=net_ref, tag_set=tag_set)

	def to_zero(mod):
		if type(mod)==np.ndarray:
			return np.zeros(shape=mod.shape)
		return 0

	def unitization(mod):
		return mod/norm

	if tag_set is None and norm==0:
		return net_ref(to_zero,to_zero)
	if tag_set is None:
		return net_ref.apply(unitization,to_zero)

	if norm==0:
		return net_ref.tag[tag_set].apply(to_zero,to_zero)
	return net_ref.tag[tag_set].apply(unitization,to_zero)

def _net_dropout_bool(net_ref, dropout_rate, dropout_tag_set={'dropout'}):

	def to_one(mod):
		if type(mod)==np.ndarray:
			return np.ones(shape=mod.shape)
		return 1

	def dropout_to_bool(mod):
		if type(mod)==np.ndarray:
			return np.random.random(size=mod.shape)>dropout_rate
		return np.random.random()>dropout_rate

	return net_ref.tag[dropout_tag_set].apply(
		inset_func=dropout_to_bool,
		outset_func=to_one
	)

def random_particle(particle_ref):
	return _net_random(particle_ref)

def normal_particle(particle_ref):
	return _net_random_normal(particle_ref)

def unit_particle(particle_ref):
	random_net=random_particle(particle_ref)
	return _net_unitization(random_net)

def unit_vector(net_ref, tag_set=None):
	random_net=_net_random_normal(net_ref, tag_set)
	return _net_unitization(random_net, tag_set)

def unit_dropout_vector(net_ref, dropout_rate=0.5, dropout_tag_set={'dropout'}):
	bool_net=_net_dropout_bool(net_ref, dropout_rate, dropout_tag_set)
	random_net=_net_random_normal(net_ref)

	dropout_vector=_net_unitization(random_net*bool_net)
	return bool_net, dropout_vector

def step_nn(nn0, unit_nn, node_id, f0=None, delta=0.01, step_rate=1, bound=None):

	delta_nn=unit_nn.all_tag.apply(lambda x: delta*x)
	nn1=nn0.all_tag.dual(delta_nn, lambda x,y: x+y)
	nn2=nn1.all_tag.dual(delta_nn, lambda x,y: x+y)

	f0=net_tool.net_get(nn0[node_id]) if f0 is None else f0
	f1=net_tool.net_get(nn1[node_id])
	f2=net_tool.net_get(nn2[node_id])

	cost1=f1-f0
	cost2=abs(f2-2*f1+f0)

	if cost2==0: return delta_nn*0

	step=(cost1/cost2)*step_rate

	if not bound is None: step=np.clip(step, a_min=-bound, a_max=bound)

	return step*delta_nn

def dropout_step_nn(nn0, random_nn, bool_nn, node_id, delta=0.01, step_rate=1, bound=None):

	drop_nn0=nn0*bool_nn
	drop_unit_nn=_net_unitization(random_nn*bool_nn)

	return step_nn(
		nn0=drop_nn0,
		unit_nn=drop_unit_nn,
		node_id=node_id,
		delta=delta, step_rate=step_rate, bound=bound
	)

def inverse_dropout(nn, dropout_rate):
	return nn.tag[{'dropout'}].apply(lambda x:x*(1-dropout_rate))

def new_pool(node_if, pool_size, random_size=1, keep=False):
	nn=node_if.net_ref
	node_id=node_if.node_id

	if keep:
		nn_list=[
			nn+random_size*_net_random_normal(nn)
			for i in range(pool_size-1)
		]+[nn.copy()]
	else:
		nn_list=[
			nn+random_size*_net_random_normal(nn)
			for i in range(pool_size)
		] 

	return pool_tool.create_pool(nn_list=nn_list, node_id=node_id)

def train_batch(batch_node_list, pool, opt, step=1, epoch=1):
	new_pool=pool.copy()
	for ep in range(epoch):
		for idx, node_if in enumerate(batch_node_list):
			node_id=node_if.node_id
			new_pool=new_pool.reset_node_id(node_id)

			new_pool=opt(new_pool)
			if (idx+1)%step==0: yield (ep, idx), new_pool, opt

	yield (ep, idx), new_pool, opt

class pool_optimization:
	pass

class epso_opt(pool_optimization):
	def __init__(self, threshold=1, dropout_rate=None, step_rate=1, bound=100):
		self.threshold=threshold
		self.dropout_rate=dropout_rate
		self.step_rate=step_rate
		self.bound=bound
		self.delta=0.01
		self.half=False
		self.adjustment=True

	def __call__(self, pool):
		node_id=pool.node_id

		if self.dropout_rate is None:
			seed_size=np.sum(pool.loss.normal<self.threshold)
			if seed_size==0: seed_size=len(pool)
			seed_list=pool.net[:seed_size]

			random_mod=lambda mod,that: (mod+that)/2
			refresh_list=[
				nn.dual(random.choice(seed_list), random_mod)
				for nn in pool.net[seed_size:]
			]

			new_nn_list=[
				nn-step_nn(
					nn0=nn,
					unit_nn=unit_vector(nn),
					node_id=node_id,
					delta=self.delta,
					step_rate=self.step_rate,
					bound=self.bound
				)
				for nn in seed_list+refresh_list
			]
			return pool_tool.create_pool(
				nn_list=new_nn_list,
				node_id=node_id
			)

		if self.half:
			seed_size=np.sum(pool.loss.normal<self.threshold)
			if seed_size==0: seed_size=len(pool)
			seed_list=pool.net[:seed_size]

			random_mod=lambda mod,that: (mod+that)/2
			refresh_list=[
				nn.dual(random.choice(seed_list), random_mod)
				for nn in pool.net[seed_size:]
			]
			
			bool_nn=_net_dropout_bool(
				net_ref=pool.net[0],
				dropout_rate=self.dropout_rate
			)

			new_nn_list=[
				nn-dropout_step_nn(
					nn0=nn,
					random_nn=_net_random_normal(nn),
					bool_nn=bool_nn,
					node_id=node_id,
					delta=self.delta,
					step_rate=self.step_rate,
					bound=self.bound
				)
				for nn in seed_list+refresh_list
			]

			return pool_tool.create_pool(
				nn_list=new_nn_list,
				node_id=node_id
			)
		
		bool_nn=_net_dropout_bool(
			net_ref=pool.net[0],
			dropout_rate=self.dropout_rate
		)
		
		if self.adjustment:
			drop_nn_pool=pool_tool.create_pool(
				nn_list=[
					nn.tag[{'dropout'}].apply(
						lambda x: x*(1-self.dropout_rate)
					)
					for nn in pool.net.real
				],
				node_id=node_id
			)
		else:
			drop_nn_pool=pool_tool.create_pool(
				nn_list=[nn*bool_nn for nn in pool.net.real],
				node_id=node_id
			)
		
		rank_pool=pool_tool.create_pool(
			nn_list=pool.net.real,
			loss_list=drop_nn_pool.loss.real,
			node_id=node_id
		)

		seed_size=np.sum(rank_pool.loss.normal<self.threshold)
		if seed_size==0: seed_size=len(pool)
		seed_list=rank_pool.net[:seed_size]

		random_mod=lambda mod,that: (mod+that)/2
		refresh_list=[
			nn.dual(random.choice(seed_list), random_mod)
			for nn in rank_pool.net[seed_size:]
		]

		new_nn_list=[
			nn-dropout_step_nn(
				nn0=nn,
				random_nn=_net_random_normal(nn),
				bool_nn=bool_nn,
				node_id=node_id,
				delta=self.delta,
				step_rate=self.step_rate,
				bound=self.bound
			)
			for nn in seed_list+refresh_list
		]

		return pool_tool.create_pool(
			nn_list=new_nn_list,
			node_id=node_id
		)
	