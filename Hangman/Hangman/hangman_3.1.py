# Hangman V3.1

import pygame, sys, random, time

SCREEN_W, SCREEN_H = 760, 960

freqTable = [8, 2, 3, 4, 12, 3, 3, 6, 7, 1, 1, 4, 2, 7, 8, 2, 1, 6, 6, 9, 3, 2, 2, 1, 2, 1]
constTable = [1] * 26
charList = []


def collide(x1, y1, w1, h1, x2, y2, w2, h2):
    if x1 + w1 >= x2 and x1 <= x2 + w2 and y1 + h1 >= y2 and y1 <= y2 + h2:
        return True
    else:
        return False


def randomize_char():
    freqSum = []
    for i in range(26):
        if chr(i + 65) not in charList:
            freqSum.append(constTable[i] * freqTable[i])
        else:
            freqSum.append(0)
    k = random.random() * sum(freqSum)
    for i in range(len(freqSum)):
        if k <= sum(freqSum[:(i + 1)]):
            ans = chr(65 + i)
            break
    return ans


class CLS_Catcher(object):
    def __init__(self):
        self.x, self.y = SCREEN_W // 2, SCREEN_H * 7 / 8
        self.w, self.h = 50, 3

    def draw(self, scr):
        if self.x>SCREEN_W-self.w:
            self.x=SCREEN_W-self.w
        pygame.draw.rect(scr, (255, 0, 0), (self.x, self.y, self.w, self.h))
        return


class CLS_Character(object):
    def __init__(self):
        self.char = randomize_char()
        while self.char in FW.doneList:
            self.char = randomize_char()
        self.x, self.y = random.randint(20, SCREEN_W - 20), 0
        self.gX, self.gY = 0, 0
        self.spdX, self.spdY = 0, 4 * random.random() + 2
        self.w, self.h = 32, 32

    def draw(self, scr):
        scr.blit(FW.font.render(self.char, True, (0, 255, 0)), (self.x, self.y))
        return

    def move(self):
        if random.randint(1, 50) == 1:
            self.gX, self.gY = random.randint(-1, 1) * 0.05, random.randint(-1, 1) * 0.05
        self.spdY += self.gY
        self.spdX += self.gX
        self.y += self.spdY
        self.x += self.spdX
        if self.x <= 0 or self.x >= SCREEN_W - 32:
            self.spdX *= -1
        return


