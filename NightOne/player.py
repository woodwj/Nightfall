import pygame as pg
import utils
from settings import *

class player(pg.sprite.Sprite):
    def __init__(self, gameScene, gameObjects, tile_x, tile_y):
        # only want player in all sprites group
        self.groups = gameObjects.groupAll
        # initilize the super with desired groups
        pg.sprite.Sprite.__init__(self, self.groups)
        # for faster coding save to local variable and acess in other class functions
        self.gameScene = gameScene
        self.gameObjects = gameObjects
        # create the square on the surface
        self.image = pg.Surface((s_tileSize, s_tileSize))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.pos_x, self.pos_y = utils.mult2by1(tile_x , tile_y, s_tileSize)
        self.vel_x, self.vel_y = 0,0
    
    # controls method here for 2 reasons 1) code on main is relevent to main 2) player is self contained and modular
    def controls(self):
        keys = pg.key.get_pressed()
        self.vel_x, self.vel_y = 0,0
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel_x = p_speed * -1
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel_x = p_speed 
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel_y = p_speed * -1
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel_y = p_speed
        # code to fix the diagonal speed problem    
        if self.vel_y !=0 and self.vel_x !=0:
            self.vel_x, self.vel_y = utils.mult2by1(self.vel_x, self.vel_y, 0.7071)
            

    def move(self, del_x, del_y):
        self.pos_x , self.pos_y = self.pos_x + del_x , self.pos_y + del_y
        self.rect.x = self.pos_x
        self.collide_with_walls('x')
        self.rect.y = self.pos_y
        self.collide_with_walls('y')

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.gameObjects.groupWalls, False)
            if hits:
                if self.vel_x > 0:
                    self.pos_x = hits[0].rect.left - self.rect.width
                if self.vel_x < 0:
                    self.pos_x = hits[0].rect.right
                self.vel_x = 0
                self.rect.x = self.pos_x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.gameObjects.groupWalls, False)
            if hits:
                if self.vel_y > 0:
                    self.pos_y = hits[0].rect.top - self.rect.height
                if self.vel_y < 0:
                    self.pos_y = hits[0].rect.bottom
                self.vel_y = 0
                self.rect.y = self.pos_y


    def update(self):
        self.controls()
        self.del_x, self.del_y = utils.mult2by1(self.vel_x, self.vel_y, self.gameScene.del_t)
        self.move(self.del_x, self.del_y)
        