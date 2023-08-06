
from nyto import particle
import numpy as np
from nyto import unit_function as uf

class layer(particle.particle):
	pass

class variable_layer(layer):
	'''
	[mod]
	(np)values: tag(variable)
	'''
	def __getitem__(self, key):
		return self.values[key]
    
	def __repr__(self):
		return f"variable_layer({self.values})"
    
	@property
	def values(self):
		return self.mod['values']
    
	@values.setter
	def values(self, new_var):
		self.mod['values']=new_var

        
class nn_layer(layer):
	'''
	[mod]
	(np)weights: tag(weights, dropout)
	(np)bias:    tag(bias)
	'''
	def __call__(self, input_data):
		if type(input_data)==np.ndarray:
			input_len=input_data.shape[0]
			bias_np=np.tile(self.bias, (input_len,1))
			return_np=input_data.dot(self.weights)+bias_np
			return return_np

		if type(input_data)==variable_layer:
			return self(input_data.values)

		raise ValueError("input data type is not correct!")

	def __repr__(self):
		return f"nn_layer({self.weights},\n{self.bias})"

	@property
	def weights(self):
		return self.mod['weights']

	@weights.setter
	def weights(self, new_weights):
		self.mod['weights'] = new_weights

	@property
	def bias(self):
		return self.mod['bias']

	@bias.setter
	def bias(self, new_bias):
		self.mod['bias'] = new_bias
		

class lstm_layer(layer):
	'''
	[mod]
		(np)compute_nn:        tag(weights, dropout, bias)
		(np)input_gate:        tag(weights, dropout, bias)
		(np)output_gate:       tag(weights, dropout, bias)
		(np)forget_gate:       tag(weights, dropout, bias)
		(np)init_memory:       tag(init_state, variable)
		(np)init_last_output:  tag(init_state, variable)
	[var]
		(def)compute_func:     _tanh
		(def)input_gate_func:  _sigmoid
		(def)output_gate_func: _sigmoid
		(def)forget_gate_func: _sigmoid
	'''
	def run(self, input_data, memory_np, last_output):
		merge_input=uf._concatenate(input_data, memory_np, last_output)

		compute_output=self.compute_func(self.compute_nn(merge_input))
		input_gate_output=self.input_gate_func(self.input_gate(merge_input))
		output_gate_output=self.output_gate_func(self.output_gate(merge_input))
		forget_gate_output=self.forget_gate_func(self.forget_gate(merge_input))

		new_memory=compute_output*input_gate_output+forget_gate_output*memory_np
		output_np=self.compute_func(new_memory)*output_gate_output

		return output_np, new_memory

	def __call__(self, input_data):
		return_data_list=[]
		last_output=self.init_last_output.values
		memory_np=self.init_memory.values
		for this_times_data_np in input_data:
			this_times_data_np=this_times_data_np[np.newaxis,:]
			last_output, memory_np=self.run(
				this_times_data_np, memory_np, last_output
			)
			return_data_list.append(last_output.squeeze(0))

		return np.array(return_data_list)
	
	@property
	def compute_nn(self): return self.mod['compute_nn']
	@compute_nn.setter
	def compute_nn(self,x): self.mod['compute_nn']=x
	
	@property
	def input_gate(self): return self.mod['input_gate']
	@input_gate.setter
	def input_gate(self,x): self.mod['input_gate']=x
	
	@property
	def output_gate(self): return self.mod['output_gate']
	@output_gate.setter
	def output_gate(self,x): self.mod['output_gate']=x
	
	@property
	def forget_gate(self): return self.mod['forget_gate']
	@forget_gate.setter
	def forget_gate(self,x): self.mod['forget_gate']=x

	@property
	def init_memory(self): return self.mod['init_memory']
	@init_memory.setter
	def init_memory(self,x): self.mod['init_memory']=x
	
	@property
	def init_last_output(self): return self.mod['init_last_output']
	@init_last_output.setter
	def init_last_output(self,x): self.mod['init_last_output']=x
	
	@property
	def compute_func(self): return self.var_dict['compute_func']
	@compute_func.setter
	def compute_func(self,x): self.var_dict['compute_func']=x
	
	@property
	def input_gate_func(self): return self.var_dict['input_gate_func']
	@input_gate_func.setter
	def input_gate_func(self,x): self.var_dict['input_gate_func']=x

	@property
	def output_gate_func(self): return self.var_dict['output_gate_func']
	@output_gate_func.setter
	def output_gate_func(self,x): self.var_dict['output_gate_func']=x
	
	@property
	def forget_gate_func(self): return self.var_dict['forget_gate_func']
	@forget_gate_func.setter
	def forget_gate_func(self,x): self.var_dict['forget_gate_func']=x


