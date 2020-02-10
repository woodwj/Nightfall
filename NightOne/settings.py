import pygame as pg
from random import randint
vec = pg.math.Vector2
pg.font.init()

# colours
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
WHITE = (255,255,255)
BLACK = (0,0,0)
GREY = (65,65,65)
bgColour = GREY
# screen Settings
s_screenWidth = 800
s_screenHeight = 500
s_FPS = 120
s_title = "NightOne"
s_tileSize = 48
s_font = pg.font.SysFont('Consolas', 28)
# tile setting #
t_weight = s_tileSize
# camera setting
c_speed = 0.05
# sprite settings
sp_scale = 2
sp_colratio = 0.8
sp_colScale = sp_colratio * sp_scale
# player settings
p_speed = 300
p_collisionRect = pg.Rect(0, 0, int(s_tileSize*sp_colScale), int(s_tileSize*sp_colScale))
p_barrelOffset = vec(p_collisionRect.bottomright) *0.38
p_health = 1000
# bullet settings
guns = {
    "handgun":{
        "b_speed" : 650,
        "b_spread" : 2,
        "b_lifeTime" : 10000,
        "b_rate" : 200,
        "b_kickback" : 200,
        "b_damage": 100
        },

    "shotgun":{
        "b_speed" : 500,
        "b_spread" : 8,
        "b_lifeTime" : 10000,
        "b_rate" : 750,
        "b_kickback" : 500,
        "b_damage": 90
        },
        
    "rifle":{
        "b_speed" : 800,
        "b_spread" : 4,
        "b_lifeTime" : 10000,
        "b_rate" : 350,
        "b_kickback" : 300,
        "b_damage": 350
        }
}
# round settings
r_countdown = 10
# zombie settings
z_collisionRect = pg.Rect(0, 0, int(s_tileSize*sp_colScale), int(s_tileSize*sp_colScale))
z_speeds = [100,150,200,250]
z_health = 750
z_maxzombies = 30
z_damage = 100
z_radius = 100
# build mode settings
bMode = False
bm_objects = {
    "wood":{
        "health":500,
        "cost": 5
        },

    "plank":{
        "health":1000,
        "cost": 10
        },

    "stone":{
        "health":1500,
        "cost": 15
        },

    "brick":{
        "health":2000,
        "cost": 20
        },

    "concrete":{
        "health":2500,
        "cost": 25
        }
}
# animation settings
a_continious = ["meleeattack", "reload", "shoot"]
# custom events
e_MATERIALGAIN = pg.USEREVENT + 1
e_ROUNDSTART = pg.USEREVENT + 2
e_ROUNDCOUNTDOWN = pg.USEREVENT + 3
