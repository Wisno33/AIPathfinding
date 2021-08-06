# Project visualization framework and functions.
import Visualization

# Creates the GUI and continues running it.
def main():

    # Creates the visualization GUI initial state is a start menu.
    WIN = Visualization.GUI()

    # The GUI event loop, this is used as the while loop to continuously take user selection and inputs.
    WIN.mainLoop()

if __name__ == "__main__":
    main()