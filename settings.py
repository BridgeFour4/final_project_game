TITLE ="final_game"
WIDTH = 1000 # width of game window
HEIGHT = 480 # height of screen
FPS = 60 # frames
FONT_NAME = 'arial'

#player properties
PLAYER_ACC = 0.5
PLAYER_FRICTION= -0.12
PLAYER_GRAV=0.8
PLAYER_JUMP = 13

#bullet properties
LIGHNING_SPEED = 6
LIGHNING_DURATION = 45


PLAYER_LAYER = 2
PLATFORM_LAYER = 1

#Spawns
MOB_SPAWN = 1
LIFE_SPAWN = 2
POINT_SPAWN = 3
#platform lists
PLATFORM_LIST1=[(0,HEIGHT-50),
                (100, 400),
                (250, 400,MOB_SPAWN),
                (400, 380,),
                (550, 330,LIFE_SPAWN),
                (700, 440),
                (950, 440),
                (1150, 400,POINT_SPAWN),
                (1300, 380,POINT_SPAWN),
                (1450, 330),
                (1700, 330,MOB_SPAWN),
                (1800, 400),
                (1950, 400,MOB_SPAWN),
                (2100, 380),
                (2350, 330),
                (2600, 440,LIFE_SPAWN),
                (2800, 440),
                (3000, 400),
                (3300, 380,POINT_SPAWN),
                (3450, 330,POINT_SPAWN),
                (3600, 330,POINT_SPAWN),
                (3750, 400,POINT_SPAWN),
                (4000, 400),
                (4300, 380,MOB_SPAWN),
                (4600, 330),
                (4800, 440,LIFE_SPAWN)]

PLATFORM_LIST2=[(0,HEIGHT-50),
                (200, 400),
                (400, 400),
                (650, 380),
                (950, 330),
                (1150, 440),
                (1350, 440),
                (1550, 400),
                (1850, 380),
                (2000, 330),
                (2200, 330),
                (2500, 400),
                (2800, 400),
                (3000, 380),
                (3150, 330),
                (3300, 440),
                (3500, 440),
                (3650, 400),
                (3800, 380),
                (4100, 330),
                (4300, 330),
                (4600, 350),
                (4800, 350),
                (5000, 400),
                (5300, 400),
                (5500, 370),
                (5700, 440),
                (5850, 350),
                (6000, 350),
                (6200, 400),
                (6400, 400),
                (6700, 370),
                (7000, 440),
                (7200, 370),
                (7300, 440)]

ENDPOINT_LIST = [(5000,380),
                 (7500,380)]




#COLORS (R,G,B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW =(255,255,0)
LIGHTBLUE = (0,155,155)
LIGHTGREEN=(0,155,100)
BGCOLOR = LIGHTGREEN