TITLE ="final_game"
WIDTH = 600 # width of game window
HEIGHT = 480 # height of screen
FPS = 60 # frames
FONT_NAME = 'arial'

#player proppeties
PLAYER_ACC = 0.5
PLAYER_FRICTION= -0.12
PLAYER_GRAV=0.8
PLAYER_JUMP = 13


PLAYER_LAYER = 2
PLATFORM_LAYER = 1
#platform lists
PLATFORM_LIST1=[(0,HEIGHT-50),
               (100, 400),
               (250,400),
               (400,380),
               (550, 330),
               (700,440)]

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