import pygame
from support import import_folder

class Tile(pygame.sprite.Sprite):

    def __init__(self, size, x, y):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft= (x, y))

    def update(self, x_shift):
        self.rect.x += x_shift


class StaticTile(Tile):
    def __init__(self, size, x, y, surface):
        super().__init__(size, x, y)
        self.image = surface


class Create(StaticTile):
    def __init__(self, size, x, y):
        super().__init__(size, x, y, pygame.image.load('./graphics/terrain/crate.png').convert_alpha())
        offset_y = y + size
        self.rect = self.image.get_rect(bottomleft= (x, offset_y))


class AnimatedTile(Tile):
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y)
        self.frames = import_folder(path )
        self.frames_index = 0
        self.image = self.frames[self.frames_index]

    def animate(self):
        self.frames_index += 0.15
        if self.frames_index >= len(self.frames):
            self.frames_index = 0
        self.image = self.frames[int(self.frames_index)]

    def update(self, x_shift):
        self.animate()
        self.rect.x += x_shift


class Coin(AnimatedTile):
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y, path)
        self.rect = self.image.get_rect(center = (x + int(size/2), y + int(size/2)))

class Palm(AnimatedTile):
    def __init__(self, size, x, y, path, offset):
        super().__init__(size, x, y, path)
        offset_y = y - offset
        self.rect.topleft= (x, offset_y)