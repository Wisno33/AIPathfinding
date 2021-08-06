# STD Library
import math

#Pygame
import pygame

# Colors used by the GUI objects, used to denote the status or state of the cell.
STATUS = {
    "OBSTACLE": (0, 0, 0),
    "CLOSED": (255, 0, 0),
    "OPEN": (0, 0, 255),
    "PATHTEMP": (48, 213, 200),
    "PATHFINAL": (0, 255, 0),
    "AVAILABLE": (255, 255, 255),
    "START": (255, 165, 0),
    "GOAL": (128, 0, 128),
}

class Cell:

    # Creates a cell with location [row][col] and pixel size, color is set to white to begin. Denotes an available cell.
    def __init__(self, row, col, size, numRows):
        self.row = row
        self.col = col
        self.size = size
        self.status = "AVAILABLE"
        self.color = STATUS[self.status]

        # Sets the x,y screen position
        self.x = row * size
        self.y = col * size

        # The cost values for the algorithm to use.
        self.cost = math.inf #g(n) actual cost.
        self.heuristicCost = math.inf #h(n) heuristic cost
        self.estimatedCost = math.inf #f_w(n) = g(n) + w(h(n)) the estimated cost with weight w applied to the heuristic value.

        # Parent node for path tracing
        self.parent = None

        # Sets the neighbors of the cell.
        self.neighbors = list()
        
        # Number of total rows used to get valid neighbors.
        self.numRows = numRows

    # Returns the row and column number location.
    def getPosition(self):
        return self.row, self.col

    # Sets the status and color of a cell.
    def setStatus(self, newStatus):
        self.status = newStatus
        self.color = STATUS[self.status]

    def getStatus(self):
        return self.status

    # Set the cell to the starting status.
    def reset(self):
        self.setStatus("AVAILABLE")

    # Set the neighboring cells, if a cell is an obstacle it is not a valid neighbor and is not added.
    def setNeighbors(self, grid):
        self.neighbors = []
        #Down
        if self.row < self.numRows - 1 and grid[self.row + 1][self.col].getStatus() != "OBSTACLE":
            self.neighbors.append(grid[self.row + 1][self.col])
        #Up
        if self.row > 0 and grid[self.row - 1][self.col].getStatus() != "OBSTACLE":
            self.neighbors.append(grid[self.row - 1][self.col])
        #Right
        if self.col < self.numRows - 1 and grid[self.row][self.col + 1].getStatus() != "OBSTACLE":
            self.neighbors.append(grid[self.row][self.col + 1])
        #Left
        if self.col > 0 and grid[self.row][self.col - 1].getStatus() != "OBSTACLE":
            self.neighbors.append(grid[self.row][self.col - 1])

    # Returns the list of neighbors of the given cell.
    def getNeighbors(self):
        return self.neighbors

    def setCost(self, cost):
        self.cost = cost
        
    def getCost(self):
        return self.cost

    def setHeuristicCost(self, costH):
        self.heuristicCost = costH

    def getHeuristicCost(self):
        return self.heuristicCost
    
    def setEstimatedCost(self, hWeight):
        self.estimatedCost = self.cost + (hWeight * self.heuristicCost)

    def getEstimatedCost(self):
        return self.estimatedCost

    # Manhattan distance function.
    def heuristicFunction(self, goal):
        x1, y1 = self.getPosition()
        x2, y2 = goal.getPosition()
        return abs(x1 - x2) + abs(y1 - y2)

    def setParent(self, pCell):
        self.parent = pCell
    
    def getParent(self):
        return self.parent

    # Fills the cell with the color coresponding to the status of the cell.
    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.size, self.size))