import pygame as pg
from random import randint
vec = pg.math.Vector2
pg.font.init()

# colours
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
WHITE = (255,255,255)
BLACK = (0,0,0)
GREY = (65,65,65)
bgColour = GREY

# Screen Settings
s_screenWidth = 800
s_screenHeight = 500
s_FPS = 120
s_title = "NightOne"
s_tileSize = 48
s_font = pg.font.SysFont('Consolas', 30)

# sprite settings
sp_scale = 2
sp_colratio = 0.75
sp_colScale = sp_colratio * sp_scale

# player settings
p_speed = 300
p_collisionRect = pg.Rect(0, 0, int(s_tileSize*sp_colScale), int(s_tileSize*sp_colScale))
p_weapon = "handgun"
p_action = "idle"
p_barrelOffset = vec(p_collisionRect.bottomright) *0.375
p_health = 500

# bullet settings
guns = {
    "handgun":{
        "b_speed" : 800,
        "b_spread" : 2,
        "b_lifeTime" : 10000,
        "b_rate" : 200,
        "b_kickback" : 200,
        "b_damage": 100
        },

    "shotgun":{
        "b_speed" : 800,
        "b_spread" : 8,
        "b_lifeTime" : 10000,
        "b_rate" : 700,
        "b_kickback" : 500,
        "b_damage": 100
        },
        
    "rifle":{
        "b_speed" : 800,
        "b_spread" : 4,
        "b_lifeTime" : 10000,
        "b_rate" : 300,
        "b_kickback" : 300,
        "b_damage": 250
        }
}

# round settings
r_countdown = 15
# zombie settings
z_collisionRect = pg.Rect(0, 0, int(s_tileSize*sp_colScale), int(s_tileSize*sp_colScale))
z_speed = 200
z_action = "idle"
z_range = [400,700]
z_health = 500
z_maxzombies = 30
z_damage = 50

# build mode settings
bMode = False
bm_objects = {
    "wood":{
        "health":500,
        "cost": 10
        },

    "plank":{
        "health":1000,
        "cost": 25
        },

    "stone":{
        "health":1500,
        "cost":50
        },

    "brick":{
        "health":2000,
        "cost": 75
        },

    "concrete":{
        "health":2500,
        "cost": 100
        }
}
# custom events
e_MATERIALGAIN = pg.USEREVENT + 1
e_ROUNDSTART = pg.USEREVENT + 2
e_ROUNDCOUNTDOWN = pg.USEREVENT + 3

