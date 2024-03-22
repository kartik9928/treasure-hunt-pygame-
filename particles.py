import pygame
from support import import_folder

class ParticleEffects(pygame.sprite.Sprite):

    def __init__(self, pos, type):
        super().__init__()

        if type == 'jump':
            self.frames = import_folder('./graphics/character/dust_particles/jump')
        else:
            self.frames = import_folder('./graphics/character/dust_particles/land')
        self.index_frame = 0
        self.animation_speed = 0.5
        self.image = self.frames[self.index_frame]
        self.rect = self.image.get_rect(center= pos)

    def animate(self):
        self.index_frame += self.animation_speed
        if self.index_frame >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.index_frame)]

    def update(self, x_shift):
        self.animate()
        self.rect.x += x_shift