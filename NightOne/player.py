import pygame as pg
from settings import *

class player(pg.sprite.Sprite):
    def __init__(self, gameScene, tile_x, tile_y):
        # only want player in all sprites group
        self.groups = gameScene.objects.groupAll
        # initilize the super with desired groups
        pg.sprite.Sprite.__init__(self, self.groups)
        # for faster coding save to local variable and acess in other class functions
        self.gameScene = gameScene
        # create the square on the surface
        self.image = pg.Surface((tileSize, tileSize))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.pos_x = tile_x
        self.pos_y = tile_y

    def move(self, del_x=0, del_y=0):
        if not self.wallCollide(del_x, del_y):
            self.pos_x += del_x
            self.pos_y += del_y

    def wallCollide(self, del_x = 0, del_y = 0):
        for wall in self.gameScene.objects.groupWalls:
            if wall.x == self.pos_x + del_x and wall.y == self.pos_y + del_y:
                return True
        return False


    def update(self):
        self.rect.x = self.pos_x * tileSize
        self.rect.y = self.pos_y * tileSize