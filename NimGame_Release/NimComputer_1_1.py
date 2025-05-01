# NimComputer Version 1.1

import pygame, sys, random, time, math, numpy

SCREEN_W, SCREEN_H = 1024, 768

def random_pick(pList):
    aList = []
    for i in range(len(pList)):
        for j in range(pList[i]):
            aList.append([i, j + 1])
    ans = random.choice(aList)
    return ans

def find_sol(pList):
    k = 0
    sol = []
    for i in pList:
        k ^= i
    if k == 0:
        return [-1, -1]
    for i in range(len(pList)):
        if k ^ pList[i] < pList[i]:
            p = i
            d = pList[i] - (k ^ pList[i])
            sol.append([p, d])
    sol = sorted(sol, key = lambda x : x[1])[::-1]
    return sol[0]

class CLS_stone(object):
    def __init__(self, x, st, maxNum, pileNum, sIndex):
        self.x = x
        self.st = st
        self.maxNum = maxNum
        self.pileNum = pileNum
        self.sIndex = sIndex
        self.y = SCREEN_H * 4 // 5 - self.st * min(SCREEN_H * 7 // 10 // self.maxNum, (SCREEN_W * 5 // 6 // self.pileNum - 6) * 0.7) + 1
        self.w = SCREEN_W * 5 // 6 // self.pileNum - 6
        self.h = min(SCREEN_H * 7 // 10 // self.maxNum - 2, (SCREEN_W * 5 // 6 // self.pileNum - 6) * 0.7 - 2)

    def draw(self, scr, maxNum, stoneNum, sIndex):
        self.sIndex = sIndex
        self.maxNum = maxNum
        self.stoneNum = stoneNum
        self.y = SCREEN_H * 4 // 5 - self.st * min(SCREEN_H * 7 // 10 // self.maxNum, (SCREEN_W * 5 // 6 // self.pileNum - 6) * 0.7) + 1
        self.h = min(SCREEN_H * 7 // 10 // self.maxNum - 2, (SCREEN_W * 5 // 6 // self.pileNum - 6) * 0.7 - 2)
        if sIndex == -1 or self.sIndex >= self.st:
            pygame.draw.ellipse(scr, (120, 120, 120), pygame.Rect(self.x + 3, self.y, self.w, self.h), 0)
        else:
            pygame.draw.ellipse(scr, (200, 200, 200), pygame.Rect(self.x + 3, self.y, self.w, self.h), 0)

class CLS_pile(object):
    def __init__(self, pI, maxNum, pileNum, stoneNum, sIndex):
        self.pI = pI
        self.pileNum = pileNum
        self.stoneList = []
        self.x = SCREEN_W // 12 + self.pI * SCREEN_W * 5 // 6 // self.pileNum
        self.stoneNum = stoneNum
        self.maxNum = maxNum
        self.font = pygame.font.Font('PixelatedEleganceRegular-ovyAA.ttf', 48 - self.pileNum)
        self.sIndex = sIndex
        self.w = SCREEN_W * 5 // 6 // self.pileNum - 6
        for stone in range(1, self.stoneNum + 1):
            kS = CLS_stone(self.x, stone, self.maxNum, self.pileNum, self.sIndex)
            self.stoneList.append(kS)

    def draw(self, scr, maxNum, stoneNum, sIndex):
        self.sIndex = sIndex
        self.maxNum = maxNum
        self.stoneNum = stoneNum
        for kS in self.stoneList:
            kS.draw(scr, self.maxNum, self.stoneNum, self.sIndex)
        scr.blit(self.font.render(str(self.pI + 1), True, (0, 0, 0)), (self.x + (SCREEN_W * 5 // 6 // self.pileNum - self.font.size(str(self.pI + 1))[0]) // 2, SCREEN_H * 33 // 40))

class NimComputerFW(object):
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('PixelatedEleganceRegular-ovyAA.ttf', 36)
        self.font2 = pygame.font.Font('PixelatedEleganceRegular-ovyAA.ttf', 18)
        self.font3 = pygame.font.Font('SIMSUN.ttf', 21)
        self.pList = [0]
        self.pileNum = 1
        self.difficulty = 0
        self.piles = []
        self.sIndex = -1
        self.pS = -1
        self.turn = 0
        self.diaStart = ['Who the gay r u', \
                         'Cotton pay, happy day!', \
                         'Do you know about GurobiPy?', \
                         'Want some apples?', \
                         'namyag', \
                         'g']
        self.dia1 = [['Oh no my d', 'wtg', 'Oh no i glundered', 'i gay', 'i namyag', 'yugger'], \
                     ['诶！', '我急了', '我红温了', 'Did i just blunder', 'IM GAY!'], \
                     ['Oh no gurobipy betrayed me', 'bruh gurobipy', 'oh no 被刘老师抓到了', 'why doesnt 元培 code work', 'gurobipy is killing me','Can every integer greater than 1 be written as a product of prime numbers?'], \
                     ['WHY IS THIS APPLE ROTTEN', 'is that a bug?', '[不嘻嘻]', 'Oh f**k', 'Where is my apple?','Nonononononono'], \
                     ['One, two, and four! Oh no!', 'Geometry and discrete... Oh no', "I'm namyag!", 'my master will whip me...'], \
                     ['g', 'i gay', 'misclick', '小失误', 'oH, nO','哎呀，AIME考了8分','oh no 我的物理']]
        self.dia2 = [['Sacrifice... DA ROOK', 'bro i played a brilliancy', 'someone call an ambulance'], \
                     ['叫上了', 'bro is a clown', '哥们以为自己是cagnus marlsen', '菜就多练', 'Cotton power!'], \
                     ['Of course we use gurobipy!', '还是元培的代码好用', "No you're wrong", 'gurobipy carry', 'im going to win with gurobipy'], \
                     ['HA!', '你IT多少分？', 'An apple a day keeps the doctor away!', '[嘻嘻]', '[受不了智障]', 'SEEEE?!', "That's why you eat fruits everyday!", "I'm going to sleep at ten"], \
                     ['LL', 'u namyag!', 'im gonna win anyways!', 'Go kill yourself', 'bro is going to get whipped', 'gayman!', 'bro 的成绩没有124分!'], \
                     ['L', 'LLLLL', 'Ur terrible! GKYS!', "No you're wrongggg!", 'L to you!', '哥们发现自己是小丑', 'Hank is a terrible person', 'Im obviously winning now', 'EZ WIN','一看就是学习态度极差','你还叫上了？']]
        self.dia = ''
        self.opp = 0
        self.oppList = ['Gayvin', 'Tixi', 'Runzhi', 'Hank', '124', 'tr1somy']
        self.tP, self.tS = -1, -1
        self.sf_frame = pygame.image.load('SF_frame.png')
        self.sf_w, self.sf_h = 800, 600
        self.sf_frame = pygame.transform.scale(self.sf_frame, (self.sf_w, self.sf_h))
        self.sf_frame.set_colorkey((255, 255, 255))

    def select_difficulty(self):
        self.screen.fill((0, 0, 0))

        self.screen.blit(self.font.render("Select Difficulty", True, (255, 255, 180)), ((SCREEN_W - self.font.size("Select Difficulty")[0]) // 2, SCREEN_H // 6))
        self.screen.blit(self.font.render("Press esc to return to homepage", True, (180, 255, 180)), ((SCREEN_W - self.font.size("Press esc to return to homepage")[0]) // 2, SCREEN_H // 4))
        self.screen.blit(self.font.render("Press Enter to continue", True, (180, 180, 255)), ((SCREEN_W - self.font.size("Press Enter to continue")[0]) // 2, SCREEN_H // 3))
        pygame.draw.rect(self.screen, (255, 255, 230), pygame.Rect(SCREEN_W // 8, SCREEN_H * 2 // 3, SCREEN_W * 3 // 4, 20))
        mX, mY = pygame.mouse.get_pos()
        if mX < SCREEN_W // 8:
            self.difficulty = 0
            mX = SCREEN_W // 8
        elif mX > SCREEN_W * 7 // 8:
            self.difficulty = 100
            mX = SCREEN_W * 7 // 8
        else:
            self.difficulty = int(100.99 * (mX - SCREEN_W // 8) / (SCREEN_W * 3 // 4))
        
        pygame.draw.circle(self.screen, (255, 255, 255), (mX, SCREEN_H * 2 // 3 + 10), 30)
        self.screen.blit(self.font.render(str(self.difficulty), True, (255, 255, 255)), (mX - self.font.size(str(self.difficulty))[0] // 2, SCREEN_H * 2 // 3 - 75))
        if self.difficulty < 17:
            self.opp = 0
            self.screen.blit(self.font.render("G", True, (255, 190, 190)), ((SCREEN_W - self.font.size("Gayvin")[0]) // 2, SCREEN_H * 2 // 3 + 75))
            self.screen.blit(self.font.render("a", True, (255, 222, 190)), ((SCREEN_W - self.font.size("Gayvin")[0]) // 2 + self.font.size("G")[0], SCREEN_H * 2 // 3 + 75))
            self.screen.blit(self.font.render("y", True, (255, 255, 190)), ((SCREEN_W - self.font.size("Gayvin")[0]) // 2 + self.font.size("Ga")[0], SCREEN_H * 2 // 3 + 75))
            self.screen.blit(self.font.render("v", True, (190, 255, 190)), ((SCREEN_W - self.font.size("Gayvin")[0]) // 2 + self.font.size("Gay")[0], SCREEN_H * 2 // 3 + 75))
            self.screen.blit(self.font.render("i", True, (190, 190, 255)), ((SCREEN_W - self.font.size("Gayvin")[0]) // 2 + self.font.size("Gayv")[0], SCREEN_H * 2 // 3 + 75))
            self.screen.blit(self.font.render("n", True, (222, 190, 255)), ((SCREEN_W - self.font.size("Gayvin")[0]) // 2 + self.font.size("Gayvi")[0], SCREEN_H * 2 // 3 + 75))
        elif self.difficulty < 34:
            self.opp = 1
            self.screen.blit(self.font.render("Tixi", True, (90, 55, 19)), ((SCREEN_W - self.font.size("Tixi")[0]) // 2, SCREEN_H * 2 // 3 + 75))
        elif self.difficulty < 50:
            self.opp = 2
            self.screen.blit(self.font.render("Runzhi", True, (255, 190, 190)), ((SCREEN_W - self.font.size("Runzhi")[0]) // 2, SCREEN_H * 2 // 3 + 75))
            self.screen.blit(self.font2.render("Gurobi", True, (255, 255, 190)), (15, 15))
            self.screen.blit(self.font2.render("Py", True, (150, 150, 210)), (15 + self.font2.size("Gurobi")[0], 15))
        elif self.difficulty < 67:
            self.opp = 3
            self.screen.blit(self.font.render("Hank", True, (255, 190, 190)), ((SCREEN_W - self.font.size("Hank")[0]) // 2, SCREEN_H * 2 // 3 + 75))
        elif self.difficulty < 84:
            self.opp = 4
            self.screen.blit(self.font.render("124", True, (255, 190, 190)), ((SCREEN_W - self.font.size("124")[0]) // 2, SCREEN_H * 2 // 3 + 75))
        else:
            self.opp = 5
            self.screen.blit(self.font.render("tr1somy 21", True, (255, 190, 190)), ((SCREEN_W - self.font.size("tr1somy 21")[0]) // 2, SCREEN_H * 2 // 3 + 75))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return -1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 1
                if event.key == pygame.K_RETURN:
                    self.dia = self.diaStart[self.opp]
                    return 2
        
        pygame.display.update()
        self.clock.tick(500)
        return 0

    def game(self):
        self.screen.fill((190, 225, 255))
        mX, mY = pygame.mouse.get_pos()
        pFlag = 0
        for pInd in range(len(self.piles)):
            p = self.piles[pInd]
            if p.x + 3 < mX and p.x + 3 + p.w > mX:
                sList = p.stoneList
                for sInd in range(len(sList)):
                    s = sList[sInd]
                    if s.y < mY and s.y + s.h > mY:
                        self.pS = pInd
                        self.sIndex = sInd
                        pFlag = 1
                        break
                break
        if pFlag == 0:
            self.pS = -1
            self.sIndex = -1

        if self.turn == 1:
            r = random.randint(1, 100)
            if r <= self.difficulty:
                ans = find_sol(self.pList)
                if ans == [-1, -1]:
                    ans = random_pick(self.pList)
                    self.dia = random.choice(self.dia1[self.opp])
                else:
                    self.dia = random.choice(self.dia2[self.opp])
            else:
                ans = random_pick(self.pList)
                self.dia = random.choice(self.dia1[self.opp])
            self.pList[ans[0]] = self.pList[ans[0]] - ans[1]
            self.piles[ans[0]] = CLS_pile(ans[0], max(self.pList), len(self.pList), self.pList[ans[0]], -1)
            self.tP = ans[0] + 1
            self.tS = ans[1]
            self.turn = 0
            if self.pList == [0] * len(self.pList):
                return 3

        if self.turn == 0:
            self.screen.blit(self.font.render("Pick a number of stones!", True, (225, 190, 190)), ((SCREEN_W - self.font.size("Pick a number of stones!")[0]) // 2, 15))

        if self.tP == -1:
            self.screen.blit(self.font3.render(f"{self.oppList[self.opp]}: {self.dia}", True, (90, 130, 90)), (15, SCREEN_H - 30))
        else:
            self.screen.blit(self.font3.render(f"{self.oppList[self.opp]}: [Takes {self.tS} stones from pile {self.tP}] {self.dia}", True, (90, 130, 90)), (15, SCREEN_H - 30))

        for p in range(len(self.piles)):
            if self.pS != p:
                self.piles[p].draw(self.screen, max(self.pList), self.pList[p], -1)
            else:
                self.piles[p].draw(self.screen, max(self.pList), self.pList[p], self.sIndex)
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return -1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 1
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.pS != -1 and self.turn == 0:
                    self.turn = 1
                    self.pList[self.pS] = self.sIndex
                    self.piles[self.pS] = CLS_pile(self.pS, max(self.pList), len(self.pList), self.sIndex, -1)
                    if self.pList == [0] * len(self.pList):
                        return 2
        pygame.display.update()
        self.clock.tick(500)
        return 0

    def win(self):
        self.screen.blit(self.sf_frame, ((SCREEN_W - self.sf_w) // 2, (SCREEN_H - self.sf_h) // 2))
        self.screen.blit(self.font.render("You won!", True, (220, 125, 25)), ((SCREEN_W - self.font.size("You won!")[0]) // 2, SCREEN_H // 3))
        self.screen.blit(self.font.render("Press Enter to", True, (225, 180, 150)), \
                         ((SCREEN_W - self.font.size("Press Enter to")[0]) // 2, SCREEN_H * 3 // 5))
        self.screen.blit(self.font.render("return to homepage", True, (225, 180, 150)), \
                         ((SCREEN_W - self.font.size("return to homepage")[0]) // 2, SCREEN_H * 2 // 3))
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

    def lose(self):
        self.screen.blit(self.sf_frame, ((SCREEN_W - self.sf_w) // 2, (SCREEN_H - self.sf_h) // 2))
        self.screen.blit(self.font.render("L", True, (220, 125, 125)), ((SCREEN_W - self.font.size("L")[0]) // 2, SCREEN_H // 3))
        self.screen.blit(self.font.render("You lost!", True, (220, 125, 25)), ((SCREEN_W - self.font.size("You lost!")[0]) // 2, SCREEN_H // 2))
        self.screen.blit(self.font.render("Press Enter to", True, (225, 180, 150)), \
                         ((SCREEN_W - self.font.size("Press Enter to")[0]) // 2, SCREEN_H * 2 // 3))
        self.screen.blit(self.font.render("return to homepage", True, (225, 180, 150)), \
                         ((SCREEN_W - self.font.size("return to homepage")[0]) // 2, SCREEN_H * 3 // 4))
        
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
        self.screen.fill((0, 0, 0))
        statusSD = 0
        while statusSD == 0:
            statusSD = self.select_difficulty()
        if statusSD == -1:
            pygame.quit()
            return -1
        if statusSD == 1:
            return 1

        while self.pList == [0] * len(self.pList):
            self.pList = []
            self.pileNum = random.randint(2, 40)
            for i in range(self.pileNum):
                self.pList.append(random.randint(0, 60))

        for i in range(len(self.pList)):
            self.piles.append(CLS_pile(i, max(self.pList), len(self.pList), self.pList[i], -1))

        while self.pList != [0] * len(self.pList):
            statusG = 0
            while statusG == 0:
                statusG = self.game()
            if statusG == -1:
                pygame.quit()
                return -1
            if statusG == 1:
                return 1
        if statusG == 2:
            statusWin = 0
            while statusWin == 0:
                statusWin = self.win()
            if statusWin == -1:
                pygame.quit()
                return -1
            if statusWin == 1:
                return 1
        else:
            statusLose = 0
            while statusLose == 0:
                statusLose = self.lose()
            if statusLose == -1:
                pygame.quit()
                return -1
            if statusLose == 1:
                return 1
        
        
        pygame.display.update()
        self.clock.tick(500)
        return 0
