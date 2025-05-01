# Hangman V3.3

import pygame, sys, random, time, numpy, colorsys

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


def avg_color(rect1):
    pArray = FW.pixel_array
    x, y, w, h = rect1
    x, y, w, h = round(x), round(y), round(w), round(h)
    region = pArray[x:(x + w + 1), y:(y + h + 1)]
    resColor = (0, 0, 0)
    if region.size > 0:
        average_color = region.mean(axis = (0, 1))
        resColor = tuple(map(int, average_color))
    return resColor


def best_color(rgb_color):
    r, g, b = rgb_color[0] / 255, rgb_color[1] / 255, rgb_color[2] / 255
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    h = (h + 2 / 3) % 1
    s = 1
    if v < 4 / 5:
        v = 1
    elif v < 7 / 8:
        v = 73 / 9 - 80 / 9 * v
    else:
        v = 1 / 3
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return tuple(int(x * 255) for x in (r, g, b))


class CLS_Catcher(object):
    def __init__(self):
        self.x, self.y = SCREEN_W // 2, SCREEN_H * 7 / 8
        self.w, self.h = 60, 4

    def draw(self, scr):
        if self.x > SCREEN_W - self.w:
            self.x = SCREEN_W - self.w
        if self.x < 0:
            self.x = 0
        pygame.draw.rect(scr, FW.ctcC, (self.x, self.y, self.w, self.h))
        return


class CLS_Character(object):
    def __init__(self):
        self.char = randomize_char()
        while self.char in FW.doneList:
            self.char = randomize_char()
        self.x, self.y = random.randint(10, SCREEN_W - 42), 0
        self.gX, self.gY = 0, 0
        self.spdX, self.spdY = 0, 3.5 * random.random() + 2
        self.w, self.h = 32, 32
        self.color = (0, 0, 0)
        self.bgAvg = (0, 0, 0)

    def draw(self, scr):
        self.bgAvg = avg_color((self.x, self.y, FW.font.size(self.char)[0], FW.font.size(self.char)[1]))
        self.color = best_color(self.bgAvg)
        scr.blit(FW.font.render(self.char, True, self.color), (self.x, self.y))
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


class CLS_Bomb(object):
    def __init__(self):
        self.x, self.y = random.randint(0, SCREEN_W - FW.bomb_w - 10), 0
        self.gX, self.gY = 0, 0
        self.spdX, self.spdY = 0, 3.5 * random.random() + 2

    def draw(self, scr):
        scr.blit(FW.bomb_img, (self.x, self.y))
        return

    def move(self):
        if random.randint(1, 50) == 1:
            self.gX, self.gY = random.randint(-1, 1) * 0.05, random.randint(-1, 1) * 0.05
        self.spdY += self.gY
        self.spdX += self.gX
        self.y += self.spdY
        self.x += self.spdX
        if self.x <= 0 or self.x >= SCREEN_W - FW.bomb_h:
            self.spdX *= -1
        return


