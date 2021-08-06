# Project Libraries
import Geometry
from Graph import AdjacencyList

# Caches the environment's graph for fast replay.
storedEnvironmentGraphs = dict()
storedEnvironmentGraphs[1] = None
storedEnvironmentGraphs[2] = None
storedEnvironmentGraphs[3] = None


# Defines the environment from 3.31 in Artificial Intelligence a Modern Approach.
def env331():

    # Start and Goal coordinates.
    start = Geometry.Point((75, 475), name='S')
    goal = Geometry.Point((1000, 50), name='G')

    # Set of the polygons and their vertices (these vertices will become the traversable nodes).
    polygons = list()

    # Creates Polygons objects from Point objects. These polygons will define the environment and the graph for searching.
    penta1Points = (Geometry.Point((50, 200), name='1'), Geometry.Point((220, 75), name='2', ), Geometry.Point((300, 175), name='3'), 
        Geometry.Point((245, 350), name='4'), Geometry.Point((80, 325), name='5'))
    penta1 = Geometry.Polygon(penta1Points, "Pentagon")
    polygons.append(penta1)

    rect1Points = (Geometry.Point((105, 400), name='6'), Geometry.Point((525, 400), name='7'), Geometry.Point((525, 525), name='8'), 
        Geometry.Point((105, 525), name='9'))
    rect1 = Geometry.Polygon(rect1Points, "Rectangle")
    polygons.append(rect1)

    tri1Points = (Geometry.Point((385, 175), name='10'), Geometry.Point((330, 330), name='11'), Geometry.Point((440, 330), name='12'))
    tri1 = Geometry.Polygon(tri1Points, "Triangle")
    polygons.append(tri1)

    quad1Points = (Geometry.Point((440, 75), name='13'), Geometry.Point((555, 50), name='14'), Geometry.Point((625, 145), name='15'), 
        Geometry.Point((440, 225), name='16'))
    quad1 = Geometry.Polygon(quad1Points, "Quadrilateral")
    polygons.append(quad1)

    tri2Points = (Geometry.Point((555, 300), name='17'), Geometry.Point((695, 400), name='18'), Geometry.Point((580, 475), name='19'))
    tri2 = Geometry.Polygon(tri2Points, "Triangle")
    polygons.append(tri2)

    rect2Points = (Geometry.Point((665, 50), name='20'), Geometry.Point((835, 50), name='21'), Geometry.Point((835, 325), name='22'), 
        Geometry.Point((665, 325), name='23'))
    rect2 = Geometry.Polygon(rect2Points, "Rectangle")
    polygons.append(rect2)

    hexa1Points = (Geometry.Point((865, 340), name='24'), Geometry.Point((920, 400), name='25'), Geometry.Point((920, 500), name='26'),
        Geometry.Point((835, 525), name='27'), Geometry.Point((750, 500), name='28'), Geometry.Point((750, 400), name='29'))
    hexa1 = Geometry.Polygon(hexa1Points, "Hexagon")
    polygons.append(hexa1)

    quad2Points = (Geometry.Point((920, 50), name='30'), Geometry.Point((860, 125), name='31'), Geometry.Point((945, 350), name='32'), 
        Geometry.Point((1000, 150), name='33'))
    quad2 = Geometry.Polygon(quad2Points, "Quadrilateral")
    polygons.append(quad2)

    # Creates the graph of catesian points using the start, end, and vertices of the polygons in 3.31.
    graph331 = environmentNeighbors(start, goal, polygons, 1)

    # Return the necessary items search algorithm.
    return start, goal, graph331, polygons

