import pygame as pg
# * import makes varibles exist in main - use varName rather than settings.varName
from settings import *
pg.init()

# master class that hold the game objects and settings
class game:
    def __init__(self):
        self.state = gameState()
        self.objects = gameObjects()

    def draw_Grid(self):
        for x in range(0, self.state._width, tileSize):
            pg.draw.line(self.state.screen, WHITE, (x, 0), (x, self.state._height))
        for y in range(0, self.state._height, tileSize):
            pg.draw.line(self.state.screen, WHITE, (0, y), (self.state._width, y))


# class for object that exists in game
class gameObjects:
    def __init__(self):
        self.ijunk = 0

        

# class for setting config
class gameState:
    def __init__(self):
        # setting file now a py file
        self._width = screenWidth
        self._height = screenHeight
        self._half_w = int( 0.5*self._width )
        self._half_h = int( 0.5*self._height )
        self._size = (self._width,self._height)
        self.screen = pg.display.set_mode( (0,0) , pg.FULLSCREEN)
        

# instatiate

clock = pg.time.Clock()
Game = game()


# Mainloop
done = False
while not done:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                done = True

    # screen drawing
    Game.draw_Grid()

 
    # lock frame rate and update the display
    pg.display.flip()
    clock.tick(FPS)
 
# Close the window and quit.
pg.quit()