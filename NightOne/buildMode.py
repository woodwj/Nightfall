import pygame as pg
import tileSprite
import environments
import animations
import settings

vec = pg.math.Vector2

class buildMode(tileSprite.tileSprite):
    def __init__(self, gameScene):
        # init #
        self.screenPos = vec(0,0)
        super().__init__(gameScene, topLeft= self.screenPos)
        # image #
        self.animator = animations.animator(self.gameScene.state.gallery,"wall")
        self.materials = ["wood","plank","stone","brick","concrete"]
        self.materialIndex, self.materialLength = 0, len(self.materials)
        self.material = self.materials[self.materialIndex]
        self.animator.changeAnim(self.material)
        self.changeImg()
        self.angle = 0
        # rect management #
        self.tileSizeVec = vec(self.gameScene.state.tileSize,self.gameScene.state.tileSize)
        # gameplay #
        self.buildPoints = 1000
        self.delay = pg.time.get_ticks()

    def buttonControls(self):
        # building controls #
        change = False
        # navigate objects #
        objectChange = 0
        if self.keys[pg.K_UP] or self.keys[pg.K_w]:
            objectChange = 1
        elif self.keys[pg.K_DOWN] or self.keys[pg.K_s]:
            objectChange = -1
        if objectChange != 0:
            self.animator.animCount = (self.animator.animCount + objectChange) % self.animator.animLength
            change = True
        # rotate object #
        if self.keys[pg.K_r]:
            self.angle = (self.angle + 90) % 360
            change = True
        # navigate materials #
        materialChange = 0
        if self.keys[pg.K_RIGHT] or self.keys[pg.K_d]:
            materialChange = 1
        elif self.keys[pg.K_LEFT] or self.keys[pg.K_a]:
            materialChange = -1
        if materialChange !=0:
            self.materialIndex = (self.materialIndex + materialChange) % self.materialLength
            self.material = self.materials[self.materialIndex]
            self.animator.changeAnim(self.material)
            change = True
        if change: 
            self.changeImg()
            self.col_rect.topleft += self.tileSizeVec.rotate(self.angle)

    def mouseControls(self):
        # mousePos ~> tile placement #
        self.col_rect.topleft = self.maptoGrid(self.mouseScreenPos)
        self.rect.center = self.col_rect.center
        # wall placement and removal #
        newScrap = self.buildPoints - settings.bm_objects[self.material]["cost"]
        if self.mousePressed[0] and newScrap >= 0:
            hits = pg.sprite.spritecollide(self, self.gameScene.objects.groupAll, False, tileSprite.collideDetect)
            if len(hits) == 0:
                environments.playerWall(self.gameScene, self.col_rect.topleft, self.image, self.material)
                self.buildPoints = newScrap
                self.gameScene.graph.walls.append(self.maptoGrid(self.mousePos))
                self.gameScene.materialsTxt = "MATERIALS: " + str(self.buildPoints)
        elif self.mousePressed[2]:   
            hits = pg.sprite.spritecollide(self, self.gameScene.objects.groupAll, False, tileSprite.collideDetect)
            if len(hits)>0:
                for hit in hits:
                    if hit.actorType == "playerWall":
                        self.buildPoints += settings.bm_objects[hits[0].material]["cost"] // 2
                        self.gameScene.materialsTxt = "MATERIALS: " + str(self.buildPoints)
                        self.gameScene.graph.walls.remove(self.maptoGrid(self.mousePos))
                        hit.kill()

    def update(self):
        # refresh inputs #
        self.keys = self.gameScene.keys
        self.mousePressed = self.gameScene.mousePressed
        self.mousePos = self.gameScene.mousePos
        self.mouseScreenPos = self.gameScene.camera.reverseVec(self.mousePos)
        # mouse controls #
        self.mouseControls()
        # button control delay #
        now = pg.time.get_ticks()
        if now - self.delay > 200:
            self.delay = now
            self.buttonControls()
