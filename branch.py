import pygame
import random
import threading
import numpy as np
import globals as gb
from pygame import Vector2

def cos(angle : float) -> float:
    return np.cos(np.radians(angle))

def sin(angle : float) -> float:
    return np.sin(np.radians(angle))

class Branch:
    def __init__(self, 
                 pos : Vector2, 
                 parentAngle : float, 
                 maxLength : float,
                 width : float, 
                 decay : float, 
                 decayRate : float, 
                 branchSplit : int, 
                 angleChange : float, 
                 color : tuple,
                 numOfBranches : int,
                 maxBranches : int,
                 branchesSinceSplit : int) -> None:
        
        print(f"New branch! branches : {numOfBranches}")
        
        self.parentAngle = parentAngle
        self.angle = parentAngle + random.randint(-angleChange, angleChange)
        self.maxLength = maxLength
        self.length = random.randint(self.maxLength//2, self.maxLength)
        self.width = width
        self.decay = decay
        self.decayRate = decayRate
        self.branchSplit = branchSplit
        self.angleChange = angleChange
        self.color = color
        self.numOfBranches = numOfBranches
        self.maxBranches = maxBranches
        self.branchesSinceSplit = branchesSinceSplit
        self.child = None

        self.pos = Vector2(pos)

        self.corners = self.getPosSides(self.pos, self.width, self.parentAngle) + self.getPosSides(self.getEndPos(), self.width * (self.decay), self.angle)

        def splitBranch():
            self.numOfBranches += 1
            self.child = []
            self.child.append(self.newBranch(branchesCounter=0))

            num = random.randint(0, 1)
            num = num if num > 0 else -1
            num = (num * 15) + (random.randint(0, 15) if num > 0 else random.randint(-15, 0))
            self.child.append(self.newBranch(self.parentAngle + num, branchesCounter=0))

        self.decay -= self.decayRate
        if self.decay > 0.2:
            if self.branchesSinceSplit == self.branchSplit and self.numOfBranches < self.maxBranches:
                if len(gb.ThreadList) <= gb.MaxThreads:
                    listenerThread = threading.Thread(target=splitBranch)
                    listenerThread.daemon = True
                    listenerThread.start()
                    gb.ThreadList.append(listenerThread)
                else:
                    splitBranch()
            else:
                self.child = self.newBranch()
        else:
            self.child = Leaf(self.getEndPos())

    def newBranch(self, angle = None, branchesCounter = None):
        if angle == None:
            angle = self.angle

        if branchesCounter == None:
            branchesCounter = self.branchesSinceSplit + 1

        return Branch(self.getEndPos(), 
                      angle, 
                      self.maxLength,
                      self.width * (self.decay), 
                      self.decay, 
                      self.decayRate, 
                      self.branchSplit, 
                      self.angleChange, 
                      self.color,
                      self.numOfBranches,
                      self.maxBranches,
                      branchesCounter)

    def getEndPos(self, angle : float = None) -> Vector2:
        """
            Defines the end position of the branch based on the angle and length defined at init
        """
        angle = angle if angle != None else self.angle
        return self.pos + Vector2(self.length * cos(angle), self.length * sin(angle))
        # return Vector2(self.pos.x + (self.length * np.cos(angle)), self.pos.y + (self.length * np.sin(angle)))
    
    def getPosSides(self, pos : Vector2, width : float, angle : float) -> list[Vector2]:
        """
            Defines the positions of the corners associated with pos based on width
        """
        positions = []
        positions.append(pos + Vector2(width * cos(angle - 90), width * sin(angle - 90)))
        positions.append(pos + Vector2(width * cos(angle + 90), width * sin(angle + 90)))
        return positions
    
    def draw(self, screen) -> None:
        """
            Draws the branch to screen
        """
        pygame.draw.polygon(screen, self.color, self.corners[0:3])
        pygame.draw.polygon(screen, self.color, self.corners[1:4])

        if type(self.child) == Branch or type(self.child) == Leaf:
            self.child.draw(screen)
        elif type(self.child) == list:
            for branch in self.child:
                branch.draw(screen)

        # for pos in self.corners:
        #     pygame.draw.circle(screen, (255, 255, 255), pos, 1)
        # pygame.draw.circle(screen, (255, 0, 0), self.pos, 1)
        # pygame.draw.circle(screen, (0, 255, 0), self.pos2, 1)

class Leaf:
    def __init__(self, pos : Vector2) -> None:
        self.pos = pos

    def draw(self, screen):
        pass
        # pygame.draw.circle(screen, (0, 255, 0), self.pos, 1)