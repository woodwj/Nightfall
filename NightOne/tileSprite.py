from settings import *
import pygame as pg
import utils
vec = pg.math.Vector2

def collideDetect(sprite1,sprite2):
        return sprite1.col_rect.colliderect(sprite2.col_rect)

class tileSprite(pg.sprite.Sprite):
    def __init__(self, gameScene, tile_x, tile_y, groups = []):
            # initilize with desired groups
            pg.sprite.Sprite.__init__(self, groups)
            # for faster coding save to local variable and acess in other class functions
            self.gameScene = gameScene
            self.image = pg.Surface((self.gameScene.state.tileSize, self.gameScene.state.tileSize))
            self.rect = self.image.get_rect()
            self.pos = vec(tile_x, tile_y) * self.gameScene.state.tileSize
            self.rect.topleft =  self.pos
            self.col_rect = self.rect          
            self.vel = vec(0,0)
            self.moveDist = (0,0)

    def move(self):
        if self.moveDist.x != 0:
            self.pos.x += self.moveDist.x
            self.col_rect.centerx = self.pos.x
            self.collide_with_walls('x')
        if self.moveDist.y != 0:
            self.pos.y += self.moveDist.y
            self.col_rect.centery = self.pos.y
            self.collide_with_walls('y')
        self.col_rect.center = self.pos
        self.rect.center = self.col_rect.center


    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.gameScene.objects.groupWalls, False, self.collideDetect)
            if hits:
                # right -> left
                if self.vel.x > 0:
                    self.col_rect.right = hits[0].col_rect.left
                # left -> right
                if self.vel.x < 0:
                    self.col_rect.left = hits[0].col_rect.right
                # fix velocity and rect
                    self.vel.x = 0

                self.pos.x = self.col_rect.centerx

                if self.type == "zombie" and self.action != "meleeattack":
                    self.action = "meleeattack"
                    self.animator.newAction("meleeattack")
                    hits[0].health -= self.damage

        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.gameScene.objects.groupWalls, False, self.collideDetect)
            if hits:
                # up - > down
                if self.vel.y > 0:
                    self.col_rect.bottom = hits[0].col_rect.top
                # down -> up
                if self.vel.y < 0:
                    self.col_rect.top = hits[0].col_rect.bottom
                # fix velocity and rect
                    self.vel.y = 0

                self.pos.y = self.col_rect.centery

                if self.type == "zombie" and self.action != "meleeattack":
                    self.action = "meleeattack"
                    self.animator.newAction("meleeattack")
                    hits[0].health -= self.damage


    def collideDetect(self,sprite1,sprite2):
        return sprite1.col_rect.colliderect(sprite2.col_rect)
    
    def changeImg(self):
        self.image = self.animator.animImg
        self.ogImage = self.image
        self.rect =self.image.get_rect(topleft = self.pos)
        self.rect.center = self.col_rect.center

    def rotate(self, angle = None):
        if angle:
            self.angle = angle
        self.image = pg.transform.rotate(self.ogImage, self.angle)
        self.rect = self.image.get_rect(topright  = self.rect.topleft)
        self.col_rect.center = self.rect.center
        #self.col_rect.center = self.rect.center    

    def update(self):
        # change in x and y is calculated off velocity and the change in time
        self.moveDist = self.vel * self.gameScene.state.del_t
        self.moveDist = vec(int(self.moveDist.x),int(self.moveDist.y))
        if self.moveDist.y !=0 or self.moveDist.x !=0:
            # performs movement
            self.move()
        self.vel = vec(0,0)
        if self.health < 0:
            self.kill()
        