import pygame
import random
import bullet
import json


class EnemyTank(pygame.sprite.Sprite):
    def __init__(self, enemyData, x=None):
        pygame.sprite.Sprite.__init__(self)
        
        self.flash = False
        self.times = 90
        tankType = 1
        self.tankType = tankType 
        
        
        self.enemy_x_0 = pygame.image.load("image/enemy_1_0.png", "r").convert_alpha()
        
        self.tank = self.enemy_x_0

        
        self.pos = x
        if not self.pos:
            self.pos = random.choice(range(1,len(enemyData["X"])+1))
        self.pos -= 1
        
        self.tank_R0 = self.tank.subsurface(( 0, 48), (48, 48))
        self.tank_R1 = self.tank.subsurface((48, 48), (48, 48))
        self.rect = self.tank_R0.get_rect()
        self.rect.left, self.rect.top = enemyData["X"][self.pos]*24+3, enemyData["Y"][self.pos]*24+3
        
        self.speed = 1
        self.dir_x, self.dir_y = 0, 1
        self.life = 1
        self.bulletNotCooling = True
        self.bullet = bullet.Bullet()
        self.dirChange = False
        
    def shoot(self):

        self.bullet.life = True
        self.bullet.changeImage(self.dir_x, self.dir_y)
        
        if self.dir_x == 0 and self.dir_y == -1:
            self.bullet.rect.left = self.rect.left + 20
            self.bullet.rect.bottom = self.rect.top + 1
        elif self.dir_x == 0 and self.dir_y == 1:
            self.bullet.rect.left = self.rect.left + 20
            self.bullet.rect.top = self.rect.bottom - 1
        elif self.dir_x == -1 and self.dir_y == 0:
            self.bullet.rect.right = self.rect.left - 1
            self.bullet.rect.top = self.rect.top + 20
        elif self.dir_x == 1 and self.dir_y == 0:
            self.bullet.rect.left = self.rect.right + 1
            self.bullet.rect.top = self.rect.top + 20
    
    def move(self, tankGroup, brickGroup, ironGroup, riverGroup, iceGroup):
        iceFix = self.onIce(iceGroup)
        self.rect = self.rect.move(self.speed * self.dir_x, self.speed * self.dir_y)
        if iceFix != self.onIce(iceGroup) and not iceFix:
            self.rect = self.rect.move(self.dir_x, self.dir_y)
        
        if self.dir_x == 0 and self.dir_y == -1:
            self.tank_R0 = self.tank.subsurface(( 0, 0),(48, 48))
            self.tank_R1 = self.tank.subsurface((48, 0),(48, 48))
        elif self.dir_x == 0 and self.dir_y == 1:
            self.tank_R0 = self.tank.subsurface(( 0, 48),(48, 48))
            self.tank_R1 = self.tank.subsurface((48, 48),(48, 48))
        elif self.dir_x == -1 and self.dir_y == 0:
            self.tank_R0 = self.tank.subsurface(( 0, 96),(48, 48))
            self.tank_R1 = self.tank.subsurface((48, 96),(48, 48))
        elif self.dir_x == 1 and self.dir_y == 0:
            self.tank_R0 = self.tank.subsurface(( 0, 144),(48, 48))
            self.tank_R1 = self.tank.subsurface((48, 144),(48, 48))
        
        
        if self.rect.top < 3:
            self.rect = self.rect.move(self.speed * 0, self.speed * 1)
            self.dir_x, self.dir_y = random.choice(([0,1],[0,-1],[1,0],[-1,0]))
        elif self.rect.bottom > 630 - 3:
            self.rect = self.rect.move(self.speed * 0, self.speed * -1)
            self.dir_x, self.dir_y = random.choice(([0,1],[0,-1],[1,0],[-1,0]))
        elif self.rect.left < 3:
            self.rect = self.rect.move(self.speed * 1, self.speed * 0)
            self.dir_x, self.dir_y = random.choice(([0,1],[0,-1],[1,0],[-1,0]))
        elif self.rect.right > 630 - 3:
            self.rect = self.rect.move(self.speed * -1, self.speed * 0)
            self.dir_x, self.dir_y = random.choice(([0,1],[0,-1],[1,0],[-1,0]))
    
        if pygame.sprite.spritecollide(self, brickGroup, False, None) \
            or pygame.sprite.spritecollide(self, ironGroup, False, None) \
            or pygame.sprite.spritecollide(self, tankGroup, False, None) \
            or pygame.sprite.spritecollide(self, riverGroup, False, None):
            self.rect = self.rect.move(self.speed * -self.dir_x, self.speed * -self.dir_y)
            self.dir_x, self.dir_y = random.choice(([0,1],[0,-1],[1,0],[-1,0]))
    
    def onIce(self, iceGroup):
        if pygame.sprite.spritecollide(self, iceGroup, False, None):
            self.speed = 2
            return True
        else:
            self.speed = 1
            return False

    def get_dir(self):
        if  self.dir_x == 0\
        and self.dir_y == 1:
            return 0
        elif  self.dir_x == 0\
        and self.dir_y == -1:
            return 1
        elif  self.dir_x == -1\
        and self.dir_y == 0:
            return 2
        elif  self.dir_x == 1\
        and self.dir_y == 0:
            return 3
            