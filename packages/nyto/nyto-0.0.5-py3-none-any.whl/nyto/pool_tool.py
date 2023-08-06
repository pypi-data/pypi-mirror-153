
from nyto import particle
from nyto import folder
from nyto import net_tool
import numpy as np


class net_pool(particle.particle):
	def __init__(self):
		super().__init__()
		self.mod['loss_list']=None
		self.mod['index_list']=None
		self.mod['node_id']=None

	@property
	def loss_list(self):
		return self.mod['loss_list']

	@loss_list.setter
	def loss_list(self, x):
		self.mod['loss_list']=x

	@property
	def index_list(self):
		return self.mod['index_list']

	@index_list.setter
	def index_list(self, x):
		self.mod['index_list']=x

	@property
	def node_id(self):
		return self.mod['node_id']

	@node_id.setter
	def node_id(self, x):
		self.mod['node_id']=x

	def __len__(self):
		return len(self.nn_name_set)

	def __getitem__(self, index):
		if type(index)==int:
			raise KeyError(f"The pool key:{index} must be slice")
		nn_list=self.net[index]
		
		if self.loss_list is None:
			return create_pool(
				nn_list=nn_list,
				node_id=self.node_id
			)
		
		return create_pool(
			nn_list=nn_list,
			loss_list=self.loss[index],
			node_id=self.node_id
		)

	def __repr__(self):
		self.init_loss_index_list()
		return f"pool(loss={self.loss[:]})"

	def apply(self, inset_func, outset_func=folder.copy_func):
		ret_pool=super().apply(inset_func, outset_func)
		ret_pool.loss_list=None
		ret_pool.index_list=None
		return ret_pool

	def dual(self, other, inset_dual_func, outset_func=folder.copy_func):
		if isinstance(other, net_pool):
			return self.pool_dual(other, inset_dual_func)

		ret_pool=super().dual(other, inset_dual_func, outset_func)
		ret_pool.loss_list=None
		ret_pool.index_list=None
		return ret_pool

	def pool_apply(self, pool_func):
		ret_pool=self.copy_without_mod()
		for nn_name in self.nn_name_set:
			ret_pool.mod[nn_name]=pool_func(self.mod[nn_name])
		ret_pool.node_id=self.node_id
		return ret_pool

	def pool_dual(self, other_pool, dual_func):
		ret_pool=self.copy_without_mod()
		for nn_name in self.nn_name_set:
			self_nn=self.mod[nn_name]
			that_nn=other_pool.mod[nn_name]
			ret_pool.mod[nn_name]=dual_func(self_nn,that_nn)
		ret_pool.node_id=self.node_id
		return ret_pool

	@property
	def nn_name_set(self):
		return {
			mod_name for mod_name in self.mod_name_set
			if type(mod_name)==int
		}

	@property
	def net_list(self):
		return [
			self.mod[idx] for idx in range(len(self))
		]

	@property
	def net(self):
		self.init_loss_index_list()
		return pool_net(self)
	
	@property
	def real_net(self):
		return pool_real_net(self)
	
	@property
	def loss(self):
		self.init_loss_index_list()
		return pool_loss(self)

	def reset_node_id(self, node_id):
		return create_pool(
			nn_list=self.net_list,
			node_id=node_id
		)

	def init_loss_index_list(self):
		if self.loss_list is None:
			self.loss_list=self.get_loss_list()

		if self.index_list is None:
			self.index_list=self.get_index_list()

	def get_loss_list(self):
		loss_list=[None]*len(self)
		for nn_name in self.nn_name_set:
			loss=net_tool.net_get(self.mod[nn_name][self.node_id])
			loss_list[nn_name]=loss
		return loss_list

	def get_index_list(self):
		return sorted(
			range(len(self)),
			key=lambda k:self.loss_list[k]
		)
	

class pool_net:
	def __init__(self, pool_ref):
		self.pool_ref=pool_ref

	def __getitem__(self, idx):
		if type(idx)==slice:
			idx_list=self.pool_ref.index_list[idx]
			return [self.pool_ref.mod[idx] for idx in idx_list]
		return self.pool_ref.mod[self.pool_ref.index_list[idx]]
	
	def __setitem__(self, idx, new_net):
		if type(idx)==slice:
			raise KeyError(f'The net key:{idx} must not be slice')
		self.pool_ref.real_net[self.pool_ref.index_list[idx]]=new_net
	
	@property
	def real(self):
		return self.pool_ref.net_list

class pool_real_net:
	def __init__(self, pool_ref):
		self.pool_ref=pool_ref
		
	def __getitem__(self, idx):
		return self.pool_ref.mod[idx]
	
	def __setitem__(self, idx, new_net):
		self.pool_ref.mod[idx]=new_net
		self.pool_ref.loss_list[idx]=net_tool.net_get(
			self.pool_ref.mod[idx][self.pool_ref.node_id]
		)
		self.pool_ref.index_list=None
	
class pool_loss:
	def __init__(self, pool_ref):
		self.pool_ref=pool_ref

	def __getitem__(self, idx):
		if type(idx)==slice:
			idx_list=self.pool_ref.index_list[idx]
			return [self.pool_ref.loss_list[idx] for idx in idx_list]
		return self.pool_ref.loss_list[self.pool_ref.index_list[idx]]

	@property
	def real(self):
		return self.pool_ref.loss_list

	@property
	def mean(self):
		return np.mean(self.pool_ref.loss_list)

	@property
	def std(self):
		return np.std(self.pool_ref.loss_list)

	@property
	def normal(self):
		return (self.real-self.mean)/self.std
	

def create_pool(nn_list, node_id, loss_list=None):
	pool=net_pool()
	for idx,nn in enumerate(nn_list):
		pool.mod[idx]=nn

	pool.node_id=node_id
	pool.loss_list=loss_list
	return pool
