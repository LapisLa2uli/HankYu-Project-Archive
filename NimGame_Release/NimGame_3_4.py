# NimGame 3.4

"""
Collaborative Project by 124, Lapiz Lazuli, and tr1somy

We aim to:
1) Create a functional pygame program that can process both win-con classification, best choice making, and pvp (including 2 piles, 3 piles, or more!)
2) Dive deeper in search of algorithms for even larger number of piles
3) Have fun!
"""

import pygame, sys, time, math, numpy, random
import NimShooting_1_2 as ns1
import NimLottery_1_2 as nl1
import NimAnalysis_1_1 as na1
import NimComputer_1_1 as nc1

SCREEN_W, SCREEN_H = 1024, 768

class homeFW(object):
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.cFrame = pygame.image.load('choice_frame.png')
        self.cFrame = pygame.transform.scale(self.cFrame, (SCREEN_W // 4, SCREEN_H // 2))
        self.cFrame.set_colorkey((255, 255, 255))
        self.bg1 = pygame.image.load('bg1.jpg')
        self.bg1 = pygame.transform.scale(self.bg1, (SCREEN_W, SCREEN_H))
        self.pvp_pic = pygame.image.load('pvp_pic.png')
        self.pvp_pic = pygame.transform.scale(self.pvp_pic, (SCREEN_W // 6, SCREEN_W // 6))
        self.pvp_pic.set_colorkey((255, 255, 255))
        self.pvc_pic = pygame.image.load('pvc_pic.png')
        self.pvc_pic = pygame.transform.scale(self.pvc_pic, (SCREEN_W // 6, SCREEN_W // 6))
        self.pvc_pic.set_colorkey((255, 255, 255))
        self.ana_pic = pygame.image.load('ana_pic.png')
        self.ana_pic = pygame.transform.scale(self.ana_pic, (SCREEN_W // 6, SCREEN_W // 6))
        self.ana_pic.set_colorkey((0, 0, 0))
        self.font = pygame.font.Font('PixelatedEleganceRegular-ovyAA.ttf', 42)
        self.font2 = pygame.font.Font('Copyduck.ttf', 100)
        self.font3 = pygame.font.Font('Copyduck.ttf', 60)
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        self.font4 = pygame.font.Font('PixelatedEleganceRegular-ovyAA.ttf', 26)
        self.font5 = pygame.font.Font('Copyduck.ttf', 40)

    def play(self):
        self.screen.blit(self.bg1, (0, 0))
        self.screen.blit(self.font2.render("<NimGame V3.4>", True, (232, 184, 56)), ((SCREEN_W - self.font2.size("<NimGame V3.4>")[0]) // 2, SCREEN_H // 10))
        self.screen.blit(self.font.render("SELECT A MODE", True, (162, 170, 243)), ((SCREEN_W - self.font.size("SELECT A MODE")[0]) // 2, SCREEN_H * 2 // 7))
        self.screen.blit(self.cFrame, (SCREEN_W // 16, SCREEN_H * 2 // 5))
        self.screen.blit(self.cFrame, (SCREEN_W * 6 // 16, SCREEN_H * 2 // 5))
        self.screen.blit(self.cFrame, (SCREEN_W * 11 // 16, SCREEN_H * 2 // 5))
        
        self.screen.blit(self.pvp_pic, (SCREEN_W * 5 // 48, SCREEN_H * 3 // 7))
        self.screen.blit(self.pvc_pic, (SCREEN_W * 20 // 48, SCREEN_H * 3 // 7))
        self.screen.blit(self.ana_pic, (SCREEN_W * 35 // 48, SCREEN_H * 3 // 7))
        
        self.screen.blit(self.font3.render("PVP", True, (219, 55, 51)), (SCREEN_W // 16 + (SCREEN_W // 4 - self.font3.size("PVP")[0]) // 2, SCREEN_H * 2 // 3))
        self.screen.blit(self.font3.render("PVC", True, (33, 37, 190)), (SCREEN_W * 6 // 16 + (SCREEN_W // 4 - self.font3.size("PVC")[0]) // 2, SCREEN_H * 2 // 3))
        self.screen.blit(self.font5.render("Analysis", True, (22, 124, 25)), (SCREEN_W * 11 // 16 + (SCREEN_W // 4 - self.font5.size("Analysis")[0]) // 2, SCREEN_H * 41 // 60))
        
        self.screen.blit(self.font4.render("Press '1'", True, (179, 45, 44)), (SCREEN_W // 16 + (SCREEN_W // 4 - self.font4.size("Press '1'")[0]) // 2, SCREEN_H * 47 // 60))
        self.screen.blit(self.font4.render("to play", True, (179, 45, 44)), (SCREEN_W // 16 + (SCREEN_W // 4 - self.font4.size("to play")[0]) // 2, SCREEN_H * 49 // 60))
        self.screen.blit(self.font4.render("Press '2'", True, (24, 29, 157)), (SCREEN_W * 6 // 16 + (SCREEN_W // 4 - self.font4.size("Press '2'")[0]) // 2, SCREEN_H * 47 // 60))
        self.screen.blit(self.font4.render("to play", True, (24, 29, 157)), (SCREEN_W * 6 // 16 + (SCREEN_W // 4 - self.font4.size("to play")[0]) // 2, SCREEN_H * 49 // 60))
        self.screen.blit(self.font4.render("Press '3'", True, (29, 166, 31)), (SCREEN_W * 11 // 16 + (SCREEN_W // 4 - self.font4.size("Press '3'")[0]) // 2, SCREEN_H * 47 // 60))
        self.screen.blit(self.font4.render("to play", True, (29, 166, 31)), (SCREEN_W * 11 // 16 + (SCREEN_W // 4 - self.font4.size("to play")[0]) // 2, SCREEN_H * 49 // 60))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return -1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 1
                elif event.key == pygame.K_2:
                    return 2
                elif event.key == pygame.K_3:
                    return 3
        pygame.display.update()
        self.clock.tick(500)

        return 0

class pvpFW(object):
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        self.pList = []
        self.font = pygame.font.Font('PixelatedEleganceRegular-ovyAA.ttf', 42)
        self.font2 = pygame.font.Font('PixelatedEleganceRegular-ovyAA.ttf', 52)
        self.font3 = pygame.font.Font('PixelatedEleganceRegular-ovyAA.ttf', 36)
        self.playerNum = 0
        self.pileNum = 0
        self.cPlayer = 0
        self.winPlayer = 0
        self.stoneNum = 0
        self.clock = pygame.time.Clock()
        self.infoIndex = 0
        self.crtList1 = ['0'] * 6
        self.crtList2 = ['0'] * 2
        self.crtList3 = ['0'] * 2
        self.pileNumLimit = 40 # To be Modified
        self.stoneNumLimit = 60 # To be Modified
        self.triggerLimitFlag = 0
        self.tlft = 0
        self.triggerStoneFlag = 0
        self.tsft = 0
        self.triggerZeroFlag = 0
        self.tzft = 0
        self.stat = 0

    def get_info(self):
        self.screen.fill((0, 0, 0))
        if self.stat == 0:
            self.screen.blit(self.font.render("Enter number of players:", True, (255, 255, 150)), \
                             ((SCREEN_W - self.font.size("Enter number of players:")[0]) // 2, 10))
        elif self.stat == 1:
            self.screen.blit(self.font.render("Enter number of piles:", True, (255, 255, 150)), \
                             ((SCREEN_W - self.font.size("Enter number of piles:")[0]) // 2, 10))
        elif self.stat == 2:
            self.screen.blit(self.font.render(f"Enter number of stones in pile {self.infoIndex + 1}:", True, (255, 255, 150)), \
                             ((SCREEN_W - self.font.size(f"Enter number of stones in pile {self.infoIndex + 1}:")[0]) // 2, 10))
            
        self.screen.blit(self.font.render("Press esc to return to homepage", True, (255, 255, 150)), \
                             ((SCREEN_W - self.font.size("Press esc to return to homepage")[0]) // 2, SCREEN_H - 55))

        if self.stat == 0:
            self.screen.blit(self.font.render(' '.join(self.crtList1), True, (255, 255, 255)), \
                             ((SCREEN_W - self.font.size(' '.join(self.crtList1))[0]) // 2, (SCREEN_H - self.font.size(' '.join(self.crtList1))[1]) // 2))
        elif self.stat == 1:
            self.screen.blit(self.font.render(' '.join(self.crtList2), True, (255, 255, 255)), \
                             ((SCREEN_W - self.font.size(' '.join(self.crtList2))[0]) // 2, (SCREEN_H - self.font.size(' '.join(self.crtList2))[1]) // 2))
        elif self.stat == 2:
            self.screen.blit(self.font.render(' '.join(self.crtList3), True, (255, 255, 255)), \
                             ((SCREEN_W - self.font.size(' '.join(self.crtList3))[0]) // 2, (SCREEN_H - self.font.size(' '.join(self.crtList3))[1]) // 2))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return -1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return -2
                if event.key <= ord('9') and event.key >= ord('0'):
                    if self.stat == 0:
                        if self.crtList1[0] != '0':
                            continue
                        self.crtList1 = self.crtList1[1:] + [chr(event.key)]
                    if self.stat == 1:
                        if self.crtList2[0] != '0':
                            continue
                        self.crtList2 = self.crtList2[1:] + [chr(event.key)]
                    if self.stat == 2:
                        if self.crtList3[0] != '0':
                            continue
                        self.crtList3 = self.crtList3[1:] + [chr(event.key)]
                if event.key == pygame.K_BACKSPACE:
                    if self.stat == 0:
                        self.crtList1 = ['0'] + self.crtList1[:-1]
                    if self.stat == 1:
                        self.crtList2 = ['0'] + self.crtList2[:-1]
                    if self.stat == 2:
                        self.crtList3 = ['0'] + self.crtList3[:-1]
                if event.key == pygame.K_RETURN:
                    if self.stat == 0:
                        self.playerNum = int(''.join(self.crtList1))
                        if self.playerNum == 0:
                            self.triggerZeroFlag = 1
                            continue
                        self.stat = 1
                    elif self.stat == 1:
                        self.pileNum = int(''.join(self.crtList2))
                        if self.pileNum == 0:
                            self.triggerZeroFlag = 1
                            continue
                        if self.pileNum > self.pileNumLimit:
                            self.triggerLimitFlag = 1
                            continue
                        self.stat = 2
                    elif self.stat == 2:
                        self.stoneNum = int(''.join(self.crtList3))
                        if self.stoneNum > self.stoneNumLimit:
                            self.triggerStoneFlag = 1
                            continue
                        self.pList.append(self.stoneNum)
                        self.crtList3 = ['0'] * 2
                        if self.infoIndex == self.pileNum - 1:
                            return 1
                        self.infoIndex += 1

        if self.triggerLimitFlag == 1:
            if self.tlft == 0:
                self.tlft = time.time()
            if time.time() - self.tlft > 1:
                self.triggerLimitFlag = 0
                self.tlft = 0
            else:
                self.screen.blit(self.font.render("Too Many Piles!", True, (255, 150, 150)), \
                             ((SCREEN_W - self.font.size("Too Many Piles!")[0]) // 2, (SCREEN_H - self.font.size("Too Many Piles!")[1]) // 2))
        if self.triggerZeroFlag == 1:
            if self.tzft == 0:
                self.tzft = time.time()
            if time.time() - self.tzft > 1:
                self.triggerZeroFlag = 0
                self.tzft = 0
            else:
                self.screen.blit(self.font.render("Enter A Number!", True, (255, 150, 150)), \
                             ((SCREEN_W - self.font.size("Enter A Number!")[0]) // 2, (SCREEN_H - self.font.size("Enter A Number!")[1]) // 2))
        if self.triggerStoneFlag == 1:
            if self.tsft == 0:
                self.tsft = time.time()
            if time.time() - self.tsft > 1:
                self.triggerStoneFlag = 0
                self.tsft = 0
            else:
                self.screen.blit(self.font.render("Too Many Stones!", True, (255, 150, 150)), \
                             ((SCREEN_W - self.font.size("Too Many Stones!")[0]) // 2, (SCREEN_H - self.font.size("Too Many Stones!!")[1]) // 2))
        
        pygame.display.update()
        self.clock.tick(500)
        return 0

    def win(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.font2.render(f"Player {self.winPlayer + 1} won!", True, (120, 150, 255)), \
                         ((SCREEN_W - self.font2.size(f"Player {self.winPlayer + 1} won!")[0]) // 2, SCREEN_H * 2 // 5))
        self.screen.blit(self.font3.render("Press Enter to return to homepage", True, (255, 230, 150)), \
                         ((SCREEN_W - self.font3.size("Press Enter to return to homepage")[0]) // 2, SCREEN_H * 3 // 5))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return -1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return 1
                
        pygame.display.update()
        self.clock.tick(500)
        return 0

    def play(self):
        statusGI = 0
        while statusGI == 0:
            statusGI = self.get_info()
        if statusGI == -1:
            sys.exit()
        if statusGI == -2:
            return
        while self.pList != [0] * len(self.pList):
            nlFW = nl1.NimLotteryFW(self.pList)
            statusNL = -1
            while statusNL == -1:
                statusNL = nlFW.play(self.cPlayer)
            if statusNL == -2:
                sys.exit()
            if statusNL == -3:
                return
            pIndex = statusNL
            tDiskNum = self.pList[pIndex]
            nsFW = ns1.NimShootingFW(tDiskNum, pIndex)
            statusNS = -2
            while statusNS == -2:
                statusNS = nsFW.play(self.cPlayer)
            if statusNS == -1:
                sys.exit()
            if statusNS == -3:
                return
            self.pList[pIndex] = self.pList[pIndex] - statusNS
            self.cPlayer = (self.cPlayer + 1) % self.playerNum
        self.winPlayer = (self.cPlayer - 1) % self.playerNum
        statusWin = 0
        while statusWin == 0:
            statusWin = self.win()
        if statusWin == -1:
            sys.exit()

class pvcFW(object):
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))

    def play(self):
        statusNC = 0
        ncFL = nc1.NimComputerFW()
        while statusNC == 0:
            statusNC = ncFL.play()
        if statusNC == -1:
            sys.exit()
    

class anaFW(object):
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))

    def play(self):
        statusNA = 0
        naFL = na1.NimAnalysisFW()
        while statusNA == 0:
            statusNA = naFL.play()
        if statusNA == -1:
            sys.exit()
        

# ----- MAIN -----
pygame.init()
while True:
    pygame.mouse.set_visible(True)
    homeFrame = homeFW()
    statHome = 0
    while statHome == 0:
        statHome = homeFrame.play()
    if statHome == -1:
        break
    if statHome == 1:
        pvpFrame = pvpFW()
        pvpFrame.play()
    elif statHome == 2:
        pvcFrame = pvcFW()
        pvcFrame.play()
    elif statHome == 3:
        anaFrame = anaFW()
        anaFrame.play()
