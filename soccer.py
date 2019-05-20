from math import sin
from math import cos
from math import pi
from math import atan2

WIDTH = 400
HEIGHT = 200

TEAM_RED = False
TEAM_BLUE = True

def make(players):
    return Stage(players)

class _Point:
    def __init__(self, x, y): #Good
        self.x = x
        self.y = y

    def add(self, p): #Good
        return _Point(self.x + p.x, self.y + p.y)

    def sub(self, p): #Good
        return _Point(self.x - p.x, self.y - p.y)

    @staticmethod
    def normSq(p, q): #Good
        return ((p.x - q.x)**2 + (p.y - q.y)**2)**(1/2)
    
    def __str__(self): #Good
        return "({},{})".format(self.x,self.y)
    
    def __eq__(self,other): #Good
        return self.x == other.x and self.y == other.y

class Stage:
    def __init__(self, players, possession):
        self.walls = [
            _Wall((_Point(0, 0), _Point(WIDTH, 0))),
            _Wall((_Point(0, HEIGHT), _Point(WIDTH, HEIGHT))),
            _Goal((_Point(0, HEIGHT), _Point(0,0)),
                (_Point(0, HEIGHT / 3), _Point(0, HEIGHT * 2 / 3))),
            _Goal((_Point(WIDTH,0), _Point(WIDTH, HEIGHT)),
                (_Point(WIDTH, HEIGHT / 3), _Point(WIDTH, HEIGHT * 2 / 3)))
        ]
        self.ball = _Ball(_Point(WIDTH / 2, HEIGHT / 2), 5)
        self.players = players
        self.possession = possession

    def __resolvePlayerCollisions(self, player):
        for other in self.players:
            if player.collide(other) and player != other:
                player.revertMove()
    
    def moveCycle(self, actions):
        new_state = []

        for i in range(len(self.players)):
            player = self.players[i]
            action = actions[i]
            if (action[0] == 1):
                player.changeMove(*action[1])
            elif (action[0] == 2):
                player.kick(self.ball, *action[1])
            elif (action[0] == 0):
                player.move()
                self.__resolvePlayerCollisions(player)
            new_state.append(player.center)

        self.ball.move()
        new_state.append(self.ball.center)
        if(self.__ballScored()):
            new_state.append(1)
        elif(self.__ballOutBounds()):
            new_state.append(2)
        else:
            new_state.append(0)
        
        return new_state

    def __ballScored(self):
        return self.walls[2].hasScored(self.ball) \
            or self.walls[3].hasScored(self.ball)

    def __ballOutBounds(self):
        return self.walls[0].collide(self.ball) \
            or self.walls[1].collide(self.ball) \
            or self.walls[2].collide(self.ball) \
            or self.walls[3].collide(self.ball)

class _Wall: # 0 for horizontal orientation , 1 for vertical
    def __init__(self, bounds): #Good
        self.bounds = bounds
        if(bounds[0].x == bounds[1].x):
            self.orientation = 1
        else:
            self.orientation = 0


    # def __orientation(p, q, r): #use cross-product to determine rotation of three points
    #     cross = (q.x - p.x) * (r.y - p.y) - (q.y - p.y) * (r.x - p.x)
    #     return 0 if cross == 0 else 1 if cross > 1 else -1

    # def __intersection(p1, p2, q1, q2): #determines intersection between line bounded by p1, p2 and line bounded by q1, q2
    #     return Wall.__orientation(p1, p2, q1) < 0 \
    #         ==  Wall.__orientation(p1, p2, q2) < 0 \
    #         and Wall.__orientation(p1, p2, q1) != 0

    # def collide(self, c):
    #     p = Point(c.radius * cos((self.angle - .5) * pi), 
    #             c.radius * sin((self.angle - .5) * pi))
    #     p = c.add(p)
    #     return Wall.__intersection(self.bounds[0], self.bounds[1], c, p)

    def collide(self, c): #Good
        
        if(not (self.orientation)):
            #Check y values
            return (abs(c.center.y - self.bounds[0].y) <= c.radius)
        else:
            #Check x values
            return (abs(c.center.x - self.bounds[0].x) <= c.radius)
    
    def __str__(self): #Good
        return "Bound 1: {}\nBound 2: {} \nOrientation: {}"\
            .format(self.bounds[0], self.bounds[1], self.orientation)

class _Goal(_Wall):
    def __init__(self, bounds, inner): #Good
        super().__init__(bounds)
        self.inner = inner

    def hasScored(self, b): #Good
        net = _Wall(self.inner)
        
        #check if b is within bounds
        if(net.orientation):
            bound1 = min(self.inner[0].y,self.inner[1].y)
            bound2 = max(self.inner[0].y,self.inner[1].y)
            withinBounds = (b.center.y >= bound1 and b.center.y <= bound2)
            
        else:
            bound1 = min(self.inner[0].x,self.inner[1].x)
            bound2 = max(self.inner[0].x,self.inner[1].x)
            withinBounds = (b.center.x >= bound1 and b.center.x <= bound2)
        return net.collide(b) and withinBounds

    def collide(self, b): #Good
        return super().collide(b) and not self.hasScored(b)
    
    def __str__(self): #Good
        return super().__str__() + "\nGoal bound 1: {}\nGoal bound 2: {}"\
            .format(self.inner[0], self.inner[1])

class _Circle:
    def __init__(self, center, radius): #Good
        self.center = center
        self.radius = radius
        self.velocity = 0
        self.angle = 0

    def move(self): #Good
        dp = _Point(self.velocity * cos(self.angle), self.velocity * sin(self.angle))
        self.center = self.center.add(dp)

    def collide(self, c): #Good
        return _Point.normSq(self.center, c.center) \
            <= self.radius + c.radius 
    
    def __str__(self): #Good
        return "\nCenter: {} \nRadius: {} \nVelocity: {} \nAngle: {}"\
            .format(self.center, self.radius, self.velocity, self.angle)

class _Ball(_Circle):
    def __init__(self, center, radius): #Good
        super().__init__(center,radius)

class _Player(_Circle):
    def __init__(self, center, radius, max_speed, max_angle, max_kick): #Good
        super().__init__(center, radius)
        self.max_speed = max_speed
        self.max_angle = max_angle
        self.max_kick = max_kick
        self.prev_pos = center

    def move(self): #Good
        self.prev_pos = self.center
        super().move()

    def revertMove(self): #Good
        self.center = self.prev_pos

    def changeMove(self, v, theta): #Good
        #Check for max speed
        if(v <= self.max_speed):
            self.velocity = v
        else:
            self.velocity = self.max_speed
            
        
        self.angle = theta

    def kick(self, b, kick, theta): #Good
        if not(self.collide(b)):
            return
        
        #Check for max angle
        if theta > self.max_angle:
            theta = self.max_angle
        elif theta < -1 * self.max_angle:
            theta = -1 * self.max_angle
            
        #Check for max kick
        if kick > self.max_kick:
            kick = self.max_kick
        elif kick < -1 * self.max_kick:
            kick = -1 * self.max_kick
            
        #Adjust ball's velocity
        b.angle = theta
        b.velocity = kick
        
    def __str__(self): #Good
        return super().__str__() + "\nMax Speed: {} \nMax Angle: {} \nMax Kick: {}"\
            .format(self.max_speed, self.max_angle, self.max_kick)
