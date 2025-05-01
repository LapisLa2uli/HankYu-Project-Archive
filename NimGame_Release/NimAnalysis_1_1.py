# NimAnalysis Version 1.1

import pygame, sys, random, numpy, math, time

SCREEN_W, SCREEN_H = 1024, 768

def find_sol(pList):
    k = 0
    sol = []
    for i in pList:
        k ^= i
    if k == 0:
        return sol
    for i in range(len(pList)):
        if k ^ pList[i] < pList[i]:
            p = i
            d = pList[i] - (k ^ pList[i])
            sol.append([p, d])
    sol = sorted(sol, key = lambda x : x[1])[::-1]
    return sol
        
class CLS_Button(object):
    def __init__(self, bType, x, y, pType):
        self.aButton = pygame.image.load('add_button.png')
        self.apButton = pygame.image.load('add_button_pressed.png')
        self.mButton = pygame.image.load('minus_button.png')
        self.mpButton = pygame.image.load('minus_button_pressed.png')

        self.aButton = pygame.transform.scale(self.aButton, (26, 26))
        self.apButton = pygame.transform.scale(self.apButton, (26, 26))
        self.mButton = pygame.transform.scale(self.mButton, (26, 26))
        self.mpButton = pygame.transform.scale(self.mpButton, (26, 26))
        
        self.aButton.set_colorkey((254, 254, 254))
        self.apButton.set_colorkey((254, 254, 254))
        self.mButton.set_colorkey((254, 254, 254))
        self.mpButton.set_colorkey((254, 254, 254))

        self.bType = bType
        self.x, self.y = x, y
        self.pType = pType
        if self.bType == 0:
            self.oPic = self.aButton
            self.pPic = self.apButton
        else:
            self.oPic = self.mButton
            self.pPic = self.mpButton

    def draw(self, scr):
        mX, mY = pygame.mouse.get_pos()
        if mX > self.x and mX < self.x + 26 and mY > self.y and mY < self.y + 26:
            scr.blit(self.pPic, (self.x, self.y))
        else:
            scr.blit(self.oPic, (self.x, self.y))
        
class NimAnalysisFW(object):
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        self.clock = pygame.time.Clock()
        
        self.font = pygame.font.Font('PixelatedEleganceRegular-ovyAA.ttf', 32)
        self.font2 = pygame.font.Font('PixelatedEleganceRegular-ovyAA.ttf', 26)

        self.pList = [1, 2, 4]
        self.colNum = (SCREEN_W - 300) // 60
        self.rowNum = (SCREEN_H - 285) // 35
        self.pageNum = (len(self.pList) - 1) // self.colNum + 1
        self.pageCrt = 0
        self.sol = []
        self.spCrt = 0
        
    def play(self):
        self.screen.fill((25, 42, 99))
        self.screen.blit(self.font.render('Press esc to return to homepage', True, (237, 219, 65)), ((SCREEN_W - self.font.size('Press esc to return to homepage')[0]) // 2, 15))
        omButton = CLS_Button(1, 15, 60, 0)
        oaButton = CLS_Button(0, 55, 60, 0)
        omButton.draw(self.screen)
        oaButton.draw(self.screen)
        self.screen.blit(self.font2.render('Pile #', True, (163, 158, 245)), (100, 60))
        self.screen.blit(self.font2.render('Stone #', True, (150, 150, 150)), (100, 95))
        self.screen.blit(self.font2.render('Press L/R to switch list page', True, (237, 219, 65)), ((SCREEN_W - self.font2.size('Press L/R to switch list page')[0]) // 2, 200))
        self.screen.blit(self.font2.render('Press A/D to switch solution page', True, (146, 235, 172)), ((SCREEN_W - self.font2.size('Press A/D to switch solution page')[0]) // 2, 235))
        self.buttonList = []
        self.sol = find_sol(self.pList)
        self.spNum = (len(self.sol) - 1) // self.rowNum + 1

        if self.pageCrt >= self.pageNum:
            self.pageCrt = self.pageNum - 1
        if self.pageCrt < 0:
            self.pageCrt = 0
        if self.spCrt >= self.spNum:
            self.spCrt = self.spNum - 1
        if self.spCrt < 0:
            self.spCrt = 0

        for i in range(len(self.pList)):
            if i >= self.pageCrt * self.colNum and i < (self.pageCrt + 1) * self.colNum:
                self.screen.blit(self.font2.render(str(i + 1), True, (255, 255, 255)), (270 + (i % self.colNum) * 60, 60))
                self.screen.blit(self.font2.render(str(self.pList[i]), True, (255, 255, 255)), (270 + (i % self.colNum) * 60, 95))
            self.buttonList.append(CLS_Button(1, 270 + (i % self.colNum) * 60, 130, 1))
            self.buttonList.append(CLS_Button(0, 270 + (i % self.colNum) * 60, 165, 1))

        if len(self.sol) == 0:
            self.screen.blit(self.font.render('Losing Game: No Solutions', True, (237, 219, 65)), ((SCREEN_W - self.font.size('Losing Game: No Solutions')[0]) // 2, 270))
        for i in range(len(self.sol)):
            if i >= self.spCrt * self.rowNum and i < (self.spCrt + 1) * self.rowNum:
                if self.sol[i][1] == 1:
                    self.screen.blit(self.font2.render(f"Solution {i + 1}: Pick {self.sol[i][1]} stone from pile {self.sol[i][0] + 1}", True, (217, 210, 255)), (30, 270 + (i % self.rowNum) * 35))
                else:
                    self.screen.blit(self.font2.render(f"Solution {i + 1}: Pick {self.sol[i][1]} stones from pile {self.sol[i][0] + 1}", True, (217, 210, 255)), (30, 270 + (i % self.rowNum) * 35))
                
        for i in range(len(self.buttonList)):
            if i // 2 >= self.pageCrt * self.colNum and i // 2 < (self.pageCrt + 1) * self.colNum:
                self.buttonList[i].draw(self.screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return -1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 1
                if event.key == pygame.K_l:
                    if self.pageCrt > 0:
                        self.pageCrt -= 1
                if event.key == pygame.K_r:
                    if self.pageCrt < self.pageNum - 1:
                        self.pageCrt += 1
                if event.key == pygame.K_a:
                    if self.spCrt > 0:
                        self.spCrt -= 1
                if event.key == pygame.K_d:
                    if self.spCrt < self.spNum - 1:
                        self.spCrt += 1
            if event.type == pygame.MOUSEBUTTONDOWN:
                mX, mY = pygame.mouse.get_pos()
                if mX > omButton.x and mX < omButton.x + 26 and mY > omButton.y and mY < omButton.y + 26:
                    if len(self.pList) > 0:
                        self.pList.pop(-1)
                        self.pageNum = (len(self.pList) - 1) // self.colNum + 1
                elif mX > oaButton.x and mX < oaButton.x + 26 and mY > oaButton.y and mY < oaButton.y + 26:
                    self.pList.append(1)
                    self.pageNum = (len(self.pList) - 1) // self.colNum + 1
                else:
                    for i in range(len(self.buttonList)):
                        if i // 2 >= self.pageCrt * self.colNum and i // 2 < (self.pageCrt + 1) * self.colNum:
                            button = self.buttonList[i]
                            if mX > button.x and mX < button.x + 26 and mY > button.y and mY < button.y + 26:
                                if button.bType == 0 and self.pList[i // 2] < 999:
                                    self.pList[i // 2] += 1
                                elif button.bType == 1 and self.pList[i // 2] > 0:
                                    self.pList[i // 2] -= 1
                                break
        pygame.display.update()
        self.clock.tick(500)
        return 0
