import pygame as pg
import utils
import pathlib
from pathlib import Path
from settings import *


class mapManager():
    def __init__(self, gameState, directory = "start.txt"):
        self.gameState = gameState
        baseFolder = pathlib.Path.cwd()
        mapDir = baseFolder / "maps" / directory
        self.data = []
        with mapDir.open() as f:
            for line in f:
                self.data.append(line.strip())

        self.tilesWide = len(self.data[0])
        self.tilesHigh = len(self.data)
        self.width = self.tilesWide * self.gameState.tileSize
        self.height = self.tilesHigh * self.gameState.tileSize
    
    def draw_Grid(self):
        for x in range(0, self.gameState.screenWidth, self.gameState.tileSize):
            pg.draw.line(self.gameState.screen, WHITE, (x, 0), (x, self.gameState.screenHeight))
        for y in range(0, self.gameState.screenHeight, self.gameState.tileSize):
            pg.draw.line(self.gameState.screen, WHITE, (0, y), (self.gameState.screenWidth, y))



class camera:
    def __init__(self, gameState, width, height):
        self.gameState = gameState
        self.camera = pg.Rect(0, 0, width, height)
        self.cSpeed = c_speed
        self.cmoveWidth = c_moveWidth
        self.cmoveHeight = c_moveHeight
        self.width = width
        self.height = height
        self.do_once = True
        self.del_x , self.del_y = 0,0
        self.vel_x , self.vel_y = 0,0
        self.dist_x, self.dist_y = 0,0
        self.x, self.y = 0,0
        
        
        
        
    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        self.del_x , self.del_y = 0,0
    
        if self.do_once:
            self.x = -target.rect.x + int(self.gameState.screenWidth / 2)
            self.y = -target.rect.y + int(self.gameState.screenHeight / 2)
            self.do_once = False

        self.cam_x = -self.x + int(self.gameState.screenWidth / 2)
        self.cam_y = -self.y + int(self.gameState.screenHeight / 2)
        self.dist_x, self.dist_y = self.cam_x - target.rect.x, self.cam_y - target.rect.y
        
        if self.dist_x > self.cmoveWidth:
            self.vel_x += self.cSpeed
        elif self.dist_x < -1*self.cmoveWidth:
            self.vel_x -= self.cSpeed
        if self.dist_y > self.cmoveHeight:
            self.vel_y += self.cSpeed
        elif self.dist_y < -1*self.cmoveHeight:
            self.vel_y -= self.cSpeed

        self.vel_x, self.vel_y = utils.mult2by1(self.vel_x, self.vel_y, self.gameState.del_t)
        self.x, self.y = self.x + self.vel_x, self.y + self.vel_y
        
        print(self.x, target.rect.x, self.dist_x)
        #limit scrolling to map size
        self.x = min(0, self.x)  # left
        self.y = min(0, self.y)  # top
        self.x = max(-(self.width - self.gameState.screenWidth), self.x)  # right
        self.y = max(-(self.height - self.gameState.screenHeight), self.y)  # bottom
        self.camera = pg.Rect(self.x, self.y, self.width, self.height)

        