class conv_layer(layer):
	'''
	[mod]
		(np)kernals_np: tag(weights, convolution)
		(np)kernals_np: 3d_np[kernal_shape, row_split, col_split]
	[var]
		(def)conv_func: _convolution
		(str)pad_mod:   'full' or 'valid' or 'same'
		(int)strides:   窗口移動間隔
	'''
	
	def __call__(self, data_4d_np):
		return self.conv_func(
			data_np=data_4d_np,
			kernals_np=self.kernals_np,
			mod=self.pad_mod,
			strides=self.strides
		)

	@property
	def kernals_np(self): return self.mod['kernals_np']
	@kernals_np.setter
	def kernals_np(self, x): self.mod['kernals_np']=x
	
	@property
	def conv_func(self): return self.var_dict['_convolution']
	@conv_func.setter
	def conv_func(self, x): self.var_dict['_convolution']=x
	
	@property
	def pad_mod(self): return self.var_dict['pad_mod']
	@pad_mod.setter
	def pad_mod(self, x): self.var_dict['pad_mod']=x

	@property
	def strides(self): return self.var_dict['strides']
	@strides.setter
	def strides(self, x): self.var_dict['strides']=x


def new_variable_layer(structure, init_values=0, random_size=None, dropout=False):
	new_variable = variable_layer()
	if random_size is None:
		new_variable.values=np.zeros(structure)+init_values
		if dropout: new_variable.tag['dropout']={'values'}
		new_variable.tag['variable']={'values'}
		return new_variable

	new_variable.values=np.random.standard_normal(size=structure)*random_size
	new_variable.values+=init_values
	if dropout: new_variable.tag['dropout']={'values'}
	new_variable.tag['variable']={'values'}
	return new_variable

def np_to_variable_layer(variable_np, dropout=False):
	new_variable = variable_layer()
	new_variable.values=variable_np
	if dropout: new_variable.tag['dropout']={'values'}
	new_variable.tag['variable']={'values'}
	return new_variable

def new_nn_layer(structure, init_values=(0,0), random_size=(None,None), dropout=True):
	new_nn = nn_layer()

	if random_size[0] is None:
		new_nn.weights=np.zeros(structure)+init_values[0]
	else:
		new_nn.weights=np.random.standard_normal(size=structure)*random_size[0]
		new_nn.weights+=init_values[0]

	if random_size[1] is None:
		new_nn.bias=np.zeros((1,structure[1]))+init_values[1]
	else:
		new_nn.bias=np.random.normal(size=(1,structure[1]))*random_size[1]
		new_nn.bias+=init_values[1]
	
	if dropout: new_nn.tag['dropout'] = {'weights'}
	new_nn.tag['weights'] = {'weights'}
	new_nn.tag['bias'] = {'bias'}
	
	return new_nn

