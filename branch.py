import pygame
import random
import numpy as np
from pygame import Vector2

def cos(angle : float) -> float:
    return np.cos(np.radians(angle))

def sin(angle : float) -> float:
    return np.sin(np.radians(angle))

class Branch:
    def __init__(self, pos : Vector2, parentAngle : float, length : float, width : float, endWidth : float, color : tuple) -> None:
        self.angle = parentAngle
        self.length = length
        self.width = width
        self.endWidth = endWidth
        self.color = color

        self.pos = Vector2(pos)

        self.corners = self.getPosSides(self.pos, self.width) + self.getPosSides(self.getEndPos(), self.endWidth)

    def getEndPos(self, angle : float = None) -> Vector2:
        """
            Defines the end position of the branch based on the angle and length defined at init
        """
        angle = angle if angle != None else self.angle
        return self.pos + Vector2(self.length * cos(angle), self.length * sin(angle))
        # return Vector2(self.pos.x + (self.length * np.cos(angle)), self.pos.y + (self.length * np.sin(angle)))
    
    def getPosSides(self, pos : Vector2, width : float) -> list[Vector2]:
        """
            Defines the positions of the corners associated with pos based on width
        """
        positions = []
        positions.append(pos + Vector2(width * cos(self.angle - 90), width * sin(self.angle - 90)))
        positions.append(pos + Vector2(width * cos(self.angle + 90), width * sin(self.angle + 90)))
        return positions
    
    def draw(self, screen) -> None:
        """
            Draws the branch to screen
        """
        pygame.draw.polygon(screen, self.color, self.corners[0:3])
        pygame.draw.polygon(screen, self.color, self.corners[1:4])

        # for pos in self.corners:
        #     pygame.draw.circle(screen, (255, 255, 255), pos, 1)
        # pygame.draw.circle(screen, (255, 0, 0), self.pos, 1)
        # pygame.draw.circle(screen, (0, 255, 0), self.pos2, 1)