import pygame
from JSON.sort import getFile
import json 
from math import floor as int

class Map:
    def __init__(self, title, image, score, x, y, surface):
        self.name = title
        self.left, self.top = x, y
        self.screen = surface
        self.image_size = 299
        self.score = score
        self.background = pygame.Color(80,120,105)
        self.white = pygame.Color(219, 235, 216)
        self.black = pygame.Color(0,0,0)
        
        try:
            self.oimage = pygame.transform.scale(pygame.image.load(image), (299, 299))
        except:
            self.oimage = pygame.transform.scale(pygame.image.load("image\\map-image-Search.png"), (299, 299))
        self.surface = pygame.Surface([315,525])
        
        self.rect = pygame.Rect(x,y,315,525)
        self.surface.fill(self.background)
        pygame.draw.rect(self.surface,self.black,[4,4,307,307])
        pygame.draw.rect(self.surface,self.background,[8,8,299,299])
        self.surface.blit(self.oimage, (8, 8))
        self.surface.blit(pygame.font.Font(None, 41).render(title, True, self.white, None), (18, 366))
        self.surface.blit(pygame.font.Font(None, 41).render(score, True, self.white, None), (18, 466))
        self.surface.blit(pygame.font.Font(None, 41).render("MAP", True, self.white, None), (18, 325))
        self.surface.blit(pygame.font.Font(None, 41).render("HIGH SCORE", True, self.white, None), (18, 425))
        self.screen.blit(self.surface,self.rect)

    def move_right(self):
        self.left += 11
        self.rect.move_ip(11,0)
        self.screen.blit(self.surface,self.rect)
    
    def move_left(self):
        self.left -= 11
        self.rect.move_ip(-11,0)
        self.screen.blit(self.surface,self.rect)

    def click(self, pos):
        if self.rect.collidepoint(pos):
            print(self.name+" selected")
            return self.name
        return None
    
    def blink(self, pos):
        if self.rect.collidepoint(pos):
            self.surface.fill(self.white)
            pygame.draw.rect(self.surface,self.black,[4,4,307,307])
            pygame.draw.rect(self.surface, self.background,[8,8,299,299])
            self.surface.blit(self.oimage, (8, 8))
            self.surface.blit(pygame.font.Font(None, 41).render(self.name, True, self.black, None), (18, 366))
            self.surface.blit(pygame.font.Font(None, 41).render(self.score, True, self.black, None), (18, 466))
            self.surface.blit(pygame.font.Font(None, 41).render("MAP", True, self.black, None), (18, 325))
            self.surface.blit(pygame.font.Font(None, 41).render("HIGH SCORE", True, self.black, None), (18, 425))
            self.screen.blit(self.surface,self.rect)
            return True
        self.surface.fill(self.background)
        pygame.draw.rect(self.surface,self.black,[4,4,307,307])
        pygame.draw.rect(self.surface,self.background,[8,8,299,299])
        self.surface.blit(self.oimage, (8, 8))
        self.surface.blit(pygame.font.Font(None, 41).render(self.name, True, self.white, None), (18, 366))
        self.surface.blit(pygame.font.Font(None, 41).render(self.score, True, self.white, None), (18, 466))
        self.surface.blit(pygame.font.Font(None, 41).render("MAP", True, self.white, None), (18, 325))
        self.surface.blit(pygame.font.Font(None, 41).render("HIGH SCORE", True, self.white, None), (18, 425))
        self.screen.blit(self.surface,self.rect)
        return False
            
    
class Selector():
    def __init__(self, surface, easteregg):
        maps = None
        extension = None
        if easteregg == 2:
            extension = "lssh"
        else:
            extension = "json"
        maps = getFile(extension)
        cnt = 0
        self.mapGroup = []
        for index in maps:
            data = json.load(open("JSON\\" + index + "." + extension))
            data["score"] = 1
            # self.map = Map(index, pygame.image.load("JSON\\" + index + ".png"), int(data["score"]), 157+cnt*443, 52, surface)
            self.mapGroup.append(Map(index, "image\\map-image-" + index + ".png", "123", 157+cnt*440, 52, surface))
            # print(len(self.mapGroup))
            cnt+=1


