""" Binary Operators used with Binary indexed Tree. """
from operator import add, sub, mul, truediv
from .btypes import Callable, _T, Optional, Union, Any


class BinaryOP:
    """ Binary Operator wrapped in a class. Quick and dirty, for now. """
    def __init__(
            self,
            op: Callable[[_T, _T], _T],
            inverse: Optional[Callable[[_T, _T], _T]] = None):
        self.binop = op
        self._inverse = inverse

    def __repr__(self) -> str:
        """ Returns a representation of BinaryOP. """
        inverse, binop = self._inverse, self.binop
        if inverse:
            args = [binop.__name__, inverse.__name__]
        else:
            args = [binop.__name__]
        return f"BinaryOP{tuple(args)}"

    def __call__(self, a: _T, b: _T) -> _T:
        """ Calls Binary operator on a, b. """
        return self.binop(a, b)

    def inverse(self, a: _T, b: _T) -> Union[_T, Any]:
        """ Return the inverse operator. """
        if self._inverse:
            # call binary inverse and return.
            return self._inverse(a, b)
        raise TypeError(f"{repr(self)} doesn't have an inverse defined.")


# define a couple of operators.
Add = BinaryOP(add, sub)
Mul = BinaryOP(mul, truediv)
