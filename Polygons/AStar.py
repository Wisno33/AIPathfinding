# Standard Library
import math

# Project Libraries
from Graph import AdjacencyList

# Node class for data relevent to A* search on a 2D plane.
class Node:

    def __init__(self, vertex, parent=None, cost=math.inf, heuristic=math.inf):
        self.vertex = vertex
        self.name = self.vertex.getName()
        self.parent = parent
        self.cost = cost # g(n) cost so far to reach n.
        self.heuristicCost = heuristic # h(n) heuristic cost uses euclidian distance from n to goal.
        self.estimatedCost = self.cost + self.heuristicCost # f(n) total estimated cost to reach goal.
        
    def getVertex(self):
        return self.vertex

    def getCoordinates(self):
        return self.vertex.getCoordinates()

    def getName(self):
        return self.name

    def setParent(self, parent):
        self.parent = parent
    
    def getParent(self):
        return self.parent

    def setCost(self, cost):
        self.cost = cost

    def getCost(self):
        return self.cost

    def getHeuristicCost(self):
        return self.heuristicCost

    def setEstimatedCost(self, cost):
        self.estimatedCost = cost

    def getEstimatedCost(self):
        return self.estimatedCost
    
# Converts a graph of points from a 2D environment to a graph of A* nodes. These nodes have additional information like cost.
def createNodeGraph(start, goal, graph):
    
    # New Graph
    nodeGraph = AdjacencyList()

    # Used to hold the new nodes created from the vertices in the points graph. For edge creation.
    nodesMap = dict()

    # Creates nodes from all vertices in the environment graph.
    for vertex in graph.getVertices():
        node = None

        # Start node has special attributes so it needs to be created separately.
        if vertex.getName() == "S":
            startNode = Node(vertex, cost=0, heuristic=heuristicFunction(vertex, goal))
            node = startNode

        # Goal node has special attributes so it needs to be created separately.
        elif vertex.getName() == "G":
            goalNode = Node(vertex, heuristic=0)
            node = goalNode

        # Create a node in the graph cost starts at infinity.
        else:
            node = Node(vertex, cost=math.inf, heuristic=heuristicFunction(vertex, goal))

        nodesMap[node.getName()] = node

    # Create the edges in the node graph as defined by the environment graph.
    for vertex in graph.getVertices():
        for neighbor in graph.getNeighbors(vertex):
                nodeGraph.addEdge(nodesMap[vertex.getName()], nodesMap[neighbor.getName()])

    return startNode, goalNode, nodeGraph


# Total estimated cost function. Cost to reach n plus heuristic cost.
def evaluationFunction(curCost, potentialNode):
    return curCost + potentialNode.getHeuristicCost()

# Euclidean distance is used for the heuristic
def heuristicFunction(n, goal):
    return math.dist(n.getCoordinates(), goal.getCoordinates())

# Get the distance between two nodes.
def travelDistance(n1, n2):
    return math.dist(n1.getCoordinates(), n2.getCoordinates())

# The A* algorithm.
def aStar(start, goal, graph):

    # Convert basic cartesian point graph, start, and goal to A* nodes.
    (start, goal, graph) = createNodeGraph(start, goal, graph)

    # Open and closed sets for node processing. Open is a list and will be sorted at the end of each iteration, to mimic a priority queue.
    # Closed is a simple list.
    open = list()
    closed = list()

    # Tracks total distance traveled so far at a particular node.
    cost = 0

    # Used to decide cost ties on nodes. Nodes encountered on an earlier iteration will be higher in the queue if costs are equal.
    count = 0

    # Queue start node into open.
    open.append(start)

    # While open is not empty run A*
    while len(open) != 0:

        # Get the best cost item (front of the list).
        nBest = open.pop(0)
        count += 1

        # Add the best node that is going to be expanded to the closed list.
        closed.append(nBest)

        # Get the cost to reach the node being expanded.
        cost = nBest.getCost()

        # If the goal node is to be expanded exit and return the explored nodes (for visualization) and the best path.
        if nBest == goal:
            return closed, getPath(closed)

        # Expand nBest get all neighbors.
        for neighbor in graph.getNeighbors(nBest):

            # Only evaluate the neighbors that have not been expanded already.
            if neighbor not in closed:

                # If the neighbor is already been placed in open check if it needs to be updated.
                if neighbor in open:
                    # Get the cost to the neighbor from the currently considered node.
                    newCost = cost + math.dist(nBest.getCoordinates(), neighbor.getCoordinates())

                    # If the cost from this new parent is better than the current parent update the neighbors parent and cost.
                    if newCost < neighbor.getCost():
                        neighbor.setParent(nBest)
                        neighbor.setCost(newCost)
                        neighbor.setEstimatedCost(evaluationFunction(newCost, neighbor))

                # If not in open add it with nBest as parent and calculate new costs, and add it to open.
                else:
                    neighbor.setParent(nBest)
                    neighbor.setCost(cost + travelDistance(nBest, neighbor))
                    neighbor.setEstimatedCost(evaluationFunction(neighbor.getCost(), neighbor))
                    open.append(neighbor)

        # Sort the open list to place the lowest cost at the front.
        open.sort(key= lambda x:x.getEstimatedCost())
    
    # Return the failed search, this will return the nodes expanded but no final path.
    return closed, list()

# Gets the path from the last child node in a set to its parent from a set of nodes.
def getPath(set):
    
    # Container for the path.
    path = list()

    # Start at end end of the set.
    cur = set[len(set) - 1]

    # Add the end node to the path.
    path.append(cur)

    # While the node has a parent get the parent and add it to the path.
    while cur.getParent() is not None:
        cur = cur.getParent()
        path.append(cur)
    
    # Reverse the list to get the past from begining to end.
    path = path[::-1]

    return path