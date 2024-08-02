from __future__ import annotations

from .animation import Animation
from ..Sprite.sprite import Sprite as sprite

class Sprite(sprite):
    def __init__(self, animation: Animation):
        sprite.__init__(self, animation.first)
        self.animation = animation

    def update(self):
        next(self.animation)
        self.blit(self.animation.frame, (0, 0))