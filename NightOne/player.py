import pygame as pg
import utils
import math
import pathlib
import animations
from settings import *

vec = pg.math.Vector2

class player(pg.sprite.Sprite):
    def __init__(self, gameScene, tile_x, tile_y):
        # for faster coding save to local variable and acess in other class functions
        self.gameScene = gameScene
        # only want player in all sprites group
        self.groups = self.gameScene.objects.groupAll
        # initilize the super with desired groups
        pg.sprite.Sprite.__init__(self, self.groups)
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
        self.rot = 0
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
            self.vel.x, self.vel.y = utils.mult2by1(self.vel.x, self.vel.y, 0.7071)

            
    # move function to add to x and y, the change in x and y plus check collision on both axis
    def move(self):
        self.pos += self.rel
        self.col_rect.centerx = self.pos.x
        self.collide_with_walls('x')
        self.col_rect.centery = self.pos.y
        self.collide_with_walls('y')
        self.rect.center = self.col_rect.center
    
    def rotate(self):
        mouse_x, mouse_y = pg.mouse.get_pos()
        dif_x, dif_y = mouse_x - self.screenPos_x, mouse_y - self.screenPos_y
        angle = (180 / math.pi) * -math.atan2(dif_y, dif_x)
        self.image = pg.transform.rotate(self.originalImage, int(angle))
        self.rect = self.image.get_rect(center=self.pos)

    # collision checker for both axis
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
    
    def col_hitrect(self, sprite1,sprite2):
        return sprite1.col_rect.colliderect(sprite2.rect)

    # player update funciton - called every gameloop
    def update(self):
        self.rotate()
        # check controls
        self.controls()
        # chane in x and y is calculated off velocity and the change in time
        self.rel = self.vel * self.gameScene.state.del_t
        # performs movement
        self.move()

        
        
        