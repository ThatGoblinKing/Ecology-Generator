import pygame, random, threading
"""  **Numpy is interchangable with the default math library.**  """
import numpy as np
"""If you need to, just replace "import numpy as np" with "import math as np".
Installation of numpy is online."""
import globals as gb
from pygame import Vector2


"""
    *PLEASE READ*
    
    Hi, This is where all the core code is.

    The branch class is filled with recursion, and is the heart of the tree gen.
    Branches are drawn as two polygons to make a shape similar in attributes to pygame.rect,
    the only difference being that they aren't limited to the axis or rotation at all.

    The way that branches handle as their core structure is almost like having a line (spine) in 
    the center with two points to the sides of each side of the spine's ends.

    For example:
¯                      _____
    0══o══0           |\    |           ███████
       ║       ---    | \   |    ---    ███████
       ║       ---    |   \ |    ---    ███████
    0══o══0           |____\|           ███████
    Raw points        Polygons          Render

    0 : endpoints/corners
    o : spine ends

    To start, I would recommend making a single branch generate and render. You can set 
    the width of the polygons that make up the branch to 1 in order to see if it is rendering
    properly or not.

    gl, feel free to msg me through Dr.Mo if you need to :)



    Note: Threading doesn't significantly improve performance in most if not all cases that I tested, 
    but since it is a simple and easy implementation of threading, I left it in.
"""


"""
    These functions are here because I didn't want to deal with converting between radians and degrees manually.)
"""
def cos(angle : float) -> float:
    return np.cos(np.radians(angle))

def sin(angle : float) -> float:
    return np.sin(np.radians(angle))

