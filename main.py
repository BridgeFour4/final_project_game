import pygame as pg
import random
from settings import *
from sprites import *
from os import path

class Game:
    def __init__(self):
        #initializize game elements
        pg.init()
        pg.mixer.init()  # for sound
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.map = 0
        self.first_hit = 0
        self.load_data()

    def load_data(self):
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, 'img')
        self.snd_dir = path.join(self.dir, 'snd')
        # load high score
        #load sritesheet
        #load_sound


    def new(self):
        #starts game again resets values
        self.score = 0
        self.lives = 3
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.platforms = pg.sprite.Group()
        self.backboard= pg.sprite.Group()
        self.projectiles= pg.sprite.Group()
        self.endpoints = pg.sprite.Group()
        #self.powerups = pg.sprite.Group()
        #self.mobs = pg.sprite.Group()
        self.board(self.map)
        self.run()


    def board(self,run):
        self.first_hit = 0
        self.player = Player(self)
        self.backwall = Backwall(self, -200, 0)
        if run ==0:
            for plat in PLATFORM_LIST1:
                Platform(self, *plat)
        if run == 1:
            for plat in PLATFORM_LIST2:
                Platform(self, *plat)
        if run ==2:
            self.show_win_screen()
            self.running = False
        # pg.mixer.music.load(path.join(self.snd_dir,''))
        self.endpoint = Endpoint(self, *ENDPOINT_LIST[run])

    def run(self):
        #pg.mixer.music.play(loops=-1)
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        #pg.mixer.music.fadeout(500)


    def update(self):
        #game loop update
        self.all_sprites.update()

        # hit mobs
        #mob_hits = pg.sprite.spritecollide(self.player,self.mobs,False, pg.sprite.collide_mask )
        #if mob_hits:
        #    self.playing = False

        #check if player hits platform only if falling
        if self.player.vel.y>0:
            hits = pg.sprite.spritecollide(self.player,self.platforms,False)
            if hits:
                if self.player.pos.y<hits[0]. rect.bottom:
                    self.player.pos.y = hits[0].rect.top
                    self.player.vel.y = 0
                    self.player.jump_check=0
                    self.player.jumping = False

        #checks to see if hitting backboard
        hits = pg.sprite.spritecollide(self.player,self.backboard,False)
        if hits:
            self.player.rect.left = hits[0].rect.right
            self.player.vel.x = 0

        hits = pg.sprite.spritecollide(self.player,self.endpoints,False)
        if hits:
            self.map+=1
            self.player.kill()
            self.backwall.kill()
            self.endpoint.kill()
            for plat in self.platforms:
                plat.kill()
            self.board(self.map)

        # if player reaches right side of screen scroll over the screen
        if self.player.rect.right > WIDTH/4:
            self.player.pos.x -=max(abs(self.player.vel.x), 2)
            self.backwall.rect.x -= max(abs(self.player.vel.x), 2)
            self.endpoint.rect.x -=max(abs(self.player.vel.x),2)
            #for mob in self.mobs:
            #    mob.rect.y +=max(abs(self.player.vel.y),2)
            for plat in self.platforms:
                plat.rect.x -=max(abs(self.player.vel.x),2)
                #come back to this part later to look at it
                if plat.rect.top>=HEIGHT:
                    plat.kill()
                    self.score+=10
        if self.player.rect.right < WIDTH/6:
            self.player.pos.x +=max(abs(self.player.vel.x), 2)
            self.backwall.rect.x += max(abs(self.player.vel.x), 2)
            self.endpoint.rect.x += max(abs(self.player.vel.x), 2)
            #for mob in self.mobs:
            #    mob.rect.y +=max(abs(self.player.vel.y),2)
            for plat in self.platforms:
                plat.rect.x +=max(abs(self.player.vel.x),2)
                #come back to this part later to look at it
                if plat.rect.top>=HEIGHT:
                    plat.kill()
                    self.score+=10

        # if player hits powerup
        #pow_hits = pg.sprite.spritecollide(self.player,self.powerups,True)
        #for pow in pow_hits:


        # if we fall off the bottom
        if self.player.rect.bottom >HEIGHT:
            if self.first_hit==0:
                self.lives -= 1
            if self.lives >= 0:
                self.player.kill()
                self.backwall.kill()
                self.endpoint.kill()
                for plat in self.platforms:
                    plat.kill()
                self.board(self.map)
            else:
                self.playing=False

        #spawn new platforms to keep some aveerage number
        #while len(self.platforms)<6:
        #    width = random.randrange(30,85)
        #    Platform(self,random.randrange(0,WIDTH - width),
        #                 random.randrange(-75,-30))

    def events(self):
        # game loop events
        # process input
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing=False
                self.running = False
            if event.type == pg.KEYDOWN:
               if event.key == pg.K_UP:
                   self.player.jump()
               if event.key == pg.K_SPACE:
                   self.player.shoot()

    def draw(self):
        #game loop draw
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score),22,WHITE,WIDTH / 4, 15)
        self.draw_text(str(self.lives), 22, WHITE, WIDTH * 3/4, 15)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        # start screen
        #pg.mixer.music.load(path.join(self.snd_dir, 'Yippee.ogg'))
        #pg.mixer.music.play(loops=-1)
        self.screen.fill(BGCOLOR)
        self.draw_text(TITLE,48,WHITE,WIDTH/2,HEIGHT/4)
        self.draw_text("arrows to move and jump space to shoot a teleport ",22,WHITE,WIDTH/2,HEIGHT/2)
        self.draw_text('press a key to start',22,WHITE,WIDTH/2, HEIGHT*3/4 )
        #self.draw_text('High Score: '+str(self.highscore), 22, WHITE, WIDTH / 2,15)
        pg.display.flip()
        self.wait_for_key()
        #pg.mixer.music.fadeout(500)

    def show_go_screen(self):
        # game over screen
        #pg.mixer.music.load(path.join(self.snd_dir, 'Yippee.ogg'))
        #pg.mixer.music.play(loops=-1)
        self.map = 0
        if not self.running or self.map ==2:
            return
        self.screen.fill(BGCOLOR)
        self.draw_text("GAME OVER", 48, RED, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Score: "+ str(self.score), 22, RED, WIDTH / 2, HEIGHT / 2)
        self.draw_text('press a key to play again', 22, RED, WIDTH / 2, HEIGHT * 3 / 4)
        #if self.score > self.highscore:
        #   self.highscore= self.score
        #    self.draw_text("NEW HIGH SCORE! ", 22, GREEN, WIDTH / 2, HEIGHT / 2+40)
        #    with open(path.join(self.dir,HS_FILE),'w')as f:
        #        f.write(str(self.highscore))
        #else:
        #    self.draw_text('High Score: ' + str(self.highscore), 22, WHITE, WIDTH / 2, HEIGHT / 2+40)
        pg.display.flip()
        self.wait_for_key()
        #pg.mixer.music.fadeout(500)

    def show_win_screen(self):
        # game over screen
        #pg.mixer.music.load(path.join(self.snd_dir, 'Yippee.ogg'))
        #pg.mixer.music.play(loops=-1)
        self.screen.fill(BGCOLOR)
        self.draw_text("Congratualtion You Won", 48, RED, WIDTH / 2, HEIGHT / 4)
        self.draw_text(" Your Score was: "+ str(self.score), 22, RED, WIDTH / 2, HEIGHT / 2)
        self.draw_text('press a key to play again', 22, RED, WIDTH / 2, HEIGHT * 3 / 4)
        #if self.score > self.highscore:
        #   self.highscore= self.score
        #    self.draw_text("NEW HIGH SCORE! ", 22, GREEN, WIDTH / 2, HEIGHT / 2+40)
        #    with open(path.join(self.dir,HS_FILE),'w')as f:
        #        f.write(str(self.highscore))
        #else:
        #    self.draw_text('High Score: ' + str(self.highscore), 22, WHITE, WIDTH / 2, HEIGHT / 2+40)
        pg.display.flip()
        self.wait_for_key()
        #pg.mixer.music.fadeout(500)

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    if event.key==pg.K_2:
                        self.map=1
                    waiting = False


    def draw_text(self,text,size,color,x,y):
        font = pg.font.Font(self.font_name,size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface,text_rect)


g = Game();
g.show_start_screen()
while g.running :
    g.new()
    g.show_go_screen()
pg.quit()