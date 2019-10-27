import pygame as pg
import utils
import math
import pathlib
import animations
import settings
import tileSprite
from random import uniform

vec = pg.math.Vector2

class player(tileSprite.tileSprite):
    def __init__(self, gameScene, tile_x, tile_y):

        # for faster coding save to local variable and acess in other class functions
        self.gameScene = gameScene
        # only want player in all sprites group
        self.groups = self.gameScene.objects.groupAll
        super().__init__(self.gameScene, tile_x, tile_y, self.groups)     
        # initilize the super with desired groups
        
        self.animator = animations.animator(self.gameScene.state.gallery, "player")
        self.animator.newAction(settings.p_action, settings.p_weapon)
        self.imgFile = self.animator.animList[0]
        self.changeImg()
        self.col_rect = settings.p_collisionRect
        self.vel = vec(0,0)
        self.pos = vec(tile_x,tile_y)*self.gameScene.state.tileSize
        self.screenPos = vec(0,0)
        
        self.action, self.weapon = settings.p_action, settings.p_weapon
        self.weapons = ["handgun", "rifle","shotgun"]
        self.weaponIndex = 0
        self.last_shot = 0
    
    # controls method here for 2 reasons 1) code on main is relevent to main 2) player is self contained and modular
    def controls(self):
        # velocity in both axis set to 0
        self.vel = vec(0,0)
        actionNew, weaponNew = self.action, self.weapon

        mouse_pressed = pg.mouse.get_pressed()
        keys = pg.key.get_pressed()    
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel.x += settings.p_speed * -1   
        elif keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel.x += settings.p_speed     
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel.y += settings.p_speed * -1 
        elif keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel.y += settings.p_speed
        
        if keys[pg.K_1]:
            weaponNew = "handgun"
        if keys[pg.K_2]:
            weaponNew = "rifle"
        if keys[pg.K_3]:
            weaponNew = "shotgun"
        elif keys[pg.K_r]:
            actionNew = "reload"
        elif keys[pg.K_v]:
            actionNew = "meleeattack"
        elif keys[pg.K_b]:
            if state.bMODE:
                self.state.FPS = 0
            else:
                self.state.FPS = settings.s_FPS
        
        # code to deal with shooting
    
        if self.vel.y == 0 and self.vel.x == 0:
            actionNew = "idle"
        else:
            if self.vel.y !=0 and self.vel.x !=0:   
                self.vel *= 0.7071
                self.vel = vec(int(self.vel.x), int(self.vel.y))
            actionNew = "move"

        if mouse_pressed[0] :
            now = pg.time.get_ticks()
            if now - self.last_shot > settings.guns[self.weapon]["b_rate"]:
                self.last_shot = now
                actionNew = "shoot"
                direction = vec(1, 0).rotate(-self.angle)
                pos = self.pos + settings.p_barrelOffset.rotate(-self.angle)
                Bullet(self.gameScene, pos, direction, self.angle, "handgun")
                self.vel = vec(-1*settings.guns[self.weapon]["b_kickback"], 0).rotate(-self.angle)

        if actionNew != self.action or weaponNew != self.weapon:
            self.action = actionNew
            self.weapon = weaponNew
            self.animator.newAction(self.action, self.weapon)

    def rotate(self):
        mouse_pos = vec(pg.mouse.get_pos())
        dif_x, dif_y = mouse_pos.x+ - self.screenPos.x, mouse_pos.y + - self.screenPos.y
        self.angle = (180 / math.pi) * -math.atan2(dif_y, dif_x)
        self.image = pg.transform.rotate(self.ogImage, int(self.angle))
        self.rect = self.image.get_rect(center=self.pos)

    # player update funciton - called every gameloop
    def update(self):
        # check controls
        self.controls()
        self.animator.update()
        if self.animator.animChange:
            self.changeImg()
        self.rotate()
        # change in x and y is calculated off velocity and the change in time
        self.moveDist = self.vel * self.gameScene.state.del_t
        self.moveDist = vec(int(self.moveDist.x),int(self.moveDist.y))
        if self.moveDist.y !=0 or self.moveDist.x !=0:
            # performs movement
            self.move()
        #print(self.action,self.animator.animCount)

