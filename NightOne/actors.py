import pygame as pg
import utils
import math
import pathlib
import animations
import settings
import tileSprite
from random import uniform,randint

vec = pg.math.Vector2

class player(tileSprite.tileSprite):
    def __init__(self, gameScene, tile_x, tile_y):

        # for faster coding save to local variable and acess in other class functions
        self.gameScene = gameScene
        # only want player in all sprites group
        self.groups = self.gameScene.objects.groupAll
        # initilize the super with desired groups
        super().__init__(self.gameScene, tile_x, tile_y, self.groups)
        
        # player image
        self.animator = animations.animator(self.gameScene.state.gallery, "player")
        self.animator.newAction(settings.p_action, settings.p_weapon)
        self.imgFile = self.animator.animList[0]
        self.changeImg()
        self.col_rect = settings.p_collisionRect
        # player location
        self.vel = vec(0,0)
        self.pos = vec(tile_x,tile_y)*self.gameScene.state.tileSize
        self.angle = 0
        self.screenPos = vec(0,0)
        # action and weapon settings
        self.action, self.weapon = settings.p_action, settings.p_weapon
        self.weapons = ["handgun", "rifle","shotgun"]
        self.weaponIndex = 0
        self.last_shot = 0
        # player settings
        self.health = settings.p_health
        self.type = "player"
    
    # controls method here for 2 reasons 1) code on main is relevent to main 2) player is self contained and modular
    def controls(self):
        # velocity in both axis set to 0
        self.vel = vec(0,0)
        actionNew, weaponNew = self.action, self.weapon
        self.mouse_pressed = self.gameScene.mouse_pressed
        self.mouse_pos = self.gameScene.mouse_pos
        self.keys = self.gameScene.keys

        # code for keyboard controls    
        if self.keys[pg.K_LEFT] or self.keys[pg.K_a]:
            self.vel.x += settings.p_speed * -1   
        elif self.keys[pg.K_RIGHT] or self.keys[pg.K_d]:
            self.vel.x += settings.p_speed     
        if self.keys[pg.K_UP] or self.keys[pg.K_w]:
            self.vel.y += settings.p_speed * -1 
        elif self.keys[pg.K_DOWN] or self.keys[pg.K_s]:
            self.vel.y += settings.p_speed
        if self.vel.y == 0 and self.vel.x ==0:
            actionNew = "idle"
        else:
            if self.vel.y !=0 and self.vel.x !=0:   
                self.vel *= 0.7071
                self.vel = vec(int(self.vel.x), int(self.vel.y))
            actionNew = "move"
        
        # keyboard controls for actions
        if self.keys[pg.K_1]:
            weaponNew = "handgun"
        elif self.keys[pg.K_2]:
            weaponNew = "rifle"
        elif self.keys[pg.K_3]:
            weaponNew = "shotgun"
        elif self.keys[pg.K_r]:
            actionNew = "reload"
        elif self.keys[pg.K_v]:
            actionNew = "meleeattack"
        
        
        # code to deal with shooting
        if self.mouse_pressed[0] :
            now = pg.time.get_ticks()
            if now - self.last_shot > settings.guns[self.weapon]["b_rate"]:
                self.last_shot = now
                direction = vec(1, 0).rotate(-self.angle)
                pos = self.pos + settings.p_barrelOffset.rotate(-self.angle)

                if self.weapon == "shotgun":
                    for b in range(-settings.guns[self.weapon]["b_kickback"],settings.guns[self.weapon]["b_kickback"], 100):
                        Bullet(self.gameScene, pos, direction, self.angle, "handgun")
                else:
                    Bullet(self.gameScene, pos, direction, self.angle, "handgun")
                self.vel += vec(-1*settings.guns[self.weapon]["b_kickback"], 0).rotate(-self.angle)
                actionNew = "shoot"
        
        # code to make shooting, reloading and melee continious
        change = False
        if actionNew != self.action or weaponNew != self.weapon:
            change = True
            if self.action == "shoot" or self.action == "reload" or self.action == "meleeattack":
                change = False
                if self.animator.animCount == self.animator.animLength-1:
                    change = True

            if change:
                self.action = actionNew
                self.weapon = weaponNew
                self.animator.newAction(self.action, self.weapon)

    # rotate towards the mouse
    def rotate(self):
        
        delPos = vec(self.mouse_pos) - self.screenPos
        self.angle = (180 / math.pi) * -math.atan2(delPos.y, delPos.x)
        self.image = pg.transform.rotate(self.ogImage, int(self.angle))
        self.rect = self.image.get_rect(center=self.pos)

    #def events(self):  

    # player update funciton - called every gameloop
    def update(self):
        self.controls()
        self.animator.update()
        if self.animator.animChange:
            self.changeImg()
        
        
        # change in x and y is calculated off velocity and the change in time
        super().update()
        self.rotate()
        
        
