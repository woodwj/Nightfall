import pygame as pg
import actors
import grid
import tileSprite
import environments
import gallery
import utils
import pathlib
# * import makes varibles exist in main - use varName rather than settings.varName
from settings import *
pg.init()
vec = pg.math.Vector2

# master class that hold the game objects and settings
class gameScene:
    def __init__(self):
        
        self.gameLoop = False
        self.clock = pg.time.Clock()
        self.state = gameState()
        self.state.gallery = gallery.gallery(self)
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
                    environments.wall(self, collumIndex, rowIndex)
                # player mapping
                if tile == 'P':
                    self.objects.player = actors.player(self, collumIndex, rowIndex)
                # zombie mapping
                if tile == "Z":
                    actors.zombie(self, collumIndex, rowIndex)

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
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps())) 
        self.state.screen.fill(bgColour)
        #self.map.draw_Grid()
        # loop to blit every sprite to the camera apply method
        for sprite in self.objects.groupAll:
            self.state.screen.blit(sprite.image, self.camera.apply(sprite))   
        #pg.draw.rect(self.state.screen, RED, self.objects.player.col_rect, 2)
        #pg.draw.rect(self.state.screen, BLUE, self.objects.player.rect, 2)
        pg.display.flip()
        
    # calls update of all sprites and camera to its follow target - called every game loop    
    def update(self):
        self.objects.groupAll.update()
        self.camera.update(self.objects.player)
        hits = pg.sprite.groupcollide(self.objects.groupZombies, self.objects.groupBullets, False, True, utils.collideDetect)
        if hits:
            for zombie in hits:
                for bullet in hits[zombie]:
                    zombie.health -= bullet.damage
        pg.sprite.groupcollide(self.objects.groupBullets, self.objects.groupWalls, True, False, utils.collideDetect)
        

# class for objects that exists in game
class gameObjects:
    def __init__(self):
        # creates or clear the sprite groups
        self.groupAll = pg.sprite.Group()
        self.groupWalls = pg.sprite.Group()
        self.groupZombies = pg.sprite.Group()
        self.groupBullets = pg.sprite.Group()

# class for setting config
class gameState:
    def __init__(self):
        self.del_t = 0
        #pg.display.set_caption(s_title)
             
        self.screenWidth = s_screenWidth
        self.screenHeight = s_screenHeight
        self.tileSize = s_tileSize
        self.gridWidth = s_gridWidth
        self.gridHeight = s_gridHeight
        self.FPS = s_FPS
        self.halfWidth = int( 0.5* self.screenWidth )
        self.halfHeight = int( 0.5* self.screenHeight )
        self.size = (self.screenWidth,self.screenHeight)
        self.title = s_title
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