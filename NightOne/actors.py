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
    def __init__(self, gameScene, topLeft):
        self.groups = gameScene.objects.groupAll
        super().__init__(gameScene, self.groups, topLeft = topLeft)
        # image #
        self.animator = animations.animator(self.gameScene.state.gallery, "player")
        self.animator.newAction(settings.p_action, settings.p_weapon)
        self.changeImg()
        self.col_rect = settings.p_collisionRect
        # movement #
        self.moveType = "dynamic"
        self.vel =self.screenPos = vec(0,0) 
        # gameplay #
        self.action, self.weapon = settings.p_action, settings.p_weapon
        self.last_shot = 0
        # player settings #
        self.health = settings.p_health
        self.actorType = "player"
    
    # controls: movements, actions #
    def controls(self):
        # refresh keys, mousePos,mousePresses #
        actionNew, weaponNew = self.action, self.weapon
        self.mousePressed = self.gameScene.mousePressed
        self.mousePos = self.gameScene.mousePos
        self.keys = self.gameScene.keys
        # movement #
        self.vel = vec(0,0)    
        if self.keys[pg.K_LEFT] or self.keys[pg.K_a]:
            self.vel.x += settings.p_speed * -1
        elif self.keys[pg.K_RIGHT] or self.keys[pg.K_d]:
            self.vel.x += settings.p_speed
        if self.keys[pg.K_UP] or self.keys[pg.K_w]:
            self.vel.y += settings.p_speed * -1
        elif self.keys[pg.K_DOWN] or self.keys[pg.K_s]:
            self.vel.y += settings.p_speed
            
        # no move: anim ~> idle #
        if self.vel == (0,0):
            actionNew = "idle"
        else:# move: anim ~> move #
            actionNew = "move"
            # bi-move: pythag adjust #
            if self.vel.y !=0 and self.vel.x !=0:   
                self.vel *= 0.7071
        # actions #
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
        # shooting #
        if self.mousePressed[0]:
            # fire rate check
            now = pg.time.get_ticks()
            if now - self.last_shot > settings.guns[self.weapon]["b_rate"]:
                self.last_shot = now
                self.fire()
                actionNew = "shoot"
        # animations continious #
        change = False
        if actionNew != self.action or weaponNew != self.weapon:
            change = True
            if self.action == "shoot" or self.action == "reload" or self.action == "meleeattack":
                change = False
                if self.animator.animCount == self.animator.animLength-1:
                    change = True
        # animation change#
            if change:
                self.action = actionNew
                self.weapon = weaponNew
                self.animator.newAction(self.action, self.weapon)

    # rotate towards the mouse
    def rotate(self, angle = None):
        if angle == None:
            delPos = self.mousePos - self.screenPos
            angle = int(180 * -math.atan2(delPos.y, delPos.x) / math.pi)
        super().rotate(angle)
    
    # fire bullet from barrel towards mouse
    def fire(self):
        # direction to mouse
        direction = vec(1,0).rotate(-self.angle)
        position = self.pos + settings.p_barrelOffset.rotate(-self.angle)
        # shotgun burst
        if self.weapon == "shotgun":
            for burst in range(0,5):
                Bullet(self.gameScene, position, direction, self.angle, self.weapon)
        # carbine bullets        
        else: Bullet(self.gameScene, position, direction, self.angle, self.weapon)
        self.vel += vec(-1*settings.guns[self.weapon]["b_kickback"], 0).rotate(-self.angle)

    def update(self):
        self.controls()
        self.animator.update()
        if self.animator.animChange:
            self.changeImg()
        super().update()
        self.rotate()

class Bullet(tileSprite.tileSprite):
    def __init__(self, gameScene, pos, direction, angle, weapon):
        self.groups = gameScene.objects.groupAll, gameScene.objects.groupBullets
        super().__init__(gameScene, self.groups, center=pos)
        # gameplay #
        self.weapon = weapon
        self.spawn_time = pg.time.get_ticks()
        self.damage = settings.guns[self.weapon]["b_damage"]
        self.kickback = settings.guns[self.weapon]["b_kickback"]
        self.actorType = "bullet"
        self.moveType = "dynamic"
        # movement #
        spread = randint(-settings.guns[self.weapon]["b_spread"], settings.guns[self.weapon]["b_spread"])
        self.vel = direction.rotate(spread) * settings.guns[self.weapon]["b_speed"]
        self.angle = angle + spread
        # image #
        self.animator = animations.animator(self.gameScene.state.gallery,"bullet")
        self.animator.newAction(weapon = self.weapon)
        self.image = self.ogImage = pg.transform.scale(self.animator.animImg, (int(self.gameScene.state.tileSize*0.7),int(self.gameScene.state.tileSize*0.3)))
        self.rotate(self.angle)    
        
    def update(self):
        self.moveDist = self.vel * self.gameScene.state.del_t
        super().move()
        # lived life ~> kill #
        if pg.time.get_ticks() - self.spawn_time > settings.guns[self.weapon]["b_lifeTime"]:
            self.kill()
        
class zombie(tileSprite.tileSprite):
    def __init__(self, gameScene, topLeft):
        self.groups = [gameScene.objects.groupAll, gameScene.objects.groupZombies]
        super().__init__(gameScene, self.groups, topLeft = topLeft)

        self.animator = animations.animator(self.gameScene.state.gallery,"zombie")
        self.animator.newAction("idle")
        self.action = "idle"
        self.changeImg()

        self.rect = self.image.get_rect(topleft = self.pos)
        self.col_rect = settings.z_collisionRect.copy()
        self.col_rect.center = self.rect.center

        self.attack = False
        self.range = randint(settings.z_range[0],settings.z_range[1])
        self.rotate(self.range)
        self.health = settings.z_health
        self.damage = settings.z_damage
        self.actorType = "zombie"
        self.moveType = "dynamic"   
        
   
    def rotate(self, angle = None):
        if angle == None: angle = (self.gameScene.objects.player.pos - self.pos).angle_to(vec(1, 0))
        super().rotate(angle)
    

    def chase(self):
        self.actionNew = "idle"
        self.vel = vec(0,0)
    # x axis
        # left ~> right #
        if self.col_rect.right < self.gameScene.objects.player.col_rect.left:
            self.vel.x = settings.z_speed
            self.actionNew = "move"
        # right ~> left #    
        elif self.col_rect.left > self.gameScene.objects.player.col_rect.right:
            self.vel.x = settings.z_speed * -1
            self.actionNew = "move"

    # y axis
        # up ~> down #
        if self.col_rect.bottom < self.gameScene.objects.player.col_rect.top:
            self.vel.y = settings.z_speed
            self.actionNew = "move"
        # down ~> up #
        elif self.col_rect.top < self.gameScene.objects.player.col_rect.bottom:
            self.vel.y = settings.z_speed * -1
            self.actionNew = "move"
        
        
        if self.vel.y !=0 and self.vel.x !=0:
            self.vel *= 0.7071
            self.vel = vec(int(self.vel.x), int(self.vel.y))

                           

    def controls(self):

        self.actionNew = "idle"        
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

        self.controls()
        super().update()
        
            

        