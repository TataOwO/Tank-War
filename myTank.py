import pygame
import bullet

tank_T1_0 = "image/tank_T1_0.png"       

class MyTank(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        
        self.tank_L0_image = pygame.image.load(tank_T1_0, "r").convert_alpha()
        self.level = 0

        self.tank = self.tank_L0_image
    
        self.tank_R0 = self.tank.subsurface((0, 0),(48, 48))
        self.rect = self.tank_R0.get_rect()
        self.rect.left, self.rect.top = 3 + x[0] * 24, 3 + y[0] * 24 

        self.speed = 2
        self.dir_x, self.dir_y = 0, -1
        self.life = 3
        self.bulletNotCooling = True
        self.bullet = bullet.Bullet() 
        self.bullet.speed = 6
        self.pdir = 0
        
        
    
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

    def moveUp(self, tankGroup, brickGroup, ironGroup, riverGroup, baseGroup, goback):
        self.tank_R0 = self.tank.subsurface((0, 0),(48, 48))
        if not goback:
            self.rect = self.rect.move(self.speed * 0, self.speed * -1)
            self.dir_x, self.dir_y = 0, -1
            if     pygame.sprite.spritecollide(self, brickGroup, False, None) \
                or pygame.sprite.spritecollide(self, ironGroup, False, None) \
                or pygame.sprite.spritecollide(self, riverGroup, False, None) \
                or pygame.sprite.spritecollide(self, tankGroup, False, None) \
                or pygame.sprite.spritecollide(self, baseGroup, False, None) \
                or self.rect.top < 3:
                self.rect = self.rect.move(self.speed * 0, self.speed * 1)
                return True
        return False
    def moveDown(self, tankGroup, brickGroup, ironGroup, riverGroup, baseGroup, goback):
        self.tank_R0 = self.tank.subsurface((0, 48),(48, 48))
        if not goback:
            self.rect = self.rect.move(self.speed * 0, self.speed * 1)
            self.dir_x, self.dir_y = 0, 1
            if     pygame.sprite.spritecollide(self, brickGroup, False, None) \
                or pygame.sprite.spritecollide(self, ironGroup, False, None) \
                or pygame.sprite.spritecollide(self, riverGroup, False, None) \
                or pygame.sprite.spritecollide(self, tankGroup, False, None) \
                or pygame.sprite.spritecollide(self, baseGroup, False, None) \
                or self.rect.bottom > 630 - 3:
                self.rect = self.rect.move(self.speed * 0, self.speed * -1)
                return True
        return False
    def moveLeft(self, tankGroup, brickGroup, ironGroup, riverGroup, baseGroup, goback):
        self.tank_R0 = self.tank.subsurface((0, 96),(48, 48))
        if not goback:
            self.rect = self.rect.move(self.speed * -1, self.speed * 0)
            self.dir_x, self.dir_y = -1, 0
            if     pygame.sprite.spritecollide(self, brickGroup, False, None) \
                or pygame.sprite.spritecollide(self, ironGroup, False, None) \
                or pygame.sprite.spritecollide(self, riverGroup, False, None) \
                or pygame.sprite.spritecollide(self, tankGroup, False, None) \
                or pygame.sprite.spritecollide(self, baseGroup, False, None) \
                or self.rect.left < 3:
                self.rect = self.rect.move(self.speed * 1, self.speed * 0)
                return True
        return False
    def moveRight(self, tankGroup, brickGroup, ironGroup, riverGroup, baseGroup, goback):
        self.tank_R0 = self.tank.subsurface((0, 144),(48, 48))
        if not goback:
            self.rect = self.rect.move(self.speed * 1, self.speed * 0)
            self.dir_x, self.dir_y = 1, 0
            if     pygame.sprite.spritecollide(self, brickGroup, False, None) \
                or pygame.sprite.spritecollide(self, ironGroup, False, None) \
                or pygame.sprite.spritecollide(self, riverGroup, False, None) \
                or pygame.sprite.spritecollide(self, tankGroup, False, None) \
                or pygame.sprite.spritecollide(self, baseGroup, False, None) \
                or self.rect.right > 630 - 3:
                self.rect = self.rect.move(self.speed * -1, self.speed * 0)
                return True
        return False
    def moveTank(self, tankGroup, brickGroup, ironGroup, riverGroup, baseGroup, movdir, goback):
        if movdir == 0:
            return self.moveUp(tankGroup, brickGroup, ironGroup, riverGroup, baseGroup, goback)
        elif movdir == 1:
            return self.moveDown(tankGroup, brickGroup, ironGroup, riverGroup, baseGroup, goback)
        elif movdir == 2:
            return self.moveLeft(tankGroup, brickGroup, ironGroup, riverGroup, baseGroup, goback)
        elif movdir == 3:
            return self.moveRight(tankGroup, brickGroup, ironGroup, riverGroup, baseGroup, goback)
        else:
            return True
    def onIce(self, iceGroup, movdir):
        if pygame.sprite.spritecollide(self, iceGroup, False, None):
            self.speed = 4
            return True
        else:
            self.pdir = movdir
            self.speed = 2
            return False
    def get_dir(self):
        return self.pdir
