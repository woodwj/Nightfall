import pygame as pg
import player
import grid
import wall
import os
from os import path
import pathlib
# * import makes varibles exist in main - use varName rather than settings.varName
from settings import *
pg.init()

# master class that hold the game objects and settings
class gameScene:
    def __init__(self):
        self.del_t = 0
        self.done = False
        self.clock = pg.time.Clock()
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



    def draw(self):
        self.state.screen.fill(bgColour)
        grid.draw_Grid(self)
        self.objects.groupAll.draw(self.state.screen)
        pg.display.flip()
        

    def update(self):
        self.objects.groupAll.update()


# class for object that exists in game
class gameObjects:
    def __init__(self, gameScene):
        self.groupAll = pg.sprite.Group()
        self.groupWalls = pg.sprite.Group()
        self.gameScene = gameScene

    def load(self, dir = "start.txt"):
        gameFolder = os.getcwd()
        mapFolder = gameFolder + "\\maps"
        mapDir = path.join(mapFolder, dir)
        with open(mapDir, "rt" ) as mapFile:
            tile_x = 0
            tile_y = 0
            for line in mapFile:
                for tile in line:
                    if tile == "w":
                        wall.wall(self.gameScene, tile_x, tile_y)
                    if tile == "P":
                        self.player = player.player(self.gameScene, tile_x,tile_y)

                    tile_x +=1
            
                tile_x = 0
                tile_y +=1
        

# class for setting config
class gameState:
    def __init__(self):
        # setting file now a py file
        self._width = s_screenWidth
        self._height = s_screenHeight
        self._half_w = int( 0.5*self._width )
        self._half_h = int( 0.5*self._height )
        self._size = (self._width,self._height)
        #self.screen = pg.display.set_mode( (0,0) , pg.FULLSCREEN)
        self.screen = pg.display.set_mode(self._size)



# instatiate

Game = gameScene()
pg.key.set_repeat(500, 100)
pg.display.set_caption(s_title)
# Mainloop

while not Game.done:
    Game.del_t = Game.clock.tick(s_FPS) / 1000
    Game.draw()
    Game.update()
    Game.events()


# Close the window and quit.
pg.quit()