from settings import *
import pygame as pg
import utils
import tileSprite
import settings
vec = pg.math.Vector2


# wall class - immobile
class wall(tileSprite.tileSprite):
        def __init__(self, gameScene, tile_x, tile_y,img = None, material = "wall", realpos = None):
            # want walls in all group and wall group
            self.groups = [gameScene.objects.groupAll, gameScene.objects.groupWalls]
            # initilize the super with desired groups
            super().__init__(gameScene, tile_x, tile_y, self.groups)
            if realpos is not None:
                self.rect.topleft = realpos
                self.col_rect = self.rect
            self.material = material
            self.type = "wall"
            if img is None:
                self.image = gameScene.state.gallery.art[self.material]["def"]
                self.health = 10000000
            else:
                self.image = img            
                self.health = settings.bm_objects[self.material]["health"]
                
                



            