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
        self.width = int(self.tilesWide * self.gameScene.state.tileSize)
        self.height = int(self.tilesHigh * self.gameScene.state.tileSize)
        
class weightedGrid:
    def __init__(self,gameScene, width, height):
        self.gameScene = gameScene
        self.mapWidth ,self.mapHeight = width, height
        # right, left, down, up directions #     
        self.connections = [vec(self.gameScene.state.tileSize, 0), vec(-self.gameScene.state.tileSize, 0), vec(0, self.gameScene.state.tileSize), vec(0, -self.gameScene.state.tileSize)]
        # br,bl,tr,tl #
        self.connections += [vec(self.gameScene.state.tileSize, self.gameScene.state.tileSize), vec(-self.gameScene.state.tileSize, self.gameScene.state.tileSize), vec(self.gameScene.state.tileSize, -self.gameScene.state.tileSize), vec(-self.gameScene.state.tileSize, -self.gameScene.state.tileSize)]
        self.walls = []
        self.weights = {}

    def in_bounds(self, node):   
        return 0 <= node.x < self.mapWidth and 0 <= node.y < self.mapHeight
    def passable(self, node):
        return node not in self.walls
    def find_neighbors(self, node):
        neighbors = [node + connection for connection in self.connections]
        neighbors = filter(self.in_bounds, neighbors)
        neighbors = filter(self.passable, neighbors)
        return list(neighbors)

    def cost(self, from_node, to_node):
        if (vec(to_node) - vec(from_node)).length_squared() == 1:
            return self.weights.get(to_node, settings.t_weight) +  int(2.5 * self.gameScene.state.tileSize)
        else:
            return self.weights.get(to_node, settings.t_weight) + self.gameScene.state.tileSize

class camera:
    def __init__(self, gameScene, width, height):
        # creates the camera and imports some settings
        self.gameScene = gameScene
        self.camera = pg.Rect(0, 0, totalWidth, totalHeight)
        self.cSpeed = settings.c_speed
        self.mapWidth = totalWidth
        self.mapHeight = totalHeight
        self.offset = vec(0,0)
        self.cam = vec(0,0)
    # applies the camera to a target #
    def applySprite(self, target):
        return target.rect.move(self.camera.topleft)
    # set targets real position on the screen for target's use #
    def applyVec(self, pos):
        self.offset = vec(self.camera.topleft)
        pos += self.offset
        return pos
    # reverses position from the screen back to real position #
    def reverseVec(self,pos):
        self.offset = vec(self.camera.topleft)
        pos -= self.offset
        return pos
    # grid alignment #
    def draw_Grid(self):
        for x in range(int(self.offset.x), self.gameScene.map.width, self.gameScene.state.tileSize):
            pg.draw.line(self.gameScene.state.screen, WHITE, (x, 0), (x, self.gameScene.map.height))
        for y in range(int(self.offset.y), self.gameScene.map.height, self.gameScene.state.tileSize):
            pg.draw.line(self.gameScene.state.screen, WHITE, (0, y), (self.gameScene.map.width, y))

    def update(self, target):
        # set targets real position on the screen for target's use
        target.screenPos = self.applyVec(vec(target.col_rect.center))
        # track target # 
        x = -target.rect.centerx + int(self.gameScene.state.screenWidth*0.5)
        y = -target.rect.centery + int(self.gameScene.state.screenHeight*0.5)
        self.cam += (vec(x, y) - self.cam) * self.cSpeed
        self.cam.x = max(-(self.mapWidth - self.gameScene.state.screenWidth), min(0, int(self.cam.x)))
        self.cam.y = max(-(self.mapHeight - self.gameScene.state.screenHeight), min(0, int(self.cam.y)))
        self.camera.topleft = self.cam

        