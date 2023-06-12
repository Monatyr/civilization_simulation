from __future__ import annotations
import math

class Vec2:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
    
    @staticmethod
    def fromList(l):
        if len(l) == 2:
            return Vec2(l[0], l[1])
        return Vec2(0, 0)
    
    def __add__(self, other):
        return Vec2(self.x + other.x, self.y + other.y)
        
    def __sub__(self, other):
        return Vec2(self.x - other.x, self.y - other.y)
        
    def __mul__(self, other):
        return Vec2(self.x * other, self.y * other)
        
    def __rmul__(self, other):
        return Vec2(self.x * other, self.y * other)
        
    def __truediv__(self, other):
        return Vec2(self.x / other, self.y / other)
        
    def __neg__(self):
        return Vec2(-self.x, -self.y)
    
    def __str__(self):
        return f"({self.x}, {self.y})"
        
    def dot(self, other):
        return self.x * other.x + self.y * other.y
        
    def cross(self, other):
        return self.x * other.y - self.y * other.x
        
    def length(self):
        return math.sqrt(self.x**2 + self.y**2)
        
    def normalized(self):
        return self / self.length()

    def isZero(self):
        return self.x == 0 and self.y == 0
    
    def getNewV(self):
        return Vec2(self.x, self.y)
