
from nyto import particle
import types


def get_and_update_temp(net_ref, node_id, get_temp_dict):
	if node_id in get_temp_dict: return get_temp_dict[node_id]

	get_temp_dict[node_id]=net_ref.node[node_id].get(net_ref, get_temp_dict)

	return get_temp_dict[node_id]


class net_node:
	def __init__(self, node_id):
		self.node_id=node_id

class unit_node(net_node):
	@property
	def connect_node_id_set(self):
		return set()

class mod_node(unit_node):
	def get(self, net_ref, get_temp_dict):
		return net_ref.mod[self.node_id]

class data_node(unit_node):
	def get(self, net_ref, get_temp_dict):
		return net_ref.data[self.node_id]

class connect_node(net_node):
	def __init__(self, node_id, connected_node_id):
		super().__init__(node_id)
		self.connected_node_id=connected_node_id

	def get(self, net_ref, get_temp_dict): 
		return get_and_update_temp(
			net_ref,
			self.connected_node_id,
			get_temp_dict
		)

	@property
	def connect_node_id_set(self):
		return {self.connected_node_id}

class method_node(net_node):
	def __init__(self, node_id, mod_name, method_str, args, kwargs):
		super().__init__(node_id)
		self.mod_name=mod_name
		self.method_str=method_str
		self.input_args=[
			net_node(data.node_id)
			if type(data)==node_interface
			else data 
			for data in args
		]
		self.input_kwargs=dict(
			(key, net_node(value.node_id))
			if type(value)==node_interface
			else (key, value)
			for key, value in kwargs.items()
		)

	def get(self, net_ref, get_temp_dict):
		mod=get_and_update_temp(net_ref, self.mod_name, get_temp_dict)
		new_args=[
			get_and_update_temp(net_ref, data.node_id, get_temp_dict)
			if isinstance(data, net_node)
			else data
			for data in self.input_args
		]
		new_kwargs=dict(
			(
				key, 
				get_and_update_temp(net_ref, value.node_id, get_temp_dict)
			)
			if isinstance(value, net_node)
			else (key, value)
			for key, value in self.input_kwargs.items()
		)

		return_method=getattr(mod, self.method_str)
		
		if callable(return_method):
			return return_method(*new_args, **new_kwargs)
		return return_method

	@property
	def connect_node_id_set(self): 
		input_args_node_id_set={
			data.node_id 
			for data in self.input_args
			if isinstance(data, net_node)
		}
		input_kwargs_node_id_set={
			value.node_id
			for key, value in self.input_kwargs.items()
			if isinstance(value, net_node)
		}
		return set.union(
			input_args_node_id_set,
			input_kwargs_node_id_set,
			{self.mod_name}
		)

class launcher_node(net_node):
	def __init__(self, node_id, get_node_id_set, push_dict):
		super().__init__(node_id)
		self.get_node_id_set=get_node_id_set
		self.push_dict=push_dict

	def get(self, net_ref, get_temp_dict):
		net_ref.push_batch(**dict(
			(push_node_id, net_ref[push_obj.node_id])
			if isinstance(push_obj, net_node)
			else (push_node_id, push_obj)
			for push_node_id, push_obj in self.push_dict.items()
		))
		ret_dict=net_ref.get_batch(self.get_node_id_set)
		return ret_dict

	@property
	def connect_node_id_set(self):
		return set.union(
			self.pre_get_node_id_set,
			self.get_node_id_set,
			set(self.push_dict.keys())
		)

	@property
	def pre_get_node_id_set(self):
		return {
			push_obj.node_id
			for push_node_id, push_obj in self.push_dict.items()
			if isinstance(push_obj, net_node)
		}

class order_node(net_node):
	def __init__(self, node_id, order_list):
		super().__init__(node_id)
		self.order_list=order_list

	def get(self, net_ref, get_temp_dict):
		return [
			net_ref.get_batch({node_id})[node_id]
			for node_id in self.order_list
		]

	@property
	def connect_node_id_set(self):
		return set(self.order_list)

