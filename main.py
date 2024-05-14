import pygame
from setting import *
from levels import Level
from game_data import level_0
# imports file


pygame.init()


# pygame variables
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# instance of class
Level = Level(level_0, screen)

# game running variables
game_on = True

while game_on:

    # pygame event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()


        # key pressed event
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()


    # pygame display and updates
    screen.fill("black")

    Level.run()


    # display refresh
    pygame.display.update()
    clock.tick(50)