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
        
    def newAction(self, action, weapon = None):
        
        self.animList = []
        if self.actorType == "player":
            actionFolder = Path(self.actorFolder / weapon / action)
        elif self.actorType =="zombie":
            actionFolder = Path(self.actorFolder / action)
        elif self.actorType == "bullet":
            actionFolder = Path(self.actorFolder / weapon)

        for path in actionFolder.iterdir():
            # because path is object not string
            self.animList.append(str(path))

    def update(self, actor):
        now = pg.time.get_ticks()
        if now - self.displayedTime > self.animSpeed:
            print("ijunk")