import pygame as pg
import tileSprite
import environments
import animations
import settings

vec = pg.math.Vector2

def collideDetect(sprite1,sprite2):
        return sprite1.rect.colliderect(sprite2.rect)

class buildMode(tileSprite.tileSprite):
    def __init__(self, gameScene):

        self.gameScene = gameScene
        self.screenPos = vec(5,5)
        self.pos = vec(0,0)
        super().__init__(self.gameScene, self.screenPos.x, self.screenPos.y)
        self.animator = animations.animator(self.gameScene.state.gallery,"wall")
        self.materials = ["wood","plank","stone","brick","concrete"]
        self.materialIndex = 0
        self.material = self.materials[self.materialIndex]
        self.angle = 0
        self.tilesize =  vec(self.gameScene.state.tileSize, self.gameScene.state.tileSize)
        self.scrap = 0

        self.animator.newAction(self.material)
        self.changeImg()
        self.ogImage = self.image 
        self.delay = pg.time.get_ticks()
        
    def start(self):

        self.rect.topleft = self.gameScene.objects.player.col_rect.topleft
        self.col_rect = self.rect
    
    def end(self):

        self.gameScene.state.FPS = settings.s_FPS

    def controls(self):

        
        # code for keyboard controls
        if self.keys[pg.K_UP]:
            #self.animator.animCount = min(0,min(self.animator.animCount+1,self.animator.animLength-1) - self.animator.animLength-1) * -1
            self.animator.animCount = (self.animator.animCount + 1) % self.animator.animLength
            self.animator.animImg = self.animator.animList[self.animator.animCount]
            self.changeImg() 
            self.rotate()

        elif self.keys[pg.K_DOWN]:
            self.animator.animCount = (self.animator.animCount -1) % self.animator.animLength
            self.animator.animImg = self.animator.animList[self.animator.animCount]
            self.changeImg()
            self.rotate()

        elif self.keys[pg.K_RIGHT]:
            self.materialIndex = (self.materialIndex +1) % len(self.materials)
            self.material = self.materials[self.materialIndex]
            self.animator.newAction(self.material)
            self.changeImg()
            self.rotate() 

        elif self.keys[pg.K_LEFT]:
            self.materialIndex = (self.materialIndex - 1) % len(self.materials)
            self.material = self.materials[self.materialIndex]
            self.animator.newAction(self.material)
            self.changeImg()
            self.rotate()

        elif self.keys[pg.K_r]:
            self.angle = (self.angle + 90) % 360
            self.rotate()     

                        
    def update(self):

        self.keys = self.gameScene.keys
        self.mousePressed = self.gameScene.mouse_pressed
        self.mousePos = vec(self.gameScene.mouse_pos)

        self.pos = self.gameScene.camera.get_pos(self.mousePos)
        self.tile = vec((self.pos.x // self.gameScene.state.tileSize),(self.pos.y // self.gameScene.state.tileSize))
        self.pos = self.tile * self.gameScene.state.tileSize
        if self.angle < 180:
            self.rect.topleft = self.pos
        else:
            self.rect.bottomright = self.pos + self.tilesize
        self.col_rect = self.rect
        realpos = self.col_rect.topleft
       
        hits = pg.sprite.spritecollide(self, self.gameScene.objects.groupAll, False, collideDetect)
        if self.mousePressed[0] and not hits and self.scrap - settings.bm_objects[self.material]["cost"] >= 0:    
            environments.wall(self.gameScene,self.tile.x,self.tile.y,self.image,self.material,realpos)
            self.scrap -= settings.bm_objects[self.material]["cost"]
            self.gameScene.scrapTxt = "SCRAP: " + str(self.scrap)

        if self.mousePressed[2] and hits:
            if hits[0].type == "wall":
                hits[0].kill()

        now = pg.time.get_ticks()
        if now - self.delay > 150:
            self.delay = now
            self.controls()