def new_lstm_layer(
	structure, 
	compute_nn_init_values=(0,0),
	compute_nn_random_size=(None,None),
	compute_nn_dropout=True,
	
	input_gate_init_values=(0,0),
	input_gate_random_size=(None,None),
	input_gate_dropout=True,

	output_gate_init_values=(0,0),
	output_gate_random_size=(None,None),
	output_gate_dropout=True,

	forget_gate_init_values=(0,0),
	forget_gate_random_size=(None,None),
	forget_gate_dropout=True,

	init_memory_init_values=0,
	init_memory_random_size=None, 

	init_last_output_init_values=0,
	init_last_output_random_size=None,

	compute_func=uf._tanh,
	input_gate_func=uf._sigmoid,
	output_gate_func=uf._sigmoid,
	forget_gate_func=uf._sigmoid
):
    
	return_lstm=lstm_layer()

	(input_size, output_size)=structure
	nn_structure=(input_size+output_size*2, output_size)
	variable_structure=(1, output_size)

	return_lstm.mod['compute_nn']=new_nn_layer(
		nn_structure, compute_nn_init_values, compute_nn_random_size,
		dropout=compute_nn_dropout
	)
	return_lstm.mod['input_gate']=new_nn_layer(
		nn_structure, input_gate_init_values, input_gate_random_size,
		dropout=input_gate_dropout
	)
	return_lstm.mod['output_gate']=new_nn_layer(
		nn_structure, output_gate_init_values, output_gate_random_size,
		dropout=output_gate_dropout
	)
	return_lstm.mod['forget_gate']=new_nn_layer(
		nn_structure, forget_gate_init_values, forget_gate_random_size,
		dropout=forget_gate_dropout
	)

	init_memory_variable_layer=new_variable_layer(
		variable_structure, init_memory_init_values, init_memory_random_size
	)
	init_memory_variable_layer.tag['init_state']={'values'}
	return_lstm.mod['init_memory']=init_memory_variable_layer

	init_last_output_variable_layer=new_variable_layer(
		variable_structure,
		init_last_output_init_values,
		init_last_output_random_size
	)
	init_last_output_variable_layer.tag['init_state']={'values'}
	return_lstm.mod['init_last_output']=init_last_output_variable_layer

	return_lstm.var_dict['compute_func']=compute_func
	return_lstm.var_dict['input_gate_func']=input_gate_func
	return_lstm.var_dict['output_gate_func']=output_gate_func
	return_lstm.var_dict['forget_gate_func']=forget_gate_func

	return return_lstm

def new_random_lstm(structure, init_values=(0,0), random_size=(None,None), dropout=True):
	return new_lstm_layer(
		structure, 
		compute_nn_init_values=init_values,
		compute_nn_random_size=random_size,
		compute_nn_dropout=dropout,

		input_gate_init_values=init_values,
		input_gate_random_size=random_size,
		input_gate_dropout=dropout,

		output_gate_init_values=init_values,
		output_gate_random_size=random_size,
		output_gate_dropout=dropout,

		forget_gate_init_values=init_values,
		forget_gate_random_size=random_size,
		forget_gate_dropout=dropout,

		init_memory_init_values=init_values[1],
		init_memory_random_size=random_size[1], 

		init_last_output_init_values=init_values[1],
		init_last_output_random_size=random_size[1],

		compute_func=uf._tanh,
		input_gate_func=uf._sigmoid,
		output_gate_func=uf._sigmoid,
		forget_gate_func=uf._sigmoid
	)

def new_conv_layer(
	structure, init_values=0, random_size=None, dropout=False,
	pad_mod='valid', strides=1
):
	new_conv = conv_layer()
	new_conv.conv_func=uf._convolution
	new_conv.pad_mod=pad_mod
	new_conv.strides=strides
	
	if random_size is None:
		new_conv.kernals_np=np.zeros(structure)+init_values
		if dropout: new_conv.tag['dropout']={'kernals_np'}
		new_conv.tag['weights']={'kernals_np'}
		new_conv.tag['convolution']={'kernals_np'}
		return new_conv

	new_conv.kernals_np=np.random.standard_normal(size=structure)*random_size
	new_conv.kernals_np+=init_values
	if dropout: new_conv.tag['dropout']={'kernals_np'}
	new_conv.tag['weights']={'kernals_np'}
	new_conv.tag['convolution']={'kernals_np'}
	return new_conv
	