class node_interface:
	def __init__(self, net_ref, node_id):
		self.net_ref = net_ref
		self.node_id = node_id

	def __getattr__(self, method_str):
		def warp(*args, **kwargs):
			for data in args:
				if type(data)!=node_interface: continue
				if not self.net_ref is data.net_ref:
					raise ValueError('net_ref should be the same!')

			for key, values in kwargs.items():
				if type(values)!=node_interface: continue
				if not self.net_ref is values.net_ref:
					raise ValueError('net_ref should be the same!')

			new_id=self.net_ref.new_id()
			mod_name=self.node_id

			new_method_node=method_node(
				new_id, mod_name,
				method_str, args, kwargs
			)

			self.net_ref.node[new_id]=new_method_node
			return node_interface(self.net_ref, new_id)

		return warp

	def __rshift__(self, input_node_if):

		if isinstance(input_node_if, add_func_to_net):
			return input_node_if(self)

		if not input_node_if.node_id in self.net_ref.unit.name_set:
			self.net_ref[input_node_if.node_id]=self
			return self.net_ref[input_node_if.node_id]

		return input_node_if(self)

	def __call__(self, *args, **kwargs):
		return self.__getattr__('__call__')(*args, **kwargs)

	def __getitem__(self, key):
		return self.__getattr__('__getitem__')(key)

	# 定義 取負數運算
	def __neg__(self):
		return self.__getattr__('__neg__')()

	# 定義 ** 運算
	def __pow__(self, that):
		return self.__getattr__('__pow__')(that)

	# 定義 + 運算
	def __add__(self, that):
		return self.__getattr__('__add__')(that)
	def __radd__(self, that):
		return self.__getattr__('__radd__')(that)

	# 定義 - 運算
	def __sub__(self, that):
		return self.__getattr__('__sub__')(that)
	def __rsub__(self, that):
		return self.__getattr__('__rsub__')(that)

	# 定義 * 運算
	def __mul__(self, that):
		return self.__getattr__('__mul__')(that)
	def __rmul__(self, that):
		return self.__getattr__('__rmul__')(that)

	# 定義 / 運算
	def __truediv__(self, that):
		return self.__getattr__('__truediv__')(that)
	def __rtruediv__(self, that):
		return self.__getattr__('__rtruediv__')(that)


class net(particle.particle):
	def __init__(self):
		super().__init__()
		self.var_dict['node']={}
		self.var_dict['data']={}
		self.var_dict['id_count']=0

	def __repr__(self):
		return f"net(mod={self.info.mod}, data={self.info.data})"

	def __getitem__(self, node_id):
		return node_interface(self, node_id)

	def __setitem__(self, node_id, value):
		
		if type(value)==node_interface:
			if node_id in self.data_name_set:
				raise KeyError(f"data {node_id} can not overwrite!")   
			
			if node_id in self.mod_name_set:
				update=get_and_update_temp(self, value.node_id, {})
				self.unit[node_id]=update
				return
				
			self.node[node_id]=connect_node(node_id, value.node_id)
			return
		
		if node_id in self.unit:
			self.unit.remove(node_id)
			self[node_id]=value
			return

		if isinstance(value, add_unit_to_net):
			value(self, node_id)
			return
		
		self.mod[node_id]=value
		self.node[node_id]=mod_node(node_id)
	
	@property
	def info(self):
		return user_info_interface(self)

	@property
	def unit(self):    
		return unit_interface(self)

	@property
	def data(self):
		return self.var_dict['data']

	@property
	def data_name_set(self):
		return set(self.data.keys())

	@property
	def node(self):
		return self.var_dict['node']

	@property
	def node_id_set(self):
		return set(self.node.keys())

	def new_id(self):
		while True:
			return_id=self.var_dict['id_count']
			self.var_dict['id_count']+=1
			if return_id in self.node_id_set:
				continue
			return return_id
	
	def get_batch(self, node_id_set):

		return_dict={}
		get_temp_dict={}
		for node_id in node_id_set:
			return_dict[node_id]=get_and_update_temp(
				net_ref=self,
				node_id=node_id,
				get_temp_dict=get_temp_dict
			)
		return return_dict

	def push_batch(self, **push_dict):
		get_node_id_set={
			push_obj.node_id
			for push_node_id, push_obj in push_dict.items()
			if push_node_id in self.mod_name_set
			and isinstance(push_obj, node_interface)
		}
		
		get_dict=self.get_batch(get_node_id_set)
		
		new_push_dict=dict(
			(push_node_id, get_dict[push_obj.node_id])
			if push_node_id in self.mod_name_set
			and isinstance(push_obj, node_interface)
			else (push_node_id, push_obj)
			for push_node_id, push_obj in push_dict.items()
		)
		
		for push_node_id, push_obj in new_push_dict.items():
			self[push_node_id]=push_obj
	
	def push_get(self, node_id_set, **push_dict):
		self.push_batch(**push_dict)
		return self.get_batch(node_id_set)

	def launcher(self, *get_tuple, **push_dict):
		new_id=self.new_id()
		get_set={node_if.node_id for node_if in get_tuple}

		remove_node_interface_dict={}
		for push_node_id, push_obj in push_dict.items():
			if type(push_obj)==node_interface:
				push_obj=net_node(push_obj.node_id)
			remove_node_interface_dict[push_node_id]=push_obj

		self.node[new_id]=launcher_node(
			new_id, get_set, remove_node_interface_dict
		)
		return self[new_id]

	def order(self, *order_tuple):
		new_id=self.new_id()
		order_list=[node_if.node_id for node_if in order_tuple]
		self.node[new_id]=order_node(new_id, order_list)
		return self[new_id]

