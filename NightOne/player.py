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
        self.image = pg.Surface((self.gameScene.state.tileSize, self.gameScene.state.tileSize))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.pos_x, self.pos_y = utils.mult2by1(tile_x , tile_y, self.gameScene.state.tileSize)
        self.vel_x, self.vel_y = 0,0
    
    # controls method here for 2 reasons 1) code on main is relevent to main 2) player is self contained and modular
    def controls(self):
        # velocity in both axis set to 0
        self.vel_x, self.vel_y = 0,0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel_x = p_speed * -1
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel_x = p_speed 
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel_y = p_speed * -1
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel_y = p_speed
        
        # code to adjust diagonal speed - diagram to show pythag    
        if self.vel_y !=0 and self.vel_x !=0:
            self.vel_x, self.vel_y = utils.mult2by1(self.vel_x, self.vel_y, 0.7071)
            
    # move function to add to x and y, the change in x and y plus check collision on both axis
    def move(self, del_x, del_y):
        self.pos_x , self.pos_y = self.pos_x + del_x , self.pos_y + del_y
        self.rect.x = self.pos_x
        self.collide_with_walls('x')
        self.rect.y = self.pos_y
        self.collide_with_walls('y')

    # collision checker for both axis
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.gameObjects.groupWalls, False)
            if hits:
                # right -> left
                if self.vel_x > 0:
                    self.pos_x = hits[0].rect.left - self.rect.width
                # left -> right
                if self.vel_x < 0:
                    self.pos_x = hits[0].rect.right
                # fix velocity and rect
                self.vel_x = 0
                self.rect.x = self.pos_x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.gameObjects.groupWalls, False)
            if hits:
                # up - > down
                if self.vel_y > 0:
                    self.pos_y = hits[0].rect.top - self.rect.height
                # down -> up
                if self.vel_y < 0:
                    self.pos_y = hits[0].rect.bottom
                # adjust velocity and rect
                self.vel_y = 0
                self.rect.y = self.pos_y

    # player update funciton - called every gameloop
    def update(self):
        # check controls
        self.controls()
        # chane in x and y is calculated off velocity and the change in time
        self.del_x, self.del_y = utils.mult2by1(self.vel_x, self.vel_y, self.gameScene.state.del_t)
        # performs movement
        self.move(self.del_x, self.del_y)
        