class CLS_Word(object):
    def __init__(self,wList):
        self.word = random.choice(wList)[:-1].upper()
        self.x, self.y = 30, 10
        self.wordList = ['_'] * len(self.word)
        self.err, self.errFlag, self.errT = 0, 0, 0
        self.font = pygame.font.Font('monaco.ttf', 32)
    def draw(self, scr):
        scr.blit(self.font.render(' '.join(self.wordList), True, (0, 255, 0)), (self.x, self.y))
        return

    def add(self, letter):
        flag = 0
        for i in range(len(self.word)):
            if self.word[i] == letter:
                self.wordList[i] = letter
                flag = 1
        if flag == 0:
            self.err += 5
            self.errFlag = 1
            self.errT = time.time()
        return

    def is_done(self):
        if self.word == ''.join(self.wordList):
            return True
        return False

    def err_notice(self, scr):
        if self.errFlag == 1:
            if time.time() - self.errT > 0.5:
                self.errFlag = 0
            else:
                scr.blit(self.font.render('+ 5 seconds', True, (255, 50, 50)), (SCREEN_W // 2 - 120, SCREEN_H // 2))
        return


class CLS_Framework(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('monaco.ttf', 32)
        self.font2 = pygame.font.Font('monaco.ttf', 24)
        self.font3 = pygame.font.Font('monaco.ttf', 16)
        self.cList = []
        wFile = open("word_cloud.txt", 'r')
        self.wList = wFile.readlines()
        wFile.close()
        self.tStart = time.time()
        self.doneList = []
        self.prevWord = ''
        self.word = CLS_Word(self.wList)
        self.catcher = CLS_Catcher()
    def completeScene(self,stat):
        vFlag = 0
        while True:
            pygame.draw.rect(self.screen, (255, 255, 80),
                             (SCREEN_W // 4 - 15, SCREEN_H // 4 - 15, SCREEN_W // 2 + 30, SCREEN_H // 2 + 30))
            pygame.draw.rect(self.screen, (255, 255, 100), (SCREEN_W // 4, SCREEN_H // 4, SCREEN_W // 2, SCREEN_H // 2))
            self.screen.blit(self.font2.render(f"The word was {self.prevWord}", True, (50, 50, 150)),
                     (SCREEN_W // 2 - 6 * len(f"The word was {self.prevWord}"), SCREEN_H // 3 + 60))
            self.screen.blit(self.font3.render("Press 'Enter' to continue", True, (0, 0, 0)),
                     (SCREEN_W // 2 - 5 * len("Press 'Enter' to continue"), SCREEN_H // 3 + 120))
            if stat == 1:
                self.screen.blit(self.font.render('NEW RECORD', True, (255, 50, 50)), (SCREEN_W // 2 - 100, SCREEN_H // 3))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        vFlag = 1
                        break
            if vFlag == 1:
                break
            pygame.display.update()
            self.clock.tick(60)
        return
    def play(self):
        self.screen.fill((0, 0, 0))
        self.catcher.x = pygame.mouse.get_pos()[0]
        self.catcher.draw(self.screen)
        charList = []
        for i in self.cList:
            charList.append(i.char)
        if random.randint(1, 5 * len(self.cList) + 5) == 1 and sum(constTable) - len(self.cList) > 1:
            c = CLS_Character()
            self.cList.append(c)
        for i in range(len(self.cList) - 1, -1, -1):
            try:
                if self.cList[i].y > SCREEN_H or self.cList[i].y < 0:
                    self.cList.pop(i)
                else:
                    if collide(self.cList[i].x, self.cList[i].y, self.cList[i].w, self.cList[i].h, self.catcher.x, self.catcher.y, self.catcher.w,
                               self.catcher.h):
                        self.word.add(self.cList[i].char)
                        self.doneList.append(self.cList[i].char)
                        constTable[ord(self.cList[i].char) - 65] = 0
                        self.cList.pop(i)
                    else:
                        self.cList[i].move()
                        self.cList[i].draw(self.screen)
            except:
                pass
        self.word.draw(self.screen)
        self.screen.blit(self.font.render(f"Previous word: {self.prevWord}", True, (255, 255, 255)), (10, SCREEN_H - 50))
        self.screen.blit(self.font.render(str(round(time.time() - self.tStart + self.word.err, 2)), True, (255, 255, 255)), (30, 50))
        if self.word.is_done():
            self.done()
        self.word.err_notice(self.screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        self.clock.tick(60)
    def done(self):
        self.prevWord = self.word.word
        self.doneList = []
        for i in range(len(constTable)):
            constTable[i]=1
        t = round(time.time() - self.tStart + self.word.err, 2)
        wLen = len(self.word.word)
        self.word = CLS_Word(self.wList)
        self.tStart = time.time()
        rFile = open("record.txt", 'r')
        rList = rFile.readlines()
        rFile.close()
        self.cList = []
        if 'none' in rList[wLen - 1]:
            prev = ''.join(rList[:(wLen - 1)])
            changed = f"{wLen}: {t}s\n"
            aft = ''.join(rList[wLen:])
            rWrite = open("record.txt", 'w')
            rWrite.write(prev + changed + aft)
            rWrite.close()
            self.completeScene(1)
        else:
            rec = rList[wLen - 1][(len(str(wLen)) + 2):-2]
            rec = eval(rec)
            if t < rec:
                prev = ''.join(rList[:(wLen - 1)])
                changed = f"{wLen}: {t}s\n"
                aft = ''.join(rList[wLen:])
                rWrite = open("record.txt", 'w')
                rWrite.write(prev + changed + aft)
                rWrite.close()
                self.completeScene(1)
            else:
                self.completeScene(0)
# ----- main -----
FW=CLS_Framework()
while True:
    FW.play()
