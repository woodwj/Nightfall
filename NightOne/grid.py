import pygame as pg
import utils
import pathlib
from pathlib import Path
from settings import *

vec = pg.math.Vector2

# class for the map to draw grid while developing and decode files
class mapManager():
    def __init__(self, gameState, directory = "start.txt"):
        self.gameState = gameState
        # using pathlib to standardize directories
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
        self.mapWidth = width
        self.mapHeight = height
        self.offset = vec(0,0)
        self.cam = vec(0,0)
    
    # applies the camera to a target    
    def apply(self, target):
        return target.rect.move(self.camera.topleft)

    # updates the movement of the camera
    def update(self, target):

        # set targets real position on the screen for target's use
        self.offset = vec(self.camera.topleft)
        targetPos_x = target.rect.x + self.offset.x
        targetPos_y = target.rect.y + self.offset.y
        # if there camera has moved then use the offset otherwise their own rect
        target.screenPos.x = target.col_rect.x
        if self.offset.x < 0:
            target.screenPos.x = targetPos_x
        target.screenPos.y = target.col_rect.y
        if self.offset.y < 0:
            target.screenPos.y = targetPos_y
        
        # x and y are the 
        x = -target.rect.centerx + int(self.gameState.screenWidth*0.5)
        y = -target.rect.centery + int(self.gameState.screenHeight*0.5)
        self.cam += (vec(x, y) - self.cam) * 0.05
        self.cam.x = max(-(self.mapWidth - self.gameState.screenWidth), min(0, int(self.cam.x)))
        self.cam.y = max(-(self.mapHeight - self.gameState.screenHeight), min(0, int(self.cam.y)))
        self.camera.topleft = self.cam
        