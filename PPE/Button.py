from __future__ import annotations
import pygame

from .Surface.surface import Surface

class Button(Surface):
    def __init__(self, texture: pygame.Surface, pos: pygame.Vector2, parent: pygame.Surface = None):
        Surface.__init__(self, pygame.Rect(pos.x, pos.y, *texture.get_size()), parent)
        self.texture: pygame.Surface = texture

        self.blit(self.texture, (0, 0))

    def clicked_on(self, mousePos: pygame.Vector2) -> bool:
        return self.rect.collidepoint(mousePos)