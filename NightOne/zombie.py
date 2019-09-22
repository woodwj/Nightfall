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
        self.ogImage = self.image
        self.rect = self.image.get_rect()
        self.originalImage = self.image
        self.pos = vec(tile_x, tile_y) * self.gameScene.state.tileSize
        self.vel = vec(0,0)
        self.rect.center = self.pos
        self.col_rect = z_collisionRect

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.gameScene.objects.groupWalls, False, self.col_hitrect)
            if hits:
                # right -> left
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - int(self.col_rect.width / 2)
                # left -> right
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right + int(self.col_rect.width / 2.0)
                # fix velocity and rect
                self.vel.x = 0
                self.col_rect.centerx = self.pos.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.gameScene.objects.groupWalls, False, self.col_hitrect)
            if hits:
                # up - > down
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - int(self.col_rect.height / 2.0)
                # down -> up
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom + int(self.col_rect.height / 2.0)
                # adjust velocity and rect
                self.vel.y = 0
                self.col_rect.centery = self.pos.y


    def rotate(self):
        self.rot = (self.gameScene.objects.player.pos - self.pos).angle_to(vec(1, 0))
        self.image = pg.transform.rotate(self.ogImage, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
    
    def chase(self):
        self.vel = vec(0,0)
        if self.rect.x < self.gameScene.objects.player.pos.x:
            self.vel.x += z_speed
        elif self.rect.x > self.gameScene.objects.player.pos.x:
            self.vel.x -= z_speed

        if self.rect.y < self.gameScene.objects.player.pos.y:
            self.vel.y += z_speed
        elif self.rect.y > self.gameScene.objects.player.pos.y:
            self.vel.y -= z_speed
        
        if self.vel.y !=0 and self.vel.x !=0:
            self.vel *= 0.7071
            
        
    def move(self):
        self.pos += self.rel
        self.rect.center = self.pos

    def update(self):
        self.rotate()
        self.chase()
        self.rel = self.vel * self.gameScene.state.del_t
        self.move()

