import pygame
import globals as gb
from pygame import Vector2
from branch import Branch

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
"""

pygame.init

screen = pygame.display.set_mode((gb.SX, gb.SY))

doExit = False
clock = pygame.time.Clock()

tree = Branch(Vector2(gb.SX/2, gb.SY * (54/55)))

while not doExit:
    delta = clock.tick(gb.FPS)/1000
    screen.fill(gb.BG)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            doExit = True

    """Reset Tree."""
    keys = pygame.key.get_pressed()
    if keys[pygame.K_r]:
        tree = Branch(Vector2(gb.SX/2, gb.SY * (54/55)))

    tree.draw(screen)

    pygame.display.flip()
pygame.quit()