class Bullet(pg.sprite.Sprite):
    def __init__(self, gameScene, pos, direction, angle, weapon):
        self.groups = gameScene.objects.groupAll, gameScene.objects.groupBullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.gameScene = gameScene
        self.weapon = weapon
        self.pos = vec(pos)
        spread = uniform(-settings.guns[self.weapon]["b_spread"], settings.guns[self.weapon]["b_spread"])
        self.vel = direction.rotate(spread) * settings.guns[self.weapon]["b_speed"]
        self.animator = animations.animator(self.gameScene.state.gallery,"bullet")
        self.animator.newAction(weapon = weapon)
        self.image = self.animator.animList[0]
        self.image = pg.transform.scale( self.image, (int(self.gameScene.state.tileSize*0.7),int(self.gameScene.state.tileSize*0.5)))
        self.image = pg.transform.rotate(self.image, angle + spread)
        self.ogImage = self.image
        self.rect = self.image.get_rect(center=self.pos)
        self.rect.center = self.pos
        self.col_rect = self.rect
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        self.pos += self.vel * self.gameScene.state.del_t
        self.rect.center = self.pos
        self.col_rect = self.rect
        if pg.sprite.spritecollideany(self, self.gameScene.objects.groupWalls):
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > settings.guns[self.weapon]["b_lifeTime"]:
            self.kill()


class zombie(tileSprite.tileSprite):
    def __init__(self, gameScene, tile_x, tile_y):

        # for faster coding save to local variable and acess in other class functions
        self.gameScene = gameScene
        self.groups = gameScene.objects.groupAll, gameScene.objects.groupZombies
        super().__init__(self.gameScene, tile_x, tile_y, self.groups)

        self.gameScene = gameScene
        self.animator = animations.animator(self.gameScene.state.gallery,"zombie")
        self.action = "idle"
        self.animator.newAction(self.action)
        self.changeImg()
        self.rect = self.image.get_rect()
        self.ogImage = self.image
        self.pos = vec(tile_x, tile_y) * self.gameScene.state.tileSize
        self.vel = vec(0,0)
        self.rect.center = self.pos
        self.col_rect = settings.z_collisionRect.copy()
   
    def rotate(self):
        self.rot = (self.gameScene.objects.player.pos - self.pos).angle_to(vec(1, 0))
        self.image = pg.transform.rotate(self.ogImage, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
    
    def detect(self):
        self.vel = vec(0,0)
        # x axis
        if self.rect.x < self.gameScene.objects.player.rect.centerx:
            self.vel.x = settings.z_speed
        elif self.rect.x > self.gameScene.objects.player.rect.centerx:
            self.vel.x = settings.z_speed * -1
        # y axis
        if self.rect.y < self.gameScene.objects.player.rect.centery:
            self.vel.y = settings.z_speed
        elif self.rect.y > self.gameScene.objects.player.rect.centery:
            self.vel.y = settings.z_speed * -1
        
        if self.vel.y == 0 and self.vel.x ==0:
            actionNew = "idle"
        else:
            if self.vel.y !=0 and self.vel.x !=0:
                self.vel *= 0.7071
                self.vel = vec(int(self.vel.x), int(self.vel.y))
            actionNew = "move"
    
        if actionNew != self.action:
            self.action = actionNew
            self.animator.newAction(self.action)       

    def update(self):
        
        self.detect()
        self.animator.update()
        if self.animator.animChange:
            self.changeImg()
        self.rotate()
        self.moveDist = self.vel * self.gameScene.state.del_t
        if self.moveDist.x != 0 or self.moveDist.y !=0:
            self.move()