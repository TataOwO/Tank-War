import pygame
import json
from os import listdir, remove
from os.path import isfile, join, dirname
from operator import itemgetter
from sort import sorting, getFile
from math import floor as int

pygame.init()

# screen
screenSize = [1280,720]
screen = pygame.display.set_mode(screenSize, pygame.FULLSCREEN)

# various
extention = "json"
Map = []
buttons = []
images = {}
BLACK       = pygame.Color(0, 0, 0)
WHITE       = pygame.Color(255, 255, 255)
GREY        = pygame.Color(160,160,160)
BACKGROUND  = pygame.Color(54, 57, 63)
FONT  = pygame.font.Font(None, 32)
MAPSIZE = 26
gridSize = MAPSIZE*26+2
gridLeft = int((screenSize[0]-gridSize)/2)
gridTop  = int((screenSize[1]-gridSize)/2)

def main():

    running = True
    frame = pygame.time.Clock()
    screen.fill(BACKGROUND)
    MAP_JSON = None
    blockData = []
    
    # file
    files = getFile(extention)
    file = None
    file = mapSelector(files)
    print(file)
    
    if file == "Search":
        file = textBlock("Enter map name" ,False)
    if file == "New Map":
        file = textBlock("Enter new map name",True)
        files.append(file)
    if file == None or file not in files:
        running = False
    else:
        file = file+"."+extention
    if running:
        MAP_JSON = json.load(open(file,"r"))
        blockData = MAP_JSON["mapBlocks"]

    if file!=None:
        Grid = MapGrid(gridLeft, gridTop, MAPSIZE, MAPSIZE, True)
        # Draw Grid
        
        for blockName in blockData:
            index = blockData[blockName]
            images[blockName] = pygame.image.load("..\\image\\" + json.dumps(index["image"]).replace('"',""))
            if index["X"] != None:
                for counting, a in enumerate(range( len(index["X"]) )):
                    Map.append(GridBlock(index["X"][counting],index["Y"][counting],index["size"],blockName, screen, False))
        # Generating Map 
            
        for count,blockName in enumerate(images):
            buttons.append(BlockButton(60, 60*count+60, blockName, blockData))
        # Draw Buttons
    
    pygame.display.flip()
    buttonUp = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and buttonUp:
                buttonUp = False
                print("mouse button down")
                pos = pygame.mouse.get_pos()
                if pos[0] > 1270:
                    running = False
                # Save the map if user clicks at right edge of the screen
                elif event.button == 3: # if right click
                    if Grid.onGrid(pos):
                        for count, blocks in enumerate(Map):
                            if blocks.delete(pos):
                                Map.pop(count)
                                break
                        pygame.display.flip()
                    else:
                        for button in buttons:
                            button.clicked(0,0)
                elif event.button == 1: # if left click
                    if Grid.onGrid(pos):
                        for button in buttons:
                            if button.active:
                                gridX, gridY = Grid.clickLoc(False)
                                for x in range(button.size[0]):
                                    for y in range(button.size[1]):
                                        for count, blocks in enumerate(Map):
                                            if blocks.delete([ pos[0] + x*26, pos[1] + y*26 ]):
                                                Map.pop(count)
                                                y-=1
                                                break
                                if button.text == "myTank":
                                    print("is myTank")
                                    for count, blocks in enumerate(Map):
                                        if blocks.block == "myTank":
                                            print("found myTank at %d %d" % (blocks.x, blocks.y))
                                            blocks.delete([blocks.left+12,blocks.top+12])
                                            Map.pop(count)
                                Map.append( GridBlock(gridX, gridY, button.size, button.text, screen, False) )
                        pygame.display.flip()
                    else:
                        for button in buttons:
                            button.clicked(pos[0], pos[1])
                print("clicked at x= %d, y= %d" % (pos[0],pos[1]))
                while (not buttonUp):
                    for eventT in pygame.event.get():    
                        if eventT.type == pygame.MOUSEBUTTONUP:
                            buttonUp = True
                            print("mouse button up")
            elif event.type == pygame.QUIT:
                running = False
        frame.tick(60)
    
    if file != None:
        for blockName in blockData:
            blockData[blockName]["X"] = []
            blockData[blockName]["Y"] = []
        for blocks in Map:
            x, y, blockName = blocks.Saving()
            blockData[blockName]["X"].append(x)
            blockData[blockName]["Y"].append(y)
        for blockName in blockData:
            if blockData[blockName]["X"] == []:
                blockData[blockName]["X"] = None
                blockData[blockName]["Y"] = None
        MAP_JSON["mapBlocks"].update(blockData)
        MAP_JSON["Mapsize"] = MAPSIZE
        
        
        MAP_JSON = sorting(MAP_JSON)
        with open(file, "w") as writeIn:
            json.dump(MAP_JSON, writeIn, indent=4)
        if True:
            Mapping = []
            savingScreen = pygame.Surface([MAPSIZE*24,MAPSIZE*24], pygame.SRCALPHA)
            savingScreen.fill(pygame.Color(0,0,0,0))
            savingScreen.set_alpha(255)
            for blockName in blockData:
                index = blockData[blockName]
                if index["X"] != None:
                    for counting, a in enumerate(range( len(index["X"]) )):
                        Mapping.append(GridBlock(index["X"][counting],index["Y"][counting],index["size"],blockName, savingScreen, True))
            pygame.image.save(savingScreen, "..\\image\\map-image-"+file.split(".")[0]+".png")

