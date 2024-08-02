from __future__ import annotations

from pygame import Rect, Color
from ..Surface.surface import Surface as surface
from .animation import Animation

class Surface(surface):
    def __init__(self, rect: Rect | list[int, int], animation: Animation, parent: Surface = None, bg: Color = Color(0, 0, 0, 255)) -> None:
        surface.__init__(self, rect, parent, bg)
        self.animation = animation

    def update(self):
        next(self.animation)
        self.blit(self.animation.frame, (0, 0))