from settings import *
import pygame as pg
import utils
import tileSprite
import settings
vec = pg.math.Vector2


# wall class - immobile
class wall(tileSprite.tileSprite):
        def __init__(self, gameScene, topLeft = None):
            # want walls in all group and wall group
            self.groups = [gameScene.objects.groupAll, gameScene.objects.groupWalls]
            # initilize the super with desired groups
            super().__init__(gameScene, self.groups, topLeft = topLeft)
            self.material = "def"
            self.actorType = "wall"
            self.image = gameScene.state.gallery.art[self.actorType][self.material]["def"]
            self.health = 10000000
            
                
class playerWall(wall):
    def __init__(self,gameScene, topLeft, img, material):
        super().__init__(gameScene, topLeft = topLeft)
        self.actorType = "playerWall"
        self.material = material
        self.image = img
        self.col_rect = self.rect = self.image.get_rect(topleft=topLeft)
        self.health = settings.bm_objects[self.material]["health"]

                
                



            