import pygame as pg
import pathlib
import settings
from random import randint
from pathlib import Path


class animator():
    def __init__(self, gallery, actorType):

        self.actorType = actorType
        self.actorDict = gallery.art[self.actorType]
        self.displayedTime = pg.time.get_ticks()
        self.animCount = 0
        self.animLenght = 0
        self.animSpeed = 1000
        self.nextChange = False
        
    def changeAnim(self, action = None, weapon = None):

        self.animList = []
        self.animCount = 0
        if weapon is None:
            self.animDict = self.actorDict[action]
        elif action is None:
            self.animDict = self.actorDict[weapon]
        else:
            self.animDict = self.actorDict[weapon][action]
        
        for key in self.animDict:
            value = self.animDict[key]
            self.animList.append(value)
        self.animLength = len(self.animList)
        
        if action == "shoot":
            self.animSpeed = 200 // self.animLength
        elif action == "move":
            #self.animCount = randint(0,self.animLength-1)
            self.animSpeed = 1500 // self.animLength
        elif action == "idle":
            self.animSpeed = 2000 // self.animLength
        elif action == "reload":
            self.animSpeed = 800 // self.animLength
        elif action == "meleeattack":
            self.animSpeed = 1000 // self.animLength

        self.animImg = self.animList[self.animCount]

    def update(self):
        self.nextChange = False
        now = pg.time.get_ticks()
        if now - self.displayedTime > self.animSpeed:
            self.displayedTime = now
            self.animCount = (self.animCount + 1) % self.animLength 
            self.animImg = self.animList[self.animCount]
            self.nextChange = True     
        