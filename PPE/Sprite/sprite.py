from __future__ import annotations
import pygame

from ..Surface.surface import Surface

class Sprite(pygame.sprite.Sprite):
    def __init__(self, surface: Surface) -> None:
        pygame.sprite.Sprite.__init__(self)
        
        self.surface = surface
    
    def update(self):
        "Update Sprite"
        pass
    
    def get_rect(self) -> pygame.Rect:
        return self.surface.rect

    def blit(self, source: Surface | pygame.Surface, position: list[int, int] | pygame.Vector2) -> None:
        self.surface.blit(source, position)