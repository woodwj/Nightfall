import pygame as pg
import utils
import math
import pathlib
import animations
import settings
import tileSprite
import pathfinding
from random import uniform,randint,choice

vec = pg.math.Vector2

class player(tileSprite.tileSprite):
    def __init__(self, gameScene, topLeft):
        self.groups = gameScene.objects.groupAll
        super().__init__(gameScene, self.groups, topLeft = topLeft)
        # image #
        self.animator = animations.animator(self.gameScene.state.gallery, "player")
        self.animator.changeAnim("idle", "handgun")
        self.changeImg()
        self.col_rect = settings.p_collisionRect
        # movement #
        self.moveType = "dynamic"
        self.vel =self.screenPos = vec(0,0)
        self.speed = settings.p_speed
        # gameplay #
        self.action, self.weapon = "idle", "handgun"
        self.last_shot = 0
        # player settings #
        self.maxHealth = self.health = settings.p_health
        self.actorType = "player"
    
    # controls: movements, actions #
    def controls(self):
        # refresh keys, mousePos,mousePresses #
        self.actionNew, self.weaponNew = self.action, self.weapon
        self.mousePressed = self.gameScene.mousePressed
        self.mousePos = self.gameScene.mousePos
        self.keys = self.gameScene.keys
        # movement #
        self.vel = vec(0,0)    
        if self.keys[pg.K_LEFT] or self.keys[pg.K_a]:
            self.vel.x += -1
        elif self.keys[pg.K_RIGHT] or self.keys[pg.K_d]:
            self.vel.x += 1
        if self.keys[pg.K_UP] or self.keys[pg.K_w]:
            self.vel.y += -1
        elif self.keys[pg.K_DOWN] or self.keys[pg.K_s]:
            self.vel.y += 1
        # no move: anim ~> idle #
        if self.vel == vec(0,0): self.actionNew = "idle"
        else: self.vel = utils.intVec(self.vel.normalize() * self.speed)
            
        # actions #
        if self.keys[pg.K_1]:
            self.weaponNew = "handgun"
        elif self.keys[pg.K_2]:
            self.weaponNew = "rifle"
        elif self.keys[pg.K_3]:
            self.weaponNew = "shotgun"
        elif self.keys[pg.K_r]:
            self.actionNew = "reload"
        elif self.keys[pg.K_v]:
            self.actionNew = "meleeattack"
        # shooting #
        if self.mousePressed[0]:
            # fire rate check
            now = pg.time.get_ticks()
            if now - self.last_shot > settings.guns[self.weapon]["b_rate"]:
                self.last_shot = now
                self.fire()
                self.actionNew = "shoot"

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
        super().update()

        if self.checkAction(self.actionNew, self.weaponNew):
            # animation change
            self.action = self.actionNew
            self.weapon = self.weaponNew
            self.animator.changeAnim(self.action, self.weapon)

        self.animator.update()
        if self.animator.nextChange:
            self.changeImg()
        else: self.rotate()
        

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
        self.vel = utils.intVec(direction.rotate(spread) * settings.guns[self.weapon]["b_speed"])
        self.angle = angle + spread
        # image #
        self.animator = animations.animator(self.gameScene.state.gallery,"bullet")
        self.animator.changeAnim(weapon = self.weapon)
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
        # visuals #
        self.animator = animations.animator(self.gameScene.state.gallery,"zombie")
        self.animator.changeAnim("idle")
        self.action = "idle"
        self.changeImg()
        # movement #
        self.rect = self.image.get_rect(topleft = self.pos)
        self.col_rect = settings.z_collisionRect.copy()
        self.col_rect.center = self.rect.center
        self.moveType = "dynamic"
        self.speed = choice(settings.z_speeds)
        self.radius = settings.z_radius
        # pathfinding #
        self.tickPathCalc = 3000
        self.sincePathCalc = 0
        self.lastTarget = None
        target, start = self.maptoGrid(vec(self.gameScene.objects.player.col_rect.center)), self.maptoGrid(vec(self.col_rect.center))
        self.foundPath = pathfinding.a_star_algorithm(self.gameScene.graph, start, target)
        # gameplay #
        self.rotate()
        self.maxHealth = self.health = settings.z_health
        self.damage = settings.z_damage
        self.actorType = "zombie"
        
    def rotate(self, angle = None):
        if angle == None: angle = (self.gameScene.objects.player.pos - self.pos).angle_to(vec(1, 0))
        super().rotate(angle)
    
    def avoidMobs(self):
        for mob in self.gameScene.objects.groupZombies:
            if mob.ID != self.ID:
                dist = self.pos - mob.pos
                if 0 < dist.length() < self.radius:
                    self.vel += dist.normalize()

    def navPath(self, path, start, target):
        pos = target
        shortestPath = []
        while pos != start:
            currentNode = path.get(utils.tup(pos),None)
            if currentNode == None: break
            pos, move = currentNode["from"], -currentNode["direct"]
            shortestPath.append(move)
        shortestPath.reverse()
        return shortestPath

    def controls(self):
        self.vel = vec(0,0)
        shortestPath = []
        target = self.maptoGrid(vec(self.gameScene.objects.player.col_rect.center))
        if self.lastTarget == None: self.lastTarget = target
        start = self.maptoGrid(self.pos)
        now = pg.time.get_ticks()
        if now - self.sincePathCalc > self.tickPathCalc:
            self.sincePathCalc = now
            self.foundPath = pathfinding.a_star_algorithm(self.gameScene.graph, start, target)
        shortestPath = self.navPath(self.foundPath, start, self.lastTarget)
        if target != self.lastTarget:
            #shortestPath.append(utils.intVec(target - self.lastTarget))
            ret = pathfinding.a_star_algorithm(self.gameScene.graph, self.lastTarget, target)
            for key in ret:
                if self.foundPath.get(key,"allowed")=="allowed":
                    self.foundPath[key]= ret[key]
            
        if shortestPath == []: 
            self.vel = vec(0,0)
            self.actionNew = "idle"
        else: self.vel = utils.intVec(shortestPath[0].normalize() * self.speed)
    # pythag speed adjustment #
        self.actionNew = "move"
        self.vel = utils.intVec(self.vel)
        self.lastTarget = target

    def update(self):
        self.controls()
        self.rotate()
        self.avoidMobs()
        super().update()

        if self.checkAction(self.actionNew):
            self.action = self.actionNew
            self.animator.changeAnim(self.actionNew)
        self.animator.update()
        if self.animator.nextChange:
            self.changeImg()