class CLS_Megabomb(object):
    def __init__(self):
        self.x, self.y = random.randint(10, SCREEN_W - FW.mgb_w - 10), 0
        self.gX, self.gY = 0, 0
        self.spdX, self.spdY = 0, 2 * random.random() + 1

    def draw(self, scr):
        scr.blit(FW.megabomb_img, (self.x, self.y))
        return

    def move(self):
        self.gX, self.gY = (FW.catcher.x - self.x) / (6 * SCREEN_W), 0.03 - 0.03 * abs(FW.catcher.x - self.x) / (SCREEN_W // 2)
        self.spdY += self.gY
        self.spdX += self.gX
        if self.spdY < 0.01:
            self.spdY = 0.01
        self.y += self.spdY
        self.x += self.spdX
        if self.x <= 0 or self.x >= SCREEN_W - FW.mgb_w:
            self.spdX *= -1
        return


class CLS_Word(object):
    def __init__(self,wList):
        self.word = random.choice(wList)[:-1].upper()
        self.x, self.y = 30, 10
        self.wordList = ['_'] * len(self.word)
        self.err, self.errFlag, self.errT = 0, 0, 0
        self.font = pygame.font.Font('PixelatedEleganceRegular-ovyAA.ttf', 32)
        self.font2 = pygame.font.Font('PixelatedEleganceRegular-ovyAA.ttf', 24)
        self.errPosX, self.errPosY = 0, 0
        self.noticeTime = 0
    def draw(self, scr):
        scr.blit(self.font.render(' '.join(self.wordList), True, FW.wrdC), (self.x, self.y))
        return

    def add(self, letter, posX, posY):
        flag = 0
        for i in range(len(self.word)):
            if self.word[i] == letter:
                self.wordList[i] = letter
                flag = 1
        if flag == 0:
            self.err += 5
            self.errFlag = 1
            self.errT = time.time()
            self.noticeTime = 5
            self.errPosX, self.errPosY = posX, posY
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
                fSize = self.font2.size(f'+ {self.noticeTime} seconds')[0]
                if self.errPosX - fSize // 2 < 0:
                    scr.blit(self.font2.render(f'+ {self.noticeTime} seconds', True, (255, 50, 50)), (0, self.errPosY))
                elif self.errPosX + fSize // 2 > SCREEN_W:
                    scr.blit(self.font2.render(f'+ {self.noticeTime} seconds', True, (255, 50, 50)), (SCREEN_W - fSize, self.errPosY))
                else:
                    scr.blit(self.font2.render(f'+ {self.noticeTime} seconds', True, (255, 50, 50)), (self.errPosX - fSize // 2, self.errPosY))
        return


class CLS_Framework(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('PixelatedEleganceRegular-ovyAA.ttf', 32)
        self.font2 = pygame.font.Font('joystix monospace.otf', 24)
        self.font3 = pygame.font.Font('joystix monospace.otf', 14)
        self.bg1 = pygame.image.load('bg.gif')
        self.bg2 = pygame.image.load('bg2.gif')
        self.cPallete = [[self.bg1, (224, 231, 255), (57, 69, 124)], 
                         [self.bg2, (255, 162, 176), (255, 202, 209)]]
        self.choice = random.randint(0, len(self.cPallete) - 1)
        self.bg = self.cPallete[self.choice][0]
        self.bg = pygame.transform.scale(self.bg, (SCREEN_W, SCREEN_H))
        self.ctcC = self.cPallete[self.choice][1]
        self.wrdC = self.cPallete[self.choice][2]
        self.bomb_w, self.bomb_h, self.mgb_w, self.mgb_h = 45, 45, 80, 96
        self.bomb_img = pygame.image.load('bomb.jpg')
        self.bomb_img = pygame.transform.scale(self.bomb_img, (self.bomb_w, self.bomb_h))
        self.bomb_img.set_colorkey((255, 255, 255))
        self.megabomb_img = pygame.image.load('megabomb.jpg')
        self.megabomb_img = pygame.transform.scale(self.megabomb_img, (self.mgb_w, self.mgb_h))
        self.megabomb_img.set_colorkey((255, 255, 255))
        self.nr_img = pygame.image.load('new_record.png')
        self.nr_img = pygame.transform.scale(self.nr_img, (SCREEN_W // 3, SCREEN_H // 12))
        self.cmp_img = pygame.image.load('completed.png')
        self.cmp_img = pygame.transform.scale(self.cmp_img, (SCREEN_W // 3, SCREEN_H // 16))
        self.frame_img = pygame.image.load('frame.png')
        self.frame_img = pygame.transform.scale(self.frame_img, (SCREEN_W // 2, SCREEN_H // 2))
        self.nr_img.set_colorkey((255, 255, 255))
        self.cmp_img.set_colorkey((255, 255, 255))
        self.frame_img.set_colorkey((255, 255, 255))
        self.nr_rect, self.cmp_rect, self.frame_rect = self.nr_img.get_rect(), self.cmp_img.get_rect(), self.frame_img.get_rect()
        self.nr_rect.center = (SCREEN_W // 2, SCREEN_H * 31 // 80)
        self.cmp_rect.center = (SCREEN_W // 2, SCREEN_H * 6 // 16)
        self.frame_rect.center = (SCREEN_W // 2, SCREEN_H // 2)
        self.wPage = pygame.Surface((SCREEN_W * 3 // 5, SCREEN_H * 3 // 5))
        self.wPage.fill((245, 245, 195))
        self.w_rect = self.wPage.get_rect()
        self.w_rect.center = (SCREEN_W // 2, SCREEN_H // 2)
        self.cList = []
        self.bList = []
        self.mgbList = []
        wFile = open("word_cloud.txt", 'r')
        self.wList = wFile.readlines()
        wFile.close()
        self.t, self.best = 'none', 'none'
        self.tStart = time.time()
        self.doneList = []
        self.prevWord = ''
        self.word = CLS_Word(self.wList)
        self.catcher = CLS_Catcher()
        self.pixel_array = pygame.surfarray.array3d(self.bg)
        
    def completeScene(self,stat):
        vFlag = 0
        tCrt = time.time()
        animation_area = pygame.Rect(0, 0, SCREEN_W * 3 // 5, SCREEN_H * 3 // 5)
        animation_area.center = (SCREEN_W // 2, SCREEN_H // 2)
        bg_copy = self.screen.subsurface(animation_area).copy()
        while True:
            tK = time.time() - tCrt
            if vFlag == 0:
                if tK < 1:
                    self.wPage = pygame.transform.scale(self.wPage, (SCREEN_W * 3 * tK // 5, SCREEN_H * 3 * tK // 5))
                    self.wPage.fill((245, 245, 195))
                    self.w_rect = self.wPage.get_rect()
                    self.w_rect.center = (SCREEN_W // 2, SCREEN_H // 2)
                    self.screen.blit(bg_copy, animation_area)
                    self.screen.blit(self.wPage, self.w_rect)
                else:
                    self.screen.blit(self.wPage, self.w_rect)
                    self.screen.blit(self.frame_img, self.frame_rect)
                    self.screen.blit(self.font2.render(f"The word was", True, (50, 50, 150)),
                             ((SCREEN_W - self.font2.size(f"The word was")[0]) // 2, SCREEN_H * 7 // 16))
                    self.screen.blit(self.font2.render(self.prevWord, True, (20, 20, 100)),
                             ((SCREEN_W - self.font2.size(self.prevWord)[0]) // 2, SCREEN_H * 8 // 17))
                    self.screen.blit(self.font3.render("Press 'Enter' to continue", True, (0, 0, 0)),
                             ((SCREEN_W - self.font3.size("Press 'Enter' to continue")[0]) // 2, SCREEN_H * 9 // 17))
                    self.screen.blit(self.font3.render(f"Time taken: {self.t}s", True, (180, 180, 40)),
                             ((SCREEN_W - self.font3.size(f"Time taken: {self.t}s")[0]) // 2, SCREEN_H * 5 // 9))
                    self.screen.blit(self.font3.render(f"Best record: {self.best}s", True, (170, 20, 10)),
                             ((SCREEN_W - self.font3.size(f"Best record: {self.best}s")[0]) // 2, SCREEN_H * 3 // 5))
                    if stat == 1:
                        self.screen.blit(self.nr_img, self.nr_rect)
                    else:
                        self.screen.blit(self.cmp_img, self.cmp_rect)
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RETURN:
                                vFlag = 1
                                tEnd = time.time()
                                self.screen.blit(bg_copy, animation_area)
                                break
            else:
                tL = time.time() - tEnd
                if tL > 1:
                    break
                self.wPage = pygame.transform.scale(self.wPage, (SCREEN_W * (3 - 3 * tL) // 5, SCREEN_H * (3 - 3 * tL) // 5))
                self.wPage.fill((245, 245, 195))
                self.w_rect = self.wPage.get_rect()
                self.w_rect.center = (SCREEN_W // 2, SCREEN_H // 2)
                self.screen.blit(bg_copy, animation_area)
                self.screen.blit(self.wPage, self.w_rect)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()
            self.clock.tick(60)
        return
    
    def play(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.bg, (0, 0))
        self.catcher.x = pygame.mouse.get_pos()[0] - self.catcher.w // 2
        self.catcher.draw(self.screen)
        global charList
        charList = []
        for i in self.cList:
            charList.append(i.char)
        if random.randint(1, 5 * len(self.cList) + 5) == 1 and sum(constTable) - len(self.cList) > 1:
            c = CLS_Character()
            self.cList.append(c)
        if random.randint(1, round(2000 / (time.time() - self.tStart))) == 1:
            b = CLS_Bomb()
            self.bList.append(b)
        if random.randint(1, round(7500 / (time.time() - self.tStart))) == 1:
            mgb = CLS_Megabomb()
            self.mgbList.append(mgb)
        for i in range(len(self.cList) - 1, -1, -1):
            try:
                if self.cList[i].y > SCREEN_H or self.cList[i].y < 0:
                    self.cList.pop(i)
                else:
                    if collide(self.cList[i].x, self.cList[i].y, self.cList[i].w, self.cList[i].h, self.catcher.x, self.catcher.y, self.catcher.w,
                               self.catcher.h):
                        self.word.add(self.cList[i].char, self.cList[i].x, self.cList[i].y)
                        self.doneList.append(self.cList[i].char)
                        constTable[ord(self.cList[i].char) - 65] = 0
                        self.cList.pop(i)
                    else:
                        self.cList[i].move()
                        self.cList[i].draw(self.screen)
            except:
                pass
        for i in range(len(self.bList) - 1, -1, -1):
            try:
                if self.bList[i].y > SCREEN_H or self.bList[i].y < 0:
                    self.bList.pop(i)
                else:
                    if collide(self.bList[i].x, self.bList[i].y, self.bomb_w, self.bomb_h, self.catcher.x, self.catcher.y, self.catcher.w,
                               self.catcher.h):
                        self.word.err += 10
                        self.word.errFlag = 1
                        self.word.errT = time.time()
                        self.word.noticeTime = 10
                        self.word.errPosX, self.word.errPosY = self.bList[i].x, self.bList[i].y
                        self.bList = []
                        self.cList = []
                    else:
                        self.bList[i].move()
                        self.bList[i].draw(self.screen)
            except:
                pass
        for i in range(len(self.mgbList) - 1, -1, -1):
            try:
                if self.mgbList[i].y > SCREEN_H or self.mgbList[i].y < 0:
                    self.mgbList.pop(i)
                else:
                    if collide(self.mgbList[i].x, self.mgbList[i].y, self.mgb_w, self.mgb_h, self.catcher.x, self.catcher.y, self.catcher.w,
                               self.catcher.h):
                        self.bList = []
                        self.cList = []
                        self.mgbList.pop(i)
                    else:
                        self.mgbList[i].move()
                        self.mgbList[i].draw(self.screen)
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
            constTable[i] = 1
        self.t = round(time.time() - self.tStart + self.word.err, 2)
        wLen = len(self.word.word)
        self.word = CLS_Word(self.wList)
        rFile = open("record.txt", 'r')
        rList = rFile.readlines()
        rFile.close()
        self.cList = []
        self.bList = []
        self.mgbList = []
        if 'none' in rList[wLen - 1]:
            self.best = self.t
            prev = ''.join(rList[:(wLen - 1)])
            changed = f"{wLen}: {self.t}s\n"
            aft = ''.join(rList[wLen:])
            rWrite = open("record.txt", 'w')
            rWrite.write(prev + changed + aft)
            rWrite.close()
            self.completeScene(1)
        else:
            self.best = rList[wLen - 1][(len(str(wLen)) + 2):-2]
            self.best = eval(self.best)
            if self.t < self.best:
                self.best = self.t
                prev = ''.join(rList[:(wLen - 1)])
                changed = f"{wLen}: {self.t}s\n"
                aft = ''.join(rList[wLen:])
                rWrite = open("record.txt", 'w')
                rWrite.write(prev + changed + aft)
                rWrite.close()
                self.completeScene(1)
            else:
                self.completeScene(0)
        self.tStart = time.time()
        self.choice = random.randint(0, len(self.cPallete) - 1)
        self.bg = self.cPallete[self.choice][0]
        self.bg = pygame.transform.scale(self.bg, (SCREEN_W, SCREEN_H))
        self.ctcC = self.cPallete[self.choice][1]
        self.wrdC = self.cPallete[self.choice][2]
        self.pixel_array = pygame.surfarray.array3d(self.bg)


# ----- main -----
FW = CLS_Framework()
while True:
    FW.play()
