
from copy import deepcopy
import types


class folder:
	def __init__(self):
		self.mod_dict={}
		self.group_dict={}
		self.var_dict={}
		
		self.mod_dict['_is_fix']=False

	def __repr__(self):
		return f"folder({self.mod_dict})"

	@property
	def is_fix(self):
		return self.mod_dict['_is_fix']

	@is_fix.setter
	def is_fix(self, status):
		self.mod_dict['_is_fix']=status

	def fix(self):
		self.is_fix=True

	def unfix(self):
		self.is_fix=False
		self.mod_dict=deepcopy(self.mod_dict)

	@property
	def mod_name_set(self):
		return set(self.mod_dict.keys())

	@property
	def mod_with_tag_set(self):
		return self.search_mod_name_set(self.tag_name_set)

	@property
	def mod_without_tag_set(self):
		return self.mod_name_set-self.mod_with_tag_set

	@property
	def tag_name_set(self):
		return set(self.group_dict.keys())

	@property
	def tag(self):
		return tag_interface(self)

	@property
	def all_tag(self):
		return self.tag[self.tag_name_set]

	@property
	def mod(self):
		return mod_interface(self)

	def search_mod_name_set(self, tag_set):
		mod_name_set=set()
		tag_name_set=self.tag_name_set
		for tag_name in tag_set:
			if not tag_name in tag_name_set: continue
			mod_name_set|=self.group_dict[tag_name]
		return mod_name_set

	def remove_mod(self, mod_name):
		if mod_name not in self.mod_dict: return

		del self.mod_dict[mod_name]
		for tag_name in list(self.tag_name_set):
			if self.group_dict[tag_name] == {mod_name}:
				del self.group_dict[tag_name]; continue
			self.group_dict[tag_name].discard(mod_name)

	def copy(self):
		return self.all_tag.apply(copy_func, copy_func)

	def copy_without_mod(self):
		ret=type(self)()
		ret.var_dict=self.var_dict
		ret.group_dict=self.group_dict
		return ret


class mod_interface:
	def __init__(self, folder_ref):
		self.folder_ref=folder_ref

	def __getitem__(self, mod_name):
		return self.folder_ref.mod_dict[mod_name]

	def __setitem__(self, mod_name, mod):
		self.folder_ref.remove_mod(mod_name)
		self.folder_ref.mod_dict[mod_name]=mod

		if not isinstance(mod, folder): return

		for tag_name in mod.tag_name_set:
			if tag_name in self.folder_ref.tag_name_set:
				self.folder_ref.group_dict[tag_name].add(mod_name)
			else:
				self.folder_ref.tag[tag_name]={mod_name}


class tag_interface:
	def __init__(self, folder_ref):
		self.folder_ref = folder_ref

	def __repr__(self):
		return f"tag(tag_set={self.folder_ref.tag_name_set})"

	def __getitem__(self, tag_set):
		if type(tag_set)==str: tag_set={tag_set}
		return tag_operate(self.folder_ref, tag_set)

	def __setitem__(self, tag_name, group_set):
		if len(group_set-self.folder_ref.mod_name_set)>0:
			raise ValueError('group_set have undef mod!')
		self.folder_ref.group_dict[tag_name]=group_set


def copy_func(mod):
	return deepcopy(mod)

def zero_func(mod):
	if type(mod)==types.MethodType: return mod
	if type(mod)==types.FunctionType: return mod
	if type(mod)==types.MethodWrapperType: return mod
	return mod*0


class tag_operate:
	def __init__(self, folder_ref, tag_set):
		self.folder_ref=folder_ref
		self.tag_set=tag_set

	def apply(self, inset_func, outset_func=copy_func):        
		return apply_operate(
			ref=self.folder_ref,
			tag_set=self.tag_set,
			inf=inset_func,
			outf=outset_func
		)

	def dual(self, other, inset_dual_func, outset_func=copy_func):       
		return dual_operate(
			left=self.folder_ref,
			right=other,
			tag_set=self.tag_set,
			dual_inf=inset_dual_func,
			outf=outset_func
		)


def not_tag_apply_operate(ref, func):
	new_folder=ref.copy_without_mod()

	if ref.is_fix:
		new_folder.mod_dict=ref.mod_dict
		return new_folder

	mod_without_tag_set=ref.mod_without_tag_set
	for mod_name, mod in ref.mod_dict.items():
		if mod_name in mod_without_tag_set:
			new_folder.mod_dict[mod_name]=deepcopy(mod)
			continue

		if isinstance(mod, folder):
			sub_folder=not_tag_apply_operate(mod, func)
			new_folder.mod_dict[mod_name]=sub_folder
			continue

		new_folder.mod_dict[mod_name]=func(mod)
	return new_folder

def apply_operate(ref, tag_set, inf, outf):
	inside_name_set=ref.search_mod_name_set(tag_set)
	new_folder=ref.copy_without_mod()

	if ref.is_fix:
		new_folder.mod_dict=ref.mod_dict
		return new_folder

	mod_without_tag_set=ref.mod_without_tag_set
	for mod_name, mod in ref.mod_dict.items():
		if mod_name in mod_without_tag_set:
			new_folder.mod_dict[mod_name]=deepcopy(mod)
			continue

		mod_is_inside=mod_name in inside_name_set
		mod_is_folder=isinstance(mod, folder)

		if mod_is_inside and not mod_is_folder:
			new_folder.mod_dict[mod_name]=inf(mod)

		elif not mod_is_inside and not mod_is_folder:
			new_folder.mod_dict[mod_name]=outf(mod)

		elif mod_is_inside and mod_is_folder:
			sub_folder=apply_operate(mod, tag_set, inf, outf)
			new_folder.mod_dict[mod_name]=sub_folder

		else: # not mod_is_inside and mod_is_folder
			sub_folder=not_tag_apply_operate(mod, outf)
			new_folder.mod_dict[mod_name]=sub_folder

	return new_folder


def dual_operate(left, right, tag_set, dual_inf, outf):

	if not isinstance(right, folder):
		new_dual_inf=lambda mod: dual_inf(mod, right)
		return apply_operate(left, tag_set, new_dual_inf, outf)

	inside_name_set=left.search_mod_name_set(tag_set)
	new_folder=left.copy_without_mod()

	if left.is_fix:
		new_folder.mod_dict=left.mod_dict
		return new_folder

	mod_without_tag_set=left.mod_without_tag_set
	for mod_name, left_mod in left.mod_dict.items():
		if mod_name in mod_without_tag_set:
			new_folder.mod_dict[mod_name]=deepcopy(left_mod)
			continue

		right_mod=right.mod[mod_name]
		mod_is_inside=mod_name in inside_name_set
		left_mod_is_folder=isinstance(left_mod, folder)

		if mod_is_inside and not left_mod_is_folder:
			new_folder.mod[mod_name]=dual_inf(left_mod,right_mod)

		elif not mod_is_inside and not left_mod_is_folder:
			new_folder.mod[mod_name]=outf(left_mod)

		elif mod_is_inside and left_mod_is_folder:
			sub_folder=dual_operate(left_mod,right_mod,tag_set,dual_inf,outf)
			new_folder.mod[mod_name]=sub_folder

		else:
			sub_folder=not_tag_apply_operate(left_mod, outf)
			new_folder.mod[mod_name]=sub_folder

	return new_folder
