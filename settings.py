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
LIGHNING_SPEED = 5
LIGHNING_DURATION = 45


PLAYER_LAYER = 2
PLATFORM_LAYER = 1
#platform lists
PLATFORM_LIST1=[(0,HEIGHT-50),
               (100, 400),
               (250,400),
               (400,380),
               (550, 330),
               (700,440),
               (950, 440),
               (1150, 400),
               (1300, 380),
               (1450, 330),
               (1700, 330),
               (1800, 400),
               (1950,400),
               (2100,380),
               (2350, 330),
               (2600,440)]

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