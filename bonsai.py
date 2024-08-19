import pygame
from pygame import Vector2
from branch import Branch

class bonsai:
    def __init__(self, pos : Vector2) -> None:
        self.pos = Vector2(pos)
        self.branchColor = (100, 50, 25)
        self.baseWidth = 50
        self.widthDecay = .5
        self.branches = [Branch(self.pos, -90, 100, self.baseWidth, self.baseWidth * (1-self.widthDecay), self.branchColor)]

    # def generate(self):
    #     while 

    def draw(self, screen) -> None:
        # pygame.draw.circle(screen, (self.branchColor), self.pos, self.baseWidth)
        for branch in self.branches:
            branch.draw(screen)