def manhattan():

    # Start and Goal coordinates.
    start = Geometry.Point((250, 75), name='S')
    goal = Geometry.Point((850, 475), name='G')

    # Set of the polygons and their vertices (these vertices will become the traversable nodes).
    polygons = list()

    # Creates Polygons objects from Point objects. These polygons will define the environment and the graph for searching.
    rect1Points = (Geometry.Point((100, 25), name='1'), Geometry.Point((200, 25), name='2'), Geometry.Point((200, 125), name='3'), 
        Geometry.Point((100, 125), name='4'))
    rect1 = Geometry.Polygon(rect1Points, "Rectangle")
    polygons.append(rect1)

    rect2Points = (Geometry.Point((300, 25), name='5'), Geometry.Point((400, 25), name='6'), Geometry.Point((400, 125), name='7'), 
        Geometry.Point((300, 125), name='8'))
    rect2 = Geometry.Polygon(rect2Points, "Rectangle")
    polygons.append(rect2)

    rect3Points = (Geometry.Point((500, 25), name='9'), Geometry.Point((600, 25), name='10'), Geometry.Point((600, 125), name='11'), 
        Geometry.Point((500, 125), name='12'))
    rect3 = Geometry.Polygon(rect3Points, "Rectangle")
    polygons.append(rect3)

    tri1Points = (Geometry.Point((700, 25), name='13'), Geometry.Point((800, 25), name='14'),  Geometry.Point((700, 125), name='15'))
    tri1 = Geometry.Polygon(tri1Points, "Triangle")
    polygons.append(tri1)

    rect4Points = (Geometry.Point((900, 25), name='16'), Geometry.Point((1000, 25), name='17'), Geometry.Point((1000, 125), name='18'), 
        Geometry.Point((900, 125), name='19'))
    rect4 = Geometry.Polygon(rect4Points, "Rectangle")
    polygons.append(rect4)

    rect5Points = (Geometry.Point((100, 225), name='20'), Geometry.Point((200, 225), name='21'), Geometry.Point((200, 325), name='22'), 
        Geometry.Point((100, 325), name='23'))
    rect5 = Geometry.Polygon(rect5Points, "Rectangle")
    polygons.append(rect5)

    rect6Points = (Geometry.Point((300, 225), name='24'), Geometry.Point((400, 225), name='25'), Geometry.Point((400, 325), name='26'), 
        Geometry.Point((300, 325), name='27'))
    rect6 = Geometry.Polygon(rect6Points, "Rectangle")
    polygons.append(rect6)

    tri2Points = (Geometry.Point((500, 225), name='28'), Geometry.Point((600, 225), name='29'), Geometry.Point((500, 335), name='30'))
    tri2 = Geometry.Polygon(tri2Points, "Triangle")
    polygons.append(tri2)

    rect7Points = (Geometry.Point((700, 225), name='31'), Geometry.Point((800, 225), name='32'), Geometry.Point((800, 325), name='33'), 
        Geometry.Point((700, 325), name='34'))
    rect7 = Geometry.Polygon(rect7Points, "Rectangle")
    polygons.append(rect7)

    rect8Points = (Geometry.Point((900, 225), name='35'), Geometry.Point((1000, 225), name='36'), Geometry.Point((1000, 325), name='37'), 
        Geometry.Point((900, 325), name="38"))
    rect8 = Geometry.Polygon(rect8Points, "Rectangle")
    polygons.append(rect8)

    rect9Points = (Geometry.Point((100, 425), name='39'), Geometry.Point((200, 425), name='40'), Geometry.Point((200, 525), name='41'), 
        Geometry.Point((100, 525), name='42'))
    rect9 = Geometry.Polygon(rect9Points, "Rectangle")
    polygons.append(rect9)

    tri3Points = (Geometry.Point((300, 425), name='43'), Geometry.Point((400, 425), name='44'), Geometry.Point((300, 525), name='45'))
    tri3 = Geometry.Polygon(tri3Points, "Triangle")
    polygons.append(tri3)

    rect10Points = (Geometry.Point((500, 425), name='46'), Geometry.Point((600, 425), name='47'), Geometry.Point((600, 525), name='48'), 
        Geometry.Point((500, 525), name='49'))
    rect10 = Geometry.Polygon(rect10Points, "Rectangle")
    polygons.append(rect10)

    rect11Points = (Geometry.Point((700, 425), name='50'), Geometry.Point((800, 425), name='51'), Geometry.Point((800, 525), name='52'), 
        Geometry.Point((700, 525), name='53'))
    rect11 = Geometry.Polygon(rect11Points, "Rectangle")
    polygons.append(rect11)

    rect12Points = (Geometry.Point((900, 425), name='54'), Geometry.Point((1000, 425), name='55'), Geometry.Point((1000, 525), name='56'), 
        Geometry.Point((900, 525), name='57'))
    rect12 = Geometry.Polygon(rect12Points, "Rectangle")
    polygons.append(rect12)

    # Creates the graph of catesian points using the start, end, and vertices of the polygons in the environment.
    graphManhattan = environmentNeighbors(start, goal, polygons, 2)

    # Return the necessary items search algorithm.
    return start, goal, graphManhattan, polygons

