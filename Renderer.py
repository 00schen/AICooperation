import graphics
from soccer import *

def render(stage):
    
    win = graphics.GraphWin("Stage", WIDTH, HEIGHT)

    #Render players:
    for player in stage.players:
        
        point = graphics.Point(player.center.x,player.center.y)
        p = graphics.Circle(point,player.radius)
        p.draw(win)

    #Render ball
    
    point = graphics.Point(stage.ball.center.x,stage.ball.center.y)
    c = graphics.Circle(point,stage.ball.radius)
    c.draw(win)
    
    win.getMouse() # pause for click in window
    win.close()
    
