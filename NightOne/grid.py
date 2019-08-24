import pygame as pg
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

        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * self.gameState.tileSize
        self.height = self.tileheight * self.gameState.tileSize
    
    def draw_Grid(self):
        for x in range(0, self.gameState.screenWidth, self.gameState.tileSize):
            pg.draw.line(self.gameState.screen, WHITE, (x, 0), (x, self.gameState.screenHeight))
        for y in range(0, self.gameState.screenHeight, self.gameState.tileSize):
            pg.draw.line(self.gameState.screen, WHITE, (0, y), (self.gameState.screenWidth, y))



class camera:
    def __init__(self, gameState, width, height):
        self.gameState = gameState
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        
        

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.x + int(self.gameState.screenWidth / 2)
        y = -target.rect.y + int(self.gameState.screenHeight / 2)
        self.camera = pg.Rect(x, y, self.width, self.height)

        # limit scrolling to map size
        #x = min(0, x)  # left
        #y = min(0, y)  # top
        #x = max(-(self.width - self.gameState.screenWidth), x)  # right
        #y = max(-(self.height - self.gameState.screenHeight), y)  # bottom
        