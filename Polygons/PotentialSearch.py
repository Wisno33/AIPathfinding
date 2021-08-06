# Standard Library
import math

# Project Libraries
from Graph import AdjacencyList

# Node class for data relevent to Potential Search on a 2D plane.
class Node:

    def __init__(self, vertex, parent=None, cost=math.inf, heuristic=math.inf, budgetEstimate=None):
        self.vertex = vertex
        self.name = self.vertex.getName()
        self.parent = parent
        self.cost = cost # g(n) cost so far to reach n.
        self.heuristicCost = heuristic # h(n) heuristic cost uses euclidian distance from n to goal.
        self.estimatedCost = budgetEstimate # u(n) budget left ratio.
        
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
    
# Converts a graph of points from a 2D environment to a graph of AStar nodes. These nodes have additional information like cost.
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
            startNode = Node(vertex, cost=0, heuristic=heuristicFunction(vertex, goal), budgetEstimate=0)
            node = startNode

        # Goal node has special attributes so it needs to be created separately.
        elif vertex.getName() == "G":
            goalNode = Node(vertex, heuristic=0)
            node = goalNode

        # Create a node in the graph cost starts at infinity.
        else:
            node = Node(vertex, heuristic=heuristicFunction(vertex, goal))

        nodesMap[node.getName()] = node

    # Create the edges in the node graph as defined by the environment graph.
    for vertex in graph.getVertices():
        for neighbor in graph.getNeighbors(vertex):
                nodeGraph.addEdge(nodesMap[vertex.getName()], nodesMap[neighbor.getName()])

    return startNode, goalNode, nodeGraph

# Euclidean distance is used for the heuristic
def heuristicFunction(n, goal):
    return math.dist(n.getCoordinates(), goal.getCoordinates())

# Get the distance between two nodes.
def travelDistance(n1, n2):
    return math.dist(n1.getCoordinates(), n2.getCoordinates())

# Calculates the ratio of the budget that is left to find a solution under C.
def budgetRatioCost(n, cost):
    return (cost - n.getCost())/n.getHeuristicCost()

def potentialSearch(start, goal, graph, cost):

    (start, goal, graph) = createNodeGraph(start, goal, graph)

    # Open and closed sets for node processing. Open is a list and will be sorted at the end of each iteration, to mimic a priority queue.
    # Closed is a simple list.
    open = list()
    closed = list()

    # Used to decide cost ties on nodes. Nodes encountered on an earlier iteration will be higher in the queue if costs are equal.
    count = 0

    # Queue start node into open.
    open.append(start)

    while len(open) != 0:

        n = open.pop(0)
        count += 1

        # Add the best node that is going to be expanded to the closed list.
        closed.append(n)

        # Process all neighbors of the node being expanded.
        for neighbor in graph.getNeighbors(n):

            # If the neighbor is has been seen or expanded check if the current cost is less than the new cost.
            if (neighbor in open or neighbor in closed) and neighbor.getCost() <= n.getCost() + travelDistance(n, neighbor):
                continue

            # Set the neighbors cost and parent node, could be initial or after the node has been seen/expanded.
            neighbor.setCost(n.getCost() + travelDistance(n, neighbor))
            neighbor.setParent(n)

            # If the cost so far plus the heuristic estimated cost is greater than the cost constraint skip.
            if neighbor.getCost() + neighbor.getHeuristicCost() >= cost:
                continue
            
            # If the neighbor is the goal end and return the path, the goal path cost will be <= cost constraint at this point.
            if neighbor == goal:
                closed.append(neighbor)
                return closed, getPath(closed)

            # Update neighbor with the its new cost, the list is sorted by the nodes u(n) value.
            if neighbor in open:
                neighbor.setEstimatedCost(budgetRatioCost(neighbor, cost))
            
            # Set neighbors u(n) value based on calculated cost, and add it to the open list.
            neighbor.setEstimatedCost(budgetRatioCost(neighbor, cost))
            open.append(neighbor)

        # Sort the list by the nodes u(n) (smallest to largest)
        open.sort(key= lambda x:x.getEstimatedCost())
        # Revese the list so the largest u(n) is first.
        open = open[::-1]

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