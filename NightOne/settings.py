import pygame as pg
vec = pg.math.Vector2

# colours
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
WHITE = (255,255,255)
BLACK = (0,0,0)
GREY = (65,65,65)
bgColour = GREY

# Screen Settings
s_screenWidth = 1980
s_screenHeight = 1080
s_halfWidth = int(s_screenWidth * 0.5)
s_halfHeight = int(s_screenHeight * 0.5)
s_FPS = 60
s_title = "NightOne"
s_tileSize = 48
s_gridWidth = int(s_screenWidth/s_tileSize)
s_gridHeight = int(s_screenHeight/s_tileSize)

# sprite settings
sp_scale = 2
sp_colratio = 0.75
sp_colScale = sp_colratio * sp_scale

# player settings
p_speed = 300
p_collisionRect = pg.Rect(0, 0, int(s_tileSize*sp_colScale), int(s_tileSize*sp_colScale))
#p_image = "survivor-move_handgun_0.png"
p_weapon = "handgun"
p_action = "idle"
#p_barrelOffset = vec(int(s_tileSize*0.5), int(p_collisionRect.height*0.5))
p_barrelOffset = vec(p_collisionRect.bottomright) *0.4

# bullet settings
guns = {
    "handgun":{
        "b_speed" : 400,
        "b_spread" : 5,
        "b_lifeTime" : 10000,
        "b_rate" : 200,
        "b_kickback" : 200},

    "shotgun":{
        "b_speed" : 250,
        "b_spread" : 45,
        "b_lifeTime" : 10000,
        "b_rate" : 700,
        "b_kickback" : 500},
        
    "rifle":{
        "b_speed" : 400,
        "b_spread" : 5,
        "b_lifeTime" : 10000,
        "b_rate" : 300,
        "b_kickback" : 300}
}


# zombie settings
z_collisionRect = pg.Rect(0, 0, int(s_tileSize*sp_colScale), int(s_tileSize*sp_colScale))
z_speed = 100
z_action = "idle"

#camera settings
c_speed = 500
c_screenRect = pg.Rect(0,0, s_screenWidth, s_screenHeight)
c_moveRect = pg.Rect(0,0, int(s_screenWidth/2), int(s_screenHeight/2))
c_boundryWidth = int(s_screenWidth/4)
c_boundryHeight = int(s_screenHeight/4)
c_returnWidth = 0
c_returnHeight = 0

