import pygame as pg
import tileSprite

class buildMode(tileSprite.tileSprite):
    def __init__(self, gameScene):
        self.gameScene = gameScene
        #load tiles ect
    def start(self):
        self.mouse = pg.mouse.get_pos()
        self.tile_x = mouse.x * self.gameState.map.width // self.gameState.tileSize
        self.tile_y = mouse.y * self.gameScene.map.height // self.gameScene.tileSize
        super().__init__(self.gameScene, tile_x, tile_y, groups)

    def update(self):
        ijunks = 0