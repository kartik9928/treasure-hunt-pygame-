import pygame
from support import import_csv_layout, import_cut_graphic
from tiles import Tile, StaticTile, Create, Coin, Palm
from setting import TILE_SIZE, SCREEN_HEIGHT, SCREEN_WIDTH
from enemy import Enemy
from decoration import Sky, Water, Clouds
from player import Player
from particles import ParticleEffects

class Level:

    def __init__(self, level_data, surface):

        # general setup
        self.display_surface = surface
        self.world_shift = 0

        # player setup
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)

        # dust
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False

        # terrain setup
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')

        # grass setup
        grass_layout = import_csv_layout(level_data['grass'])
        self.grass_sprites = self.create_tile_group(grass_layout, 'grass')

        # crates setup
        crate_layout = import_csv_layout(level_data['crates'])
        self.crate_sprites = self.create_tile_group(crate_layout, 'crates')

        # coins setup
        coin_layout = import_csv_layout(level_data['coins'])
        self.coin_sprites = self.create_tile_group(coin_layout, 'coins')

        # foregroud palms setup
        fg_palm_layout = import_csv_layout(level_data['fg palms'])
        self.fg_palm_sprites = self.create_tile_group(fg_palm_layout, 'fg palms')

        # backgroud palms setup
        bg_palm_layout = import_csv_layout(level_data['fg palms'])
        self.bg_palm_sprites = self.create_tile_group(bg_palm_layout, 'bg palms')

        # enemies setup
        enemy_layout = import_csv_layout(level_data['enemies'])
        self.enemy_sprites = self.create_tile_group(enemy_layout, 'enemies')

        # constraints setup
        constraints_layout = import_csv_layout(level_data['constraints'])
        self.constraints_sprites = self.create_tile_group(constraints_layout, 'constraints')

        # decoration
        self.sky = Sky(7)
        level_width = len(terrain_layout[0]) * TILE_SIZE
        self.water = Water(SCREEN_HEIGHT - 60, level_width)
        self.cloud = Clouds(400, level_width, 20)

        self.setup_levels(level_data)
        self.current_x = 0


    def player_setup(self, layout):
        for row_index, row in enumerate(layout):
            for  col_index, val in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if val == '0':
                    sprite = Player((x, y), self.display_surface, self.create_jump_particles)
                    self.player.add(sprite)
                if val == '1':
                    hat_surface = pygame.image.load("./graphics/character/hat.png").convert_alpha()
                    sprite = StaticTile(TILE_SIZE, x, y, hat_surface)
                    self.goal.add(sprite)

    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for  col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * TILE_SIZE
                    y = row_index * TILE_SIZE

                    sprite = ''
                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphic('./graphics/terrain/terrain_tiles.png')
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(TILE_SIZE, x, y, tile_surface)

                    if type == 'grass':
                        grass_tile_list = import_cut_graphic('./graphics/decoration/grass/grass.png')
                        tile_surface = grass_tile_list[int(val)]
                        sprite = StaticTile(TILE_SIZE, x, y, tile_surface)

                    if type == 'crates':
                         sprite = Create(TILE_SIZE, x, y)

                    if type == 'coins':
                        if val == '0' : sprite = Coin(TILE_SIZE, x, y, './graphics/coins/gold')
                        if val == '1' : sprite = Coin(TILE_SIZE, x, y, './graphics/coins/silver')

                    if type == 'fg palms':
                        if val == '1': sprite = Palm(TILE_SIZE, x, y, './graphics/terrain/palm_small', 38)
                        if val == '2': sprite = Palm(TILE_SIZE, x, y, './graphics/terrain/palm_large', 64)

                    if type == 'bg palms':
                        sprite = Palm(TILE_SIZE, x, y, './graphics/terrain/palm_bg', 64)

                    if type == 'enemies':
                        sprite = Enemy(TILE_SIZE, x, y)

                    if type == 'constraints':
                        sprite = Tile(TILE_SIZE, x, y)

                    sprite_group.add(sprite)

        return sprite_group

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

        collidable_sprite = self.terrain_sprites.sprites() + self.crate_sprites.sprites() + self.fg_palm_sprites.sprites()
        for sprite in collidable_sprite:
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

        collidable_sprite = self.terrain_sprites.sprites() + self.crate_sprites.sprites() + self.fg_palm_sprites.sprites()
        for sprite in collidable_sprite :
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
        print(f"{not self.player_on_ground} \t {self.player.sprite.on_ground} \t {not self.dust_sprite.sprites()}")
        # print(f"part 2 ============================================= {not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites()}\n\n")

        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
            if self.player.sprite.right_facing:
                offset = pygame.math.Vector2(10, 15)
            else:
                offset = pygame.math.Vector2(-10, 15)
            fall_dust_particles = ParticleEffects(self.player.sprite.rect.midbottom - offset, 'land')
            self.dust_sprite.add(fall_dust_particles)

    def enemies_collision_reverse(self):
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraints_sprites, False ):
                enemy.reverse()

    def run(self):
        # tiles

        # sky
        self.sky.draw(self.display_surface)
        self.cloud .draw(self.display_surface, self.world_shift)

        # bg palm
        self.bg_palm_sprites.update(self.world_shift)
        self.bg_palm_sprites.draw(self.display_surface)

        # terrain
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)

        # enemy
        self.enemy_sprites.update(self.world_shift)
        self.constraints_sprites.update(self.world_shift)
        self.enemies_collision_reverse()
        self.enemy_sprites.draw(self.display_surface)

        # crates
        self.crate_sprites.update(self.world_shift)
        self.crate_sprites.draw(self.display_surface)

        # grass
        self.grass_sprites.update(self.world_shift)
        self.grass_sprites.draw(self.display_surface)

        # coins
        self.coin_sprites.update(self.world_shift)
        self.coin_sprites.draw(self.display_surface)

        # fg palm
        self.fg_palm_sprites.update(self.world_shift)
        self.fg_palm_sprites.draw(self.display_surface)

        # player goal
        self.player.update()
        self.horizontal_movement_collide()
        self.get_player_on_ground()
        self.vertical_movement_collide()
        self.create_landing_animation()
        self.scroll_x()
        self.player.draw(self.display_surface)
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)

        # dust particle
        self.dust_sprite.update(self.world_shift)
        self.dust_sprite.draw(self.display_surface)

        # water
        self.water.draw(self.display_surface, self.world_shift)
