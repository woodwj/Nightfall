import settings
import pygame as pg
import utils
from random import randint
vec = pg.math.Vector2

# collision method - outside class for extramodular colision handling #
def collideDetect(sprite1,sprite2):
    if sprite1.ID != sprite2.ID: return sprite1.col_rect.colliderect(sprite2.col_rect)
def collideDetectWide(sprite1,sprite2):
    if sprite1.ID != sprite2.ID: return sprite1.rect.colliderect(sprite2.rect)

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
            self.action = self.actionNew= ""
            self.rect = self.image.get_rect()
            if topLeft != None: self.rect.topleft = topLeft
            elif center != None: self.rect.center = center
            self.col_rect = self.rect
            self.pos = vec(self.rect.center) 
            # movement #
            self.moveType = "static"
            self.angle = 0
            self.ID = self.spriteHash(hash(randint(0,999999)))
            
    def spriteHash(self,key):  
        if key not in self.gameScene.objects.spriteID:
            self.gameScene.objects.spriteID.append(key)
            return(key)
        else:
            self.spriteHash(key+3)  

    def maptoGrid(self, v):
        return vec(v.x // self.gameScene.state.tileSize, v.y//self.gameScene.state.tileSize) * self.gameScene.state.tileSize

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
        hits = pg.sprite.spritecollide(self, self.gameScene.objects.groupAll, False, collided= collideDetect)
        collide = False
        if len(hits)>0:
            collide = True
            for hit in hits:
                # stop bullet from interacting with walls #
                if hit.actorType == "bullet" or self.actorType== "bullet":
                    collide = False
                    # bullet hits target ~> deal damage ~> destroy bullet #
                    if hit.actorType in self.gameScene.objects.bTargets:
                        hit.health -= self.damage
                        self.kill()
                # zombie hits target ~> attack animation #
                if self.actorType == "zombie" and self.action not in settings.a_continious and hit.actorType in self.gameScene.objects.zTargets:
                    if hit.health // self.damage + self.gameScene.state.upZombies < 10:
                        collide = False
                    self.actionNew =self.action = "meleeattack"
                    self.animator.changeAnim(self.actionNew)
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
    
    # animation change ~> new image # 
    def changeImg(self):
        self.image = self.ogImage = self.animator.animImg = self.animator.animList[self.animator.animCount]
        self.rotate(self.angle)
    
    def checkAction(self, action, weapon = None):
        change = False
        # when change should happen #
        if hasattr(self, "weapon"):
            if action != self.action or weapon != self.weapon:
                change = True
        elif action != self.action:
                change = True
        # when change shouldnt happen #
        if self.action in settings.a_continious:
            change = False
            # at the end of a continueous action #
            if self.animator.animCount == self.animator.animLength-1:
                change = True
        return change

    # rotate img + adjust rects
    def rotate(self, angle):
        self.angle = angle
        self.image = pg.transform.rotate(self.ogImage, self.angle)
        self.rect = self.image.get_rect(center  = self.pos)
        self.col_rect.center = self.pos

    def update(self):
        # change in x and y is calculated off velocity and the change in time
        if self.moveType == "dynamic":
            self.moveDist = self.vel * (self.gameScene.state.del_t%0.5)
            self.moveDist = utils.intVec(self.moveDist)
            if self.moveDist.y !=0 or self.moveDist.x !=0:
                # performs movement
                self.move()

        if self.health < 0:
            if self.actorType == "zombie":
                self.gameScene.objects.buildMode.buildPoints += 5
            self.kill()
