from __future__ import annotations
from math import sqrt, sin, cos, atan, pi, ceil, floor, trunc
from typing import Any, List, Sequence, Callable

class Matrix(Sequence):
	def __init__(self, *inputs: tuple[Any, ...]) -> None:
		"Initialize a new matrix object with the given inputs"
		self.type = type(inputs[0])
		self.matrix = True
		self.items: list[self.type] = [i for i in inputs]

		self.iter = 0

	def dot(self, other: Matrix) -> float:
		return sum(self * other)

	def magnitude(self) -> float:
		return sqrt(self.tss())
	
	def magnitude_squared(self) -> float:
		return self.tss()
	
	def length(self) -> float:
		return self.magnitude()
	
	def length_squared(self) -> float:
		return self.tss()
	
	def normalize(self) -> Matrix:
		"Return a normalized version of the matrix."

		mag = self.magnitude()
		return type(self)(*[item / mag for item in self])
	
	def normalize_ip(self) -> None:
		"Normalized the matrix."

		mag = self.magnitude()
		for i in range(len(self)):
			self[i] /= mag

	def is_normalized(self) -> bool:
		return self.length() == 1
	
	def distance_to(self, other: Matrix) -> float:
		tss = 0
		for i in range(len(self)):
			tss += (other[i] - self[i])**2

		return sqrt(tss)
	
	def distance_squared_to(self, other: Matrix) -> float:
		return self.distance_to(other) ** 2
	
	def tss(self) -> float:
		"return the sum of squares of the matrix"
		return sum([item ** 2 for item in self])
	
	def map(self, function: Callable[[Any], Any]) -> Matrix:
		return type(self)(*[function(item) for item in self])

	def map_ip(self, function: Callable[[Any], Any]) -> None:
		for i in range(len(self)):
			self[i] = function(self[i])
	
	#Overloads
	def __sum__(self) -> float:
		return sum(self.items)
	
	def __next__(self) -> float:
		if (self.iter >= len(self)):
			raise StopIteration
		
		self.iter += 1
		return self[self.iter - 1]

	def __iter__(self) -> Matrix:
		self.iter = 0
		return self

	def __getitem__(self, i) -> Any:
		return self.items[i]

	def __setitem__(self, i, item) -> None:
		self.items[i] = item

	def __len__(self) -> int:
		return len(self.items)

	def __int__(self) -> Matrix:
		return type(self)(*[int(self[i]) for i in range(len(self.items))])
	
	def __float__(self) -> Matrix:
		return type(self)(*[float(self[i]) for i in range(len(self.items))])
	
	def __trunc__(self) -> Matrix:
		return type(self)(*[trunc(self[i]) for i in range(len(self.items))])

	def __ceil__(self) -> Matrix:
		return type(self)(*[ceil(self[i] + 1) for i in range(len(self.items))])
	
	def __floor__(self) -> Matrix:
		return type(self)(*[floor(self[i]) for i in range(len(self.items))])
	
	def __round__(self) -> Matrix:
		return type(self)(*[round(self[i]) for i in range(len(self.items))])
	
	def __abs__(self) -> Matrix:
		return type(self)(*[abs(self[i]) for i in range(len(self.items))])
	
	def __str__(self) -> str:
		return f'({", ".join([str(self[i]) for i in range(len(self))])})'

	def __neg__(self) -> Matrix:
		return type(self)(*[-self[i] for i in range(len(self.items))])
	
	def __invert__(self) -> Matrix:
		type(self)(*[~self[i] for i in range(len(self.items))])
	
	def __eq__(self, other: Matrix | Any) -> bool:
		return type(other) in TYPES and self.magnitude() == other.magnitude()
	
	def __ne__(self, other: Matrix | Any) -> bool:
		return not type(other) in TYPES or self.magnitude() != other.magnitude()
	
	def __lt__(self, other: Matrix) -> bool:
		return self.magnitude() < other.magnitude()
	
	def __le__(self, other: Matrix) -> bool:
		return self.magnitude() <= other.magnitude()
	
	def __gt__(self, other: Matrix) -> bool:
		return self.magnitude() > other.magnitude()
	
	def __ge__(self, other: Matrix) -> bool:
		return self.magnitude() >= other.magnitude()
	
	def __add__(self, other: Matrix) -> Matrix:
		if (len(self.items) != len(other.items)): raise ValueError(f'Cannot add two matrices of differing lengths ({len(self.items)} & {len(other.items)}).')
		return type(self)(*[self[i] + other[i] for i in range(len(self.items))])
	
	def __radd__(self, other: Matrix) -> Matrix:
		return other + self
	
	def __iadd__(self, other: Matrix) -> Matrix:
		return self + other
	
	def __sub__(self, other: Matrix) -> Matrix:
		if (len(self.items) != len(other.items)): raise ValueError(f'Cannot subtract two matrices of differing lengths ({len(self.items)} & {len(other.items)}).')
		return type(self)(*[self[i] - other[i] for i in range(len(self.items))])
	
	def __rsub__(self, other: Matrix) -> Matrix:
		return other - self
	
	def __isub__(self, other: Matrix) -> Matrix:
		return self - other
	
	def __mul__(self, other: Matrix | Any) -> Matrix:
		if (not type(other) in TYPES):
			return type(self)(*[self[i] * other for i in range(len(self.items))])

		if (len(self.items) != len(other.items)): raise ValueError(f'Cannot multiply two matrices of differing lengths ({len(self.items)} & {len(other.items)}).')
		return type(self)(*[self[i] * other[i] for i in range(len(self.items))])
	
	def __rmul__(self, other: Matrix) -> Matrix:
		return other * self
	
	def __imul__(self, other: Matrix | Any) -> Matrix:
		return self * other
	
	def __truediv__(self, other: Matrix | Any) -> Matrix:
		if (not type(other) in TYPES):
			return type(self)(*[self[i] / other for i in range(len(self.items))])
		
		if (len(self.items) != len(other.items)): raise ValueError(f'Cannot divide two matrices of differing lengths ({len(self.items)} & {len(other.items)}).')
		return type(self)(*[self[i] / other[i] for i in range(len(self.items))])
	
	def __rdiv__(self, other: Matrix) -> Matrix:
		return other / self
	
	def __idiv__(self, other: Matrix | Any) -> Matrix:
		return self / other
	
	def __floordiv__(self, other: Matrix | Any) -> Matrix:
		if (len(self.items) != len(other.items)): raise ValueError(f'Cannot divide two matrices of differing lengths ({len(self.items)} & {len(other.items)}).')
		return type(self)(*[self[i] // other[i] for i in range(len(self.items))])
	
	def __rfloordiv__(self, other: Matrix) -> Matrix:
		return other // self

	def __ifloordiv__(self, other: Matrix | Any) -> Matrix:
		return self // other
	
	def __pow__(self, other: Matrix | Any) -> Matrix:
		if (not type(other) in TYPES):
			return type(self)(*[self[i] ** other for i in range(len(self.items))])

		if (len(self.items) != len(other.items)): raise ValueError(f'Cannot raise two matrices of differing lengths ({len(self.items)} & {len(other.items)}).')
		return type(self)(*[self[i] ** other[i] for i in range(len(self.items))])
	
	def __rpow__(self, other: Matrix) -> Matrix:
		return other ** self

	def __ipow__(self, other: Matrix | Any) -> Matrix:
		return self ** other
	
	def __mod__(self, other: Matrix | Any) -> Matrix:
		if (not type(other) in TYPES):
			return type(self)(*[self[i] % other for i in range(len(self.items))])

		if (len(self.items) != len(other.items)): raise ValueError(f'Cannot divide two matrices of differing lengths ({len(self.items)} & {len(other.items)}).')
		return type(self)(*[self[i] % other[i] for i in range(len(self.items))])
	
	def __rmod__(self, other: Matrix) -> Matrix:
		return other % self

	def __imod__(self, other: Matrix | Any) -> Matrix:
		return self % other
	
	def __rshift__(self, other: Matrix | Any) -> Matrix:
		if (not type(other) in TYPES):
			return type(self)(*[self[i] >> other for i in range(len(self.items))])

		if (len(self.items) != len(other.items)): raise ValueError(f'Cannot shift two matrices of differing lengths ({len(self.items)} & {len(other.items)}).')
		return type(self)(*[self[i] >> other[i] for i in range(len(self.items))])
	
	def __rrshift__(self, other: Matrix) -> Matrix:
		return other >> self

	def __irshift__(self, other: Matrix | Any) -> Matrix:
		return self >> other
	
	def __lshift__(self, other: Matrix | Any) -> Matrix:
		if (not type(other) in TYPES):
			return type(self)(*[self[i] << other for i in range(len(self.items))])

		if (len(self.items) != len(other.items)): raise ValueError(f'Cannot shift two matrices of differing lengths ({len(self.items)} & {len(other.items)}).')
		return type(self)(*[self[i] << other[i] for i in range(len(self.items))])
	
	def __rlshift__(self, other: Matrix) -> Matrix:
		return other << self

	def __ilshift__(self, other: Matrix | Any) -> Matrix:
		return self << other
	
	def __and__(self, other: Matrix | Any) -> Matrix:
		if (not type(other) in TYPES):
			return type(self)(*[self[i] & other for i in range(len(self.items))])

		if (len(self.items) != len(other.items)): raise ValueError(f'Cannot shift two matrices of differing lengths ({len(self.items)} & {len(other.items)}).')
		return type(self)(*[self[i] & other[i] for i in range(len(self.items))])
	
	def __rand__(self, other: Matrix) -> Matrix:
		return other & self
	
	def __iand__(self, other: Matrix | Any) -> Matrix:
		return self & other
	
	def __or__(self, other: Matrix | Any) -> Matrix:
		if (not type(other) in TYPES):
			return type(self)(*[self[i] | other for i in range(len(self.items))])

		if (len(self.items) != len(other.items)): raise ValueError(f'Cannot shift two matrices of differing lengths ({len(self.items)} & {len(other.items)}).')
		return type(self)(*[self[i] | other[i] for i in range(len(self.items))])
	
	def __ror__(self, other: Matrix) -> Matrix:
		return other | self
	
	def __ior__(self, other: Matrix | Any) -> Matrix:
		return self | other
	
	def __xor__(self, other: Matrix | Any) -> Matrix:
		if (not type(other) in TYPES):
			return type(self)(*[self[i] ^ other for i in range(len(self.items))])

		if (len(self.items) != len(other.items)): raise ValueError(f'Cannot shift two matrices of differing lengths ({len(self.items)} & {len(other.items)}).')
		return type(self)(*[self[i] ^ other[i] for i in range(len(self.items))])
	
	def __rxor__(self, other: Matrix) -> Matrix:
		return other ^ self
	
	def __ixor__(self, other: Matrix | Any) -> Matrix:
		return self ^ other

def __UpdateTypes__(*toAdd: tuple[Any, ...]) -> None:
	for _type_ in toAdd:
		if (not _type_ in TYPES): TYPES.append(_type_)

TYPES = [Matrix]