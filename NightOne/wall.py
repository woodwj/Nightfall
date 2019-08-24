from settings import *
import pygame as pg

class wall(pg.sprite.Sprite):
        def __init__(self, gameScene, tile_x, tile_y):
            # want walls in all group and wall group
            self.groups = gameScene.objects.groupAll, gameScene.objects.groupWalls
            # initilize the super with desired groups
            pg.sprite.Sprite.__init__(self, self.groups)
            # for faster coding save to local variable and acess in other class functions
            self._gameScene = gameScene
            self.image = pg.Surface((s_tileSize, s_tileSize))
            self.image.fill(BLUE)
            self.rect = self.image.get_rect()
            self.x , self.y = tile_x, tile_y
            self.rect.x = self.x * s_tileSize
            self.rect.y = self.y * s_tileSize