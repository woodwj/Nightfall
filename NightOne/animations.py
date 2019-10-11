import pygame as pg
import pathlib
from pathlib import Path


class animator():
    def __init__(self, actorType):
        
        self.baseFolder = pathlib.Path.cwd()
        self.actorType = actorType
        self.animList = []        
        self.actorFolder = self.baseFolder / "art" / self.actorType
        self.displayedTime = pg.time.get_ticks()
        self.animCount = 0
        self.animSpeed = 1000
        self.animDirection = "up"
        self.animChange = False
        
    def newAction(self, action = None, weapon = None):
        
        self.animList = []
        self.animCount = 0
        if weapon is None:
            actionFolder = Path(self.actorFolder / action)
        elif action is None:
            actionFolder = Path(self.actorFolder / weapon)
        else:
            actionFolder = Path(self.actorFolder / weapon / action)

        for path in actionFolder.iterdir():
            # because path is object not string
            self.animList.append(str(path))
        self.animImg = self.animList[self.animCount]
        self.animLength = len(self.animList)
        if action == "shoot":
            self.animSpeed = 500 // self.animLength
        if action == "move":
            self.animSpeed = 2500 // self.animLength
        if action == "idle":
            self.animSpeed = 2500 // self.animLength

        self.animDir = self.animList[self.animCount]


    def update(self):
        now = pg.time.get_ticks()
        if now - self.displayedTime > self.animSpeed:
            self.displayedTime = now
            self.animChange = True
            if self.animDirection == "up" and self.animCount < self.animLength-1:
                self.animCount += 1
            else:
               self.animDirection = "down"     
            if self.animDirection == "down" and self.animCount > 0 :
               self.animCount -= 1
            else:
               self.animDirection = "up"
        else:
            self.animChange = False
        self.animDir = self.animList[self.animCount]
        