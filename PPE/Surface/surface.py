from __future__ import annotations

from pygame import Surface as pygSurface
from pygame import Rect, Color, Vector2, SRCALPHA

class Surface(pygSurface):
    def __init__(self, rect: Rect | list[int], parent: Surface = None, bg: Color = Color(0, 0, 0, 255)) -> None:
        pygSurface.__init__(self, [rect.width, rect.height] if (type(rect) == Rect) else rect, flags = SRCALPHA)

        self.rect: Rect = rect if (type(rect) == Rect) else Rect(0, 0, rect[0], rect[1])
        self.parent: Surface = parent if (parent) else pygSurface([rect.width, rect.height])

        self.background: Color = bg
        self.flush()

    def super_flush(self) -> None:
        pygSurface.__init__(self, [self.rect.width, self.rect.height], flags = SRCALPHA)

    def flush(self) -> None:
        """Refresh / Flush the surface.

        os.system("cls/clear") equivalent"""
        self.fill(self.background)

    def set_pos(self, pos: list[float, float]) -> None:
        "Set the local top left coordinate of the surface"
        self.rect.topleft = pos
    
    def set_center(self, pos: list[float, float]) -> None:
        "Set the local center coordinate of the surface"
        self.rect.center = pos
    
    def get_pos(self) -> Vector2:
        "Return the local top left coordinate of the surface"
        return Vector2(self.rect.topleft)
    
    def get_center(self) -> Vector2:
        "Return the local center coordinate of the surface"
        return Vector2(self.rect.center)

    def draw(self, where: Surface = None) -> None:
        "Will draw on an empty defaut parent if no surface or parent is provided."
        if (where != None): where.blit(self, self.get_pos())
        else: self.parent.blit(self, self.get_pos())