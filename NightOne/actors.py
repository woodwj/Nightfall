import pygame as pg
import utils
import math
import pathlib
import animations
from settings import *
import tiletemplate

vec = pg.math.Vector2

class player(tiletemplate.tileSprite):
    def __init__(self, gameScene, tile_x, tile_y):

        # for faster coding save to local variable and acess in other class functions
        self.gameScene = gameScene
        # only want player in all sprites group
        self.groups = self.gameScene.objects.groupAll
        super().__init__(self.gameScene, tile_x, tile_y, self.groups)
                
        # initilize the super with desired groups
        self.action = p_action
        self.weapon = p_weapon

        self.animator = animations.animator("player")
        self.animator.newAction(p_action, p_weapon)
        self.imgFile = self.animator.animList[0]
        self.image = pg.image.load(self.imgFile).convert_alpha()
        self.image = pg.transform.scale( self.image, (self.gameScene.state.tileSize * 2,self.gameScene.state.tileSize *2))
        self.rect = self.image.get_rect()
        self.originalImage = self.image

        self.col_rect = p_collisionRect
        self.vel = vec(0,0)
        self.pos = vec(tile_x,tile_y)*self.gameScene.state.tileSize
        #self.rot = 0
        self.screenPos_x, self.screenPos_y = 0,0
    
    # controls method here for 2 reasons 1) code on main is relevent to main 2) player is self contained and modular
    def controls(self):
        # velocity in both axis set to 0
        self.vel = vec(0,0)
        
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel.x = p_speed * -1
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel.x = p_speed 
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel.y = p_speed * -1
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel.y = p_speed
        
        # code to adjust diagonal speed - diagram to show pythag    
        if self.vel.y !=0 and self.vel.x !=0:
            self.vel *= 0.7071
            self.vel = vec(int(self.vel.x), int(self.vel.y))

    
    def rotate(self):
        mouse_x, mouse_y = pg.mouse.get_pos()
        dif_x, dif_y = mouse_x - self.screenPos_x, mouse_y - self.screenPos_y
        angle = (180 / math.pi) * -math.atan2(dif_y, dif_x)
        self.image = pg.transform.rotate(self.originalImage, int(angle))
        self.rect = self.image.get_rect(center=self.pos)

    
    # player update funciton - called every gameloop
    def update(self):
        self.rotate()
        # check controls
        self.controls()
        # chane in x and y is calculated off velocity and the change in time
        self.rel = self.vel * self.gameScene.state.del_t
        # performs movement
        self.move()


class zombie(tiletemplate.tileSprite):
    def __init__(self, gameScene, tile_x, tile_y):

        # for faster coding save to local variable and acess in other class functions
        self.gameScene = gameScene
        self.groups = gameScene.objects.groupAll, gameScene.objects.groupZombies
        super().__init__(self.gameScene, tile_x, tile_y, self.groups)

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
        self.col_rect = z_collisionRect.copy()
   
    def rotate(self):
        self.rot = (self.gameScene.objects.player.pos - self.pos).angle_to(vec(1, 0))
        self.image = pg.transform.rotate(self.ogImage, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
    
    def chase(self):
        self.vel = vec(0,0)
        # x axis
        if self.rect.x < self.gameScene.objects.player.rect.centerx:
            self.vel.x = z_speed
        if self.rect.x > self.gameScene.objects.player.rect.centerx:
            self.vel.x = z_speed * -1
        # y axis
        if self.rect.y < self.gameScene.objects.player.rect.centery:
            self.vel.y = z_speed
        if self.rect.y > self.gameScene.objects.player.rect.centery:
            self.vel.y = z_speed * -1
        
        if self.vel.y !=0 and self.vel.x !=0:   
            self.vel *= 0.7071
            
    def update(self):
        self.rotate()
        self.chase()
        self.rel = self.vel * self.gameScene.state.del_t
        self.move()