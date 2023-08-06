
from nyto import net
import numpy as np

def _variable_to_np(var):
	return var.values

def _linear(data):
	return data

def _relu(data):
	return np.maximum(0, data)

def _lulu(data):
	'''UC_a1ZYZ8ZTXpjg9xUY9sj8w'''
	return np.log(np.maximum(1,data+1))

def _gaussian(data):
	return np.exp(-data**2)

def _sigmoid(data):
	return 1 / (1 + np.exp(-data))

def _tanh(data):
	return np.tanh(data)

def _col_nor(data):
	return (data-np.mean(data, axis=0))/np.std(data, axis=0)

def _row_nor(data):
	return (
		data-np.mean(data, axis=1)[:,np.newaxis]
	)/np.std(data, axis=1)[:,np.newaxis]

def _softmax(data):
	exp_x=np.exp(data-np.max(data, axis=-1, keepdims=True))
	return exp_x/np.sum(exp_x, axis=-1, keepdims=True)

def _concatenate(*args, axis=1):
	return np.concatenate(args, axis=axis)

def _tile(data, size_tuple):
	return np.tile(data, size_tuple)

def _accuracy(pre_np, target_np):
    return np.mean(pre_np.argmax(axis=1)==target_np.argmax(axis=1))

def _MSE(pre_np, target_np):
	return np.mean(np.square(pre_np-target_np))

def _RMSE(pre_np, target_np):
	return np.sqrt(_MSE(pre_np, target_np))

def _MAE(pre_np, target_np):
	return np.mean(np.abs(pre_np-target_np))

def _MAPE(pre_np, target_np):
	return np.mean(np.abs((pre_np-target_np)/target_np))

def _cross_entropy(pre_np, target_np, epsilon=1e-12):
	pre_np = np.clip(pre_np, epsilon, 1.-epsilon)
	N = pre_np.shape[0]
	ce = - np.sum(target_np*np.log(pre_np)) / N
	return ce

def _binary_cross_entropy(pre_np, target_np, epsilon=1e-12):
	pre_np = np.clip(pre_np, epsilon, 1.-epsilon)
	ce = - np.mean(target_np*np.log(pre_np)+(1-target_np)*np.log(1-pre_np))
	return ce

def _pad(data_np, kernel_shape, mod='valid', constant=0):
	'''
	圖片周圍補值(0)
	[param]
	(np)data_np:          4d_np[data_idx][img_idx][row_idx][col_idx]
	(tuple)kernel_shape:  exp:(3,2)
	(str)mode:            'valid' or 'full'
	(float/int)constant:  填充值
	[return]
	(np)4d_np
	'''
	if mod=='full':
		row_size,col_size=kernel_shape
		row_pad=(row_size-1,row_size-1)
		col_pad=(col_size-1,col_size-1)
		return np.pad(
			data_np,
			((0,0), (0,0), row_pad, col_pad),
			"constant",
			constant_values=(constant, constant)
		)

	if mod=='valid':
		row_size,col_size=kernel_shape
		row_pad_size=int(row_size/2)
		col_pad_size=int(col_size/2)
		row_pad=(row_pad_size,row_pad_size)
		col_pad=(col_pad_size,col_pad_size)
		return np.pad(
			data_np,
			((0,0), (0,0), row_pad, col_pad),
			"constant", 
			constant_values=(constant, constant)
		)

	return data_np

def _fix_pad(data_np, kernel_shape, strides):
	'''
	當移動窗口無法剛好分割時，可以用相鄰的值擴充右邊跟下邊
	[param]
	(np)data_np:          4d_np[data_idx][img_idx][row_idx][col_idx]
	(tuple)kernel_shape:  exp:(3,2)
	(int)strides:         步伐大小(窗口間隔)
	[return]
	(np)4d_np:            [data_idx][img_idx][row_idx][col_idx]
	'''

	(data_shape,img_shape,row_shape,col_shape)=data_np.shape
	(row_split,col_split)=kernel_shape

	row_excess=(row_shape-row_split)%strides
	row_fix=0 if row_excess==0 else strides-row_excess

	col_excess=(col_shape-col_split)%strides
	col_fix=0 if col_excess==0 else strides-col_excess

	return np.pad(
		data_np,
		((0,0), (0,0), (0, row_fix),(0,col_fix)),
		'edge'
	)

