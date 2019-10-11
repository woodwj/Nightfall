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
        returnStruct = []
        for path in baseDir.iterdir():
            if path.is_file():
                if isinstance(returnStruct, dict):
                    returnStruct = []
                img = pg.image.load(path._str).convert_alpha()
                img = pg.transform.scale(img, (self.gameScene.state.tileSize * 2, self.gameScene.state.tileSize *2))
                returnStruct.append(img)

            elif path.is_dir():
                if isinstance(returnStruct, list): 
                    returnStruct = {}
                returnStruct[path.stem] =  self.ripArt(path)

        return returnStruct 
        
            

