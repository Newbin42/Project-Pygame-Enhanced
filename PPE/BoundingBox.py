from __future__ import annotations
from math import sin, cos, pi
import pygame
from PPE.Matrix import Matrix, Vector2

class mixins:
    """Mixins for any center point of a bounding box.
    
    You should have no reason to use them under normal circumstances."""
    def __init__(self, center: pygame.Vector2 = Vector2(0, 0)):
        self.center = center

    def set_center(self, center: pygame.Vector2 = Vector2(0, 0)) -> None:
        self.center = center

    def shift(self, vector: pygame.Vector2) -> None:
        if (type(vector) != Vector2): vector = Vector2(vector.x, vector.y)
        self.center += vector

    def __rotate_point__(self, point: Vector2, theta: float) -> pygame.Vector2:
        x = point.x * cos(theta) - point.y * sin(theta)
        y = point.x * sin(theta) + point.y * cos(theta)
        return Vector2(x, y)
    
    def __area_of_tri__(self, A: pygame.Vector2, B: pygame.Vector2, P: pygame.Vector2) -> float:
        return abs((B.x * A.y - A.x * B.y) + (P.x * B.y - B.x * P.y) + (A.x * P.y - P.x * A.y) ) / 2

class BoundingBox(mixins):
    def __init__(self, points: list[pygame.Vector2], center: pygame.Vector2 = None) -> None:
        self.shape: list[Vector2] = points if (type(points) == Matrix) else Matrix(points.topleft, points.topright, points.bottomright, points.bottomleft) if (type(points) == pygame.Rect) else Matrix(*points)
        mixins.__init__(self, center if (center != None) else self.find_centroid())

        self.area = self.find_convex_area()

    def find_centroid(self) -> Vector2:
        centroid_x = 0
        centroid_y = 0

        for point in self.shape:
            centroid_x += point.x
            centroid_y += point.y

        return Vector2(centroid_x / len(self.shape), centroid_y / len(self.shape))
    
    def find_convex_area(self) -> float:
        area = 0

        for i in range(len(self.shape)):
            if (i < len(self.shape) - 1): area += self.__area_of_tri__(self.shape[i], self.shape[i + 1], self.center)
            else: area += self.__area_of_tri__(self.shape[i], self.shape[0], self.center)
        
        return area
    
    def convex_point_area(self, point: pygame.Vector2) -> float:
        if (type(point) == tuple):
            point = pygame.Vector2(*point)

        sumArea = 0
        for i in range(len(self.shape)):
            if (i < len(self.shape) - 1): sumArea += self.__area_of_tri__(self.shape[i], self.shape[i + 1], point)
            else: sumArea += self.__area_of_tri__(self.shape[i], self.shape[0], point)
        
        return sumArea

    def rotate(self, theta: float) -> None:
        """Theta is in radians."""
        for i in range(len(self.shape)):
            self.shape[i] = self.__rotate_point__(self.shape[i] - self.center, theta) + self.center
        
        self.center = self.find_centroid()

    def shift(self, vector: pygame.Vector2) -> None:
        for i in range(len(self.shape)):
            self.shape[i] = self.shape[i] + vector
        
        self.center = self.find_centroid()

    def draw_centroid(self, surface: pygame.Surface, width: int) -> None:
        pygame.draw.circle(surface, pygame.Color(255, 0, 0, 255), self.center, width)

    def draw_edges(self, surface: pygame.Surface, width: int) -> None:
        pygame.draw.lines(surface, pygame.Color(255, 255, 255, 255), True, self.shape, width)
    
    def draw_vertices(self, surface: pygame.Surface, width: int = 1) -> None:
        for point in self.shape:
            pygame.draw.circle(surface, pygame.Color(255, 0, 0, 255), point, width)

    def debug_draw(self, surface: pygame.Surface, width: int) -> None:
        self.draw_edges(surface, width // 2)
        self.draw_vertices(surface, width)
        self.draw_centroid(surface, width)

class Circle(BoundingBox):
    def __init__(self, radius: float, center: pygame.Vector2 = pygame.Vector2(0, 0)) -> None:
        BoundingBox.__init__(self, [center], center)
        self.radius = radius
    
    def collidepoint(self, point: pygame.Vector2) -> bool:
        if (self.center.distance_to(point) <= self.radius): return True
        return False
    
    def draw_outline(self, surface: pygame.Surface, width: int) -> None:
        pygame.draw.circle(surface, pygame.Color(255, 255, 255, 255), self.center, self.radius, width)

    def draw_offset_point(self, surface: pygame.Surface, width: int) -> None:
        pygame.draw.circle(surface, pygame.Color(0, 0, 255, 255), self.center, 1 * width, width)

    def debug_draw(self, surface: pygame.Surface, width: int) -> None:
        self.draw_outline(surface, width)
        self.draw_offset_point(surface, width)

class Convex(BoundingBox):
    def __init__(self, shape: list[pygame.Vector2]) -> None:
        BoundingBox.__init__(self, shape)

    def collidepoint(self, point: pygame.Vector2 | tuple[float, float]) -> bool:
        if (type(point) == tuple):
            point = pygame.Vector2(*point)

        sumArea = 0
        for i in range(len(self.shape)):
            if (i < len(self.shape) - 1): sumArea += self.__area_of_tri__(self.shape[i], self.shape[i + 1], point)
            else: sumArea += self.__area_of_tri__(self.shape[i], self.shape[0], point)
            
            if (sumArea > self.area): return False

        return True if (sumArea <= self.area) else False
    
    def collide_other(self, other: Convex | Rect | Circle) -> bool:
        return False

class Tri(Convex):
    def __init__(self, initTri: list[pygame.Vector2]) -> None:
        if (len(initTri) != 3): raise ArithmeticError("Warning! Triangles may only contain 3 vertices.")
        Convex.__init__(self, initTri)

class Rect(Convex):
    def __init__(self, initRect: pygame.Rect) -> None:
        if (type(initRect) == pygame.Rect):
            rect: Matrix[pygame.Vector2] = Matrix(initRect.topleft, initRect.topright, initRect.bottomright, initRect.bottomleft)
        else:
            raise TypeError(f"Warning! initRect must be type pygame.Rect, was {type(initRect)}.")
        
        Convex.__init__(self, rect)

class Composite(Matrix):
    """A bounding box made of other bounding boxes.
    
    WARNING! Unfinished and buggy during rotations."""
    def __init__(self, *boundingBoxes: tuple[Convex, ...]):
        Matrix.__init__(self, *boundingBoxes)

        self.center = self.find_centroid()
        self.shape = self.generate_shape()

    def generate_shape(self: list[Convex] | Composite) -> list[Vector2]:
        vertices = []
        for boundingBox in self:
            vertices = vertices + [vertex for vertex in boundingBox.shape]
        
        return vertices

    def collidepoint(self: list[Convex], vector: pygame.Vector2) -> bool:
        for boundingBox in self:
            if (boundingBox.collidepoint(vector)): return True
        
        return False
    
    def find_centroid(self: list[Convex]) -> Vector2:
        centroid = Vector2(0, 0)
        for boundingBox in self:
            centroid += boundingBox.center

        return centroid / len(self)
    
    def rotate(self: list[Convex] | Composite, theta: float) -> None:
        """Theta is in radians."""
        for boundingBox in self:
            for i in range(len(boundingBox.shape)):
                boundingBox.shape[i] = boundingBox.__rotate_point__(boundingBox.shape[i] - self.center, theta) + self.center
                boundingBox.center = boundingBox.find_centroid()
        
        self.center = self.find_centroid()

    def draw_centroid(self: list[Convex] | Composite, surface: pygame.Surface, width: int) -> None:
        pygame.draw.circle(surface, pygame.Color(255, 255, 0, 255), self.center, width)

    def draw_edges(self: list[Convex] | Composite, surface: pygame.Surface, width: int) -> None:
        pygame.draw.lines(surface, pygame.Color(255, 255, 255, 255), True, self.shape, width)
    
    def draw_vertices(self: list[Convex] | Composite, surface: pygame.Surface, width: int = 1) -> None:
        for point in self.shape:
            pygame.draw.circle(surface, pygame.Color(255, 0, 0, 255), point, width)
            
    def debug_draw(self: list[Convex] | Composite, surface: pygame.Surface, width: int, multiBox = False) -> None:
        if (multiBox):
            for boundingBox in self:
                boundingBox.debug_draw(surface, width)
        else:
            self.draw_edges(surface, width // 2)
            self.draw_vertices(surface, width)
                
        self.draw_centroid(surface, width)