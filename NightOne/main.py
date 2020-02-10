import pygame as pg
import actors
import grid
import tileSprite
import environments
import buildMode
import gallery
import utils
import pathfinding
import pathlib
from random import choice
import settings
pg.init()
vec = pg.math.Vector2

# master class that hold the game objects and settings #
class gameScene:
    def __init__(self):
        # activates game loop
        self.gameLoop = True
        # create the game clock to track time
        self.clock = pg.time.Clock()
        # create the state to hold constants
        self.state = gameState()
        # create object to hold sprites
        self.objects = gameObjects()
        self.objects.buildMode = buildMode.buildMode(self)
        # start the scene
        self.initScene()
        
    # start/restart a scene #  
    def initScene(self):
        # re-create the map, camera, spawners for new scene
        self.map = grid.mapManager(self)
        self.camera = grid.camera(self, self.map.width, self.map.height)
        self.objects.spawners = []
        self.graph = grid.weightedGrid(self,self.map.width,self.map.height)

        # map parsing #
        for rowIndex, tiles in enumerate(self.map.data):
            for collumIndex, tile in enumerate(tiles):
                # cordinates  using row and collum index
                topLeft = vec(collumIndex,rowIndex) * self.state.tileSize
                self.graph.weights[utils.tup(topLeft)] = settings.t_weight
                # wall sprite #
                if tile == 'w':
                    environments.wall(self, topLeft)
                    self.graph.walls.append(utils.tup(topLeft))
                # player sprite #
                elif tile == 'P':
                    self.objects.player = actors.player(self, topLeft)
                # zombie sprite #
                elif tile == "Z":
                    actors.zombie(self, topLeft)
                # spawner tile #
                elif tile == "s":
                    self.objects.spawners.append(topLeft)

        # initilize text
        self.materialsTxt = "MATERIALS: " + str(self.objects.buildMode.buildPoints)

    # events each gameloop #
    def events(self):
        for event in pg.event.get():
        # input events #
            # quit event #
            if event.type == pg.QUIT:
                pg.quit()
            # key events #
            if event.type == pg.KEYUP:
                # Esc ~> quit #
                if event.key == pg.K_ESCAPE:
                    self.gameLoop = False
                # b ~> buildmode #
                if event.key == pg.K_b:
                    self.state.bMode = not(self.state.bMode)
        # gameplay events #            
            # scrap gain #
            if event.type == settings.e_MATERIALGAIN:
                if not self.state.bMode:
                    self.objects.buildMode.buildPoints += 1
                    self.materialsTxt = "MATERIALS: " + str(self.objects.buildMode.buildPoints)
            # round start #
            if event.type == settings.e_ROUNDSTART:
                self.state.round = True
                self.state.roundnumber = event.roundnumber + 1
                # calculate round's zombies
                multiplier = self.state.roundnumber * 0.15
                self.state.roundzombies = int(multiplier * self.state.maxzombies)
                # update round text
                self.roundTxt = "ROUND: " + str(self.state.roundnumber)
            # round countdown #
            if event.type == settings.e_ROUNDCOUNTDOWN:
                if not self.state.round:
                    self.roundTxt = "NEXT ROUND: " + str(self.state.countdown)
                    self.state.countdown -= 1
                    if self.state.countdown < 0:
                        ROUNDSTART = pg.event.Event(settings.e_ROUNDSTART, roundnumber = self.state.roundnumber)
                        pg.event.post(ROUNDSTART)
                        self.state.countdown = settings.r_countdown
    # draw backround -> grid -> spridtes -> text #
    def draw(self):
        # backround #
        self.state.screen.fill(settings.bgColour)
        # grid #
        if self.state.bMode:
            self.camera.draw_Grid()
            self.state.screen.blit(self.objects.buildMode.image, self.camera.applySprite(self.objects.buildMode))
        # camera-adjusted sprites #
        for sprite in self.objects.groupAll:
            if sprite.actorType == "zombie":
                sprite.draw_health()
            self.state.screen.blit(sprite.image, self.camera.applySprite(sprite))
        # text #
        self.state.screen.blit(self.state.font.render(self.materialsTxt, True, settings.WHITE),(10,10))
        self.state.screen.blit(self.state.font.render(self.roundTxt, True, settings.WHITE),(10,self.state.tileSize *1))
        # render display #
        pg.display.flip()
        
    # updates control -> buildmode or camera + sprites #    
    def update(self):
        # update inputs #
        self.keys = pg.key.get_pressed()
        self.mousePos = vec(pg.mouse.get_pos())
        self.mousePressed = pg.mouse.get_pressed()
        # if buildmode ~> update buildmode = pause #
        if self.state.bMode: self.objects.buildMode.update()
        else: # update all sprites and track camera to player #
            self.camera.update(self.objects.player)
            self.objects.groupAll.update()
        # if zombie kill and more zombies this round ~> spawn new zombie #
        self.state.upZombies = len(self.objects.groupZombies.sprites())
        if self.state.upZombies < self.state.maxzombies and self.state.roundzombies > 0 and len(self.objects.spawners) > 0:
            spawn = choice(self.objects.spawners)        
            actors.zombie(self, spawn)
            self.state.roundzombies -= 1
            self.state.upZombies += 1
        # end of round handling #  
        if self.state.upZombies <= 0 and self.state.round:
            self.state.round = False
            pg.time.set_timer(settings.e_ROUNDCOUNTDOWN, 1000)          

# structure to hold sprites #
class gameObjects:
    def __init__(self):
        # IDs #
        self.spriteID = []
        # groups #
        self.groupAll = pg.sprite.Group()
        self.groupWalls = pg.sprite.Group()
        self.groupZombies = pg.sprite.Group()
        self.groupBullets = pg.sprite.Group()
        # targets #
        self.bTargets = ["zombie", "wall","playerWall"]
        self.zTargets = ["player","playerWall"]

# structure to hold constants #
class gameState:
    def __init__(self):
        # time #
        self.del_t = 0
        # screen #
        pg.display.set_caption(settings.s_title)
        self.screenWidth = settings.s_screenWidth
        self.screenHeight = settings.s_screenHeight
        self.tileSize = settings.s_tileSize
        self.FPS = settings.s_FPS
        self.size = (self.screenWidth,self.screenHeight)
        #self.screen = pg.display.set_mode( (0,0) , pg.FULLSCREEN)
        self.screen = pg.display.set_mode(self.size)
        # text #
        self.font = settings.s_font
        # gameplay #
        self.maxzombies = settings.z_maxzombies
        self.countdown = settings.r_countdown
        self.round = False
        self.upZombies = 0
        # art #
        self.gallery = gallery.gallery(self)
        self.bMode = False
#~~MAIN~~#
# instatiate #
Game = gameScene()
pg.key.set_repeat(1, 10) 
# gain materials /s #
pg.time.set_timer(settings.e_MATERIALGAIN, 1000)
# start round #
ROUNDSTART = pg.event.Event(settings.e_ROUNDSTART, roundnumber = 0)
pg.event.post(ROUNDSTART)
# gameLoop #
while Game.gameLoop:
    Game.state.del_t = Game.clock.tick(Game.state.FPS) / 1000
    Game.events()
    Game.update()
    Game.draw()
# Close the window and quit.
pg.quit()