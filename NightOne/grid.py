import pygame as pg
import utils
import pathlib
from pathlib import Path
from settings import *

vec = pg.math.Vector2

# class for the map to draw grid while developing and decode files
class mapManager():
    def __init__(self, gameScene, directory = "start.txt"):
        self.gameScene = gameScene
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
        self.width = self.tilesWide * self.gameScene.state.tileSize
        self.height = self.tilesHigh * self.gameScene.state.tileSize

class camera:
    def __init__(self, gameScene, width, height):
        # creates the camera and imports some settings
        self.gameScene = gameScene
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
    def get_pos(self, target):
        # set targets real position on the screen for target's use
        self.offset = vec(self.camera.topleft)
        target.x -= self.offset.x
        target.y -= self.offset.y
        # if there camera has moved then use the offset otherwise their own rect
        return (target)

    # temporary grid for developmet
    def draw_Grid(self):
        for x in range(int(self.offset.x), self.gameScene.map.width, self.gameScene.state.tileSize):
            pg.draw.line(self.gameScene.state.screen, WHITE, (x, 0), (x, self.gameScene.map.height))
        for y in range(int(self.offset.y), self.gameScene.map.height, self.gameScene.state.tileSize):
            pg.draw.line(self.gameScene.state.screen, WHITE, (0, y), (self.gameScene.map.width, y))

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
        x = -target.rect.centerx + int(self.gameScene.state.screenWidth*0.5)
        y = -target.rect.centery + int(self.gameScene.state.screenHeight*0.5)
        self.cam += (vec(x, y) - self.cam) * 0.05
        self.cam.x = max(-(self.mapWidth - self.gameScene.state.screenWidth), min(0, int(self.cam.x)))
        self.cam.y = max(-(self.mapHeight - self.gameScene.state.screenHeight), min(0, int(self.cam.y)))
        self.camera.topleft = self.cam