class unit_interface:

	def __init__(self, net_ref):
		self.ref=net_ref

	def __getitem__(self, node_id):
		if node_id in self.ref.data:
			return self.ref.data[node_id]
		return self.ref.mod[node_id]

	def __setitem__(self, node_id, value):
		if not node_id in self:
			raise KeyError(f"unit {node_id} can not find")

		if node_id in self.ref.data:
			self.ref.data[node_id]=value; return
		self.ref.mod[node_id]=value

	def __contains__(self, unit_name):
		return unit_name in self.name_set
	
	def remove(self, unit_name):
		if unit_name in self.ref.mod_name_set:
			self.ref.remove_mod(unit_name)
			del self.ref.node[unit_name]
			return
			
		if unit_name in self.ref.data_name_set:
			del self.ref.data[unit_name]
			del self.ref.node[unit_name]
			return
		
	@property
	def name_set(self):
		return self.ref.data_name_set|self.ref.mod_name_set

def _remove_hide_name(name_set):
	return {
		name
		for name in name_set
		if type(name)==str and name[0]!='_'
	}

class user_info_interface:
	def __init__(self, net_ref):
		self.ref=net_ref
	
	@property
	def unit(self):
		return _remove_hide_name(self.ref.unit.name_set)
	
	@property
	def mod(self):
		return _remove_hide_name(self.ref.mod_name_set)
	
	@property
	def data(self):
		return _remove_hide_name(self.ref.data_name_set)
	
	@property
	def node(self):
		return _remove_hide_name(self.ref.node_id_set)
	
	def is_unit(self, unit_name):
		return unit_name in self.unit
	
	def is_mod(self, mod_name):
		return mod_name in self.mod
	
	def is_data(self, data_name):
		return data_name in self.data
	
	def is_connect_node(self, node_id):
		return isinstance(self.ref.node[node_id], connect_node)
	
	def connect_id_set(self, node_id):
		return _remove_hide_name(
			self.ref.node[node_id].connect_node_id_set
		)
	
	def mod_is_fix(self, mod_name):
		return self.ref.mod[mod_name].is_fix

class add_unit_to_net:
	def __call__(self, net_ref, node_id):
		pass

class static_unit(add_unit_to_net):
	def __init__(self, data):
		self.data=data

	def __call__(self, net_ref, node_id):
		net_ref.data[node_id]=self.data
		net_ref.node[node_id]=data_node(node_id)

class add_func_to_net:
	def __call__(self, node_if):
		pass

def create_connecter(net_ref):
	class node_connecter:
		def __getattr__(self, node_id):
			return net_ref[node_id]
		def __setattr__(self, node_id, that):
			net_ref[node_id]=that
	return node_connecter()

def new_net(**push_dict):
	nn=net()
	nn.push_batch(**push_dict)
	return nn, create_connecter(nn)