def aroundTheBlock():

    # Start and Goal coordinates.
    start = Geometry.Point((100, 150), name='S')
    goal = Geometry.Point((900, 400), name='G')

    # Set of the polygons and their vertices (these vertices will become the traversable nodes).
    polygons = list()

    # Creates Polygons objects from Point objects. These polygons will define the environment and the graph for searching.
    rect1Points = (Geometry.Point((300, 100), name='1'), Geometry.Point((700, 100), name='2'), Geometry.Point((700, 450), name='3'), 
        Geometry.Point((300, 450), name='4'))
    rect1 = Geometry.Polygon(rect1Points, "Rectangle")
    polygons.append(rect1)

    penta1Points = (Geometry.Point((150, 250), name='5'), Geometry.Point((250, 300), name='6'), Geometry.Point((225, 400), name='7'), 
        Geometry.Point((75, 400), name='8'), Geometry.Point((50, 300), name='9'))
    penta1 =Geometry.Polygon(penta1Points, "Pentagon")
    polygons.append(penta1)

    tri1Points = (Geometry.Point((400, 25), name='10'), Geometry.Point((600, 75), name='11'), Geometry.Point((500, 75), name='12'))
    tri1 = Geometry.Polygon(tri1Points, "Triangle")
    polygons.append(tri1)

    tri2Points = (Geometry.Point((400, 525), name='13'), Geometry.Point((600, 475), name='14'), Geometry.Point((500, 475), name='15'))
    tri2 = Geometry.Polygon(tri2Points, "Triangle")
    polygons.append(tri2)

    octa1Points = (Geometry.Point((800, 150), name='16'), Geometry.Point((850, 150), name='17'), Geometry.Point((900, 200), name='18'),
        Geometry.Point((900, 250), name='19'), Geometry.Point((850, 300), name='20'), Geometry.Point((800, 300), name='21'), 
        Geometry.Point((750, 250), name='22'), Geometry.Point((750, 200), name='23'))
    octa1 = Geometry.Polygon(octa1Points, "Octagon")
    polygons.append(octa1)

    rect2Points = (Geometry.Point((925, 100), name='24'), Geometry.Point((975, 100), name='25'), Geometry.Point((975, 500), name='26'), 
        Geometry.Point((925, 500), name='27'))
    rect2 = Geometry.Polygon(rect2Points, "Rectangle")
    polygons.append(rect2)

    rect3Points = (Geometry.Point((25, 475), name='28'), Geometry.Point((250, 475), name='29'), Geometry.Point((250, 500), name='30'), 
        Geometry.Point((25, 500), name='31'))
    rect3 = Geometry.Polygon(rect3Points, "Rectangle")
    polygons.append(rect3)

    # Creates the graph of catesian points using the start, end, and vertices of the polygons in the environment.
    graphAroundTheBlock = environmentNeighbors(start, goal, polygons, 3)

    # Return the necessary items search algorithm.
    return start, goal, graphAroundTheBlock, polygons

# This is the ACTIONS function, it operates on all vertices at once rather than at the time of the algorithm.
# Due to this it is a time consuming function, but it only needs to run once on the environment as the graph is cached.
'''Given a set of polygons, where vertices on the polygon are equivalent to vertices in a graph.
 The neighbors of a given vertex are computed, by testing if a line between two vertices intersects a polygon.
 If, so the vertices are not neighbors, if not they are. Returns an adjacency list representing the graph. '''
def environmentNeighbors(start, goal, polygons, environmentID):
    
    if storedEnvironmentGraphs[environmentID] != None:
        return storedEnvironmentGraphs[environmentID]

    # The graph to return
    graph = AdjacencyList()

    # Adds all vertices in the environment to the graph.
    graph.addVertex(start)
    for polygon in polygons:
        for vertex in polygon.getVertices():
            graph.addVertex(vertex)
    graph.addVertex(goal)

    # List of completed points in the environment speeds up creation.
    finished = list()

    # For all vertices check all other vertices to see if they are connected in the environment without intersecting a obstacle.
    for vertex in graph.getVertices():
        for potentialNeighbor in graph.getVertices():

            # If a neighbor is finished or the vertex being considred skip.
            if potentialNeighbor in finished:
                continue
            if vertex == potentialNeighbor:
                continue

            # Assumed to be a neighbor unless contradicted.
            isNeighbor = True
            
            # Used to see if the loop should be broken early due to a an invalid environment edge.
            onPolygon = False
            isBlocked = False

            # The path to be considred if this path exists with out issue, the points are valid neighbors.
            possiblePath = Geometry.Line(vertex, potentialNeighbor)

            # For all polygons check all edges of the polygons.
            for polygon in polygons:
                for side in polygon.getPolygon().sides:

                    # Flags to see if an obstacle contains a vertex being considred.
                    sideContainsVertex = side.contains(vertex.getPoint())
                    sideContainsPotentialNeighbor = side.contains(potentialNeighbor.getPoint())

                    # If an edge contains both points they are neighbors on the same polygon.
                    if sideContainsVertex and sideContainsPotentialNeighbor:
                        onPolygon = True
                        break

                    # If an edge contains only one point in question it may be valid.
                    if sideContainsVertex or sideContainsPotentialNeighbor:

                        # The point on the line is in side a polygon it is invalid.
                        if polygon.getPolygon().encloses_point(possiblePath.getLine().midpoint):
                            isBlocked = True
                            isNeighbor = False
                            break

                        # Possibly valid as the path is not inside a polygon.
                        else:
                            continue
                    
                    # Find all points of intersection with the given line and the path, if the size of the list > 0 there the line is invalid.
                    intersectionPoints = side.intersection(possiblePath.getLine())
                    if len(intersectionPoints) != 0:
                        isBlocked = True
                        isNeighbor = False
                        break

                # Break early for a confirmed path status.     
                if onPolygon or isBlocked:
                    break

            # If the vertices do not have their path blocked add to the graph.
            if isNeighbor:
                graph.addEdge(vertex, potentialNeighbor)

        # Add the checked vertex to finished.
        finished.append(vertex)

    storedEnvironmentGraphs[environmentID] = graph

    # Return the graph representing the environment.
    return graph 