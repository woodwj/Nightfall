import pygame as pg
import player
import grid
import wall

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
        self.initScene()
        
    def initScene(self):
        self.state = gameState()
        self.objects = gameObjects(self)
        self.map = grid.mapManager(self.state)
        self.camera = grid.camera(self.state, self.map.width, self.map.height)

        for rowIndex, tiles in enumerate(self.map.data):
            for collumIndex, tile in enumerate(tiles):
                if tile == 'w':
                    wall.wall(self, collumIndex, rowIndex)
                if tile == 'P':
                    self.objects.player = player.player(self, self.objects, collumIndex, rowIndex)
        

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.done = True

    def draw(self):
        self.state.screen.fill(bgColour)
        self.map.draw_Grid()
        for sprite in self.objects.groupAll:
            self.state.screen.blit(sprite.image, self.camera.apply(sprite))
        pg.display.flip()
        

    def update(self):
        self.objects.groupAll.update()
        self.camera.update(self.objects.player)


# class for object that exists in game
class gameObjects:
    def __init__(self, gameScene):
        self.groupAll = pg.sprite.Group()
        self.groupWalls = pg.sprite.Group()
        self.gameScene = gameScene

# class for setting config
class gameState:
    def __init__(self):
        # setting file now a py file
        pg.display.set_caption(s_title)
        pg.key.set_repeat(500, 100)
        self.screenWidth = s_screenWidth
        self.screenHeight = s_screenHeight
        self.tileSize = s_tileSize
        self.gridWidth = s_gridWidth
        self.gridHeight = s_gridHeight
        self.FPS = s_FPS
        self.half_w = int( 0.5*self.screenWidth )
        self.half_h = int( 0.5*self.screenHeight )
        self.size = (self.screenWidth,self.screenHeight)
        #self.screen = pg.display.set_mode( (0,0) , pg.FULLSCREEN)
        self.screen = pg.display.set_mode(self.size)



# instatiate

Game = gameScene()


# Mainloop

while not Game.done:
    Game.del_t = Game.clock.tick(Game.state.FPS) / 1000
    Game.events()
    Game.update()
    Game.draw()
    


# Close the window and quit.
pg.quit()