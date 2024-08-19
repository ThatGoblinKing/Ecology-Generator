import pygame
import globals as gb
from pygame import Vector2
from bonsai import bonsai

pygame.init

screen = pygame.display.set_mode((gb.SX, gb.SY))

doExit = False
clock = pygame.time.Clock()

test = bonsai(Vector2(gb.SX/2, gb.SY * (54/55)))

while not doExit:
    delta = clock.tick(gb.FPS)/1000
    screen.fill(gb.BG)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            doExit = True

    keys = pygame.key.get_pressed()

    if keys[pygame.K_r]:
        test = bonsai(Vector2(gb.SX/2, gb.SY * (54/55)))

    test.draw(screen)

    pygame.display.flip()
pygame.quit()