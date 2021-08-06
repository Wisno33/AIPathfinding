# GUI framework
import pygame
import pygame_menu

# Project Libraries
import Environments
from Graph import AdjacencyList
import AStar
import PotentialSearch

# Colors used by the GUI objects.
COLORS = {
    "BLACK": (0, 0, 0),
    "RED": (255, 0, 0),
    "BLUE": (0, 0, 255),
    "GREEN": (0, 255, 0),
    "WHITE": (255, 255, 255)
}

# The visualization class.
class GUI:

    # Creates a blank screen GUI.
    def __init__(self):

        # Create pygame window
        pygame.init()
        self.width = 1050
        self.height = 550
        self.window = pygame.display.set_mode((self.width, self.height), vsync=True)

        # The environment and algorithm to be visualized
        self.environment = ("None", 0)
        self.algorithm = ("None", 0)

        # Initialize GUI to start menu.
        self.startMenu()

    # Serves as the SWITCH-CASE for environment selection.
    # Callback function for use with the start menu to set the selected environment.
    def setEnvironment(self, env, args=None):
        self.environment = env[0]

    # Serves as the SWITCH-CASE for algorithm selection.
    # Callback function for use with the start menu to set the selected algorithm.
    def setAlgorithm(self, algo, args=None):
        self.algorithm = algo[0]

        # Check if potential search is selected if true add the cost field.
        if self.algorithm[0] == "Potential Search":

            # Removes widgets to relocate them under the cost entry field.
            self.menu.remove_widget(self.runButton)
            self.menu.remove_widget(self.infoButton)
            self.setInformationLabels()
            self.menu.remove_widget(self.quitButton)  

            # Cost entry field.
            self.costField = self.menu.add_text_input("Cost (C): ", input_type=pygame_menu.locals.INPUT_INT)

            # Relocated widgets
            self.runButton = self.menu.add_button('Visualize', self.runAlgorithm)
            self.infoButton = self.menu.add_button("Information", self.setInformationLabels)
            self.quitButton = self.menu.add_button('Quit', pygame_menu.events.EXIT)
            self.setInformationLabels()

        # If potential search is not selected and the cost field is present remove it.
        elif self.costField != None:
            self.menu.remove_widget(self.costField)
            self.costField = None

    # Creates the start selection menu for environment, algorithm selection.
    def startMenu(self, notify=False):

        # The environment and algorithm to be visualized
        self.environment = ("None", 0)
        self.algorithm = ("None", 0)
        
        self.window.fill(COLORS["WHITE"])

        pygame.display.set_caption("CAP4630 Assignment 2")

        pygame.display.update()

        # Create the menu object on the pyagame window.
        self.menu = pygame_menu.Menu(self.height, self.width, "Welcome", theme=pygame_menu.themes.THEME_DEFAULT)
        
        # Notify the user that the goal could not be found for a given cost.
        if notify:
            self.notifyLowCost = self.menu.add_label("Cost too low no path found!", max_char=-1, font_size=20)

        # Add widgets to the menu.
        self.environmentSelector = self.menu.add_selector("Environment:", [("Select an Environment", 0),("3.31", 1), ("Manhattan", 2), ("Around the Block", 3)],
             onchange=self.setEnvironment)
        self.algorithmSelector = self.menu.add_selector("Algorithm:", [("Select an Algorithm", 0),("A*", 1), ("Potential Search", 2)], onchange=self.setAlgorithm)
        self.costField = None
        self.runButton = self.menu.add_button('Visualize', self.runAlgorithm)
        self.infoButton = self.menu.add_button("Information", self.setInformationLabels)
        # Information is hidden until the button it toggled.
        self.informationLabelsVisible = False
        self.quitButton = self.menu.add_button('Quit', pygame_menu.events.EXIT)
        
        self.menu.mainloop(self.window)

    # Adds or removes information text.
    def setInformationLabels(self):
        if not self.informationLabelsVisible:
            self.addInformationLabels()
            self.informationLabelsVisible = True
        
        else:
            self.removeInformationLabels()
            self.informationLabelsVisible = False

    # Adds the information text to the menu.
    def addInformationLabels(self):

        # Removes the quit button to be relocated.
        self.menu.remove_widget(self.quitButton)

        # Adds all information labels to the menu.
        self.informationLabels = list()

        self.informationLabels.append(self.menu.add_label("Instructions:", max_char=-1, font_size=25))
        self.informationLabels.append(self.menu.add_label("1) Select an environment with the selector.", 
        max_char=-1, font_size=20))
        self.informationLabels.append(self.menu.add_label("2) Select an algorithm with the selector.", 
        max_char=-1, font_size=20))
        self.informationLabels.append(self.menu.add_label("3) Select Visualize to run the selected algorithm on the selected environment.", 
        max_char=-1, font_size=20))
        self.informationLabels.append(self.menu.add_label("4) Press esc to leave the visualization window and return to the menu.", 
        max_char=-1, font_size=20))
        self.informationLabels.append(self.menu.add_label("5) For the Potential Search algorithm a cost field is added, input a cost constraint into the entry box.", 
        max_char=-1, font_size=20))
        self.informationLabels.append(self.menu.add_label("Notes:", max_char=-1, font_size=25))
        self.informationLabels.append(self.menu.add_label("Please allow the tool time to generate the environment. This is longer on the first run of the environment.",
         max_char=-1, font_size=20))
        self.informationLabels.append(self.menu.add_label("After an environment is visualized it is cached so it can be run instantly next time.",
         max_char=-1, font_size=20))

        # Relocates the quit button to the end of the menu.
        self.quitButton = self.menu.add_button('Quit', pygame_menu.events.EXIT)
    
    # Removes the information text from the menu.
    def removeInformationLabels(self):

        for label in self.informationLabels:
            self.menu.remove_widget(label)

    # When the user wishes to visualize the selected algorithm on the selected environment, this method acts as the switch
    # case to generate the chosen environment.
    def createEnvironment(self, envID):

        self.window.fill(COLORS["WHITE"])

        # The 3.31 Environment
        if envID == 1 :
            (start, goal, graph, obstacles) = Environments.env331()

        # The Downtown Environment
        elif envID == 2:
            (start, goal, graph, obstacles) = Environments.manhattan()

        # The Around the Block Environment
        elif envID == 3:
             (start, goal, graph, obstacles) = Environments.aroundTheBlock()
        
        else:
            return

        # Draw the environment to the screen.
        self.drawEnvironment(start, goal, obstacles)

        # Return the items of the environment needed for search.
        return start, goal, graph

    # Draws a given environment consisting of a start and goal node, along with polygon obstacles.
    def drawEnvironment(self, start, goal, polygons):
        # Draws start and goal node.
        pygame.draw.circle(self.window, COLORS["BLACK"], start.getPoint().coordinates, 10)
        pygame.draw.circle(self.window, COLORS["BLACK"], goal.getPoint().coordinates, 10)

        # Draws all polygon obstacles.
        for polygon in polygons:
            # Special draw needed for rectangles.
            if polygon.getType() == "Rectangle":
                length = abs(polygon.getPolygon().vertices[0][0] - polygon.getPolygon().vertices[1][0])
                height = abs(polygon.getPolygon().vertices[0][1] - polygon.getPolygon().vertices[2][1])
                pygame.draw.rect(self.window, COLORS["BLACK"], (polygon.getPolygon().vertices[0], (length, height)), width=1)
            # All other polygons.
            else:
                pygame.draw.polygon(self.window, COLORS["BLACK"], polygon.getPolygon().vertices, width=1)

        pygame.display.update()

    # Shows the paths explored along with the shortest path from start to goal.
    def showExploration(self, exploredNodes, bestPath):
        
        # Delayes the start to allow for the GUI to draw the environment before paths are drawn.
        pygame.time.delay(1000)

        # Stores all the node to node paths to be drawn.
        paths = list()

        # Reverses the explored nodes list so goal is at the begining an the path can be built from the leaf nodes up to the root.
        exploredNodes = exploredNodes[::-1]
        for x in exploredNodes:
            if(x.getParent() == None):
                break
            p1 = x.getCoordinates()
            p2 = x.getParent().getCoordinates()
            # Inserts paths at the begining so the start is the first node.
            paths.insert(0,(p1,p2))

        # Draw all the explored paths, with a small delay for help visualizing.
        for line in paths:
            pygame.draw.line(self.window, COLORS["BLUE"], line[0] , line[1], 5)
            pygame.display.update()
            pygame.time.delay(500)
        
        # Highlight the best path in a different color.
        for index in range(len(bestPath)-1):
            p1 = bestPath[index].getCoordinates()
            p2 = bestPath[index+1].getCoordinates()
            pygame.draw.line(self.window, COLORS["GREEN"], p1, p2, 5)
        
        pygame.display.update()

    # When the use wishes to visualize the selected algorithm on the selected environment, this method acts as the switch case
    # to run and animate the selected algorithm.
    def runAlgorithm(self):
        
        (envName, envID) = self.environment
        (algoName, algoID) = self.algorithm

        # Stays on the start menu if no environment or algorithm are selected.
        if envID == 0 or algoID == 0:
            return

        # Destroys start menu page.
        self.menu.disable()

        # Creates the environment window, and returns the corresponding points in the environmen.
        (start, goal, graph) = self.createEnvironment(envID)

        # Runs the A* algorithm in the selected environment.
        if algoID == 1:
            (exploration, path) = AStar.aStar(start, goal, graph)
            self.showExploration(exploration, path)

        # Runs the Potential Search algorithm in the selected environment.
        elif algoID == 2:
            (exploration, path) = PotentialSearch.potentialSearch(start, goal, graph, self.costField.get_value())
            self.showExploration(exploration, path)
            
            if len(path) == 0:
                pygame.time.delay(2500)
                self.startMenu(notify=True)

        # Returns to start menu on selection error.
        else:
            self.startMenu()

    # Gameloop runs the tool continuously until the user decides to exit. 
    # The user can return to the menu by pressing esc to select new values. This is the WHILE loop functionality.
    def mainLoop(self):
        run = True

        # Checks user inputs.
        while run:
            for event in pygame.event.get():
                # If the exit button is selected quit.
                if event.type == pygame.QUIT:
                    run = False
                # If escape is pressed retrun to the start menu.
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.startMenu()

        pygame.quit()