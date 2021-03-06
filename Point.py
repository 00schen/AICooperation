class Point:
    def __init__(self, x, y): # Good
        self.x = x
        self.y = y

    def add(self, p): # Good
        return Point(self.x + p.x, self.y + p.y)

    def sub(self, p): # Good
        return Point(self.x - p.x, self.y - p.y)

    def mult(self, m):
        return Point(self.x * m, self.y * m)

    def normSq(p, q): # Good
        return (p.x - q.x)**2 + (p.y - q.y)**2
    
    def __str__(self): # Good
        return "({},{})".format(self.x, self.y)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other): # Good
        return self.x == other.x and self.y == other.y
