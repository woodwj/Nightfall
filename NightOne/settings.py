import pygame as pg

# colours
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
WHITE = (255,255,255)
BLACK = (0,0,0)

bgColour = BLACK

# Screen Settings
s_screenWidth = 1920
s_screenHeight = 1080
s_FPS = 120
s_title = "NightOne"
s_tileSize = 48
s_gridWidth = int(s_screenWidth/s_tileSize)
s_gridHeight = int(s_screenHeight/s_tileSize)

# player settings
p_speed = 300
p_collisionRect = pg.Rect(0, 0, int(s_tileSize*1.5), int(s_tileSize*1.5))
p_image = "survivor-move_handgun_0.png"
p_weapon = "handgun"
p_action = "move"

#camera settings
c_speed = 400
c_boundryWidth = int(s_screenWidth/4)
c_boundryHeight = int(s_screenHeight/4)
c_returnWidth = 0
c_returnHeight = 0





