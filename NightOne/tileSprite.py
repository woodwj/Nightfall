from settings import *
import pygame as pg
import utils
vec = pg.math.Vector2

# collision method outside class #
def collideDetect(sprite1,sprite2):
    if sprite1.col_rect != sprite2.col_rect:
        return sprite1.col_rect.colliderect(sprite2.col_rect)

# parent class to all sprites; contains common functions and attributes #
class tileSprite(pg.sprite.Sprite):
    def __init__(self, gameScene, groups = [], topLeft = None, center = None):
            # initilize with desired groups #
            pg.sprite.Sprite.__init__(self, groups)
            # save reference to gameScene #
            self.gameScene = gameScene
            # visual #
            self.image = pg.Surface((self.gameScene.state.tileSize, self.gameScene.state.tileSize))
            # rect handling #
            self.rect = self.image.get_rect()
            if topLeft != None: self.rect.topleft = topLeft
            elif center != None: self.rect.center = center
            self.col_rect = self.rect
            self.pos = vec(self.rect.center) 

            # movement #
            self.moveType = "static"
            self.angle = 0

    def move(self):
        # x-direction #
        if self.moveDist.x != 0:
            self.pos.x += self.moveDist.x
            self.col_rect.centerx = self.pos.x
            self.handleCollision("x")
        # y-direction #    
        if self.moveDist.y != 0:
            self.pos.y += self.moveDist.y
            self.col_rect.centery = self.pos.y
            self.handleCollision("y")
        # adjust rect and pos #    
        self.rect.center = self.col_rect.center
        self.pos = vec(self.col_rect.center)
        
    def handleCollision(self, direct):
        collide = False
        hits = pg.sprite.spritecollide(self, self.gameScene.objects.groupAll, False, collided=self.collideDetect)
        if hits:
            collide = True
            for hit in hits:
                # stop bullet from interacting with walls #
                if hit.actorType == "bullet" or self.actorType== "bullet":
                    collide = False
                # bullet hits target ~> deal damage ~> destroy bullet #
                if self.actorType == "bullet" and hit.actorType in self.gameScene.objects.bTargets:
                    hit.health -= self.damage
                    self.kill()
                # zombie hits target ~> attack animation #
                if self.actorType == "zombie" and self.action != "meleeattack" and hit.actorType in self.gameScene.objects.zTargets:
                    self.action = "meleeattack"
                    self.animator.newAction("meleeattack")
                    hit.health -= self.damage
                
        if collide:
            if direct == "x":
                # left ~> right #
                if self.vel.x > 0:
                    self.col_rect.right = hits[0].col_rect.left
                # right ~> left #
                elif self.vel.x < 0:
                    self.col_rect.left = hits[0].col_rect.right
                self.vel.x = 0

            elif direct == "y":
                # up ~> down #
                if self.vel.y > 0:
                    self.col_rect.bottom = hits[0].col_rect.top
                # down -> up
                elif self.vel.y < 0:
                    self.col_rect.top = hits[0].col_rect.bottom    
                self.vel.y = 0
    
    # collision handling method #
    def collideDetect(self,sprite1,sprite2):
        if sprite1 != sprite2: return sprite1.col_rect.colliderect(sprite2.col_rect)
    
    # animation change ~> new image #
    def changeImg(self):
        self.ogImage = self.animator.animImg
        self.rotate(self.angle)
    
    # rotate img + adjust rects
    def rotate(self, angle):
        self.angle = angle
        self.image = pg.transform.rotate(self.ogImage, self.angle)
        self.rect = self.image.get_rect(center  = self.pos)
        self.col_rect.center = self.pos
        
    def update(self):
        # change in x and y is calculated off velocity and the change in time
        if self.moveType == "dynamic":
            self.moveDist = self.vel * self.gameScene.state.del_t
            self.moveDist = vec(int(self.moveDist.x),int(self.moveDist.y))
            if self.moveDist.y !=0 or self.moveDist.x !=0:
                # performs movement
                self.move()
        
        if self.health < 0:
            self.kill()