class BlockButton:
    def __init__(self, x, y, block, blockData):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, 180, 54)
        self.size = blockData[block]["size"]
        self.text = block
        self.imageLoc = images[block]
        self.scaledImages = pygame.transform.scale(self.imageLoc, [48, 48])
        self.active = False
        
        screen.blit(self.scaledImages, [x+3, y+3])
        screen.blit(FONT.render(self.text, True, BLACK), [x+54, y+17])
    
    def clicked(self, mouseX, mouseY):
        if self.rect.collidepoint([mouseX, mouseY]):
            self.active = True
            pygame.draw.rect(screen, BLACK, [self.x, self.y, 180, 54])
            screen.blit(FONT.render(self.text, True, WHITE), [self.x+54, self.y+17])
            print("Selected %s" % (self.text))
        else:
            self.active = False
            pygame.draw.rect(screen, BACKGROUND, [self.x, self.y, 180, 54])
            screen.blit(FONT.render(self.text, True, BLACK), [self.x+54, self.y+17])
        screen.blit(self.scaledImages, [self.x+3, self.y+3])
        pygame.display.flip()
    
    def redraw(self):
        screen.blit(self.scaledImages, [self.x+3, self.y+3])
        screen.blit(FONT.render(self.text, True, BLACK), [self.x+54, self.y+17])
        
class MapButton:
    def __init__(self, Map, index):
        self.mapName = Map
        self.index = index
        self.width, self.height = 600, 150
        self.mov = 0
        self.rect = pygame.Rect(340,100+self.index*180+self.mov*10,1280-(340*2),self.height)
        self.surface = pygame.Surface([self.width,self.height])
        self.backgroundColor = WHITE
        self.textColor = BLACK
        self.image = pygame.Surface([108,108])
        self.image.fill(BLACK)
        
        try:
            self.image.blit(pygame.transform.scale(pygame.image.load("..\\image\\map-image-"+self.mapName+".png"), [104,104]), [2,2])
        except:
            self.image = pygame.Surface([104,104])
            self.image.fill(WHITE)
        
        self.redraw()
    
    def blink(self, pos):
        if self.rect.collidepoint(pos):
            self.backgroundColor = GREY
            self.textColor = WHITE
        else:
            self.backgroundColor = WHITE
            self.textColor = BLACK
        self.redraw()
        pygame.display.flip()
    
    def clicked(self, pos):
        if self.rect.collidepoint(pos):
            print(self.mapName)
            return self.mapName
        else:
            print("no map selected")
            return ""
    
    def redraw(self):
        pygame.draw.rect(self.surface,self.backgroundColor,[0,0,self.width,self.height])
        self.surface.blit(self.image, [21,21])
        self.surface.blit(pygame.font.Font(None, 100).render(self.mapName, True, self.textColor), [175,45])
        screen.blit(self.surface, self.rect)

class MapGrid:
    
    def __init__(self, x, y, sizeX, sizeY, newObj):
        if newObj:
            self.x = x
            self.y = y
            self.rect = pygame.Rect( self.x, self.y, sizeX*26+2, sizeY*26+2 )
        pygame.draw.rect(screen, BLACK, [x, y, sizeX*26+2, sizeY*26+2])
        for gridX in range(sizeX):
            for gridY in range(sizeY):
                pygame.draw.rect(screen, WHITE, [26*gridX+x+2, 26*gridY+y+2,24,24])
    
    def clickLoc(self, absloc):
        mousePos = pygame.mouse.get_pos()
        gridX = (mousePos[0]-self.x)//26
        gridY = (mousePos[1]-self.y)//26
        if gridX >= MAPSIZE:
            gridX = MAPSIZE-1
        elif gridX <= 0:
            gridX = 0
        if gridY >= MAPSIZE:
            gridY = MAPSIZE-1
        elif gridY <= 0:
            gridY = 0
        if absloc:
            gridX *= 26
            gridY *= 26
        # to prevent crashes or blocks out of grid when clicking on outlines
        return gridX, gridY

    def onGrid(self, mousePos):
        if self.rect.collidepoint(mousePos):
            return True
        return False

