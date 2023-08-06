
from nyto import folder
from copy import deepcopy


class particle(folder.folder):
    def __init__(self):
        super().__init__()
        
    def apply(self, inset_func, outset_func=folder.copy_func):
        return self.all_tag.apply(
            inset_func=inset_func,
            outset_func=outset_func
        )
    
    def dual(self, other, inset_dual_func, outset_func=folder.copy_func):
        return self.all_tag.dual(
            other=other,
            inset_dual_func=inset_dual_func,
            outset_func=outset_func
        )
        
    def __neg__(self):
        return self.apply(lambda x:-x)
    
    def __pow__(self, that):
        return self.apply(lambda x:x**that)
    
    def __add__(self, that):
        return self.dual(that, lambda s,t:s+t)
	
    def __radd__(self, that):
        return self+that
    
    def __sub__(self, that):
        return self.dual(that, lambda s,t:s-t)
	
    def __rsub__(self, that):
        return -self+that
    
    def __mul__(self, that):
        return self.dual(that, lambda s,t:s*t)
	
    def __rmul__(self, that):
        return self*that
    
    def __truediv__(self, that):
        return self.dual(that, lambda s,t:s/t)
	
    def __rtruediv__(self, that):
        return that * (self**-1)   
