import pygame as pg
import pathlib
from random import randint
from pathlib import Path


class animator():
    def __init__(self, gallery, actorType):
        
        self.actorType = actorType
        self.actorDict = gallery.art[self.actorType]

        self.displayedTime = pg.time.get_ticks()
        self.animCount = 0
        self.animSpeed = 1000
        self.animDirection = "up"
        self.animChange = False
        
    def newAction(self, action = None, weapon = None):
        
        self.animList = []
        self.animCount = 0
        if weapon is None:
            self.animList = self.actorDict[action]
        elif action is None:
            self.animList = self.actorDict[weapon]
        else:
            self.animList = self.actorDict[weapon][action]

        self.animImg = self.animList[self.animCount]
        self.animLength = len(self.animList)
        
        if action == "shoot":
            self.animSpeed = 200 // self.animLength
        elif action == "move":
            self.animCount = randint(0,self.animLength-1)
            self.animSpeed = 1500 // self.animLength
        elif action == "idle":
            self.animSpeed = 2000 // self.animLength
        elif action == "reload":
            self.animSpeed = 800 // self.animLength
        elif action == "meleeattack":
            self.animSpeed = 1000 // self.animLength

        self.animImg = self.animList[self.animCount]


    def update(self):
        now = pg.time.get_ticks()
        if now - self.displayedTime > self.animSpeed:
            self.displayedTime = now
            self.animChange = True
        else:
            self.animChange = False

        if self.animChange:    
            if self.animDirection == "up" and self.animCount < self.animLength-1:
                self.animCount += 1
            else:
               self.animDirection = "down"     
            if self.animDirection == "down" and self.animCount > 0 :
               self.animCount -= 1
            else:
               self.animDirection = "up"
        
        self.animImg = self.animList[self.animCount]
        