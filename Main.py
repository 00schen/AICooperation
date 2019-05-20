import Renderer
from soccer import *

def main():

    player1 = _Player( _Point(50,50) ,20,2, 2*pi,200 )
    player2 = _Player( _Point(30,100),30,5,6,7)
    primaryStage = Stage([player1,player2])

    Renderer.render(primaryStage)
    
    
main()
