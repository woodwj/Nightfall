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
        
        self.gameLoop = False
        self.clock = pg.time.Clock()
        self.state = gameState()
        self.objects = gameObjects()
        self.initScene()
        
        
    # an init Scene to reset/start scene in a new map zone ect    
    def initScene(self):
        
        # re/created map and camera objects
        self.map = grid.mapManager(self.state)
        self.camera = grid.camera(self.state, self.map.width, self.map.height)

        # loop to create sprites from parsed map files
        for rowIndex, tiles in enumerate(self.map.data):
            for collumIndex, tile in enumerate(tiles):
                # wall mapping
                if tile == 'w':
                    wall.wall(self, collumIndex, rowIndex)
                # player mapping
                if tile == 'P':
                    self.objects.player = player.player(self, self.objects, collumIndex, rowIndex)

    # deals with relevent game level events for quit/pause ect - called every game loop
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.gameLoop = True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.gameLoop = True
    
    # draws sprites to the screen and adjusts to the camera - called every game loop
    def draw(self):
        self.state.screen.fill(bgColour)
        self.map.draw_Grid()
        # loop to blit every sprite to the camera apply method
        for sprite in self.objects.groupAll:
            self.state.screen.blit(sprite.image, self.camera.apply(sprite))
        pg.display.flip()
        
    # calls update of all sprites and camera to its follow target - called every game loop    
    def update(self):
        self.objects.groupAll.update()
        self.camera.update(self.objects.player)

# class for object that exists in game
class gameObjects:
    def __init__(self):
        # creates or clear the sprite groups
        self.groupAll = pg.sprite.Group()
        self.groupWalls = pg.sprite.Group()

# class for setting config
class gameState:
    def __init__(self):
        self.del_t = 0
        # setting.py file holds screen data - stored here
        pg.display.set_caption(s_title)
        #pg.key.set_repeat(500, 100)
        self.screenWidth = s_screenWidth
        self.screenHeight = s_screenHeight
        self.tileSize = s_tileSize
        self.gridWidth = s_gridWidth
        self.gridHeight = s_gridHeight
        self.FPS = s_FPS
        self.halfWidth = int( 0.5* self.screenWidth )
        self.halfHeight = int( 0.5* self.screenHeight )
        self.size = (self.screenWidth,self.screenHeight)
        # will eventually be fullscreen, but for debugging will use windowed
        #self.screen = pg.display.set_mode( (0,0) , pg.FULLSCREEN)
        self.screen = pg.display.set_mode(self.size)

# instatiate
Game = gameScene()


# Mainloop
while not Game.gameLoop:
    Game.state.del_t = Game.clock.tick(Game.state.FPS) / 1000
    Game.events()
    Game.update()
    Game.draw()
    


# Close the window and quit.
pg.quit()