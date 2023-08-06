from nyto import net
from nyto import folder
import random
import numpy as np

new_net=net.new_net
create_connecter=net.create_connecter


def net_get(node_if):
	node_id=node_if.node_id	
	return net.get_and_update_temp(
		net_ref=node_if.net_ref,
		node_id=node_id,
		get_temp_dict={}
	)

def net_gets(*node_ifs):
	id_dict={} # {net_id: {node_id1, node_id2}, ...}
	ref_dict={} # {net_id: net_ref}
	for node_if in node_ifs:
		net_id=id(node_if.net_ref)
		node_id=node_if.node_id

		if not net_id in id_dict:
			id_dict[net_id]=set()
			ref_dict[net_id]=node_if.net_ref

		id_dict[net_id]|={node_id}

	ret_dict={} # {net_id: {node_id: node_ret } }
	for net_id,node_id_set in id_dict.items():
		# ret={node_id: node_ret }
		ret=ref_dict[net_id].get_batch(node_id_set)
		ret_dict[net_id]=ret

	return tuple(
		ret_dict[id(node_if.net_ref)][node_if.node_id]
		for node_if in node_ifs
	)

def get(*node_ifs):
	if len(node_ifs)==1:
		return net_get(node_ifs[0])
	return net_gets(*node_ifs)


class mod_with_tag(net.add_unit_to_net):
	def __init__(self, mod, tag_set={'def'}):
		self.mod=mod
		self.tag_set=tag_set

	def __call__(self, net_ref, node_id):
		net_ref.mod[node_id]=self.mod

		for add_tag in self.tag_set:
			if not add_tag in net_ref.tag_name_set:
				net_ref.tag[add_tag]={node_id}; continue
			net_ref.group_dict[add_tag]|={node_id}

		net_ref.node[node_id]=net.mod_node(node_id)

def add_mod(mod, tag_set):
	return mod_with_tag(mod=mod, tag_set=tag_set)

def add_data(data):
	return net.static_unit(data=data)

def _get_data_size(push_dict):
	data=list(push_dict.values())[0]
	if isinstance(data, net.node_interface):
		return len(get(data))
	return len(data)

def batch_launcher(nn, batch_push, get, batch_size, static_push={}, shuffle=True):

	data_size=_get_data_size(batch_push)
	idx_list=list(range(data_size))

	if shuffle:
		if data_size%batch_size!=0:
			excess_n=batch_size-data_size%batch_size
			idx_list+=random.sample(idx_list, excess_n)

		random.shuffle(idx_list)

	batch_n=int(len(idx_list)/batch_size)
	idx_np=np.array(idx_list).reshape(batch_n, batch_size)

	launcher_node_list=[]
	for idx in idx_np:
		push={
			k:v[idx] for k,v in batch_push.items()
		}
		push={**push, **static_push}

		batch_node=nn.launcher(*get, **push)
		launcher_node_list.append(batch_node)

	return launcher_node_list

def fix_mod(net_ref, node_id):
	net_ref.mod[node_id].fix()

def unfix_mod(net_ref, node_id):
	net_ref.mod[node_id].unfix()

def free_unused_nodes(net_ref, user_node_id_set):
	used_node_id_set=net_ref.unit.name_set

	def visit_node(node_id_set):
		nonlocal used_node_id_set
		used_node_id_set|=node_id_set

		for node_id in node_id_set:
			next_node_id_set=net_ref.node[node_id].connect_node_id_set
			if len(next_node_id_set)==0: continue
			visit_node(next_node_id_set)

	visit_node(user_node_id_set)
	unused_node_id_set=net_ref.node_id_set-(net_ref.node_id_set&used_node_id_set)
	for unused_node_id in unused_node_id_set:
		del net_ref.node[unused_node_id]
	return unused_node_id_set
