import pygame as pg
from settings import *

class player(pg.sprite.Sprite):
    def __init__(self, gameScene, tile_x, tile_y):
        # only want player in all sprites group
        self.groups = gameScene.objects.groupAll
        # initilize the super with desired groups
        pg.sprite.Sprite.__init__(self, self.groups)
        # for faster coding save to local variable and acess in other class functions
        self.gameScene = gameScene
        # create the square on the surface
        self.image = pg.Surface((s_tileSize, s_tileSize))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.pos_x, self.pos_y = tile_x, tile_y
        self.vel_x, self.vel_y = 0,0
    
    # controls method here for 2 reasons 1) code on main is relevent to main 2) player is self contained and modular
    def controls(self):
        keys = pg.key.get_pressed()
        self.vel_x, self.vel_y = 0,0
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel_x = p_speed * -1
        elif keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel_x = p_speed 
        elif keys[pg.K_UP] or keys[pg.K_w]:
            self.vel_y = p_speed * -1
        elif keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel_y = p_speed 
            

    def move(self, del_x=0, del_y=0):
        if not self.wallCollide(del_x, del_y):
            self.pos_x += del_x
            self.pos_y += del_y

    def wallCollide(self, del_x = 0, del_y = 0):
        for wall in self.gameScene.objects.groupWalls:
            if wall.x == self.pos_x + del_x and wall.y == self.pos_y + del_y:
                return True
        return False


    def update(self):
        self.controls()
        self.pos_x += self.vel_x * self.gameScene.del_t
        self.pos_y += self.vel_y * self.gameScene.del_t
        self.rect.topleft = (self.pos_x, self.pos_y)