def _strided(data_np, kernel_shape, strides=1):
	'''
	將圖片分割成許多小窗口
	[param]
	(np)data_np:          4d_np[data_idx][img_idx][row_idx][col_idx]
	(tuple)kernel_shape:  exp:(3,2)
	(int)strides:         步伐大小(窗口間隔)
	[return]
	(np)6d_np: [data_shape, img_shape, row_stepn, col_stepn, row_split, col_split]
	'''
	data_btyes=data_np.strides[-1]
	(data_shape,img_shape,row_shape,col_shape)=data_np.shape

	(row_split,col_split)=kernel_shape
	col_stepn=((col_shape-col_split)//strides)+1
	row_stepn=((row_shape-row_split)//strides)+1

	return np.lib.stride_tricks.as_strided(
		data_np,
		shape=(data_shape, img_shape, row_stepn, col_stepn, row_split, col_split),
		strides=(
			img_shape*row_shape*col_shape*data_btyes,
			row_shape*col_shape*data_btyes,
			strides*col_shape*data_btyes,
			strides*data_btyes,
			col_shape*data_btyes,
			data_btyes
		)
	)

def _conv_compute(batch_np, kernals_np):
	'''
	計算窗口與kernl的乘積
	[param]
	(np)batch_np:   4d_np[data_shape, batch_shape, row_split, col_split]
	(np)kernals_np: 3d_np[kernal_shape, row_split, col_split]

	[return]
	(np)4d_np:      [data_shape, kernal_shape, img_shape*row_stepn*col_stepn]
	*ps. batch_shape=img_shape*row_stepn*col_stepn
	'''
	return np.einsum('dbij,kij -> dkb', batch_np, kernals_np)

def _convolution(data_np, kernals_np, mod='valid', strides=1):
	'''
	[param]
	(np)data_np:     4d_np[data_shape][img_shape][row_shape][col_shape]
	(np)kernals_np:  3d_np[kernal_shape][row_split][col_split]
	(str)mod:        'full' or 'valid' or 'same'
	(int)strides:    窗口移動間隔
	[return]
	(np)new_data_np: 4d_np[data_shape][conv_shape][row_stepn][col_stepn]
	'''
	(data_shape, img_shape, row_shape, col_shape)=data_np.shape
	(kernal_shape, row_split, col_split)=kernals_np.shape

	# 周圍補0 #
	pad_np=data_np if mod=='same' else _pad(
		data_np=data_np,
		kernel_shape=(row_split,col_split),
		mod=mod,constant=0
	)

	# 切割出窗口 #
	# (6d_np)strided_np
	#[data_shape][img_shape][row_stepn][col_stepn][row_split][col_split]
	strided_np=_strided(
		data_np=pad_np,
		kernel_shape=(row_split,col_split),
		strides=strides
	)

	# 合併窗口的排列方式: 2d排列 -> 1d排列 #
	(
		data_shape, img_shape,
		row_stepn, col_stepn,
		row_split, col_split
	)=strided_np.shape

	batch_shape=img_shape*row_stepn*col_stepn
	batch_np=strided_np.reshape(
		data_shape, batch_shape, row_split, col_split
	)

	# 計算窗口與kernl的乘積 #
	conv_np=_conv_compute(batch_np, kernals_np)

	# 將卷集完變成1d的imgs分開並變成2d的img #
	# before:[data_shape, kernal_shape, img_shape*row_stepn*col_stepn]
	# after:[data_shape, kernal_shape*img_shape, row_stepn, col_stepn]
	conv_shape=img_shape*kernal_shape
	new_data_np=conv_np.reshape(
		data_shape, conv_shape, row_stepn, col_stepn
	)

	return new_data_np

def _max_pooling(data_np, kernel_shape, strides=1):
	'''
	[param]
		(np)data_np:         4d_np[data_shape][img_shape][row_shape][col_shape]
		(tuple)kernel_shape: exp=(2,3)
		(int)strides:        窗口移動間隔
	[return]
		(np)4d_np:           [data_shape][img_shape][row_stepn][col_stepn]
	'''
	fix_np=_fix_pad(
		data_np=data_np,
		kernel_shape=kernel_shape,
		strides=strides
	)

	strided=_strided(
		data_np=fix_np,
		kernel_shape=kernel_shape,
		strides=strides
	)
	return strided.max(axis=(4,5))    

def _average_pooling(data_np, kernel_shape, strides=1):
	'''
	[param]
		(np)data_np:         4d_np[data_shape][img_shape][row_shape][col_shape]
		(tuple)kernel_shape: exp=(2,3)
		(int)strides:        窗口移動間隔
	[return]
		(np)4d_np:           [data_shape][img_shape][row_stepn][col_stepn]
	'''
	fix_np=_fix_pad(
		data_np=data_np,
		kernel_shape=kernel_shape,
		strides=strides
	)

	strided=_strided(
		data_np=fix_np,
		kernel_shape=kernel_shape,
		strides=strides
	)
	return strided.mean(axis=(4,5))

def _global_average_pooling(data_np):
	'''
	[param]
	(np)data_np: 4d_np[data_shape][img_shape][row_shape][col_shape]
	[return]
	(np)2d_np:   [data_shape][feature_shape]
	'''
	return data_np.mean(axis=(2,3))

def _global_max_pooling(data_np):
	'''
	[param]
	(np)data_np: 4d_np[data_shape][img_shape][row_shape][col_shape]
	[return]
	(np)2d_np:   [data_shape][feature_shape]
	'''
	return data_np.max(axis=(2,3))

def _flattening(data_np):
	'''
	[param]
	(np)data_np: 4d_np[data_shape][img_shape][row_shape][col_shape]
	[return]
	(np)2d_np:   [data_shape][feature_shape]
	'''
	data_shape=data_np.shape[0]
	return data_np.reshape(
		data_shape, int(data_np.size/data_shape)
	)

def add_func_to_data_ref(net_ref, node_id, func):
	if not node_id in net_ref.unit:
		net_ref.data[node_id]=func

	if not node_id in net_ref.node_id_set:
		net_ref.node[node_id]=net.data_node(node_id)

class add_func_node(net.add_func_to_net):
	def __init__(self, node_id, func):
		self.node_id=node_id
		self.func=func

	def __call__(self, node_if):
		net_ref=node_if.net_ref
		add_func_to_data_ref(net_ref, self.node_id, self.func)
		return net_ref[self.node_id](node_if)

class variable_to_np(add_func_node):
	def __init__(self): super().__init__(
		node_id='_variable_to_np', func=_variable_to_np
	)

class linear(add_func_node):
	def __init__(self): super().__init__(
		node_id='_linear', func=_linear
	)

class relu(add_func_node):
	def __init__(self): super().__init__(
		node_id='_relu', func=_relu
	)

class lulu(add_func_node):
	def __init__(self): super().__init__(
		node_id='_lulu', func=_lulu
	)

class gaussian(add_func_node):
	def __init__(self): super().__init__(
		node_id='_gaussian', func=_gaussian
	)

class sigmoid(add_func_node):
	def __init__(self): super().__init__(
		node_id='_sigmoid', func=_sigmoid
	)

class tanh(add_func_node):
	def __init__(self): super().__init__(
		node_id='_tanh', func=_tanh
	)

class col_nor(add_func_node):
	def __init__(self): super().__init__(
		node_id='_col_nor', func=_col_nor
	)

class row_nor(add_func_node):
	def __init__(self): super().__init__(
		node_id='_raw_nor', func=_row_nor
	)

class softmax(add_func_node):
	def __init__(self): super().__init__(
		node_id='_softmax', func=_softmax
	)

class global_average_pooling(add_func_node):
	def __init__(self): super().__init__(
		node_id='_global_average_pooling',
		func=_global_average_pooling
	)

class global_max_pooling(add_func_node):
	def __init__(self): super().__init__(
		node_id='_global_max_pooling',
		func=_global_max_pooling
	)

class flattening(add_func_node):
	def __init__(self): super().__init__(
		node_id='_flattening',
		func=_flattening
	)

class max_pooling(net.add_func_to_net):
	'''
	node.data_np >> max_pooling(node.kernel_shape, node.strides) >> 
	'''
	def __init__(self, kernel_shape_node_if, strides=1):
		self.kernel_shape_node_if=kernel_shape_node_if
		self.strides_node_if=strides

	def __call__(self, data_np_node_if):
		net_ref=data_np_node_if.net_ref
		func_node_id='_max_pooling'
		add_func_to_data_ref(
			net_ref=net_ref,
			node_id=func_node_id,
			func=_max_pooling
		)
		return net_ref[func_node_id](
			data_np=data_np_node_if,
			kernel_shape=self.kernel_shape_node_if,
			strides=self.strides_node_if
		)

class average_pooling(net.add_func_to_net):
	'''
	node.data_np >> average_pooling(node.kernel_shape, node.strides) >> 
	'''
	def __init__(self, kernel_shape_node_if, strides=1):
		self.kernel_shape_node_if=kernel_shape_node_if
		self.strides_node_if=strides

	def __call__(self, data_np_node_if):
		net_ref=data_np_node_if.net_ref
		func_node_id='_average_pooling'
		add_func_to_data_ref(
			net_ref=net_ref,
			node_id=func_node_id,
			func=_average_pooling
		)
		return net_ref[func_node_id](
			data_np=data_np_node_if,
			kernel_shape=self.kernel_shape_node_if,
			strides=self.strides_node_if
		)

def to_np(node_if):
	net_ref=node_if.net_ref
	(node_id,func)=('_variable_to_np',_variable_to_np)

	add_func_to_data_ref(net_ref, node_id, func)
	return net_ref[node_id](node_if)

def concatenate(*node_ifs, axis=1):
	net_ref=node_ifs[0].net_ref
	(node_id,func)=('_concatenate',_concatenate)

	add_func_to_data_ref(net_ref, node_id, func)
	return net_ref[node_id](*node_ifs, axis=axis)

def tile(node_if, size_tuple):
	net_ref=node_if.net_ref
	(node_id,func)=('_tile',_tile)

	add_func_to_data_ref(net_ref, node_id, func)
	return net_ref[node_id](node_if, size_tuple)

def MSE(pre_if, target_if):
	net_ref=pre_if.net_ref
	(node_id,func)=('_MSE',_MSE)

	add_func_to_data_ref(net_ref, node_id, func)
	return net_ref[node_id](pre_if, target_if)

def RMSE(pre_if, target_if):
	net_ref=pre_if.net_ref
	(node_id,func)=('_RMSE',_RMSE)

	add_func_to_data_ref(net_ref, node_id, func)
	return net_ref[node_id](pre_if, target_if)

def MAE(pre_if, target_if):
	net_ref=pre_if.net_ref
	(node_id,func)=('_MAE',_MAE)

	add_func_to_data_ref(net_ref, node_id, func)
	return net_ref[node_id](pre_if, target_if)

def MAPE(pre_if, target_if):
	net_ref=pre_if.net_ref
	(node_id,func)=('_MAPE',_MAPE)

	add_func_to_data_ref(net_ref, node_id, func)
	return net_ref[node_id](pre_if, target_if)

def cross_entropy(pre_if, target_if):
	net_ref=pre_if.net_ref
	(node_id,func)=('_cross_entropy',_cross_entropy)

	add_func_to_data_ref(net_ref, node_id, func)
	return net_ref[node_id](pre_if, target_if)

def binary_cross_entropy(pre_if, target_if):
	net_ref=pre_if.net_ref
	(node_id,func)=('_binary_cross_entropy',_binary_cross_entropy)

	add_func_to_data_ref(net_ref, node_id, func)
	return net_ref[node_id](pre_if, target_if)

def accuracy(pre_if, target_if):
	net_ref=pre_if.net_ref
	(node_id,func)=('_accuracy',_accuracy)
	
	add_func_to_data_ref(net_ref, node_id, func)
	return net_ref[node_id](pre_if, target_if)
