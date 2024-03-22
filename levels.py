import pygame
from tiles import Tile
from setting import TILE_SIZE, SCREEN_WIDTH
from player import Player
from particles import ParticleEffects

class Level:

    def __init__(self, map_level, surface):

        # level setup
        self.display_surface = surface
        self.setup_levels(map_level)
        self.world_shift = 0
        self.current_x = 0

        # dust
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False

    def setup_levels(self, layouts):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()

        for index_r, rows in enumerate(layouts):
            for index_c, cals in enumerate(rows):
                if cals == 'x':
                    x = index_r * TILE_SIZE
                    y = index_c * TILE_SIZE
                    tile = Tile((y, x), TILE_SIZE)
                    self.tiles.add(tile)
                elif cals == 'p':
                    self.player.add(Player((index_c*TILE_SIZE, index_r*TILE_SIZE), self.display_surface, self.create_jump_particles))

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        dimention_x = player.dimention.x

        if player_x < SCREEN_WIDTH / 4 and dimention_x < 0:
            self.world_shift = 5
            player.speed = 0
        elif player_x > SCREEN_WIDTH - (SCREEN_WIDTH / 4) and dimention_x > 0:
            self.world_shift = -5
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 5

    def horizontal_movement_collide(self):
        player = self.player.sprite
        player.rect.x += player.dimention.x * player.speed

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.dimention.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.dimention.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right

        if player.on_left and (player.rect.left < self.current_x or player.dimention.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.dimention.x <= 0):
            player.on_right = False

    def vertical_movement_collide(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.dimention.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.dimention.y = 0
                    player.on_ground = True
                elif player.dimention.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.dimention.y = 0
                    player.on_ceiling = True

        if player.on_ground and player.dimention.y < 0 or player.dimention.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.dimention.y > 0:
            player.on_ceiling = False

    def create_jump_particles(self, pos):
        if self.player.sprite.right_facing:
            pos += pygame.math.Vector2(10, 5)
        else:
            pos -= pygame.math.Vector2(10, -5)
        jump_particle_sprtie = ParticleEffects(pos, 'jump')
        self.dust_sprite.add(jump_particle_sprtie)

    def get_player_on_ground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    def create_landing_animation(self):
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
            if self.player.sprite.right_facing:
                offset = pygame.math.Vector2(10, 15)
            else:
                offset = pygame.math.Vector2(-10, 15)
            fall_dust_particles = ParticleEffects(self.player.sprite.rect.midbottom - offset, 'land')
            self.dust_sprite.add(fall_dust_particles)

    def run(self):
        # tiles
        self.tiles.update(self.world_shift)
        self.scroll_x()
        self.tiles.draw(self.display_surface)

        # dust particle
        self.dust_sprite.update(self.world_shift)
        self.dust_sprite.draw(self.display_surface)

        # player
        self.player.update()
        self.horizontal_movement_collide()
        self.get_player_on_ground()
        self.vertical_movement_collide()
        self.create_landing_animation()
        self.player.draw(self.display_surface)