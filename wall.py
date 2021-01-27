import pygame
import json
from JSON import sort

class Brick(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load(Map.brickImage)
        self.rect = self.image.get_rect()

class Iron(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load(Map.ironImage)
        self.rect = self.image.get_rect()

class River(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(Map.riverImage)
        self.rect = self.image.get_rect()

class Ice(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(Map.iceImage)
        self.rect = self.image.get_rect()

class Base(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(Map.baseImage)
        self.broke = pygame.image.load(Map.brokeImage)
        self.rect = self.image.get_rect()

class Map:
    def __init__(self):
        self.brickGroup = pygame.sprite.Group()
        self.ironGroup = pygame.sprite.Group()
        self.riverGroup = pygame.sprite.Group()
        self.iceGroup = pygame.sprite.Group()
        self.baseGroup = pygame.sprite.Group()
        

    def loadMap(self, mapName, easteregg):
        if easteregg == 2:
            mapName = mapName + ".lssh"
        else:
            mapName = mapName + ".json"
        MAP_JSON = json.load(open("JSON\\"+mapName))

        Map.brickImage          = "image\\" + json.dumps( MAP_JSON["mapBlocks"]["brick"]["image"] ).replace('"',"")
        Map.ironImage           = "image\\" + json.dumps( MAP_JSON["mapBlocks"]["iron"]["image"]  ).replace('"',"")
        Map.riverImage          = "image\\" + json.dumps( MAP_JSON["mapBlocks"]["river"]["image"] ).replace('"',"")
        Map.iceImage            = "image\\" + json.dumps( MAP_JSON["mapBlocks"]["ice"]["image"]   ).replace('"',"")
        Map.baseImage           = "image\\" + json.dumps( MAP_JSON["mapBlocks"]["base"]["image"]  ).replace('"',"")
        Map.brokeImage          = "image/home_destroyed.png"

        blockData = MAP_JSON["mapBlocks"]

        for index in MAP_JSON["mapBlocks"]:
            if index == "brick" and blockData[index]["X"] != None:
                for counting in range( 0, len(blockData[index]["X"]) ):
                    self.brick = Brick()
                    self.brick.rect.left, self.brick.rect.top = 3 + blockData[index]["X"][counting] * 24, 3 + blockData[index]["Y"][counting] * 24
                    self.brickGroup.add(self.brick)
                
            elif index == "iron" and blockData[index]["X"] != None:
                for counting in range( 0, len(blockData[index]["X"]) ):
                    self.iron = Iron()
                    self.iron.rect.left, self.iron.rect.top = 3 + blockData[index]["X"][counting] * 24, 3 + blockData[index]["Y"][counting] * 24
                    self.ironGroup.add(self.iron)
                for x in range(1, 26):
                    self.iron = Iron()
                    self.iron.rect.left, self.iron.rect.top = 3 + x * 24, 3 + 27 * 24
                    self.ironGroup.add(self.iron)
                    self.iron.rect.left, self.iron.rect.top = 3 + x * 24, 3 + 30 * 24
                    self.ironGroup.add(self.iron)
                for y in range(28, 29):
                    self.iron = Iron()
                    self.iron.rect.left, self.iron.rect.top = 3 + 1 * 24, 3 + y * 24
                    self.ironGroup.add(self.iron)
                    self.iron.rect.left, self.iron.rect.top = 3 + 26 * 24, 3 + y * 24
                    self.ironGroup.add(self.iron)

            elif index == "river" and blockData[index]["X"] != None:
                for counting in range( 0, len(blockData[index]["X"]) ):
                    self.river = River()
                    self.river.rect.left, self.river.rect.top = 3 + blockData[index]["X"][counting] * 24, 3 + blockData[index]["Y"][counting] * 24
                    self.riverGroup.add(self.river)
        
            elif index == "ice" and blockData[index]["X"] != None:
                for counting in range( 0, len(blockData[index]["X"]) ):
                    self.ice = Ice()
                    self.ice.rect.left, self.ice.rect.top = 3 + blockData[index]["X"][counting] * 24, 3 + blockData[index]["Y"][counting] * 24
                    self.iceGroup.add(self.ice)
                    
            if index == "base" and blockData[index]["X"] != None:
                for counting in range( 0, len(blockData[index]["X"]) ):
                    self.base = Base()
                    self.base.rect.left, self.base.rect.top = 3 + blockData[index]["X"][counting] * 24, 3 + blockData[index]["Y"][counting] * 24
                    self.baseGroup.add(self.base)
        
        return MAP_JSON["mapBlocks"]["myTank"], MAP_JSON["mapBlocks"]["enemy"]




