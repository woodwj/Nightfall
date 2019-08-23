import pygame as pg
from settings import *

class player(pg.sprite.Sprite):
    def __init__(self, gameScene, tile_x, tile_y):
        # only want player in all sprites group
        self.groups = gameScene.objects.groupAll
        # initilize the super with desired groups
        pg.sprite.Sprite.__init__(self, self.groups)
        # for faster coding save to local variable and acess in other class functions
        self._gameScene = gameScene
        # create the square on the surface
        self.image = pg.Surface((tileSize, tileSize))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = tile_x
        self.y = tile_y

    def move(self, vel_x=0, vel_y=0):
        self.x += vel_x
        self.y +=vel_y


    def update(self):
        self.rect.x = self.x * tileSize
        self.rect.y = self.y * tileSize