from settings import *
import pygame as pg
import utils
vec = pg.math.Vector2


class tileSprite(pg.sprite.Sprite):
    def __init__(self, gameScene, tile_x, tile_y, groups):
            # initilize with desired groups
            pg.sprite.Sprite.__init__(self, groups)
            # for faster coding save to local variable and acess in other class functions
            self.gameScene = gameScene
            self.image = pg.Surface((self.gameScene.state.tileSize, self.gameScene.state.tileSize))
            self.rect = self.image.get_rect()
            self.col_rect = self.rect
            self.pos = vec(tile_x, tile_y) * self.gameScene.state.tileSize
            self.rect.topleft =  self.pos 

    def move(self):
        self.pos += self.moveDist
        self.col_rect.centerx = self.pos.x
        self.collide_with_walls('x')
        self.col_rect.centery = self.pos.y
        self.collide_with_walls('y')
        self.rect.center = self.col_rect.center

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.gameScene.objects.groupWalls, False, self.collideDetect)
            if hits:
                # right -> left
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - int(self.col_rect.width / 2)
                # left -> right
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right + int(self.col_rect.width / 2)
                # fix velocity and rect
                self.vel.x = 0
                self.col_rect.centerx = self.pos.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.gameScene.objects.groupWalls, False, self.collideDetect)
            if hits:
                # up - > down
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - int(self.col_rect.height / 2)
                # down -> up
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom + int(self.col_rect.height / 2)
                # fix velocity and rect
                self.vel.y = 0
                self.col_rect.centery = self.pos.y

    def collideDetect(self,sprite1,sprite2):
        return sprite1.col_rect.colliderect(sprite2.rect)
    
    def changeImg(self):
        self.image = self.animator.animImg
        self.ogImage = self.image
        self.rect =self.image.get_rect(center = self.rect.center)
        