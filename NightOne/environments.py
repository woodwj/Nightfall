from settings import *
import pygame as pg
import utils
import tileSprite
vec = pg.math.Vector2


# wall class - immobile
class wall(tileSprite.tileSprite):
        def __init__(self, gameScene, tile_x, tile_y):
            # want walls in all group and wall group
            self.groups = [gameScene.objects.groupAll, gameScene.objects.groupWalls]
            # initilize the super with desired groups
            super().__init__(gameScene, tile_x, tile_y, self.groups)
            self.image.fill(GREEN)