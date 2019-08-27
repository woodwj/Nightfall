import pygame as pg
import animations
from settings import *

vec = pg.math.Vector2

class zombie(pg.sprite.Sprite):
    def __init__(self, gameScene, tile_x, tile_y):
        self.groups = gameScene.objects.groupAll, gameScene.objects.groupZombies
        pg.sprite.Sprite.__init__(self, self.groups)

        self.gameScene = gameScene
        self.animator = animations.animator("zombie")
        self.animator.newAction("idle")
        self.imgFile = self.animator.animList[0]
        self.image = pg.image.load(self.imgFile).convert_alpha()

        self.image = pg.transform.scale( self.image, (self.gameScene.state.tileSize * 2,self.gameScene.state.tileSize *2))
        self.rect = self.image.get_rect()
        self.originalImage = self.image
        self.pos = vec(tile_x, tile_y) * self.gameScene.state.tileSize
        self.rect.center = self.pos
        self.col_rect = z_collisionRect

        self.segments = [
                {"a": {"x": self.col_rect.left,"y": self.col_rect.top} ,"b":{"x": self.col_rect.right,"y": self.col_rect.top}},
                {"a": {"x": self.col_rect.left,"y": self.col_rect.top}, "b":{"x": self.col_rect.left,"y": self.col_rect.bottom}},
                {"a": {"x": self.col_rect.left,"y": self.col_rect.bottom}, "b": {"x": self.col_rect.right,"y": self.col_rect.bottom}},
                {"a": {"x": self.col_rect.right,"y": self.col_rect.bottom}, "b": {"x": self.col_rect.right,"y": self.col_rect.top}}
                ]

