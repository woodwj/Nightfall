import pygame as py



class mApplication(py.sprite.Sprite):
    def __init__(self, settings_file, *arks, **kwargs):
        super.Super__init__(self)
        self.cfg = settings_file
