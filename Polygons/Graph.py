''' Data structure to store a graph. This is a generic container that will form a graph out of related items.
 The items are referred to as vertices for the purposes of this class. While nodes of different types is allowed the best practice
 is to store items of the same type. Each vertex is mapped (hash table) to a unordered list (array list) of its neighbors.'''
class AdjacencyList:

    # Creates an adjacency list object.
    def __init__(self, directed=False):
        self.directed = directed
        self.graph = {}
        self.vertices = 0
        self.edges = 0

    # Adds a new vertex to the adjacency list vertices are generic.
    def addVertex(self, v):
        self.graph[v] = list()
        self.vertices += 1

    '''Adds a given edge if the form (v1, v2) to the adjacency list.  If the given vertex is not present is is added.
     If the graph is directed then v1 is assumed to goto v2 and not visa versa, otherwise (v2, v1) is also added.
     Duplicates are not allowed.'''
    def addEdge(self, v1, v2):
        if v1 not in self.graph:
            self.addVertex(v1)

        if v2 not in self.graph[v1]:
            self.graph[v1].append(v2)

        if not self.directed:

            if v2 not in self.graph:
                self.addVertex(v2)

            if v1 not in self.graph[v2]:
                self.graph[v2].append(v1)

        self.edges += 1

    # Returns a list of all the vertices in the graph.
    def getVertices(self):
        return self.graph.keys()

    # Returns the list of neighbors of a given vertex.
    def getNeighbors(self, v):
        return self.graph[v]

    # Prints all neighbors to console.
    def printNeighbors(self, v):
        for n in self.getNeighbors(v):
            print(n)

    # Prints the graph as an adjacency list to the console.
    def printGraph(self):
        for v in self.graph:
            s = v.getName() + '['
            for n in self.getNeighbors(v):
                s = s + ' ' + n.getName()
            print(s + ' ]')