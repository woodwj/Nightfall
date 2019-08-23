import pygame as pg
import player
import grid
import wall
# * import makes varibles exist in main - use varName rather than settings.varName
from settings import *
pg.init()

# master class that hold the game objects and settings
class gameScene:
    def __init__(self):
        self.done = False
        self.state = gameState()
        self.objects = gameObjects(self)
        self.objects.load()
        

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.done = True
                if event.key == pg.K_LEFT:
                    self.objects.player.move(vel_x=-1)
                if event.key == pg.K_RIGHT:
                    self.objects.player.move(vel_x=1)
                if event.key == pg.K_UP:
                    self.objects.player.move(vel_y=-1)
                if event.key == pg.K_DOWN:
                    self.objects.player.move(vel_y=1)


    def draw(self):
        self.state.screen.fill(bgColour)
        self.objects.groupAll.draw(self.state.screen)
        grid.draw_Grid(self)
    

    def update(self):
        self.objects.groupAll.update()


# class for object that exists in game
class gameObjects:
    def __init__(self, gameScene):
        self.groupAll = pg.sprite.Group()
        self.groupWalls = pg.sprite.Group()
        self.gameScene = gameScene

    def load(self):
        self.player = player.player(self.gameScene, 0,0)
        for x in range(0,10):
            wall.wall(self.gameScene, x,4)

# class for setting config
class gameState:
    def __init__(self):
        # setting file now a py file
        self._width = screenWidth
        self._height = screenHeight
        self._half_w = int( 0.5*self._width )
        self._half_h = int( 0.5*self._height )
        self._size = (self._width,self._height)
        #self.screen = pg.display.set_mode( (0,0) , pg.FULLSCREEN)
        self.screen = pg.display.set_mode(self._size)
        

# instatiate
clock = pg.time.Clock()
Game = gameScene()
pg.key.set_repeat(500, 100)
pg.display.set_caption(title)
# Mainloop

while not Game.done:
    Game.draw()
    Game.update()
    Game.events()

    # lock frame rate and update the display
    pg.display.flip()
    clock.tick(FPS)

 
# Close the window and quit.
pg.quit()