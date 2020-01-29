import pygame as pg
import actors
import grid
import tileSprite
import environments
import buildMode
import gallery
import utils
import pathlib
from random import choice
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
        self.objects.spawners = []

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
                if tile == "s":
                    self.objects.spawners.append(vec(collumIndex,rowIndex))
        
        self.scrapTxt = "MATERIALS: " + str(self.objects.buildMode.scrap)

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

            if event.type == settings.e_SCRAPGAIN:
                if not self.state.bMode:
                    self.objects.buildMode.scrap += 1
                    self.scrapTxt = "MATERIALS: " + str(self.objects.buildMode.scrap)
            
            if event.type == settings.e_ROUNDSTART:
                self.state.round = True
                self.state.roundnumber = event.roundnumber + 1
                multiplier = self.state.roundnumber * 0.15
                self.state.roundzombies = int(multiplier * self.state.maxzombies)
                self.roundTxt = "ROUND: " + str(self.state.roundnumber)
            
            if event.type == settings.e_ROUNDCOUNTDOWN:
                if not self.state.round:
                    self.roundTxt = "NEXT ROUND:" + str(self.state.countdown)
                    self.state.countdown -= 1
                    if self.state.countdown < 0:
                        ROUNDSTART = pg.event.Event(settings.e_ROUNDSTART, roundnumber = self.state.roundnumber)
                        pg.event.post(ROUNDSTART, )
                        self.state.countdown = settings.r_countdown
            
    
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

        self.state.screen.blit(self.state.font.render(self.scrapTxt, True, settings.WHITE),(10,10))
        self.state.screen.blit(self.state.font.render(self.roundTxt, True, settings.WHITE),(10,self.state.tileSize *1))   
   
        pg.display.flip()    
        
    # calls update of all sprites and camera to its follow target - called every game loop    
    def update(self):
        self.keys = pg.key.get_pressed()
        self.mouse_pos = pg.mouse.get_pos()
        self.mouse_pressed = pg.mouse.get_pressed()
        
        if self.state.bMode:
            self.objects.buildMode.update()
        else:
            self.camera.update(self.objects.player)
            self.objects.groupAll.update()
        
        hits = pg.sprite.groupcollide(self.objects.groupBullets,self.objects.groupDestructable, True, False, utils.collideDetect)
        if hits:
            for bullet in hits:
                target = hits[bullet][0]
                target.health -= bullet.damage
                    
        
        #hits = pg.sprite.spritecollide(self.objects.player, self.objects.groupZombies, False, utils.collideDetect)
        #if hits:
            #for zombie in hits:
                ##self.objects.player.health -= zombie.damage
                #if zombie.action != "meleeattack":
                    #zombie.action = "meleeattack"
                    #zombie.animator.newAction("meleeattack")

        
        self.upzombies = len(self.objects.groupZombies.sprites())
        if self.upzombies < self.state.maxzombies and self.state.roundzombies > 0:
            spawn = choice(self.objects.spawners)        
            actors.zombie(self, spawn.x,spawn.y)
            self.state.roundzombies -= 1
            self.upzombies += 1
            
          
        if self.upzombies <= 0 and self.state.round:
            self.state.round = False
            pg.time.set_timer(settings.e_ROUNDCOUNTDOWN, 1000)          

# class for objects that exists in game
class gameObjects:
    def __init__(self):
        # creates or clear the sprite groups
        self.groupAll = pg.sprite.Group()
        self.groupWalls = pg.sprite.Group()
        self.groupZombies = pg.sprite.Group()
        self.groupBullets = pg.sprite.Group()
        self.groupDestructable = pg.sprite.Group()
        

# class for setting config
class gameState:
    def __init__(self):
        self.del_t = 0
        #pg.display.set_caption(settings.s_title)
        self.screenWidth = settings.s_screenWidth
        self.screenHeight = settings.s_screenHeight
        self.tileSize = settings.s_tileSize
        self.FPS = settings.s_FPS
        self.size = (self.screenWidth,self.screenHeight)
        self.title = settings.s_title
        # will eventually be fullscreen, but for debugging will use windowed
        #self.screen = pg.display.set_mode( (0,0) , pg.FULLSCREEN)
        self.screen = pg.display.set_mode(self.size)
        self.font = settings.s_font
        self.maxzombies = settings.z_maxzombies
        self.countdown = settings.r_countdown
        self.round = False

# instatiate
Game = gameScene()
pg.time.set_timer(settings.e_SCRAPGAIN, 1000)
ROUNDSTART = pg.event.Event(settings.e_ROUNDSTART, roundnumber = 0)
pg.event.post(ROUNDSTART)
pg.key.set_repeat(500,1)

# Mainloop
while not Game.gameLoop:
    Game.state.del_t = Game.clock.tick(Game.state.FPS) / 1000
    Game.events()
    Game.update()
    Game.draw()
    
# Close the window and quit.
pg.quit()