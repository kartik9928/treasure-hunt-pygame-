import pygame
from support import import_folder

class Player(pygame.sprite.Sprite):

    def __init__(self, pos, surface, create_jump_particles):
        self.import_character_asserts()
        super().__init__()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft= pos)
        self.create_jump_particles = create_jump_particles

        # dust particles
        self.dust_frame_index = 0
        self.dust_animation_speed = 0.15
        self.display_surface = surface
        self.import_run_dust_particles()

        # player movement
        self.dimention = pygame.math.Vector2(0, 0)
        self.speed = 8
        self.jump_speed = -16
        self.gravity = 0.8

        # player statues
        self.status = 'idle'
        self.right_facing = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

    def import_character_asserts(self):
        character_path = './graphics/character/'
        self.animations = {'idle': [], 'fall': [], 'jump': [], 'run': []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def import_run_dust_particles(self):
        self.dust_run_particles = import_folder('./graphics/character/dust_particles/run')

    def get_inut(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.dimention.x = 1
            self.right_facing = True
        elif keys[pygame.K_LEFT]:
            self.dimention.x = -1
            self.right_facing = False
        else:
            self.dimention.x = 0

        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump()
            self.create_jump_particles(self.rect.center + pygame.math.Vector2(0, 10))

    def get_status(self):
        if self.dimention.y < 0:
            self.status = 'jump'
        elif self.dimention.y > 1:
            self.status = 'fall'
        else:
            if self.dimention.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'

    def apply_gravity(self):
        self.dimention.y += self.gravity
        self.rect.y += self.dimention.y

    def jump(self):
        self.dimention.y = self.jump_speed

    def animation(self):
        animation = self.animations[self.status]

        # loop over frame index
        self.frame_index +=  self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        image = animation[int(self.frame_index)]
        if self.right_facing:
            self.image = image
        else:
            self.image = pygame.transform.flip(image, True, False)

        # set the rect
        if self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
        elif self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft = self.rect.topleft)
        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright = self.rect.topright)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop = self.rect.midtop)

    def run_dust_animation(self):
        if self.status == 'run' and self.on_ground:
            self.dust_frame_index += self.dust_animation_speed
            if self.dust_frame_index >= len(self.dust_run_particles):
                self.dust_frame_index = 0

            dust_particles = self.dust_run_particles[int(self.dust_frame_index)]

            if self.right_facing:
                pos = self.rect.bottomleft - pygame.math.Vector2(6, 10)
            else:
                dust_particles = pygame.transform.flip(dust_particles, True, False)
                pos = self.rect.bottomright - pygame.math.Vector2(6, 10)

            self.display_surface.blit(dust_particles, pos)

    def update(self):
        self.get_inut()
        self.get_status()
        self.animation()
        self.run_dust_animation()