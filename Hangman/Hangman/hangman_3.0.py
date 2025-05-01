# Hangman V3.0

import pygame,sys,random, time
SCREEN_W,SCREEN_H=760,960

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
        self.x,self.y=SCREEN_W//2,SCREEN_H*7/8
        self.w,self.h=50,3
    def draw(self,scr):
        pygame.draw.rect(scr,(255,0,0),(self.x,self.y,self.w,self.h))
        return

    
class CLS_Character(object):
    def __init__(self):
        self.char = randomize_char()
        while self.char in doneList:
            self.char = randomize_char()
        self.x,self.y=random.randint(20,SCREEN_W-20),0
        self.gX,self.gY=0,0
        self.spdX,self.spdY =0, 4 * random.random() + 2
        self.w,self.h=32,32
    def draw(self,scr):
        scr.blit(font.render(self.char,True,(0,255,0)), (self.x, self.y))
        return
    def move(self):
        if random.randint(1,50)==1:
            self.gX,self.gY=random.randint(-1,1)*0.05,random.randint(-1,1)*0.05
        self.spdY+=self.gY
        self.spdX+=self.gX
        self.y+=self.spdY
        self.x+=self.spdX
        if self.x<=0 or self.x>=SCREEN_W-32:
            self.spdX*=-1
        return


class CLS_Word(object):
    def __init__(self):
        self.word=random.choice(wList)[:-1].upper()
        self.x,self.y=30,10
        self.wordList=['_']*len(self.word)
        self.err, self.errFlag, self.errT = 0, 0, 0
    def draw(self,scr):
        scr.blit(font.render(' '.join(self.wordList), True, (0, 255, 0)), (self.x, self.y))
        return
    def add(self,letter):
        flag = 0
        for i in range(len(self.word)):
            if self.word[i]==letter:
                self.wordList[i]=letter
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
                scr.blit(font.render('+ 5 seconds', True, (255, 50, 50)), (SCREEN_W // 2 - 120, SCREEN_H // 2))
        return


def complete(scr, word, stat):
    vFlag = 0
    while True:
        pygame.draw.rect(scr, (255, 255, 80), (SCREEN_W // 4 - 15, SCREEN_H // 4 - 15, SCREEN_W // 2 + 30, SCREEN_H // 2 + 30))
        pygame.draw.rect(scr, (255, 255, 100), (SCREEN_W // 4, SCREEN_H // 4, SCREEN_W // 2, SCREEN_H // 2))
        scr.blit(font2.render(f"The word was {word}", True, (50, 50, 150)), (SCREEN_W // 2 - 6 * len(f"The word was {word}"), SCREEN_H // 3 + 60))
        scr.blit(font3.render("Press 'Enter' to continue", True, (0, 0, 0)), (SCREEN_W // 2 - 5 * len("Press 'Enter' to continue"), SCREEN_H // 3 + 120))
        if stat == 1:
            scr.blit(font.render('NEW RECORD', True, (255, 50, 50)), (SCREEN_W // 2 - 100, SCREEN_H // 3))
        for event in pygame.event.get():
            if event.type ==pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    vFlag = 1
                    break
        if vFlag == 1:
            break
        pygame.display.update()
        clock.tick(60)
    return


# ----- main -----
pygame.init()
screen=pygame.display.set_mode((SCREEN_W,SCREEN_H))
clock=pygame.time.Clock()
font=pygame.font.Font('monaco.ttf',32)
font2 = pygame.font.Font('monaco.ttf', 24)
font3 = pygame.font.Font('monaco.ttf', 16)
cList =[]
catcher=CLS_Catcher()
wFile = open("word_cloud.txt", 'r')
wList = wFile.readlines()
wFile.close()
word=CLS_Word()
tStart = time.time()
doneList=[]
prevWord = ''
while True:
    screen.fill((0,0,0))
    catcher.x=pygame.mouse.get_pos()[0]
    if catcher.x > SCREEN_W - 50:
        catcher.x = SCREEN_W - 50
    catcher.draw(screen)
    charList = []
    for i in cList:
        charList.append(i.char)
    if random.randint(1,5 * len(cList) + 5)==1 and sum(constTable) - len(cList) > 1:
        c = CLS_Character()
        cList.append(c)
    for i in range(len(cList) - 1,-1,-1):
        try:
            if cList[i].y>SCREEN_H or cList[i].y < 0:
                cList.pop(i)
            else:
                if collide(cList[i].x,cList[i].y,cList[i].w,cList[i].h,catcher.x,catcher.y,catcher.w,catcher.h):
                    word.add(cList[i].char)
                    doneList.append(cList[i].char)
                    constTable[ord(cList[i].char) - 65] = 0
                    cList.pop(i)
                else:
                    cList[i].move()
                    cList[i].draw(screen)
        except:
            pass
    word.draw(screen)
    screen.blit(font.render(f"Previous word: {prevWord}", True, (255, 255, 255)), (10, SCREEN_H - 50))
    screen.blit(font.render(str(round(time.time() - tStart + word.err, 2)), True, (255, 255, 255)), (30, 50))
    if word.is_done():
        prevWord = word.word
        doneList = []
        constTable = [1] * 26
        t = round(time.time() - tStart + word.err, 2)
        wLen = len(word.word)
        word = CLS_Word()
        tStart = time.time()
        rFile = open("record.txt", 'r')
        rList = rFile.readlines()
        rFile.close()
        cList = []
        if 'none' in rList[wLen - 1]:
            prev = ''.join(rList[:(wLen - 1)])
            changed = f"{wLen}: {t}s\n"
            aft = ''.join(rList[wLen:])
            rWrite = open("record.txt", 'w')
            rWrite.write(prev + changed + aft)
            rWrite.close()
            complete(screen, prevWord, 1)
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
                complete(screen, prevWord, 1)
            else:
                complete(screen, prevWord, 0)
    word.err_notice(screen)
    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
    clock.tick(60)
