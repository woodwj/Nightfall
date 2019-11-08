from settings import *
import pygame as pg
import utils
import tileSprite
vec = pg.math.Vector2


# wall class - immobile
class wall(tileSprite.tileSprite):
        def __init__(self, gameScene, tile_x, tile_y, img = None):
            # want walls in all group and wall group
            self.groups = [gameScene.objects.groupAll, gameScene.objects.groupWalls]
            # initilize the super with desired groups
            super().__init__(gameScene, tile_x, tile_y, self.groups)
            self.type = "wall"
            if img is None:
                self.image = gameScene.state.gallery.art["wall"]["stone"][0]
            else:
                self.image = img
            