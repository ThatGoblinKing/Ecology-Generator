import pygame
import globals as gb
from pygame import Vector2
from bonsai import bonsai

pygame.init

screen = pygame.display.set_mode((gb.SX, gb.SY))

doExit = False
clock = pygame.time.Clock()

test = bonsai(Vector2(gb.SX/2, gb.SY * (4/5)))

while not doExit:
    delta = clock.tick(gb.FPS)/1000
    screen.fill(gb.BG)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            doExit = True

    test.draw(screen)

    pygame.display.flip()
pygame.quit()