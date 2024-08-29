import pygame, random, threading
import math
import constants as const
from constants import Defaults
from pygame import Vector2
from typing import Self
from math import radians as deg2rad

class Branch:
    def __init__(self, 
                 branchList : list[Self],
                 previousBranches : int = 0,
                 pos : Vector2 = Vector2(0, 0),
                 parentAngle : float = deg2rad(90),
                 maxLength : float = Defaults.MAX_LENGTH,
                 minLength : float = Defaults.MIN_LENGTH,
                 width : float = Defaults.WIDTH,
                 widthDecay : float = Defaults.DECAY_RATE,
                 angleChangeMax : float = deg2rad(Defaults.ANGLE_CHANGE),
                 angleChangeMin : float = deg2rad(-Defaults.ANGLE_CHANGE),
                 color : tuple = Defaults.TREE_COLOR,) -> None:
        self.pos = pos
        self.parentAngle = parentAngle
        self.angle = parentAngle + random.uniform(angleChangeMin, angleChangeMax)
        self.length = random.randint(minLength, maxLength)
        self.width = width
        self.color = color
        self.branchList = branchList
        self.previousBranches = previousBranches
        self.topWidth = width * widthDecay
        if previousBranches == 0:
            self.width *= 2
        self.topPos = Vector2(self.pos.x - (self.length * math.cos(self.angle)), self.pos.y - (self.length * math.sin(self.angle)))

        self.vertices = self.getVerts()

        if previousBranches < const.MAX_DEPTH:
            if previousBranches != 0 and previousBranches % const.SPLIT_RATE == 0:
                branchList.extend(self.splitBranches())
            else:
                branchList.append(Branch(branchList,
                                        previousBranches=previousBranches + 1,
                                        pos=self.topPos,
                                        parentAngle=self.angle,
                                        maxLength=maxLength,
                                        width=self.topWidth,
                                        widthDecay=widthDecay,
                                        angleChangeMax=angleChangeMax,
                                        angleChangeMin=angleChangeMin,
                                        color=color))

    def getVerts(self) -> list[Vector2]:
        positions : list[Vector2] = []
        #Get Bottoms Verts
        positions.append(Vector2(self.pos.x + (self.width * math.cos(self.parentAngle - deg2rad(90))), self.pos.y + (self.width * math.sin(self.parentAngle - deg2rad((90))))))
        positions.append(Vector2(self.pos.x + (self.width * math.cos(self.parentAngle - deg2rad(-90))), self.pos.y + (self.width * math.sin(self.parentAngle - deg2rad((-90))))))
        #Get Top Verts
        positions.append(Vector2(self.topPos.x + (self.topWidth * math.cos(self.angle - deg2rad(-90))), self.topPos.y + (self.topWidth * math.sin(self.angle - deg2rad((-90))))))
        positions.append(Vector2(self.topPos.x + (self.topWidth * math.cos(self.angle - deg2rad(90))), self.topPos.y + (self.topWidth * math.sin(self.angle - deg2rad((90))))))

        return positions

    def draw(self, screen:pygame.Surface):
        pygame.draw.polygon(screen, self.color, self.vertices)
        if const.DEBUG_MODE:
            # for coord in self.vertices:
            #     pygame.draw.circle(screen, (0,255,0), coord, 5)
            pygame.draw.circle(screen, (255,0,255), self.pos, 5)
            pygame.draw.circle(screen, (0,0,255), self.topPos, 5)
            pygame.draw.circle(screen, (0,255,255), self.vertices[0], 5)
            pygame.draw.circle(screen, (0,255,255), self.vertices[1], 5)

    def splitBranches(self) -> list[Self, Self]:
        leftWidthPercent = random.uniform(.25,.75)
        rightWidth = self.topWidth * leftWidthPercent
        leftWidth = self.topWidth * (1- leftWidthPercent)
        leftPos = self.topPos + (math.cos(self.angle + deg2rad(90)) * leftWidth, math.sin(self.angle + deg2rad(90)) * leftWidth)
        rightPos = self.topPos + (math.cos(self.angle - deg2rad(90)) * rightWidth , math.sin(self.angle - deg2rad(90)) * rightWidth )
        leftBranch = Branch(branchList=self.branchList,
                            previousBranches=self.previousBranches * 2,
                            pos=leftPos,
                            parentAngle=self.angle,
                            width=rightWidth,
                            angleChangeMax=deg2rad(-30),
                            angleChangeMin=deg2rad(5)
                            )
        rightBranch = Branch(branchList=self.branchList,
                            previousBranches=self.previousBranches * 2,
                            pos=rightPos,
                            parentAngle=self.angle,
                            width=leftWidth,
                            angleChangeMin=deg2rad(-5),
                            angleChangeMax=deg2rad(30)
                            )

        return [leftBranch, rightBranch]