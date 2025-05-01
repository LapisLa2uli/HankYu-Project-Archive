# Hangman V2.0
import pygame,sys,random
SCREEN_W,SCREEN_H=760,960
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
        self.x,self.y=random.randint(20,SCREEN_W-20),0
        self.spdY = 4 * random.random() + 2
    def draw(self,scr):
        scr.blit(font.render(self.char,True,(0,255,0)), (self.x, self.y))
        return
    def move(self):
        self.y+=self.spdY
        return
    
pygame.init()
screen=pygame.display.set_mode((SCREEN_W,SCREEN_H))
clock=pygame.time.Clock()
font=pygame.font.Font('monaco.ttf',32)
cList =[]
catcher=CLS_Catcher()
while True:
    screen.fill((0,0,0))
    catcher.x=pygame.mouse.get_pos()[0]
    catcher.draw(screen)
    charList, xyList = [], []
    for i in cList:
        charList.append(i.char)
        xyList.append([i.x, i.y])
    if random.randint(1,12 * len(cList) + 10)==1:
        c = CLS_Character()
        while c.char in charList:
            c = CLS_Character()
        while True:
            flag = 0
            for coord in xyList:
                if (abs(coord[0] - c.x) <= 30) and (abs(coord[1] - c.y) <= 30):
                    flag = 1
                    break
            if flag == 1:
                c = CLS_Character()
                continue
            break
        cList.append(c)
    for i in range(-1,-len(cList)-1,-1):
        try:
            if cList[i].y>SCREEN_H:
                cList.pop(i)
            else:
                cList[i].move()
                cList[i].draw(screen)
        except:
            pass
        
    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
    clock.tick(60)
