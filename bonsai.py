import pygame
from pygame import Vector2
from branch import Branch

class bonsai:
    def __init__(self, pos : Vector2) -> None:
        self.pos = Vector2(pos)
        self.branchColor = (100, 50, 25)
        self.baseWidth = 50
        self.widthDecay = .03
        self.baseAngle = -90
        self.length = 50
        self.branchSplit = 2
        self.angleChange = 15
        maxBranches = 7
        self.branches = [Branch(self.pos, -90, self.length, self.baseWidth, 1, self.widthDecay, self.branchSplit, self.angleChange, self.branchColor, 1, maxBranches, 0)]

    def draw(self, screen) -> None:
        # pygame.draw.circle(screen, (self.branchColor), self.pos, self.baseWidth)
        for branch in self.branches:
            branch.draw(screen)