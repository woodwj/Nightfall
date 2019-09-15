import pygame as pg
import pathlib
from pathlib import Path


class animator():
    def __init__(self, actortype):
        
        self.baseFolder = pathlib.Path.cwd()
        self.actorFolder = self.baseFolder / "art" / actortype
        
    def newAction(self, weapon, action ,speed = 1):
        self.animList = []
        
        actionFolder = Path(self.actorFolder / weapon / action)
        for path in actionFolder.iterdir():
            # because path is object not string
            self.animList.append(str(path))

    #def update(self, actor)

