# STD Library
import math
import random
import time

# GUI framework
import pygame
import pygame_menu

#Project Library
from Cell import Cell

# Colors used by the GUI objects.
COLORS = {
    "BLACK": (0, 0, 0),
    "GREY": (100,100,100),
    "RED": (255, 0, 0),
    "BLUE": (0, 0, 255),
    "GREEN": (0, 255, 0),
    "WHITE": (255, 255, 255)
}

class GUI:

    # Creates a blank screen GUI.
    def __init__(self):

        # Initialize pygame
        pygame.init()

        #Set pygame window size
        self.width = 900
        self.height = 900
            

        # Selector variables.
        self.gridSize = ("None", 0)
        self.obstaclePercent = ("0%", 0)
        self.autoGenSG = ("No", 0)

        # Initialize GUI to start menu.
        self.startMenu()

    # Callback function for use with the start menu to set the selected environment.
    def setGrid(self, gridS, args=None):
        self.gridSize = gridS[0]
    
    # Callback function for use with the start menu to set the selected obstacle percentage.
    def setObstacles(self, obsP, args=None):
        self.obstaclePercent = obsP[0]

    def setAutoGen(self, isAuto, args=None):
        self.autoGenSG = isAuto[0]

    # Adds or removes information text.
    def setInformationLabels(self):
        if not self.informationLabelsVisible:
            self.addInformationLabels()
            self.informationLabelsVisible = True
        
        else:
            self.removeInformationLabels()
            self.informationLabelsVisible = False
        
    # Creates the start selection menu for environment, algorithm selection.
    def startMenu(self, notify=False):

        # Create pygame window.
        self.window = pygame.display.set_mode((self.width, self.height), vsync=True)

        # Checks if the algorithm has run, used to prevent changes.
        self.run = False

        # Start and goal nodes for the algorithm, will be a cell object.
        self.start = None
        self.goal = None

        # Selector variables.
        self.gridSize = ("None", 0)
        self.obstaclePercent = ("0%", 0)
        self.autoGenSG = ("No", 0)
        
        self.window.fill(COLORS["WHITE"])

        pygame.display.set_caption("CAP4630 Final Project")

        pygame.display.update()

        # Create the menu object on the pygame window.
        self.menu = pygame_menu.Menu(self.height, self.width, "Welcome", theme=pygame_menu.themes.THEME_DEFAULT)

        # Notify the user that the goal could not be found for a given cost.
        if notify:
            self.notifyNoPath = self.menu.add_label("A path from the start to goal does not exist.", max_char=-1, font_size=20)
        
        # Add widgets to the menu.
        self.menu.add_selector("Grid Size:", [("Select a Grid Size", 0), ("50x50", 50), ("100x100", 100), ("200x200", 200), ("300x300", 300)], onchange=self.setGrid)
        self.menu.add_selector("Obstacle Percentage", [("0%", 0), ("10%", 10), ("20%", 20), ("30%", 30)], onchange=self.setObstacles)
        self.menu.add_selector("Auto Generate Start and Goal", [("No", 0), ("Yes", 1)], onchange=self.setAutoGen)
        self.weightField = self.menu.add_text_input("Weight (w): ", input_type=pygame_menu.locals.INPUT_INT)
        self.deltaWeightField = self.menu.add_text_input("Change in Weight (delta_w): ", input_type=pygame_menu.locals.INPUT_FLOAT)
        self.menu.add_button("Create Grid", self.runAlgorithm)
        self.menu.add_button("Information", self.setInformationLabels)
        # Information is hidden until the button it toggled.
        self.informationLabelsVisible = False
        self.quitButton = self.menu.add_button('Quit', pygame_menu.events.EXIT)
        
        self.menu.mainloop(self.window)

    # Adds the information text to the menu.
    def addInformationLabels(self):

        # Removes the quit button to be relocated.
        self.menu.remove_widget(self.quitButton)

        # Adds all information labels to the menu.
        self.informationLabels = list()

        self.informationLabels.append(self.menu.add_label("Instructions:", max_char=-1, font_size=25))
        self.informationLabels.append(self.menu.add_label("1) Select a grid size with the selector.", 
        max_char=-1, font_size=15))
        self.informationLabels.append(self.menu.add_label("2) Optionally, select the percentage of cells to be generated as obstacles, the default is zero.", 
        max_char=-1, font_size=15))
        self.informationLabels.append(self.menu.add_label("3) Optionally, select to generate a cell for the start and a cell for the goal.", 
        max_char=-1, font_size=15))
        self.informationLabels.append(self.menu.add_label("4) Set a w and delta w by entering a number in the entry boxes.", 
        max_char=-1, font_size=15))
        self.informationLabels.append(self.menu.add_label("5) Select Create Grid to generate the selected grid and obstacles.", 
        max_char=-1, font_size=15))
        self.informationLabels.append(self.menu.add_label("6) Once in the grid the you may left click to create a start, end, and obstacles.", 
        max_char=-1, font_size=15))
        self.informationLabels.append(self.menu.add_label("7) In the grid the you may right click to reset a cell.", 
        max_char=-1, font_size=15))
        self.informationLabels.append(self.menu.add_label("8) To run the algorithm hit the space bar.", 
        max_char=-1, font_size=15))
        self.informationLabels.append(self.menu.add_label("9) Press esc to leave the visualization window and return to the menu. From here you may select new options.", 
        max_char=-1, font_size=15))
        self.informationLabels.append(self.menu.add_label("Notes:", max_char=-1, font_size=25))
        self.informationLabels.append(self.menu.add_label("For the obstacle and start/goal genrators all cells selected are random, but can be changed as mentioned above.",
        max_char=-1, font_size=15))
        self.informationLabels.append(self.menu.add_label("When selecting your own cells, the order in which they will be generates is start, goal, obstacles.",
        max_char=-1, font_size=15))
        self.informationLabels.append(self.menu.add_label("It is recommended to auto-generate the obstacles, start, and goal for the 200x200 and 300x300 grid.",
        max_char=-1, font_size=15))

        # Relocates the quit button to the end of the menu.
        self.quitButton = self.menu.add_button('Quit', pygame_menu.events.EXIT)

    # Removes the information text from the menu.
    def removeInformationLabels(self):

        for label in self.informationLabels:
            self.menu.remove_widget(label)

    # Creates a grid of nxn cells.
    def makeGrid(self):

        grid = list()
        for l in range(self.numCells1D):
            grid.append([None] * self.numCells1D)


        # Computes the size of an individual cell.
        size = self.width // self.numCells1D

        # Creates n^2 cells in a grid matrix.
        for i in range(self.numCells1D):
            for j in range(self.numCells1D):
                cell = Cell(i, j, size, self.numCells1D)
                grid[i][j] = cell

        self.grid = grid

    # Randomly generates a start and goal cell on the grid. 
    def generateSG(self):
        randX = random.randint(0, self.numCells1D) -1
        randY = random.randint(0, self.numCells1D) -1

        self.grid[randY][randX].setStatus("START")
        self.start = self.grid[randY][randX]

        # Check goal is not the same as start.
        while self.goal is None:
            randX = random.randint(0, self.numCells1D) -1
            randY = random.randint(0, self.numCells1D) -1

            cell = self.grid[randY][randX]

            if cell is self.start:
                continue
            else:
                self.grid[randY][randX].setStatus("GOAL")
                self.goal = self.grid[randY][randX]

    # Randomly generates obstacles on the grid, number generates is user selected percentage of the number of grid cells.
    def createObstacles(self, obsPercent):

        numObs = (self.numCells1D * self.numCells1D) * obsPercent

        while numObs > 0:
            randX = random.randint(0, self.numCells1D) -1
            randY = random.randint(0, self.numCells1D) -1
            if self.grid[randY][randX].getStatus() != "AVAILABLE":
                continue
            else:
                self.grid[randY][randX].setStatus("OBSTACLE")
                numObs -= 1

    # Draws the grid lines to creates the cells.
    def drawGrid(self):

        # Computes the size of an individual cell.
        size = self.width // self.numCells1D

        # Draws column and row lines.
        for i in range(self.numCells1D+1):
            pygame.draw.line(self.window, COLORS["GREY"], (0, i*size), (self.width, i*size))
            for j in range(self.numCells1D+1):
                pygame.draw.line(self.window, COLORS["GREY"], (j*size, 0), (j*size, self.width))

    # Computes the path given a goal cell by following its parents to start.
    def getPath(self, cell):

        path = list()

        path.insert(0, cell)
        while cell.getParent() != None:
            path.insert(0, cell.getParent())
            cell = cell.getParent()

        return path

    # Draws the path to goal from start.
    def drawPath(self, path, pathType):
        pathType = "PATH"+pathType
        for node in path:
            node.setStatus(pathType)
            self.draw()

        self.draw()

    # Resets the board, then redraws the lines and any cell changes.
    def draw(self):

        self.window.fill(COLORS["WHITE"])

        # Redraw each cell.
        for row in self.grid:
            for cell in row:
                cell.draw(self.window)

        # Redraw grid lines.
        self.drawGrid()

        # Update the display.
        pygame.display.update()

    # When the user wishes to visualize the selected algorithm on the selected environment, this method acts as the switch case
    # to run and animate the selected algorithm.
    def runAlgorithm(self):
        
        (envName, envID) = self.gridSize
        (obstacles, obstaclePercentVal) = self.obstaclePercent
        (autoGen, isAutoGenSG) = self.autoGenSG

        # Stays on the start menu if no environment or algorithm are selected.
        if envID == 0:
            return

        # Destroys start menu page.
        self.menu.disable()
    
        # Sets the number of cells, and preforms the initial draw.
        self.numCells1D = envID

        if(self.numCells1D == 200):
            self.window = pygame.display.set_mode((self.width-100, self.height-100), vsync=True)


        # Creates the grid of cells matrix.
        self.makeGrid()
        
        if isAutoGenSG == 1:
            self.generateSG()

        # Creates the specified percentage of obstacles cells, the cells are random.
        self.createObstacles(obstaclePercentVal/100)

        # Draws the initial board.
        self.draw()

    # The ARA* algorithm, uses a weight on the heuristic component that is lowered after every improve subroutine. Eventually pure A* is reached.
    def araStar(self):

        # The weight applied to the heuristic cost, the hight the w the more greedy the search.
        w = self.weightField.get_value()

        # Value to lower the weight by every iteration.
        delta_w  = self.deltaWeightField.get_value()

        # The current solution.
        incumbent = None

        # The recently found solution.
        solution  = None

        # The current solutions cost.
        costG = math.inf

        # Open and closed sets.
        open = dict()
        closed = list()

        # Sets the initial costs and heuristic costs for all the nodes.
        self.start.setCost(0)
        self.start.setHeuristicCost(self.start.heuristicFunction(self.goal))
        self.start.setEstimatedCost(w)

        for i in range(self.numCells1D):
            for j in range(self.numCells1D):
                if self.grid[i][j] is self.start or self.grid[i][j] is self.goal:
                    continue
                else:
                    self.grid[i][j].setCost(math.inf)
                    self.grid[i][j].setHeuristicCost(self.grid[i][j].heuristicFunction(self.goal))
                    self.grid[i][j].setEstimatedCost(w)

        self.goal.setCost(math.inf)
        self.goal.setHeuristicCost(0)
        self.goal.setEstimatedCost(math.inf)


        # Places the start node in the open set to begin search.
        open[self.start] = self.start

        # While there are nodes in open try to improve.
        while len(open) != 0:

            # Attempts to find a solution with a lower cost than the current solution.
            solution = self.improveSolution(open, closed, w, costG)

            # If a solution is found, set cost and incumbent to the result of the solution, and draw the current solutions path.
            if solution is not None:
                costG = solution[0]
                incumbent = solution[1]
                self.drawPath(incumbent, "TEMP")
            
            # A new solution was not found, if no solution exists notify, else draw the current best solutions path.
            else:
                if incumbent == None:
                    pygame.time.delay(2500)
                    self.startMenu(notify=True)
                    return
                self.drawPath(incumbent, "FINAL")
                return
            
            # Decrease weight.
            w = w - delta_w

            # Prune nodes with g() + h() >= cost
            nodesToRemove = list()
            for key in open:
                if open[key].getCost() + open[key].getHeuristicCost()  > costG:
                    open[key].setStatus("CLOSED")
                    nodesToRemove.append(key)
                    closed.append(open[key])

            for key in nodesToRemove:    
                open.pop(key)

            # Update costs with new w.
            for key in open:
                open[key].setEstimatedCost(w)

            # Draw the new state.
            self.draw()

        # Draw the final path.  
        self.drawPath(incumbent, "FINAL")

    # The solution finder of the ARA* algorithm.
    def improveSolution(self, open, closed, w, costG):

        # While nodes are in open search.
        while len(open) != 0:

            # Sort open by f_w(n).
            openList = list(open)
            openList.sort(key=lambda x:x.getEstimatedCost())

            # Get the n with min f_w(n).
            n = openList[0]

            # Remove node from open and place in closed.
            if n is not self.start and n is not self.goal:
                open[n].setStatus("CLOSED")
            closed.append(n)
            open.pop(n)

            # Show the new state of the grid.
            self.draw()

            # Test that cost is w admissable, if cost < estimated costs no new better solution exists.
            if costG <= n.getEstimatedCost():
                return None
            
            # Process the neighbors.
            for neighbor in n.getNeighbors():

                # If the neighbor is has not been expanded, and is not in open or has a better new cost, set costs.
                if neighbor not in closed and (neighbor not in open or n.getCost() + 1 < neighbor.getCost()):

                    # Sets the cost to reach a node, estimated cost, and parent node.
                    neighbor.setCost(n.getCost() + 1)
                    neighbor.setEstimatedCost(w)
                    neighbor.setParent(n)

                    # Check that the f(n) meets the constraint.
                    if neighbor.getCost() + neighbor.getHeuristicCost() < costG:

                        # If the neighbor is a goal end and return.
                        if neighbor is self.goal:
                            return (neighbor.getCost(), self.getPath(neighbor))

                        # If not a goal place in open.
                        if neighbor not in open:
                            open[neighbor] = neighbor
                            neighbor.setStatus("OPEN")

        # No new solution.
        return None

    # Gameloop
    def mainLoop(self):

        run = True
        # Checks user inputs.
        while run:
            self.draw()
            for event in pygame.event.get():
                # If the exit button is selected quit.
                if event.type == pygame.QUIT:
                    run = False

                # If escape is pressed return to the start menu.
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.startMenu()

                    if event.key == pygame.K_SPACE and self.start and self.goal:
                        self.run = True
                        for i in range(self.numCells1D):
                            for j in range(self.numCells1D):
                                self.grid[i][j].setNeighbors(self.grid)
                        start_time = time.time()
                        self.araStar()
                        print("--- %s seconds ---" % (time.time() - start_time))
                
                # Checks for a left mouse click.
                if pygame.mouse.get_pressed()[0] and not self.run:

                    # Gets the cell coresponding to the mouse click location.
                    row, col = getMousePosCell(pygame.mouse.get_pos(), self.numCells1D, self.width)
                    cell = self.grid[row][col]

                    # Sets the start cell if not already.
                    if not self.start and cell is not self.goal:
                        self.start = cell
                        cell.setStatus("START")

                    # Sets the goal cell if not already.
                    elif not self.goal and cell is not self.start:
                        self.goal = cell
                        cell.setStatus("GOAL")

                    # Sets obstacle cells if start and goal are already created.
                    elif cell is not self.start and cell is not self.goal:
                        cell.setStatus("OBSTACLE")

                # Checks for a right mouse click.
                elif pygame.mouse.get_pressed()[2] and not self.run:

                    # Gets the cell coresponding to the mouse click location.
                    row, col = getMousePosCell(pygame.mouse.get_pos(), self.numCells1D, self.width)
                    cell = self.grid[row][col]

                    # Resets the cell status, and resets start or goal if clicked.
                    cell.reset()
                    if cell is self.start:
                        self.start = None
                    elif cell is self.goal:
                        self.goal = None

        pygame.quit()

# Computes the cell given the position of a mouse click.
def getMousePosCell(mousePos, rows, size):
    spacing = size // rows
    y,x = mousePos

    row = y // spacing
    col = x // spacing

    return row, col