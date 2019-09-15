import pygame as pg
import pathlib
from pathlib import Path


class animator():
    def __init__(self, actorType):
        
        self.actorType = actorType
        self.baseFolder = pathlib.Path.cwd()
        self.actorFolder = self.baseFolder / "art" / self.actorType
        
    def newAction(self, action, weapon = None):
        self.animList = []
        
        if self.actorType == "player":
            actionFolder = Path(self.actorFolder / weapon / action)
        else:
            actionFolder = Path(self.actorFolder / action)

        for path in actionFolder.iterdir():
            # because path is object not string
            self.animList.append(str(path))

    #def update(self, actor)

