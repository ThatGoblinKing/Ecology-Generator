import pygame, random, threading
import numpy as np
import constants as const
from pygame import Vector2
from typing import Self

class Branch:
    def __init__(self, 
                 pos : Vector2|tuple = (0, 0),
                 parentAngle : float = -90,
                 maxLength : float = 50,
                 width : float = 50,
                 decay : float = 1,
                 decayRate : float = .03,
                 branchSplit : int = 2,
                 angleChange : float = 15,
                 color : tuple = (100, 50, 25),
                 numOfBranches : int = 1,
                 maxBranchSplits : int = 7,
                 branchesSinceSplit : int = 0) -> None:
        self.pos = Vector2(pos)
        self.parentAngle = parentAngle
        self.angle = parentAngle + random.randint(-angleChange, angleChange)
        self.maxLength = maxLength
        """length is somewhere between maxLength//2 and maxLength, it prevents the tree from looking super uniform."""
        self.length = random.randint(self.maxLength//2, self.maxLength)
        """The parent width without any modifiers applied to it to ensure that the base of the branch lines up with the end of it's parent branch."""
        self.parentWidth = width
        self.width = width
        self.decay = decay
        self.decayRate = decayRate
        self.branchSplit = branchSplit
        self.angleChange = angleChange
        self.color = color
        self.numOfBranches = numOfBranches
        self.maxBranchSplits = maxBranchSplits
        self.branchesSinceSplit = branchesSinceSplit
        self.vertices = []

        self.decay -= self.decayRate

        self.child = None
        self.topPos = (self.pos.x + (self.length * np.cos(self.angle)), self.pos.y + (self.length * np.sin(self.angle)))
        
        self.vertices.append(self.getPosSides(self.pos, self.width, self.parentAngle))
        self.vertices.append(self.getPosSides(self.topPos, self.width, self.angle))

    def getPosSides(self, pos : Vector2, width : float, angle : float) -> list[Vector2]:
        """
            Defines the positions of the corners associated with pos based on width.
        """
        positions = []
        """These positions are each 90 degrees to the side of the given angle, distanced by width."""
        positions.append(pos + Vector2(width * np.cos(angle - (np.pi/2)), width * np.sin(angle - (np.pi/2))))
        positions.append(pos + Vector2(width * np.cos(angle + (np.pi/2)), width * np.sin(angle + (np.pi/2))))
        return positions

    def drawChunk(self, screen:pygame.Surface):
        pygame.draw.polygon(screen, self.color, self.formatVertices(self.vertices))
        
    def formatVertices(self, vertices:list[Vector2]):
        vertices = [x for xs in vertices for x in xs]
        return [vertices[1], vertices[0], vertices[2], vertices[3]]