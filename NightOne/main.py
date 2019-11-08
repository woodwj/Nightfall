import pygame as pg
import actors
import grid
import tileSprite
import environments
import buildMode
import gallery
import utils
import pathlib
# * import makes varibles exist in main - use varName rather than settings.varName
import settings
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
        self.state.bMode = settings.bMode
        self.objects.buildMode = buildMode.buildMode(self)
        self.initScene()
        
    # an init Scene to reset/start scene in a new map zone ect    
    def initScene(self):
        # re/created map and camera objects
        self.map = grid.mapManager(self)
        self.camera = grid.camera(self, self.map.width, self.map.height)

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
                if event.key == pg.K_b:
                    self.state.bMode = not(self.state.bMode)
                    if self.state.bMode:
                        self.objects.buildMode.start()
                    else:
                        self.objects.buildMode.end()
            
    
    # draws sprites to the screen and adjusts to the camera - called every game loop
    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps())) 
        self.state.screen.fill(settings.bgColour)
        # loop to blit every sprite to the camera apply method
        for sprite in self.objects.groupAll:
            self.state.screen.blit(sprite.image, self.camera.apply(sprite))

        if self.state.bMode:
            self.camera.draw_Grid()
            self.state.screen.blit(self.objects.buildMode.image, self.camera.apply(self.objects.buildMode))
        pg.draw.rect(self.state.screen, settings.RED, self.objects.player.col_rect, 1)


        pg.display.flip()    
        
    # calls update of all sprites and camera to its follow target - called every game loop    
    def update(self):
        self.keys = pg.key.get_pressed()
        self.mouse_pos = pg.mouse.get_pos()
        self.mouse_pressed = pg.mouse.get_pressed()
        
        if self.state.bMode:
            self.objects.buildMode.update()
        else:
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
        #pg.display.set_caption(settings.s_title)
        self.screenWidth = settings.s_screenWidth
        self.screenHeight = settings.s_screenHeight
        self.tileSize = settings.s_tileSize
        self.gridWidth = settings.s_gridWidth
        self.gridHeight = settings.s_gridHeight
        self.FPS = settings.s_FPS
        self.halfWidth = int( 0.5* self.screenWidth )
        self.halfHeight = int( 0.5* self.screenHeight )
        self.size = (self.screenWidth,self.screenHeight)
        self.title = settings.s_title
        # will eventually be fullscreen, but for debugging will use windowed
        #self.screen = pg.display.set_mode( (0,0) , pg.FULLSCREEN)
        self.screen = pg.display.set_mode(self.size)

# instatiate
Game = gameScene()
pg.key.set_repeat(500,1)

# Mainloop
while not Game.gameLoop:
    Game.state.del_t = Game.clock.tick(Game.state.FPS) / 1000
    Game.events()
    Game.update()
    Game.draw()
    
# Close the window and quit.
pg.quit()