# AIPathfinding
A collection of path finding algorithms, in polygon and grid environments.

The algorithms implemented are A* search in a polygon environment, Potential Search in a polygon environment, and Anytime Non-Parametric 
A* in a grid environment.

The algorithms are shown graphically. For the polygons several environments are provided, and for the grid the user can draw the environment. 

Note: For the polygon environments run time can be high as a graph representing the environment is first generated, using the polygons geometry.

The later two algorithms are from the following paper:
Stern, R., Felner, A., van den Berg, J., Puzis, R., Shah, R., & Goldberg, K. (2014). Potential-based bounded-cost search and Anytime Non-Parametric A*.
https://doi.org/10.1016/j.artint.2014.05.002

# Requirements
-- Python 3.8.10 <br />
-- pygame 2.0.1 <br />
-- pygame_menu 4.0.2 <br />
-- sympy 1.8 <br />
