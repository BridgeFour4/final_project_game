import pygame as pg
from settings import *
from random import choice, randrange
vec=pg.math.Vector2


class Spritesheet:
    #utility class for loading and parsing spritesheets
    def __init__(self,filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y , width, height):
        # grab image out of a larger spritesheet
            image = pg.Surface((width,height))
            image.blit(self.spritesheet, (0,0),(x,y,width,height))
            image = pg.transform.scale(image,(width//2,height//2))
            return image


class Player(pg.sprite.Sprite):
    def __init__(self,game):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game=game
        self.walking =False
        self.casting = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.standing_frame
        self.rect = self.image.get_rect()
        self.rect.center = (40, HEIGHT-100)
        self.pos = vec(40, HEIGHT-100)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.hit =0

    def load_images(self):
        self.standing_frame = self.game.standing_image
        self.standing_frame.set_colorkey(WHITE)
        self.walking_frames_right = [self.game.walking1_image,
                                     self.game.walking2_image,
                                     self.game.walking3_image]
        self.walking_frames_left = []
        for frame in self.walking_frames_right:
            frame.set_colorkey(WHITE)
            self.walking_frames_left.append(pg.transform.flip(frame, True, False))
        self.cast_frame = self.game.casting_image
        self.cast_frame.set_colorkey(WHITE)

    def update(self):
        self.animate()
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

        self.rect.midbottom = self.pos

        if self.hit >0:
            self.hit -=1

    def animate(self):
        now = pg.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False

        if self.casting:
            if now - self.last_update > 200:
                self.last_update = now
                bottom = self.rect.bottom
                self.image = self.cast_frame
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        elif self.walking:
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walking_frames_right)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walking_frames_right[self.current_frame]
                else:
                    self.image = self.walking_frames_left[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        else:
            if now - self.last_update > 200:
                self.last_update = now
                bottom = self.rect.bottom
                self.image = self.standing_frame
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom




    def jump(self):
        # jump only if standing on platform
        self.rect.x += 2
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 2
        if hits and not self.jumping:
            self.game.jumpsound.play()
            self.jumping = True
            self.vel.y = -PLAYER_JUMP

    def shoot(self):
        self.game.shootsound.play()
        Lightning(self.game,self)


    def teleport(self,x,y):
        self.casting = False
        Flash(game=self.game, x=self.pos.x-50, y=self.pos.y-50,image=self.game.teleport2_image)
        self.pos.x = x
        self.pos.y = y
        Flash(game=self.game, x=self.pos.x-50, y=self.pos.y-50, image=self.game.teleport1_image)

    def hurt(self):
        Flash(game=self.game, x=self.pos.x-50, y=self.pos.y-50, image=self.game.Hurt_image)
        self.game.hurtsound.play()
        self.hit =5*FPS

class Platform(pg.sprite.Sprite):
    def __init__(self,game,x,y,spawn=0):
        self._layer = PLATFORM_LAYER
        self.groups = game.all_sprites, game.platforms
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.platform_image
        #self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        if spawn == LIFE_SPAWN:
            Pow(self.game,self,LIFE_SPAWN)
        if spawn == POINT_SPAWN:
            Pow(self.game,self,POINT_SPAWN)
        if spawn ==MOB_SPAWN:
            Mob(self.game,self)


class Lightning(pg.sprite.Sprite):
    def __init__(self, game, player):
        self.layer = PLAYER_LAYER
        self.groups = game.all_sprites, game.projectiles
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.player = player
        self.image = game.lightning_image
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = self.player.rect.x
        self.rect.y = self.player.rect.y
        self.dx = LIGHNING_SPEED
        self.spawn_time = 0
    def update(self):
        self.rect.x+=self.dx
        self.spawn_time+=1
        if self.spawn_time>=LIGHNING_DURATION:
            self.player.teleport(self.rect.x,self.rect.y)
            self.kill()


class Endpoint(pg.sprite.Sprite):
    def __init__(self,game,x,y):
        self.layer = PLATFORM_LAYER
        self.groups = game.all_sprites, game.endpoints
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image_orig = game.endpoint_image
        self.image = self.image_orig.copy()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rot = 0
        self.rot_speed = 4
        self.last_update = pg.time.get_ticks()

    def update(self):
        self.rotate()

    def rotate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            # do rotation here)
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pg.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center


class Mob(pg.sprite.Sprite):

    def __init__(self,game,plat):
        self.layer = PLAYER_LAYER
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.plat = plat
        self.image = pg.Surface((30,30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = self.plat.rect.left + ((self.plat.rect.right-self.plat.rect.left)/2)
        self.rect.bottom = self.plat.rect.top
        self.dx = 2

    def update(self):
        self.rect.x += self.dx
        if self.rect.right== self.plat.rect.right:
            self.dx = -self.dx

        elif self.rect.left == self.plat.rect.left:
            self.dx = -self.dx

class Pow(pg.sprite.Sprite):

    def __init__(self,game,plat,type):
        self.layer = PLAYER_LAYER
        self.groups = game.all_sprites, game.powerups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.plat = plat
        self.type = type
        if self.type == LIFE_SPAWN:
            self.image = game.one_up_image
        elif self.type == POINT_SPAWN:
            self.image = game.coin_image
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = self.plat.rect.left + ((self.plat.rect.right - self.plat.rect.left) / 2)
        self.rect.bottom = self.plat.rect.top


class Flash(pg.sprite.Sprite):
    def __init__(self, game, image, x, y):
        self.layer = EFX_LAYER
        self.groups = game.all_sprites, game.efx
        pg.sprite.Sprite.__init__(self,self.groups)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.lifetime = 10

    def update(self):
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()

