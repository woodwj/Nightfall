import pygame as pg
from settings import *

def draw_Grid(gameState):
        for x in range(0, gameState.state._width, tileSize):
            pg.draw.line(gameState.state.screen, WHITE, (x, 0), (x, gameState.state._height))
        for y in range(0, gameState.state._height, tileSize):
            pg.draw.line(gameState.state.screen, WHITE, (0, y), (gameState.state._width, y))