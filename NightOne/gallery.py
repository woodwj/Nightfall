import pygame as pg 
import pathlib
from pathlib import Path

class gallery():
    def __init__(self, gameState):
        self.gameState = gameState
        self.artFolder = pathlib.Path.cwd() / "art"
        self.art = self.ripArt(self.artFolder)
    def ripArt(self,baseDir):
        returnStruct = {}
        for path in baseDir.iterdir():
            if path.is_file():
                img = pg.image.load(path._str).convert_alpha()
                if path.stem == "c" or path.stem == "def":
                    img = pg.transform.scale(img, (self.gameState.tileSize, self.gameState.tileSize))
                elif path.stem == "v":
                    img = pg.transform.scale(img, (int(self.gameState.tileSize*0.3), self.gameState.tileSize))    
                else:
                    img = pg.transform.scale(img, (int(self.gameState.tileSize * settings.sp_scale), int(self.gameState.tileSize *settings.sp_scale)))
                returnStruct[path.stem] = (img)
            elif path.is_dir():
                returnStruct[path.stem] = self.ripArt(path)
        return returnStruct

