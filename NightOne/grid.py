import pygame as pg
import utils
import pathlib
from pathlib import Path
from settings import *

# class for the map to draw grid while developing and decode files
class mapManager():
    def __init__(self, gameState, directory = "start.txt"):
        self.gameState = gameState
        # using pathlib to standarise directories
        baseFolder = pathlib.Path.cwd()
        mapDir = baseFolder / "maps" / directory
        self.data = []
        with mapDir.open() as f:
            for line in f:
                self.data.append(line.strip())

        # tilemap calculations
        self.tilesWide = len(self.data[0])
        self.tilesHigh = len(self.data)
        self.width = self.tilesWide * self.gameState.tileSize
        self.height = self.tilesHigh * self.gameState.tileSize
    
    # temporary grid for developmet
    def draw_Grid(self):
        for x in range(0, self.width, self.gameState.tileSize):
            pg.draw.line(self.gameState.screen, WHITE, (x, 0), (x, self.height))
        for y in range(0, self.height, self.gameState.tileSize):
            pg.draw.line(self.gameState.screen, WHITE, (0, y), (self.width, y))



class camera:
    def __init__(self, gameState, width, height):
        # creates the camera and imports some settings
        self.gameState = gameState
        self.camera = pg.Rect(0, 0, width, height)
        self.cSpeed = c_speed
        self.cmoveWidth = c_moveWidth
        self.cmoveHeight = c_moveHeight
        self.width = width
        self.height = height
        self.del_x , self.del_y = 0,0
        self.vel_x , self.vel_y = 0,0
        self.dist_x, self.dist_y = 0,0
        self.x, self.y = 0,0
        
        
        
    # applies the camera to a target    
    def apply(self, target):
        return target.rect.move(self.camera.topleft)

    # updates the movement of the camera
    def update(self, target):
        
        # takes the cam position and calculates the distance between the rect and the camera x and y
        self.del_x , self.del_y = 0,0
        self.cam_x = -self.x + int(self.gameState.screenWidth / 2)
        self.cam_y = -self.y + int(self.gameState.screenHeight / 2)
        self.dist_x, self.dist_y = self.cam_x - target.rect.x, self.cam_y - target.rect.y
        
        # internal movement
        # right
        if self.dist_x > self.cmoveWidth:
            self.vel_x += self.cSpeed
        # left
        elif self.dist_x < -1*self.cmoveWidth:
            self.vel_x -= self.cSpeed
        # down
        if self.dist_y > self.cmoveHeight:
            self.vel_y += self.cSpeed
        # up
        elif self.dist_y < -1*self.cmoveHeight:
            self.vel_y -= self.cSpeed

        # adjust vel then position
        self.vel_x, self.vel_y = utils.mult2by1(self.vel_x, self.vel_y, self.gameState.del_t)
        self.x, self.y = self.x + self.vel_x, self.y + self.vel_y
        
        print(self.x, target.rect.x, self.dist_x)
        #limit scrolling to map size
        # left
        self.x = min(0, self.x)
        # top
        self.y = min(0, self.y)  
        # right
        self.x = max(-(self.width - self.gameState.screenWidth), self.x)
        # bottom  
        self.y = max(-(self.height - self.gameState.screenHeight), self.y)
        # change the camerea rect  
        self.camera = pg.Rect(self.x, self.y, self.width, self.height)

        