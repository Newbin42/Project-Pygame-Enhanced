from __future__ import annotations
from math import atan, cos, pi, sin
from typing import List

from .. import Matrix

class Vector2(Matrix.Matrix):
    @staticmethod
    def from_polar(vector: PVector2) -> Vector2:
        return vector.cartesian()

    def __init__(self, x: float, y: float) -> None:
        Matrix.Matrix.__init__(self, x, y)

        self.x = x
        self.y = y

        self.xx = [x, x]
        self.xy = [x, y]
        self.yy = [y, y]

    def rotate_around(point: tuple[int, int] | Vector2, origin: tuple[int, int] | Vector2, theta: int) -> Vector2:
        if (type(point) != Vector2): point = Vector2(*point)
        if (type(origin) != Vector2): origin = Vector2(*origin)

        """Rotate a 2d point by theta degrees around an [x, y] origin."""
        diff = abs(point - origin)

        point -= diff

        theta *= 0.0174532925199433
        ct = cos(theta)
        st = sin(theta)

        x = point[0] * ct - point[1] * st
        y = point[0] * st + point[1] * ct

        return Vector2(int(x), int(y)) + diff

    def shift_x(self, x: float) -> None:
        self.x += x

        self.xx = [self.x, self.x]
        self.xy = [self.x, self.y]

    def shift_y(self, y: float) -> None:
        self.y += y

        self.yy = [self.y, self.y]
        self.xy = [self.x, self.y]

    def update(self, x: float, y: float = None) -> None:
        self.x = x
        self.y = y

        self.xx = [x, x]
        self.xy = [x, y]
        self.yy = [y, y]

    def polar(self) -> PVector2:
        return PVector2(self.magnitude(), atan(self.y / self.x) if (self.x != 0) else (pi / 2))

class PVector2(Matrix.Matrix):
	@staticmethod
	def from_cartesian(coord: Vector2 | List[float], relativeOffset = Vector2(0, 0)) -> PVector2:
		coord -= relativeOffset
		return PVector2(coord.magnitude(), atan(coord.y / coord.x) if (coord.x != 0) else (pi / 2))
		
	def __init__(self, radius: float, theta: float) -> None:
		Matrix.Matrix.__init__(self, radius, theta)

		self.r = radius
		self.t = theta
		
		self.rt = [radius, theta]
		self.rr = [radius, radius]
		self.tt = [theta, theta]

	def update(self, radius: float, theta: float) -> None:
		self.r = radius
		self.t = theta
		
		self.rt = [radius, theta]
		self.rr = [radius, radius]
		self.tt = [theta, theta]
		
	def cartesian(self) -> Vector2:
		return Vector2(self.r * cos(self.t), self.r * sin(self.t))
	
class SphericalVector(Matrix.Matrix):
    """Not Yet Implemented"""
    def __init__(self, radius: float, theta: float, phi: float) -> None:
        """Azimuth (phi) is measured clockwise (from the west)."""
        raise NotImplementedError("Warning. SphericalVector is Not Yet Implemented and does not do anything.")

        Matrix.Matrix.__init__(self, radius, theta)

        self.r = radius
        self.t = theta
        self.p = phi

    def update(self, radius: float, theta: float, phi: float) -> None:
        self.r = radius
        self.t = theta
        self.p = phi
	
TYPES = [Vector2, PVector2]
Matrix.__UpdateTypes__(TYPES) # Used to prove existance to parent library