class GridBlock:
    
    def __init__(self, x, y, size, block, surface, absloc):
        self.x = x
        self.y = y 
        self.left = 26*x+gridLeft+2
        self.top = 26*y+gridTop+2
        self.block = block
        self.size = size
        if absloc:
            self.left = x*24
            self.top  = y*24
            self.rect = pygame.Rect(self.left, self.top, 24*size[0], 24*size[1])
            self.image = surface.blit(images[block], [self.left, self.top])
        else:
            self.rect = pygame.Rect(self.left, self.top, 24*size[0]+2*(size[0]-1), 24*size[1]+2*(size[1]-1))
            self.image = surface.blit(images[block], [self.left+(size[0]-1) , self.top+(size[1]-1)])
        # print("%d %d, %d %d, %s" % (x, y, self.left, self.top, block))
    
    def delete(self, pos):
        if self.rect.collidepoint(pos):
            MapGrid(self.left-2, self.top-2, self.size[0], self.size[1], False)
            pygame.display.flip()
            print("Deleted %s at %d %d" % (self.block, self.x, self.y))
            del self
            return True
        return False
        
    def Saving(self):
        x = self.x
        y = self.y
        block = self.block
        del self
        return x, y, block
    
    def redraw(self):
        screen.blit(images[self.block], [self.left+(self.size[0]-1) , self.top+(self.size[1]-1)])

def mapSelector(files):
    frame = pygame.time.Clock()
    button = []
    buttonUp = True
    button.append( MapButton("Search", 0) )
    for count, file in enumerate(files):
        button.append( MapButton(file, count+1) )
    button.append( MapButton("New Map", len(button)) )
    file = ""
    moveStat = 0
    while (file not in files or file!="New Map" or file!="Search" or file!=None):
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                buttonUp = False
                if pos[0] > 1270:
                    file = None
                    break
                elif event.button == 1:
                    for each in button:
                        file = each.clicked(pos)
                        if file in files or file=="New Map" or file=="Search":
                            break
                elif event.button == 4 and moveStat<5:
                    moveStat += 2
                elif event.button == 5 and moveStat>-5:
                    moveStat -= 2
            while (not buttonUp):
                for eventT in pygame.event.get():    
                    if eventT.type == pygame.MOUSEBUTTONUP:
                        buttonUp = True
        if moveStat==0:
            for each in button:
                if each.blink(pos):
                    break
        screen.fill(BACKGROUND)
        for each in button:
            each.rect.move_ip(0,8*moveStat)
            screen.blit(each.surface, each.rect)
        
        if moveStat>0:
            moveStat-=1
        elif moveStat<0:
            moveStat+=1
        
        if file in files or file == "New Map" or file == "Search" or file == None:
            break
        pygame.display.flip()
        frame.tick(60)
    screen.fill(BACKGROUND)
    return file

def textBlock(title,createMap):
    font = pygame.font.Font(None, 128)
    clock = pygame.time.Clock()
    input_box = pygame.Rect(100, 295, 1000, 128)
    text = ''
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    running = False
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode

        screen.fill(BACKGROUND)
        width = max(500, font.render(text, True, WHITE).get_width()+10)
        input_box.w = width
        if title == "Enter new map name":
            screen.blit(pygame.font.Font(None, 64).render("if map exists, data will be cleared.", True, WHITE),\
            [input_box.x+5, input_box.y-83])
        screen.blit(font.render(text, True, WHITE), [input_box.x+5, input_box.y+5])
        screen.blit(font.render(title, True, WHITE), [input_box.x+5, input_box.y-200])
        pygame.draw.rect(screen, WHITE, input_box, 2)

        pygame.display.flip()
        clock.tick(30)
    screen.fill(BACKGROUND)
    if createMap:
        with open("emptyMap.idk", "r") as emptyMap:
            with open(text+".json", "w+") as newFile:
                newFile.write(emptyMap.read())
    return text


if __name__ == "__main__":
    main()
    pygame.quit()
    input("\n\nPress Enter to quit")
