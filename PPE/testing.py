import pygame
from BoundingBox import *
from Surface.surface import Surface
from exts import getResolution
from .Matrix import Matrix
from .Vector.vector import Vector2

class Cursor:
    def __init__(self):
        self.pos = pygame.Vector2(0, 0)
        self.draw_lines = False

    def update_pos(self, new_pos):
        self.pos = new_pos

    def draw_lines_between(self, surface, shape):
        if (self.draw_lines):
            for point in shape:
                pygame.draw.line(surface, pygame.Color(0, 0, 255, 255), self.pos, point, 2)

    def draw(self, surface):
        pygame.draw.circle(surface, pygame.Color(255, 0, 255, 255), self.pos, 4, 0)

def main():
    pygame.init()

    cursor = Cursor()

    cursor_f = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW)
    cursor_t = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)

    pygame.mouse.set_cursor(cursor_f)
    is_f = True

    screenDims = pygame.Vector2(getResolution()) * 0.7
    screen = pygame.display.set_mode(screenDims.xy)

    A = Convex(Matrix(Vector2(2, 1), Vector2(3, 2), Vector2(1, 2), Vector2(1, 2)) * 50)
    B = Convex(Matrix(Vector2(2, 2), Vector2(3, 2), Vector2(3, 4), Vector2(1, 3)) * 50)
    test_bounds = Composite(A, B)

    running = True
    pygame.key.set_repeat(10, 100)
    while running:
        mpos = pygame.mouse.get_pos()
        if (running):
            screen.fill(pygame.Color(0, 0, 0, 255))

            test_bounds.debug_draw(screen, 3, True)

            if (not is_f and not test_bounds.collidepoint(mpos)):
                pygame.mouse.set_cursor(cursor_f)
                is_f = True

            elif (is_f and test_bounds.collidepoint(mpos)):
                pygame.mouse.set_cursor(cursor_t)
                is_f = False

            pygame.display.update()

        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()
                running = False
            elif (event.type == pygame.MOUSEMOTION):
                cursor.update_pos(pygame.Vector2(*mpos))
            elif (event.type == pygame.MOUSEBUTTONDOWN):
                print(test_bounds.collidepoint(mpos))
            elif (event.type == pygame.KEYDOWN):
                keys = pygame.key.get_pressed()
                if (keys[pygame.K_r]):
                    test_bounds.rotate(pi/180)
                elif (keys[pygame.K_a]):
                    print(test_bounds.center, test_bounds.area, test_bounds.convex_point_area(mpos))
                elif (keys[pygame.K_d]):
                    cursor.draw_lines = not cursor.draw_lines

if __name__ == "__main__":
    main()