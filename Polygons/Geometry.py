# Geometric objects from sympy math library.
import sympy

# STD library
import math

''' Includes the sympy Point class to include all geometric properties of a point. 
This Point class adds a name for identification.''' 
class Point():

    def __init__(self, orderedPair, name=None):
        self.point = sympy.Point(orderedPair)
        self.name = name

    def getPoint(self):
        return self.point

    def getName(self):
        return self.name

    def getCoordinates(self):
        return self.point.coordinates

''' Includes the sympy Segment class to include all geometric properties of a line segment.
This Line class adds a name for identification. The name is the orderer pair of the point names. '''
class Line():

    def __init__(self, p1, p2):
        self.line = sympy.Segment(p1.getPoint().coordinates, p2.getPoint().coordinates)
        self.name = '(' + p1.getName() + ',' + p2.getName() + ')' 

    def getLine(self):
        return self.line

    def getName(self):
        return self.name

''' Includes the sympy Polygon class to include all geometric properties of a polygon.
This polygon class adds a type to identify the type of polygon, and a name for identification. '''
class Polygon():

    def __init__(self, points, polyType, name=None):
        
        orderedPairs = list()
        for point in points:
            orderedPairs.append(point.getPoint().coordinates)
        tuple(orderedPairs)
        self.polygon = sympy.Polygon(*orderedPairs)
        self.vertices = points
        self.type = polyType
        self.name = name
    
    def getPolygon(self):
        return self.polygon

    def getVertices(self):
        return self.vertices

    def getType(self):
        return self.type

    def getName(self):
        return self.name
         