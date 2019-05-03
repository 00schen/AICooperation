from math import sin
from math import cos
from math import pi

WIDTH = 400
HEIGHT = 200

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self, p):
        return Point(self.x + p.x, self.y + p.y)

    def sub(self, p):
        return Point(self.x - p.x, self.y - p.y)

    @staticmethod
    def normSq(p, q):
        return (p.x - q.x)**2 + (p.y - q.y)**2

class Stage:
    def __init__(self, players):
        self.walls = [
            Wall([Point(0, 0), Point(WIDTH, 0), 0]),
            Wall([Point(0, HEIGHT), Point(WIDTH, HEIGHT)], 0),
            Goal([Point(0, HEIGHT), Point(0,0)],
                [Point(0, HEIGHT / 3), Point(0, HEIGHT * 2 / 3)], -.5),
            Goal([Point(WIDTH,0), Point(WIDTH, HEIGHT)],
                [Point(WIDTH, HEIGHT / 3), Point(WIDTH, HEIGHT * 2 / 3)], .5)
        ]
        self.ball = Ball(Point(WIDTH / 2, HEIGHT / 2), 5)
        self.players = players

    def __resolvePlayerCollisions(self):
        for player in self.players:
            for other in self.players:
                if player.collide(other) \
                and player != other:
                    player.revertMove()
    
    def moveCycle(self):
        for player in self.players:
            player.move
        self.__resolvePlayerCollisions()
        self.ball.move

    def ballScored(self):
        return self.walls[2].hasScored(self.ball) \
            or self.walls[3].hasScored(self.ball)

    def ballOutBounds(self):
        return self.walls[0].collide(self.ball) \
            or self.walls[1].collide(self.ball) \
            or self.walls[2].collide(self.ball) \
            or self.walls[3].collide(self.ball)

class Wall: #for simplicity, angle ranges from [-.5, .5]
    def __init__(self, bounds, angle):
        self.boundaries = bounds
        self.angle = angle

    def __orientation(p, q, r): #use cross-product to determine rotation of three points
        cross = (q.x - p.x) * (r.y - p.y) - (q.y - p.y) * (r.x - p.x)
        return 0 if cross == 0 else 1 if cross > 1 else -1

    def __intersection(p1, p2, q1, q2): #determines intersection between line bounded by p1, p2 and line bounded by q1, q2
        return Wall.__orientation(p1, p2, q1) < 0 \
            ==  Wall.__orientation(p1, p2, q2) < 0 \
            and Wall.__orientation(p1, p2, q1) != 0

    def collide(self, c):
        p = Point(c.radius * cos((self.angle - .5) * pi), 
                c.radius * sin((self.angle - .5) * pi))
        p = c.add(p)
        return Wall.__intersection(self.bounds[0], self.bounds[1], c, p)

class Goal(Wall):
    def __init__(self, bounds, inner, angle):
        super(self, bounds, angle)
        self.inner = inner

    def hasScored(self, b):
        net = Wall(self.inner, self.angle)
        return net.collide(b)

    def collide(self, b):
        return self.collide(b) and not self.hasScored(b)

class Circle:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius
        self.velocity = 0
        self.angle = 0

    def move(self):
        dp = Point(self.velocity * cos(self.angle * pi), \
            self.velocity * sin(self.angle * pi))
        self.center = self.center.add(dp)

    def collide(self, c):
        return Point.normSq(self.center, c.center) \
            <= self.radius + c.radius 

class Ball(Circle):
    def __init__(self, center, radius):
        super(self, center, radius)

class Player:
    def __init__(self, center, radius, max_speed, max_angle, max_kick):
        super(self, center, radius)
        self.max_speed = max_speed
        self.max_angle = max_angle
        self.max_kick = max_kick
        self.prev_pos = center

    def move(self):
        self.prev_pos = self.center
        Circle.move(self)

    def revertMove(self):
        self.center = self.prev_pos

    def changeMove(self, v, theta):
        self.velocity = v
        self.angle = theta

    def kick(self, b, kick, theta):
        if theta > self.max_angle:
            theta = self.max_angle
        elif theta < -1 * self.max_angle:
            theta = -1 * self.max_angle
        if kick > self.max_kick:
            kick = self.max_kick
        elif kick < -1 * self.max_kick:
            kick = -1 * self.kick
        b.angle = theta
        b.velocity = kick
