# NimGame Lottery Version 1.1

import pygame, sys, random, numpy, math, time

SCREEN_W, SCREEN_H = 1024, 768

class CLS_pile(object):
    def __init__(self, pI, maxNum, pileNum, stoneNum, light):
        self.pI = pI
        self.pileNum = pileNum
        self.x = SCREEN_W // 12 + pI * SCREEN_W * 5 // 6 // self.pileNum
        self.stoneNum = stoneNum
        self.light = light
        self.pdColor = (230, 230, 50)
        self.maxNum = maxNum
        self.font = pygame.font.Font('PixelatedEleganceRegular-ovyAA.ttf', 52 - self.pileNum)

    def draw(self, scr):
        if self.light == 0:
            self.pdColor = (130, 130, 30)
            if self.stoneNum == 0:
                self.pdColor = (100, 100, 20)
        elif self.light == -1:
            self.pdColor = (230, 230, 50)
            if self.stoneNum == 0:
                self.pdColor = (100, 100, 20)
        else:
            self.pdColor = (230, 230, 50)
        for stone in range(1, self.stoneNum + 1):
            pygame.draw.ellipse(scr, (150, 150, 150), \
                                pygame.Rect(self.x + 3, SCREEN_H * 4 // 5 - stone * min(SCREEN_H * 7 // 10 // self.maxNum, (SCREEN_W * 5 // 6 // self.pileNum - 6) * 0.7) + 1, \
                                 SCREEN_W * 5 // 6 // self.pileNum - 6, min(SCREEN_H * 7 // 10 // self.maxNum - 2, (SCREEN_W * 5 // 6 // self.pileNum - 6) * 0.7 - 2)), \
                                0)
        pygame.draw.rect(scr, (170, 130, 30), (self.x + 1, SCREEN_H * 7 // 8, SCREEN_W * 5 // 6 // self.pileNum - 2, SCREEN_H // 16))
        pygame.draw.rect(scr, self.pdColor, (self.x + 4, SCREEN_H * 7 // 8 + 3, SCREEN_W * 5 // 6 // self.pileNum - 8, SCREEN_H // 16 - 6))
        scr.blit(self.font.render(str(self.pI + 1), True, (0, 0, 0)), (self.x + (SCREEN_W * 5 // 6 // self.pileNum - self.font.size(str(self.pI + 1))[0]) // 2, SCREEN_H * 33 // 40))

class NimLotteryFW(object):
    def __init__(self, pList):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('PixelatedEleganceRegular-ovyAA.ttf', 32)
        self.font2 = pygame.font.Font('PixelatedEleganceRegular-ovyAA.ttf', 40)
        self.font3 = pygame.font.Font('PixelatedEleganceRegular-ovyAA.ttf', 48)
        self.font4 = pygame.font.Font('PixelatedEleganceRegular-ovyAA.ttf', 26)
        self.pList = pList
        self.pileNum = len(self.pList)
        self.maxNum = max(self.pList)
        self.newList = []
        
        for i in range(self.pileNum):
            if self.pList[i] != 0:
                self.newList.append(i)

        self.bg = pygame.Surface((1024,768))
        self.bg.fill((150, 180, 255))
        
        self.sf_frame = pygame.image.load('SF_frame.png')
        self.sf_w, self.sf_h = 800, 600
        self.sf_frame = pygame.transform.scale(self.sf_frame, (self.sf_w, self.sf_h))
        self.sf_frame.set_colorkey((255, 255, 255))

        self.piles = []
        for i in range(self.pileNum):
            newPile = CLS_pile(i, self.maxNum, self.pileNum, self.pList[i], -1)
            self.piles.append(newPile)
        self.pointer = random.randint(0, len(self.newList) - 1)
        self.spd = 0.05
        self.acc = -random.random() / 50000 - 0.00002
        self.stat = 0
        self.crtLight = 0
        self.endP = 0
        self.ctS = 0

    def play(self, cPlayer):
        self.screen.fill((150, 180, 255))
        self.screen.blit(self.bg,(0, 0))

        self.screen.blit(self.font.render(f"Player {cPlayer + 1}", True, (255, 50, 50)), (SCREEN_W - self.font.size(f"Player {cPlayer + 1}")[0] - 10, SCREEN_H - self.font.size(f"Player {cPlayer + 1}")[1] - 10))
        self.screen.blit(self.font4.render("Press esc to return to homepage", True, (255, 255, 150)), (15, SCREEN_H - 30))
        for p in self.piles:
            p.draw(self.screen)

        if len(self.newList) == 1:
            self.stat = 3
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return -2
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return -3
                if event.key == pygame.K_RETURN:
                    if self.stat == 0:
                        self.stat = 1
                    elif self.stat == 1:
                        self.stat = 2
                    elif self.stat == 3:
                        return self.newList[self.endP]
        if self.stat == 0:
            self.screen.blit(self.font.render("Press ENTER to start the pile lottery!", True, (20, 25, 80)), ((SCREEN_W - self.font.size("Press ENTER to start the pile lottery!")[0]) // 2, 10))
        if self.stat == 1:
            self.pointer += self.spd
            self.crtLight = int(self.pointer) % len(self.newList)
            self.screen.blit(self.font.render("Press ENTER to stop!", True, (20, 25, 80)), ((SCREEN_W - self.font.size("Press ENTER to stop!")[0]) // 2, 10))
        elif self.stat == 2:
            self.spd += self.acc
            if self.spd < 0:
                self.ctS = time.time()
                self.stat = 3
            else:
                self.pointer += self.spd
            self.crtLight = int(self.pointer) % len(self.newList)

        if self.stat != 0:
            for i in range(len(self.newList)):
                pI = self.newList[i]
                if self.crtLight == i:
                    self.piles[pI].light = 1
                else:
                    self.piles[pI].light = 0

        if self.stat == 3 and time.time() - self.ctS > 1:
            self.endP = self.crtLight
            self.screen.blit(self.sf_frame, ((SCREEN_W - self.sf_w) // 2, (SCREEN_H - self.sf_h) // 2))
            self.screen.blit(self.font3.render(f"You picked pile {self.newList[self.endP] + 1}!", True, (150, 150, 255)), ((SCREEN_W - self.font3.size(f"You picked pile {self.newList[self.endP] + 1}!")[0]) // 2, SCREEN_H * 2 // 5))
            self.screen.blit(self.font.render("Press Enter to Continue", True, (255, 150, 50)), ((SCREEN_W - self.font.size("Press Enter to Continue")[0]) // 2, SCREEN_H * 3 // 4))
        
        pygame.display.update()
        self.clock.tick(500)

        return -1