class Branch:
    """
    ## Core branch class
    Please see the top of branch.py for more details
    """
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
        """
            This is the branch class, all of the variables and recursion happens at init.

            Some of the variables that are passed to the init are dormant and not meant to be tinkered with.

            #### pos
            - The position the branch is spawned at.
            - This will also be the start position of the entire tree and is located at the base of the branch.

            #### parentAngle
            - The angle inherited from the branch's "parent branch".
            - This angle is used to set the starting angle of the tree.

            #### maxLength
            - The maximum length that a branch can be.

            #### width
            - The width of the branch.
            - This is used to determine the starting width of the tree, and child branches will never be bigger 
            than the original set number.

            #### decay
            - This is a dormant variable.
            - Decay defines the % of how much width the branch should have relative to width.

            #### decayRate
            - The amount that a branch should decay in size (width) each time a branch ends or splits.

            #### branchSplit
            - This is a dormant variable.
            - The number of branches until the branch should split in two.

            #### angleChange
            - Affects how the angle of the child branches are determined.
            - If a branch is split, please see the local function, splitBranch(), in __init__() for more info
            on how the child angle of the split branch is determined.
            - If there is no split, the branch's angle = parentAngle + random.randint(-angleChange, angleChange)

            #### color
            - The color of the branch.
            - No changes are made to this through child branches.

            #### numOfBranches
            - This is a dormant variable.
            - Counts the number of branches.

            #### maxBranchSplits
            - Sets the maximum number of splits a branch can have.
            - The sum number of branches this correlates to is 2^maxBranchSplits.

            #### branchesSinceSplit
            - This is a dormant variable.
            - Counts the number of branches since the branch split in two.
        """
        
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

        """Increases width decay %"""
        self.decay -= self.decayRate

        """self.child isn't set yet, but will be soon after all of the variable initializations."""
        self.child = None
        """self.corners is a list of 4 Vector2's of each of the corners of the branch."""
        self.corners = self.getPosSides(self.pos, self.parentWidth, self.parentAngle) + self.getPosSides(self.getEndPos(), self.width * (self.decay), self.angle)

        def splitBranch():
            """
                When splitting a branch in two, this function is used to define the children of the branch.

                One of the branches will follow the roughly the same trajectory as the parent branch,
                whereas the other branch will *branch off* to a different path.
            """
            self.numOfBranches += 1
            self.child = []
            """First branch."""
            self.child.append(self.newBranch(branchesCounter=0))

            """
            This code determines the angle of the branch. It sets an offset and then give the angle change as
            a range of [self.angleChange-15, -15] to [15, 15+self.angleChange].
            """
            offset = random.randint(0, 1)
            offset = offset if offset > 0 else -1
            offset = (offset * 15) + (random.randint(0, self.angleChange) if offset > 0 else random.randint(-self.angleChange, 0))
            """Second branch."""
            self.child.append(self.newBranch(self.parentAngle + offset, branchesCounter=0))



        """If the decay is more than a min size, then the branch can split."""
        if self.decay > 0.2:
            """Logic controlling if a branch should split or not."""
            if self.branchesSinceSplit == self.branchSplit and self.numOfBranches < self.maxBranchSplits:
                """Threading"""
                if len(gb.ThreadList) <= gb.MaxThreads:
                    """
                    target is the function to run with the thread.
                    daemon is complicated, look it up if needed.
                    Make sure you store the somewhere so that it doesn't kill itself before it starts.
                    """
                    listenerThread = threading.Thread(target=splitBranch, daemon=False)
                    listenerThread.start()
                    gb.ThreadList.append(listenerThread)
                else:
                    """If there is no available space for threads, then a thread isn't created."""
                    splitBranch()
            else:
                self.child = self.newBranch()
        else:
            """Otherwise, the branch should have a leaf at the end."""
            self.child = Leaf(self.getEndPos())

    def newBranch(self, angle : float = None, branchesCounter : int = None):
        """
            This function is used to make new branches without having to input all variables 
            that are required to be passed when making a new branch, leaving only the variable that 
            need to be editable left.

            angle is treated as the __init__'s parentAngle argument.
            branchesCounter is the same as that of the __init__'s branchesCounter argument.
        """

        """Logic handling edge cases where the variables aren't defined when running newBranch()."""
        if angle == None:
            angle = self.angle

        if branchesCounter == None:
            branchesCounter = self.branchesSinceSplit + 1

        """returns the branch that was created."""
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
                      self.maxBranchSplits,
                      branchesCounter)

    def getEndPos(self, angle : float = None) -> Vector2:
        """
            Defines the end position of the branch based on the angle and length defined at init.
        """
        angle = angle if angle != None else self.angle
        """Takes the angle of the branch and the length of the branch to determine a point at which is considered the end of the branch"""
        return self.pos + Vector2(self.length * cos(angle), self.length * sin(angle))
    
    def getPosSides(self, pos : Vector2, width : float, angle : float) -> list[Vector2]:
        """
            Defines the positions of the corners associated with pos based on width.
        """
        positions = []
        """These positions are each 90 degrees to the side of the given angle, distanced by width."""
        positions.append(pos + Vector2(width * cos(angle - 90), width * sin(angle - 90)))
        positions.append(pos + Vector2(width * cos(angle + 90), width * sin(angle + 90)))
        return positions
    
    def draw(self, screen : pygame.surface) -> None:
        """
            Draws the branch to screen with two polygons and then draws all children of the parent branch.
        """
        pygame.draw.polygon(screen, self.color, self.corners[0:3])
        pygame.draw.polygon(screen, self.color, self.corners[1:4])

        if type(self.child) == Branch or type(self.child) == Leaf:
            self.child.draw(screen)
        elif type(self.child) == list:
            for branch in self.child:
                branch.draw(screen)

        """
            This code is to visualize the core points of the branch. 
            (These can be seen in the diagram at the top introduction paragraph and the text image example.)
        """
        # for pos in self.corners:
        #     pygame.draw.circle(screen, (255, 255, 255), pos, 1)
        # pygame.draw.circle(screen, (255, 0, 0), self.pos, 1)
        # pygame.draw.circle(screen, (0, 255, 0), self.getEndPos(), 1)

class Leaf:
    """
        Dummy class for the end branches of the tree.

        Doesn't do anything right now, but could be used later to create a mesh of leaves to be displayed.
    """
    def __init__(self, pos : Vector2) -> None:
        self.pos = pos

    def draw(self, screen : pygame.surface):
        """Can be used to draw the end points as "leaves"/green circles. Otherwise is just a dummy function to avoid bugs."""
        pass
        # pygame.draw.circle(screen, (0, 255, 0), self.pos, 1)