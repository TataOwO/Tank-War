import pygame
import wall
import myTank
import enemyTank
import json
import mapSelector

def main():
    
    pygame.init()
    pygame.mixer.init()
    
    GameStatus = 1
    
    while GameStatus:
        
        background_image     = pygame.image.load("image/background.png")
        gameover_image       = pygame.image.load("image/gameover.png")
        title_image          = pygame.image.load("image/title.png")
        originalGameOver_image = gameover_image

        start = pygame.mixer.Sound("music\\start.wav")
        bang = pygame.mixer.Sound("music\\bang.wav")
        blast = pygame.mixer.Sound("music\\blast.wav")
        enemyfire = pygame.mixer.Sound("music\\fire.wav")
        playerfire = pygame.mixer.Sound("music\\Gunfire.wav")
        hit = pygame.mixer.Sound("music\\hit.wav")
        iron_hit = pygame.mixer.Sound("music\\iron_hit.wav")
        player_hit = pygame.mixer.Sound("music\\player_hit.wav")
        game_over = pygame.mixer.Sound("music\\game_over.wav")
        
        resolution = 630, 660
        screen = pygame.display.set_mode(resolution)
        pygame.display.set_caption("Tank War")
        
        RED = pygame.Color(255, 0, 0)
        WHITE = pygame.Color(255, 255, 255)
        font = pygame.font.SysFont('arial', 24)
        menuFont = pygame.font.SysFont('arial', 36)
        scoreFont = pygame.font.SysFont('arial', 30)
        
        allTankGroup     = pygame.sprite.Group()
        mytankGroup      = pygame.sprite.Group()
        allEnemyGroup    = pygame.sprite.Group() 
        enemyBulletGroup = pygame.sprite.Group()
        noGroup          = pygame.sprite.Group()
        
        bgMap = wall.Map()
        bgSelector = mapSelector.Selector(screen, GameStatus)

        DELAYEVENT = pygame.constants.USEREVENT
        pygame.time.set_timer(DELAYEVENT, 200)

        ENEMYBULLETNOTCOOLINGEVENT = pygame.constants.USEREVENT + 1
        pygame.time.set_timer(ENEMYBULLETNOTCOOLINGEVENT, 1000)

        MYBULLETNOTCOOLINGEVENT = pygame.constants.USEREVENT + 2
        pygame.time.set_timer(MYBULLETNOTCOOLINGEVENT, 200)
       
        NOTMOVEEVENT = pygame.constants.USEREVENT + 3
        pygame.time.set_timer(NOTMOVEEVENT, 8000)
        
        time = 0
        minute = 3
        second = 0
        moving = 0
        movdir = 0
        myTankData = None
        enemyData = None
        enemyCouldMove      = True
        running_T1          = True
        clock = pygame.time.Clock()
        score = 0
        onIce = False
        deathPause = 0
        GameEnd = False
        fontDelay = 0
        drawFont = True
        menu = True
        running = False
        selector = True
        current = 1
        
        lssh = ["","","",""]
        while menu:
            lLetter = pygame.Rect([[351,260] , [18,19]])
            sLetter = pygame.Rect([[541,255] , [18,18]])
            hLetter = pygame.Rect([[243,263] , [18,18]])
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    menu = False
                    GameStatus = 0
                    break
                elif event.type == pygame.KEYDOWN:
                    menu = False
                    running = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    lssh.pop(0)
                    if lLetter.collidepoint(pos):
                        lssh.append("l")
                    elif sLetter.collidepoint(pos):
                        lssh.append("s")
                    elif hLetter.collidepoint(pos):
                        lssh.append("h")
                    else:
                        lssh.append("")
            screen.blit(title_image, (0, 0))
            if (drawFont%2==0):
                screen.blit(menuFont.render("press any key to start", True, WHITE, None), (3 + 10 * 12, 3 + 21 * 24 ))
            drawFont = not drawFont
            pygame.display.flip()
            if lssh==["l","s","s","h"]:
                GameStatus = 2
                menu = False
            clock.tick(10)
        
        screen.fill(pygame.Color(0,0,0))
        
        if running: # Map Selector
            stat = 0
            movin = 0
            mousewait = 0
            selectedMap = None
            waited = False
            for index in bgSelector.mapGroup:
                screen.blit(index.surface, (index.left, index.top))
            pygame.display.flip()
            while selector:
                pos = pygame.mouse.get_pos()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        selector = False
                        running = False
                        GameStatus = 0
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 4 and bgSelector.mapGroup[0].left != 157 and movin == 0:
                            movin = 40
                            stat = 4
                            current += 1
                            mousewait = 8
                        elif event.button == 5 and bgSelector.mapGroup[len(bgSelector.mapGroup)-1].left != 157 and movin == 0:
                            movin = 40
                            stat = 5
                            current -= 1
                            mousewait = 8
                        if event.button == 1:
                            for index in bgSelector.mapGroup:
                                selectedMap = index.click(pos)
                                if selectedMap != None:
                                    myTankData, enemyData = bgMap.loadMap(selectedMap, GameStatus)
                                    selector = False
                                    break
                if movin > 0:
                    if mousewait == 0:
                        screen.fill(pygame.Color(0,0,0))
                        if stat == 4:
                            for index in bgSelector.mapGroup:
                                index.move_right()
                            movin -= 1
                        elif stat == 5:
                            for index in bgSelector.mapGroup:
                                index.move_left()
                            movin -= 1
                        waited = True
                    else:
                        mousewait -= 1
                else:
                    for each in bgSelector.mapGroup:
                        if each.blink(pos):
                            break
                    stat = 0
                
                pygame.display.flip()
                clock.tick(60)

        start.play()

        myTank_T1 = myTank.MyTank(myTankData["X"],myTankData["Y"])
        allTankGroup.add(myTank_T1)
        mytankGroup.add(myTank_T1)

        for i in range(1, len(enemyData["X"])+1):
            enemy = enemyTank.EnemyTank(enemyData, i)
            allTankGroup.add(enemy)
            allEnemyGroup.add(enemy)
        enemyNumber = len(enemyData["X"])

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    GameStatus = 0
                if event.type == MYBULLETNOTCOOLINGEVENT:
                    myTank_T1.bulletNotCooling = True

                if event.type == ENEMYBULLETNOTCOOLINGEVENT:
                    for each in allEnemyGroup:
                        each.bulletNotCooling = True

                if event.type == NOTMOVEEVENT:
                    enemyCouldMove = True
                
                if event.type == DELAYEVENT:
                    if enemyNumber < len(enemyData["X"])+1:
                        enemy = enemyTank.EnemyTank(enemyData)
                        if pygame.sprite.spritecollide(enemy, allTankGroup, False, None):
                            break
                        allEnemyGroup.add(enemy)
                        allTankGroup.add(enemy)
                        enemyNumber += 1
            
            key_pressed = pygame.key.get_pressed()

            if moving: 
                allTankGroup.remove(myTank_T1)
                if myTank_T1.moveTank(allTankGroup, bgMap.brickGroup, bgMap.ironGroup, bgMap.riverGroup, bgMap.baseGroup, movdir, False) \
                    or onIce != myTank_T1.onIce(bgMap.iceGroup, movdir) and onIce:
                    moving = 0
                elif not myTank_T1.onIce(bgMap.iceGroup, movdir):
                    moving -= 1
                elif onIce:
                    moving = 1
                if moving == 0:
                    if (movdir == 0 or movdir ==1) and myTank_T1.rect.top%24!=3:
                        moving = 1
                    elif (movdir == 2 or movdir == 3) and myTank_T1.rect.left%24!=3:
                        moving = 1
                onIce = myTank_T1.onIce(bgMap.iceGroup, movdir)
                allTankGroup.add(myTank_T1)
                running_T1 = True
                print(int(moving))
                
            if not moving:
                if key_pressed[pygame.K_w]: 
                    onIce = myTank_T1.onIce(bgMap.iceGroup, 0) #
                    movdir = myTank_T1.pdir
                    allTankGroup.remove(myTank_T1)
                    if myTank_T1.moveTank(allTankGroup, bgMap.brickGroup, bgMap.ironGroup, bgMap.riverGroup, bgMap.baseGroup , movdir, False):
                        if onIce:
                            moving = 24/myTank_T1.speed-1
                            myTank_T1.pdir = movdir = 0 #
                    else:
                        moving = 24/myTank_T1.speed-1
                        if onIce:
                            myTank_T1.pdir = movdir = 0 #
                    running_T1 = True
                    myTank_T1.moveUp(allTankGroup, bgMap.brickGroup, bgMap.ironGroup, bgMap.riverGroup, bgMap.baseGroup, True)
                    allTankGroup.add(myTank_T1)
                    print("Pressed UP")
                    print(int(moving))
                elif key_pressed[pygame.K_s]:
                    onIce = myTank_T1.onIce(bgMap.iceGroup, 1) #
                    movdir = myTank_T1.pdir
                    allTankGroup.remove(myTank_T1)
                    if myTank_T1.moveTank(allTankGroup, bgMap.brickGroup, bgMap.ironGroup, bgMap.riverGroup, bgMap.baseGroup, movdir, False):
                        if onIce:
                            moving = 24/myTank_T1.speed-1
                            myTank_T1.pdir = movdir = 1 #
                    else:
                        moving = 24/myTank_T1.speed-1
                        if onIce:
                            myTank_T1.pdir = movdir = 1 #
                    running_T1 = True
                    myTank_T1.moveDown(allTankGroup, bgMap.brickGroup, bgMap.ironGroup, bgMap.riverGroup, bgMap.baseGroup, True)
                    allTankGroup.add(myTank_T1)
                    print("Pressed DOWN")
                    print(int(moving))
                elif key_pressed[pygame.K_a]:
                    onIce = myTank_T1.onIce(bgMap.iceGroup, 2) #
                    movdir = myTank_T1.pdir
                    allTankGroup.remove(myTank_T1)
                    if myTank_T1.moveTank(allTankGroup, bgMap.brickGroup, bgMap.ironGroup, bgMap.riverGroup, bgMap.baseGroup, movdir, False):
                        if onIce:
                            moving = 24/myTank_T1.speed-1
                            myTank_T1.pdir = movdir = 2 #
                    else:
                        moving = 24/myTank_T1.speed-1
                        if onIce:
                            myTank_T1.pdir = movdir = 2 #
                    running_T1 = True
                    myTank_T1.moveLeft(allTankGroup, bgMap.brickGroup, bgMap.ironGroup, bgMap.riverGroup, bgMap.baseGroup, True)
                    allTankGroup.add(myTank_T1)
                    print("Pressed LEFT")
                    print(int(moving))
                elif key_pressed[pygame.K_d]:
                    onIce = myTank_T1.onIce(bgMap.iceGroup, 3) #
                    movdir = myTank_T1.pdir
                    allTankGroup.remove(myTank_T1)
                    if myTank_T1.moveTank(allTankGroup, bgMap.brickGroup, bgMap.ironGroup, bgMap.riverGroup, bgMap.baseGroup, movdir, False):
                        if onIce:
                            moving = 24/myTank_T1.speed-1
                            myTank_T1.pdir = movdir = 3 #
                    else:
                        moving = 24/myTank_T1.speed-1
                        if onIce:
                            myTank_T1.pdir = movdir = 3 #
                    running_T1 = True
                    myTank_T1.moveRight(allTankGroup, bgMap.brickGroup, bgMap.ironGroup, bgMap.riverGroup, bgMap.baseGroup, True)
                    allTankGroup.add(myTank_T1)
                    print("Pressed RIGHT")
                    print(int(moving))
            if key_pressed[pygame.K_j]:
                if not myTank_T1.bullet.life and myTank_T1.bulletNotCooling:
                    myTank_T1.shoot()
                    playerfire.play()
                    myTank_T1.bulletNotCooling = False
            
            screen.fill(pygame.Color(0,0,0))
            screen.blit(background_image, (0, 0))
            if second>=10:
                screen.blit(scoreFont.render(str(minute)+":"+str(second)+"          LIVES: "+str(myTank_T1.life)+"           SCORE: "+str(score),\
                True, WHITE, None), [0,630])
            else:
                screen.blit(scoreFont.render(str(minute)+":0"+str(second)+"          LIVES: "+str(myTank_T1.life)+"           SCORE: "+str(score),\
                True, WHITE, None), [0,630])
            for each in bgMap.brickGroup:
                screen.blit(each.image, each.rect)
            for each in bgMap.ironGroup:
                screen.blit(each.image, each.rect)
            for each in bgMap.riverGroup:
                screen.blit(each.image, each.rect)
            for each in bgMap.iceGroup:
                screen.blit(each.image, each.rect)
            for each in bgMap.baseGroup:
                screen.blit(each.image, each.rect)
            

            screen.blit(myTank_T1.tank_R0, (myTank_T1.rect.left, myTank_T1.rect.top))

            for each in allEnemyGroup:      
                screen.blit(each.tank_R0, (each.rect.left, each.rect.top))
                if enemyCouldMove:
                    allTankGroup.remove(each)
                    each.move(allTankGroup, bgMap.brickGroup, bgMap.ironGroup, bgMap.riverGroup, bgMap.iceGroup)
                    allTankGroup.add(each)                 

            if myTank_T1.bullet.life:
                myTank_T1.bullet.move()    
                screen.blit(myTank_T1.bullet.bullet, myTank_T1.bullet.rect)
                brickCount = len(bgMap.brickGroup)
                
                for bases in bgMap.baseGroup:
                    if pygame.sprite.collide_rect(myTank_T1.bullet, bases):
                        GameEnd = 1
                        running = False
                        break
                
                for each in enemyBulletGroup:
                    if each.life:
                        if pygame.sprite.collide_rect(myTank_T1.bullet, each):
                            myTank_T1.bullet.life = False
                            each.life = False
                            pygame.sprite.spritecollide(myTank_T1.bullet, enemyBulletGroup, True, None)
                            score += 5
                if pygame.sprite.spritecollide(myTank_T1.bullet, allEnemyGroup, True, None):
                    bang.play()
                    enemyNumber -= 1
                    myTank_T1.bullet.life = False
                    score += 100

                if pygame.sprite.spritecollide(myTank_T1.bullet, bgMap.brickGroup, True, None):
                    hit.play()
                    myTank_T1.bullet.life = False
                    myTank_T1.bullet.rect.left, myTank_T1.bullet.rect.right = 3 + 12 * 24, 3 + 24 * 24
                    score += brickCount - len(bgMap.brickGroup)

                if pygame.sprite.spritecollide(myTank_T1.bullet, bgMap.ironGroup, False, None):
                    iron_hit.play()
                    myTank_T1.bullet.life = False
                    myTank_T1.bullet.rect.left, myTank_T1.bullet.rect.right = 3 + 12 * 24, 3 + 24 * 24
                
            for each in allEnemyGroup:

                if not each.bullet.life and each.bulletNotCooling and enemyCouldMove:
                    enemyBulletGroup.remove(each.bullet)
                    each.shoot()
                    enemyBulletGroup.add(each.bullet)
                    each.bulletNotCooling = False

                if each.bullet.life:
                    if enemyCouldMove:
                        each.bullet.move()
                    screen.blit(each.bullet.bullet, each.bullet.rect)
                    
                    for bases in bgMap.baseGroup:
                        if pygame.sprite.collide_rect(each.bullet, bases):
                            GameEnd = 2
                            running = False
                            break
                    if myTank_T1.life == 0:
                        GameEnd = 3
                        running = False
                    if pygame.sprite.collide_rect(each.bullet, myTank_T1):
                        player_hit.play()
                        myTank_T1.life -= 1
                        score -= 300
                        myTank_T1.rect.left, myTank_T1.rect.top = 3 + 12 * 24, 3 + 20 * 24 
                        each.bullet.life = False
                        moving = 0 

                    if pygame.sprite.spritecollide(each.bullet, bgMap.brickGroup, True, None):
                            hit.play()
                            each.bullet.life = False
                    
                    if pygame.sprite.spritecollide(each.bullet, bgMap.ironGroup, False, None):
                            iron_hit.play()
                            each.bullet.life = False
            time += 1
            if minute<=0 and second<=0:
                GameEnd = 4
                running = False
            if time%60==0:
                second -= 1
            if second < 0:
                minute -= 1
                second = 59
            pygame.display.flip()
            clock.tick(60)
        
        if GameEnd:
            gmLeft = 283
            gmTop = 299
            gmWidth = 64
            gmLength = 32
            exitStat = ""
            if GameEnd == 1:
                exitStat = "You destroyed you base!"
            elif GameEnd == 2:
                exitStat = "The enemies destroyed your base!"
            elif GameEnd == 3:
                exitStat = "Your HP reached 0!"
            elif GameEnd == 4:
                exitStat = "Time's up!"
            for a in range(30):
                clock.tick(60)
            screen.blit(bgMap.base.broke, bgMap.base.rect)
            pygame.display.flip()
            game_over.play()
            screen.blit(background_image, (0, 0))
            pygame.display.flip()
            while GameEnd:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        GameStatus = 0
                        GameEnd = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        running = False
                        GameEnd = False
                        GameStatus = 1
                if (gmLeft >= 0):
                    screen.fill([0, 0, 0])
                    screen.blit(gameover_image, (int(gmLeft), int(gmTop)))
                    pygame.display.flip()

                    gmLength = int(gmLength*1.07)
                    gmWidth = gmLength * 2
                    gameover_image = pygame.transform.scale(originalGameOver_image, (gmWidth, gmLength))
                    gmLeft = (630 - gmWidth) / 2
                    gmTop = (630 - gmLength) / 2

                    pygame.time.delay(100)
                else:
                    screen.blit(font.render(exitStat, True, RED, None), (3 + 26 * 5, 3 + 21 * 24 ))
                    screen.blit(font.render("Your final score: " + str(score), True, RED, None), (3+26*5, 3+22*24))
                    screen.blit(font.render("Click to restart...", True, RED, None), (3+26*5, 3+24*24))
                    pygame.display.flip()
                clock.tick(60)
                pygame.display.flip()
        if GameStatus:
            print("restarting the game...")
        else:
            return 0

if __name__ == '__main__':
    main()
    pygame.mixer.quit()
    pygame.quit()
