# Hangman V2.2

import pygame,sys,random
SCREEN_W,SCREEN_H=760,960

def collide(x1, y1, w1, h1, x2, y2, w2, h2):
    if x1 + w1 >= x2 and x1 <= x2 + w2 and y1 + h1 >= y2 and y1 <= y2 + h2:
        return True
    else:
        return False

class CLS_Catcher(object):
    def __init__(self):
        self.x,self.y=SCREEN_W//2,SCREEN_H*7/8
        self.w,self.h=50,3
    def draw(self,scr):
        pygame.draw.rect(scr,(255,0,0),(self.x,self.y,self.w,self.h))
        return

    
class CLS_Character(object):
    def __init__(self):
        self.char=chr(random.randint(65,90))
        while self.char in doneList:
            self.char = chr(random.randint(65, 90))
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

def process(ans, gList, guess):
    cnt += 1
    """
    if len(guess) == len(ans):
        if guess == ans:
            for i in range(len(ans)):
                gList[i] = ans[i]
    """
    if len(guess) == 1:
        guess = guess.upper()
        if guess in ans:
            for i in range(len(ans)):
                if ans[i] == guess:
                    gList[i] = ans[i]
    return gList, cnt

class CLS_Word(object):
    def __init__(self):
        self.word=random.choice(wList)[:-1].upper()
        self.x,self.y=30,10
        self.wordList=['_']*len(self.word)
    def draw(self,scr):
        scr.blit(font.render(' '.join(self.wordList), True, (0, 255, 0)), (self.x, self.y))
        return
    def add(self,letter):
        for i in range(len(self.word)):
            if self.word[i]==letter:
                self.wordList[i]=letter
        return
    def is_done(self):
        if self.word == ''.join(self.wordList):
            return True
        return False

def blink(scr):
    scr.blit(font.render('NEW RECORD', True, (255, 120, 120)), (SCREEN_W // 2 - 180, SCREEN_H // 2))
    return

# ----- main -----
pygame.init()
screen=pygame.display.set_mode((SCREEN_W,SCREEN_H))
clock=pygame.time.Clock()
font=pygame.font.Font('monaco.ttf',32)
cList =[]
catcher=CLS_Catcher()
wFile = open("word_cloud.txt", 'r')
wList = wFile.readlines()
wFile.close()
word=CLS_Word()
tStart = time.time()
doneList=[]
while True:
    screen.fill((0,0,0))
    catcher.x=pygame.mouse.get_pos()[0]
    catcher.draw(screen)
    charList = []
    for i in cList:
        charList.append(i.char)
    if random.randint(1,12 * len(cList) + 10)==1:
        cList.append(CLS_Character())
    for i in range(-1,-len(cList)-1,-1):
        try:
            if cList[i].y>SCREEN_H:
                cList.pop(i)
            else:
                if collide(cList[i].x,cList[i].y,cList[i].w,cList[i].h,catcher.x,catcher.y,catcher.w,catcher.h):
                    word.add(cList[i].char)
                    doneList.append(cList[i].char)
                    cList.pop(i)
                cList[i].move()
                cList[i].draw(screen)
        except:
            pass
    word.draw(screen)
    screen.blit(font.render(str(round(time.time() - tStart, 2)), True, (255, 255, 255)), (30, 50))
    if word.is_done():
        wLen = len(word)
        word = CLS_Word()
        t = time.time() - tStart
        tStart = time.time()
        rFile = open("record.txt", 'r')
        rEntire = rFile.
        rList = rFile.readlines()
        rFile.close()
        if 'none' in rList[wLen - 1]:
            
    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
    clock.tick(60)
