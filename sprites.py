import pygame as pg
from settings import *
from random import choice, randrange
vec=pg.math.Vector2



class Player(pg.sprite.Sprite):
    def __init__(self,game):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game=game
        self.walking =False
        self.current_frame = 0
        self.last_update = 0
        #self.load_images()
        self.image = pg.Surface((30,30))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (40, HEIGHT-100)
        self.pos = vec(40, HEIGHT-100)
        self.vel = vec(0,0)
        self.acc = vec(0,0)

    def update(self):
        self.acc = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC

        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc
        # wrap around sides of screen
        if self.pos.x > WIDTH + self.rect.width / 2:
            self.pos.x = 0 - self.rect.width / 2
        if self.pos.x < 0 - self.rect.width / 2:
            self.pos.x = WIDTH + self.rect.width / 2

        self.rect.midbottom = self.pos

    def jump(self):
        # jump only if standing on platform
        self.rect.x += 2
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 2
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -PLAYER_JUMP

    def shoot(self):
        pass

class Platform(pg.sprite.Sprite):
    def __init__(self,game,x,y):
        self._layer = PLATFORM_LAYER
        self.groups = game.all_sprites, game.platforms
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((100,20))
        self.image.fill(RED)
        #self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        #if randrange(100) < POW_SPAWN:
        #    Pow(self.game,self)
        #if randrange(100) < MOB_SPAWN:
        #    Pow(self.game,self)


class Backwall(pg.sprite.Sprite):
    def __init__(self,game,x,y):
        self._layer = PLATFORM_LAYER
        self.groups = game.all_sprites, game.backboard
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((100,480))
        self.image.fill(RED)
        #self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        #if randrange(100) < POW_SPAWN:
        #    Pow(self.game,self)
        #if randrange(100) < MOB_SPAWN:
        #    Pow(self.game,self)