from settings import *
import pygame as pg

class wall(pg.sprite.Sprite):
        def __init__(self, gameScene, tile_x, tile_y):
            # want walls in all group and wall group
            self.groups = gameScene.objects.groupAll, gameScene.objects.groupWalls
            # initilize the super with desired groups
            pg.sprite.Sprite.__init__(self, self.groups)
            # for faster coding save to local variable and acess in other class functions
            self.gameScene = gameScene
            self.image = pg.Surface((self.gameScene.state.tileSize, self.gameScene.state.tileSize))
            self.image.fill(BLUE)
            self.rect = self.image.get_rect()
            self.pos_x , self.pos_y = tile_x, tile_y
            self.rect.x = self.pos_x * self.gameScene.state.tileSize
            self.rect.y = self.pos_y * self.gameScene.state.tileSize