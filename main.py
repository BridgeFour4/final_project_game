# happy flute by Tomasz Kucza / magory.games / based on piermic's Improvisation with Sopranino recorder
#Yippee by http://opengameart.org/users/snabisk
# coin and platform art by kenny.nl

import pygame as pg
import random
from settings import *
from sprites import *
from os import path



class Game:
    def __init__(self):
        # initializize game elements
        pg.init()
        pg.mixer.init()  # for sound
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.map = 0
        self.first_hit = 0
        self.move_forward=0
        self.load_data()


    def load_data(self):
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, 'img')
        self.snd_dir = path.join(self.dir, 'snd')
        # load high score
        with open(path.join(self.dir, HS_FILE), "r") as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0
        # load sritesheet and images
        self.background = pg.image.load(path.join(img_dir,"background.png"))
        self.background_rect= self.background.get_rect()
        self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))
        self.lightning_image = pg.image.load(path.join(img_dir, "Lightning.png"))
        self.Hurt_image = pg.image.load(path.join(img_dir, "Hurt.png"))
        self.teleport1_image = pg.image.load(path.join(img_dir, "teleport1.png"))
        self.teleport2_image= pg.image.load(path.join(img_dir, "teleport2.png"))
        self.endpoint_image = pg.image.load(path.join(img_dir, "endpoint.png"))

        self.walking1_image = pg.image.load(path.join(img_dir, "walking1.png"))
        self.walking2_image = pg.image.load(path.join(img_dir, "walking2.png"))
        self.walking3_image = pg.image.load(path.join(img_dir, "walking3.png"))
        self.standing_image = pg.image.load(path.join(img_dir, "standing_frames.png"))
        self.casting_image = pg.image.load(path.join(img_dir, "casting (2).png"))

        self.platform_image = pg.image.load(path.join(img_dir,"platform.png"))
        self.coin_image = pg.image.load(path.join(img_dir,"coin.png"))
        self.one_up_image= pg.image.load(path.join(img_dir,"life.png"))
        # load_sound
        self.jumpsound = pg.mixer.Sound(path.join(self.snd_dir, 'Jump.wav'))
        self.coinsound = pg.mixer.Sound(path.join(self.snd_dir, 'Coin.wav'))
        self.hurtsound = pg.mixer.Sound(path.join(self.snd_dir, 'Hurt.wav'))
        self.lifesound = pg.mixer.Sound(path.join(self.snd_dir, 'Life.wav'))
        self.shootsound = pg.mixer.Sound(path.join(self.snd_dir, 'Shoot.wav'))
        self.levelsound = pg.mixer.Sound(path.join(self.snd_dir, 'LevelChange.wav'))



    def new(self):
        # starts game again resets values
        pg.mixer.music.load(path.join(self.snd_dir, 'tkucza-happyflutes.ogg'))
        self.score = 0
        self.lives = 3
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.platforms = pg.sprite.Group()
        self.projectiles= pg.sprite.Group()
        self.backboard = pg.sprite.Group()
        self.endpoints = pg.sprite.Group()
        self.powerups = pg.sprite.Group()
        self.efx= pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.board(self.map)
        self.run()

    def board(self,run):
        self.first_hit = 0
        self.move_forward=0
        self.player = Player(self)
        if run == 0:
            for plat in PLATFORM_LIST1:
                Platform(self, *plat)
                self.endpoint = Endpoint(self, *ENDPOINT_LIST[run])
        if run == 1:
            for plat in PLATFORM_LIST2:
                Platform(self, *plat)
                self.endpoint = Endpoint(self, *ENDPOINT_LIST[run])
        if run >=len(ENDPOINT_LIST):
            self.playing = False



    def run(self):
        pg.mixer.music.play(loops=-1)
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pg.mixer.music.fadeout(500)


    def update(self):
        # game loop update
        self.all_sprites.update()

        # check if player hits platform only if falling
        if self.player.vel.y>0:
            hits = pg.sprite.spritecollide(self.player,self.platforms,False)
            if hits:
                if self.player.pos.y<hits[0]. rect.bottom:
                    self.player.pos.y = hits[0].rect.top
                    self.player.vel.y = 0
                    self.player.jump_check=0
                    self.player.jumping = False

        # checks to see if hitting backboard
        hits = pg.sprite.spritecollide(self.player,self.backboard,False)
        if hits:
            self.player.rect.left = hits[0].rect.right
            self.player.vel.x = 0

        # checks to see if hit endpoint
        hits = pg.sprite.spritecollide(self.player,self.endpoints,False)
        if hits:
            self.levelsound.play()
            if self.lives >=3:
                self.score+=1000
            self.map+=1
            self.reset()


        # check to see if projectile hits mob and kills the mob but not the bullet
        hits=pg.sprite.groupcollide(self.projectiles,self.mobs,False,True)
        for hit in hits:
            self.score+=10

         #check to see if the player hits the mob and from what direction
        hits = pg.sprite.spritecollide(self.player, self.mobs,False)
        for hit in hits:

            if self.player.rect.bottom <= (hit.rect.top+(hit.rect.bottom-hit.rect.top)/8):
                hit.kill()
                self.score+=10
            elif self.player.rect.bottom > hit.rect.center[1] and self.player.hit ==0:
                self.lives-=1
                self.player.hurt()

            if self.lives<=0:
                self.playing = False

        # checks to see if player hit powerup and what type
        hits = pg.sprite.spritecollide(self.player,self.powerups,True)
        for hit in hits:
            if hit.type ==LIFE_SPAWN:
                self.lifesound.play()
                self.lives+=1
                if self.lives >5:
                    self.lives =5
            if hit.type == POINT_SPAWN:
                self.coinsound.play()
                self.score+=100

        # constantly scroll the screen to force player forward
        if self.move_forward==1:
            self.player.pos.x -= 2
            self.endpoint.rect.x -= 2
            for powerup in self.powerups:
                powerup.rect.x -= 2
            for bullet in self.projectiles:
                bullet.rect.x -= 2
            for mob in self.mobs:
                mob.rect.x -= 2
            for plat in self.platforms:
                plat.rect.x -= 2
            for efx in self.efx:
                efx.rect.x -= 2


        # if player reaches right side of screen scroll over the screen
        if self.player.rect.right > WIDTH/4:
            self.player.pos.x -= max(abs(self.player.vel.x), 2)
            self.endpoint.rect.x -=max(abs(self.player.vel.x),2)
            for powerup in self.powerups:
                powerup.rect.x-=max(abs(self.player.vel.x),2)
            for bullet in self.projectiles:
                bullet.rect.x -=max(abs(self.player.vel.x),2)
            for mob in self.mobs:
                mob.rect.x -=max(abs(self.player.vel.x),2)
            for plat in self.platforms:
                plat.rect.x -=max(abs(self.player.vel.x),2)
            for efx in self.efx:
                efx.rect.x -= max(abs(self.player.vel.x), 2)

        # if we fall off the bottom or off the left
        if self.player.rect.bottom > HEIGHT or self.player.rect.right<0:
            if self.first_hit == 0:
                self.lives -= 1
            if self.lives > 0:
                self.reset()
            else:
                self.playing=False


    def events(self):
        # game loop events
        # process input
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.move_forward=1
                    self.player.jump()
                if event.key == pg.K_SPACE:
                    self.player.casting=True
                    self.player.shoot()

    def draw(self):
        # game loop draw
        self.screen.fill(BGCOLOR)
        self.screen.blit(self.background,self.background_rect)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score),22,WHITE,WIDTH / 4, 15)
        self.draw_text(str(self.lives), 22, WHITE, WIDTH * 3/4, 15)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        # start screen
        pg.mixer.music.load(path.join(self.snd_dir, 'Yippee.ogg'))
        pg.mixer.music.play(loops=-1)
        self.screen.fill(BGCOLOR)
        self.draw_text(TITLE,48,WHITE,WIDTH/2,HEIGHT/4)
        self.draw_text("arrows to move and jump space to shoot a teleport ",22,WHITE,WIDTH/2,HEIGHT/2)
        self.draw_text('press a key to start',22,WHITE,WIDTH/2, HEIGHT*3/4 )
        self.draw_text('High Score: '+str(self.highscore), 22, WHITE, WIDTH / 2,15)
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(500)

    def show_go_screen(self):
        # game over screen
        pg.mixer.music.load(path.join(self.snd_dir, 'Yippee.ogg'))
        pg.mixer.music.play(loops=-1)
        if not self.running or self.map >=len(ENDPOINT_LIST):
            return
        self.map = 0
        self.screen.fill(BGCOLOR)
        self.draw_text("GAME OVER", 48, RED, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Score: " + str(self.score), 22, RED, WIDTH / 2, HEIGHT / 2)
        self.draw_text('press a key to play again', 22, RED, WIDTH / 2, HEIGHT * 3 / 4)
        if self.score > self.highscore:
            self.highscore= self.score
            self.draw_text("NEW HIGH SCORE! ", 22, GREEN, WIDTH / 2, HEIGHT / 2+40)
            with open(path.join(self.dir,HS_FILE),'w')as f:
                 f.write(str(self.highscore))
        else:
            self.draw_text('High Score: ' + str(self.highscore), 22, WHITE, WIDTH / 2, HEIGHT / 2+40)
        pg.display.flip()
        self.reset()
        self.wait_for_key()
        pg.mixer.music.fadeout(500)

    def show_win_screen(self):

        if not self.running or self.map < len(ENDPOINT_LIST):
            return
        # game over screen
        self.map=0
        pg.mixer.music.load(path.join(self.snd_dir, 'Yippee.ogg'))
        pg.mixer.music.play(loops=-1)
        self.screen.fill(BGCOLOR)
        self.draw_text("Congratualtions You Won", 48, RED, WIDTH / 2, HEIGHT / 4)
        self.draw_text(" Your Score was: "+ str(self.score), 22, RED, WIDTH / 2, HEIGHT / 2)
        self.draw_text('press a key to Replay', 22, RED, WIDTH / 2, HEIGHT * 3 / 4)
        if self.score > self.highscore:
            self.highscore= self.score
            self.draw_text("NEW HIGH SCORE! ", 22, GREEN, WIDTH / 2, HEIGHT / 2+40)
            with open(path.join(self.dir,HS_FILE),'w')as f:
                f.write(str(self.highscore))
        else:
            self.draw_text('High Score: ' + str(self.highscore), 22, WHITE, WIDTH / 2, HEIGHT / 2+40)
        pg.display.flip()
        self.reset()
        self.wait_for_key()
        pg.mixer.music.fadeout(500)




    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    self.map = 0
                    if event.key == pg.K_2:
                        self.map = 1
                    waiting = False

    def reset(self):
        self.player.kill()
        self.endpoint.kill()
        for bullet in self.projectiles:
            bullet.kill()
        for mob in self.mobs:
            mob.kill()
        for powerup in self.powerups:
            powerup.kill()
        for plat in self.platforms:
            plat.kill()
        for efx in self.efx:
            efx.kill()
        self.board(self.map)

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)


g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()
    g.show_win_screen()
pg.quit()
