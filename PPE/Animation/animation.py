from __future__ import annotations
from pygame import Rect, Surface, image
from ..Surface import surface

class Animation(Surface):
    @staticmethod
    def from_file(filename, spriteDimensions: tuple[int, int] = (32, 32), deadzones: int = 0) -> Animation:
        return Animation(image.load(filename), spriteDimensions, deadzones)

    def __init__(self, spritesheet: Surface, spriteDimensions: tuple[int, int] = (32, 32), deadzones: int = 0) -> None:
        self.sheet: Surface = spritesheet
        self.sWidth: int = spriteDimensions[0]
        self.sHeight: int = spriteDimensions[1]

        self.sprites: list[Surface] = self.__format__(deadzones)
        self.first = self.sprites[0]
        self.last = self.sprites[-1]

        self.frames: int = len(self.sprites)
        self.frameNum: int = 0
        self.frame: surface.Surface = surface.Surface(Rect(0, 0, *spriteDimensions))

    def __len__(self) -> int:
        return self.frames
    
    def __iter__(self) -> Animation:
        self.frameNum = 0
        return self

    def __next__(self) -> surface.Surface:
        self.frameNum += 1
        if (self.frameNum >= self.frames):
            raise StopIteration
        
        self.frame.flush()
        self.frame.blit(self.sprites[self.frameNum])
        return self.frame

    def __format__(self, deadzones: int = 0) -> list[Surface]:
        w = self.sheet.get_width() // self.sWidth
        h = self.sheet.get_height() // self.sHeight

        sprites = []
        for y in range(h):
            for x in range(w - deadzones):
                sprite = Surface(self.sWidth, self.sHeight)
                sprite.blit(self.sheet, (x * self.sWidth, y * self.sHeight))
                sprites.append(sprite)
        
        return sprites