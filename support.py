# from os import walk
import pygame
from csv import reader
from setting import TILE_SIZE
from os import walk

# def import_folder(path):
#     surface_list = []

#     for _,__,img_files in walk(path):
#         for image in img_files:
#             full_path = path + '/' + image
#             image_surf = pygame.image.load(full_path).convert_alpha()
#             surface_list.append(image_surf)

#     return surface_list

def import_csv_layout(path):
    terrain_map = []
    with open(path) as map:
        level = reader(map, delimiter= ',')
        for i in level:
            terrain_map.append(list(i))
        return terrain_map

def import_cut_graphic(path):
    surface = pygame.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_size()[0] / TILE_SIZE)
    tile_num_y = int(surface.get_size()[1] / TILE_SIZE)

    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * TILE_SIZE
            y = row * TILE_SIZE
            new_surface = pygame.Surface((TILE_SIZE, TILE_SIZE), flags= pygame.SRCALPHA)
            new_surface.blit(surface, (0,0), pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
            cut_tiles.append(new_surface)


    return cut_tiles

def import_folder(path):
    surface_list = []

    for folder_name, sub_folder, image_files in walk(path):
        for image in image_files:
            full_path = path + '/' + image
            image_surface = pygame.image.load(full_path)
            surface_list.append(image_surface)

    return surface_list