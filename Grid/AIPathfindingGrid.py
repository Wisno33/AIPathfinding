# Project visualization framework and functions.
import ARAStarVisualization

# Creates the GUI and continues running it.
def main():

    # Creates the visualization GUI initial state is a start menu.
    WIN = ARAStarVisualization.GUI()

    WIN.mainLoop()

if __name__ == "__main__":
    main()
    