class Bullet(pg.sprite.Sprite):
    def __init__(self, gameScene, pos, direction, angle, weapon):
        self.groups = gameScene.objects.groupAll, gameScene.objects.groupBullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.gameScene = gameScene
        self.weapon = weapon
        self.angle = angle
        
        spread = uniform(-settings.guns[self.weapon]["b_spread"], settings.guns[self.weapon]["b_spread"])
        self.vel = direction.rotate(spread) * settings.guns[self.weapon]["b_speed"]
        self.animator = animations.animator(self.gameScene.state.gallery,"bullet")
        self.animator.newAction(weapon = weapon)
        self.image = self.animator.animImg
        self.image = pg.transform.scale(self.image, (int(self.gameScene.state.tileSize*0.7),int(self.gameScene.state.tileSize*0.5)))
        self.image = pg.transform.rotate(self.image, angle + spread)
        self.ogImage = self.image

        self.pos = vec(pos)
        self.rect = self.image.get_rect(center=self.pos)
        self.col_rect = self.rect
        self.rect.center = self.pos
        self.spawn_time = pg.time.get_ticks()

        self.damage = settings.guns[self.weapon]["b_damage"]
        self.kickback = settings.guns[self.weapon]["b_kickback"]
        self.type = "bullet"

    def update(self):
        self.pos += self.vel * self.gameScene.state.del_t
        self.rect.center = self.pos
        self.col_rect.center = self.rect.center
        if pg.time.get_ticks() - self.spawn_time > settings.guns[self.weapon]["b_lifeTime"]:
            self.kill()


class zombie(tileSprite.tileSprite):
    def __init__(self, gameScene, tile_x, tile_y):

        # for faster coding save to local variable and acess in other class functions
        self.groups = gameScene.objects.groupAll, gameScene.objects.groupZombies, gameScene.objects.groupDestructable
        super().__init__(gameScene, tile_x, tile_y, self.groups)

        self.action = "idle"
        self.animator = animations.animator(self.gameScene.state.gallery,"zombie")
        self.animator.newAction(self.action)
        self.changeImg()
        self.ogImage = self.image

        self.rect = self.image.get_rect(topleft = self.pos)
        self.col_rect = settings.z_collisionRect.copy()
        self.col_rect.center = self.rect.center

        self.attack = False
        self.vel = vec(0,0)
        self.range = randint(settings.z_range[0],settings.z_range[1])
        self.rotate(self.range)
        self.health = settings.z_health
        self.damage = settings.z_damage
        self.type = "zombie"    
        
   
    def rotate(self, angle = None):
        if angle == None:
            angle = (self.gameScene.objects.player.pos - self.pos).angle_to(vec(1, 0))
        self.angle = angle
        self.image = pg.transform.rotate(self.ogImage, self.angle)
        self.rect = self.image.get_rect(center = self.pos)
        self.col_rect.center = self.rect.center
    
    def chase(self):
        # x axis
        if self.col_rect.x < self.gameScene.objects.player.rect.centerx:
            self.vel.x = settings.z_speed
        elif self.col_rect.x > self.gameScene.objects.player.rect.centerx:
            self.vel.x = settings.z_speed * -1
        # y axis
        if self.col_rect.y < self.gameScene.objects.player.rect.centery:
            self.vel.y = settings.z_speed
        elif self.col_rect.y > self.gameScene.objects.player.rect.centery:
            self.vel.y = settings.z_speed * -1
        
        if self.vel.y !=0 and self.vel.x !=0:
            self.vel *= 0.7071
            self.vel = vec(int(self.vel.x), int(self.vel.y))

        self.actionNew = "move"                   

    def detect(self):
        
        self.actionNew = "move" 
        self.chase()
        self.rotate()
    
        change = False
        if self.actionNew != self.action:
            change = True
            if self.action == "meleeattack":
                change = False
                if self.animator.animCount == self.animator.animLength-1:
                    change = True
                    
        if change:
            self.action = self.actionNew
            self.animator.newAction(self.action)

    def update(self):
        
        self.animator.update()
        if self.animator.animChange:
            self.changeImg()

        self.detect()
        super().update()
        
            

        