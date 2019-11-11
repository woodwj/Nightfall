import pygame as pg 
import pathlib
from pathlib import Path

class gallery():
    def __init__(self, gameScene):
        self.gameScene = gameScene
        self.baseFolder = pathlib.Path.cwd()
        self.artFolder = self.baseFolder / "art"
        self.art = self.ripArt(self.artFolder)
        
    def ripArt(self,baseDir):
        returnStruct = {}
        for path in baseDir.iterdir():
            if path.is_file():
                img = pg.image.load(path._str).convert_alpha()
                if path.stem == "c" or path.stem == "def":
                    img = pg.transform.scale(img, (self.gameScene.state.tileSize, self.gameScene.state.tileSize))
                elif path.stem == "v":
                    img = pg.transform.scale(img, (int(self.gameScene.state.tileSize*0.3), self.gameScene.state.tileSize))    
                else:
                    img = pg.transform.scale(img, (self.gameScene.state.tileSize * 2, self.gameScene.state.tileSize *2))
                returnStruct[path.stem] = (img)
            elif path.is_dir():
                returnStruct[path.stem] =  self.ripArt(path)

        return returnStruct

