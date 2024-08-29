import pygame
import constants as const
from pygame import Vector2
from branch import Branch
import random

"""For information on how exactly the program functions, please go to branch.py."""

"""
    Hello student! My name is Tess and I made this tree generator, I hope you have fun looking at my code and best of luck!


    Here are some things to do in order to make your own tree gen:
    - Render two polygons by using 4 points that make a quad on the screen

    - Define the points in relation to a line that goes at the center of the quad. (check branch.py for visuals)

    - Define a branch class with all of the previous steps included in it

    - Recursion!!! Make the branch spawn branches that spawn branches that spawn branches that spawn branches that spawn branches that spawn branches that spawn branches that spawn branches that spawn branches that spawn branches that spawn branches that spawn branches that spawn branches that spawn branches that spawn branches that spawn branches that spawn branches that spawn branches that spawn branches that spawn branches that spawn branches that spawn branches that spawn branches that spawn branches that spawn branches that spawn branches that spawn branches that spawn branches that spawn branches that spawn branches that spawn branches that spawn branches that spawn branches that spawn branches that spawn branches that spawn branches that spawn branches that spawn branches that spawn branches that spawn branches that spawn branches that spawn branches that spawn branches that spawn branches that spawn branches that spawn branches etc. 

    - Congrats, that's all I have here now.

    
    Potential next steps:
    - something with the empty dummy Leaf class

    - Wind and updating the branch positions relative to each parent branch



    Cool keyboard shortcuts:
    - ctrl + bracket keys
        Move your line back and forth by a tab
    
    - ctrl + shift + Enter
        Create a new line above your selected line

    - alt + numpad
        You can create a bunch of super cool symbols like: ™ü╚▼☻Y
        Look up a list of the commands to figure out which ones are there if you need
"""

pygame.init

screen = pygame.display.set_mode((const.SCREEN_X, const.SCREEN_Y))

doExit = False
clock = pygame.time.Clock()
branches : list[Branch] = []

branches.append(Branch(branchList=branches,pos=Vector2(const.SCREEN_X/2, const.SCREEN_Y)))

while not doExit:
    delta = clock.tick(const.FPS)/1000
    screen.fill(const.BACKGROUND_COLOR)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            doExit = True

    """Reset Tree."""
    keys = pygame.key.get_pressed()
    if keys[pygame.K_r]:
        branches = []
        branches.append(Branch(branchList=branches,pos=Vector2(const.SCREEN_X/2, const.SCREEN_Y)))

    for branch in branches:
        branch.draw(screen)

    pygame.display.flip()
pygame.quit()