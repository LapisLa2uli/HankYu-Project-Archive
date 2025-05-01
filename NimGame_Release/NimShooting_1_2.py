# NimGame Shooting Version 1.1

import pygame, sys, random, numpy, math, time

SCREEN_W, SCREEN_H = 1024, 768

def collide(x1, y1, w1, h1, x2, y2, w2, h2):
    if x1 + w1 >= x2 and x1 <= x2 + w2 and y1 + h1 >= y2 and y1 <= y2 + h2:
        return True
    else:
        return False

'''
def RT_get_pic(w,h,data,clrList,dw,scale):
    scr = pygame.Surface((w,h))
    RT_drawb(scr,data,clrList,dw,scale)
    return scr
def RT_drawb(scr,data,clrList,dw,scale):
    for y in range(len(data)):
        row=bin(data[y])[2:]
        row='0'*(dw-len(row))+row
        for x in range(dw):
            c=clrList[int(row[x])]
            pygame.draw.rect(scr, c,
                             (int(x * scale), int(y * scale), scale, scale), 0)
'''

class CLS_disk(object):
    group = []

    def __init__(self, rect, color, speedX, speedY):
        self.rect = pygame.Rect(rect)
        self.color = color
        self.speedX, self.speedY, self.accY = speedX, speedY, 0.02
        CLS_disk.group.append(self)

    def run(self):
        self.speedY += self.accY
        self.rect.x += self.speedX
        self.rect.y += self.speedY

    def draw(self,scr):
        pygame.draw.ellipse(scr, self.color, self.rect, 0)


class CLS_gun(object):
    def __init__(self, x, y, r, tDiskNum, pIndex):
        self.x, self.y, self.r = x, y, r
        self.score = 0
        self.tDiskNum = tDiskNum
        self.pIndex = pIndex
        self.diskNum = self.tDiskNum
        self.bulletNum = 12
        self.fireTime = 0
        self.font = pygame.font.Font('PixelatedEleganceRegular-ovyAA.ttf', 32)
        self.font2 = pygame.font.Font('PixelatedEleganceRegular-ovyAA.ttf', 40)
        self.font3 = pygame.font.Font('PixelatedEleganceRegular-ovyAA.ttf', 26)
        self.reloadT = 0

    def update(self):
        if pygame.time.get_ticks() - self.fireTime > 100:
            self.fireTime = 0

    def draw(self, scr):
        self.update()
        x, y, r = self.x, self.y, self.r
        pygame.draw.circle(scr, (255, 255, 255), (x, y), r, 1)
        pygame.draw.circle(scr, (255, 255, 255), (x, y), int(r * 0.4), 1)
        pygame.draw.line(scr, (155, 155, 155), (x - r, y), (x + r, y), 1)
        pygame.draw.line(scr, (155, 155, 155), (x, y - r), (x, y + r), 1)
        if self.fireTime > 0:
            pygame.draw.polygon(scr, (255, 0, 0), \
                                ((x - int(r * 0.4), y - 4), (x - int(r * 0.4), y + 4), (x, y)), 0)
            pygame.draw.polygon(scr, (255, 0, 0), \
                                ((x + int(r * 0.4), y - 4), (x + int(r * 0.4), y + 4), (x, y)), 0)
        if self.bulletNum != -1:
            scr.blit(self.font.render(f"Ammo: {self.bulletNum} / 12", True, (255, 255, 150)), \
                     ((SCREEN_W - self.font.size(f"Ammo: {self.bulletNum} / 12")[0]) // 2, SCREEN_H * 4 // 5))
        else:
            scr.blit(self.font.render(f"Reloading...", True, (255, 255, 150)), \
                     ((SCREEN_W - self.font.size(f"Reloading...")[0]) // 2, SCREEN_H * 4 // 5))
class CLS_shooter(object):
    def __init__(self):
        self.x=SCREEN_W // 2
        self.y=SCREEN_H - 20
        self.w=30
        self.h=10
        self.spdX=0
        self.bulletList=[]
        self.gunPic=pygame.Surface((self.w,self.h))
        self.gunPic.set_colorkey((0,0, 0))
        self.rotation=0
        pygame.draw.rect(self.gunPic, (0, 0, 255), (0,0, self.w, self.h))
    def rotate(self,mouseX,mouseY):
        self.gunPic=pygame.Surface((self.w,self.h))
        pygame.draw.rect(self.gunPic, (0, 0, 255), (0, 0, self.w, self.h))
        self.gunPic.set_colorkey((0,0, 0))

        try:
            self.rotation=-numpy.degrees(numpy.arctan((mouseY-self.y)/(mouseX-self.x)))
            self.gunPic=pygame.transform.rotate(self.gunPic,self.rotation)
        except ZeroDivisionError:
            self.gunPic = pygame.transform.rotate(self.gunPic, -90)
            pass

    def shoot(self):
        self.bulletList.append(CLS_bullet(self.x,self.y,self.rotation))
    def draw(self,scr):
        scr.blit(self.gunPic,(self.x - self.gunPic.get_width() / 2,
                              self.y - self.gunPic.get_height() / 2))
class CLS_bullet(object):
    def __init__(self, x, y, dir):
        self.x, self.y = x, y
        speed = 5
        if dir > 0:
            self.spdX = (speed ** 2 / (numpy.tan(numpy.radians(dir)) ** 2 + 1)) ** 0.5
            self.spdY = int(self.spdX * numpy.tan(numpy.radians(dir)))
        elif dir <= 0:
            self.spdX = -(speed ** 2 / (numpy.tan(numpy.radians(dir)) ** 2 + 1)) ** 0.5
            self.spdY = self.spdX * numpy.tan(numpy.radians(dir))
        if self.spdX == 0 and self.spdY == 0:
            self.spdY = 7
        self.bulletPic=pygame.image.load('bullet.bmp')
        self.bulletPic.set_colorkey((0,0,0))
        self.bulletPic=pygame.transform.rotate(self.bulletPic,dir)
        self.bulletPic=pygame.transform.scale(self.bulletPic, (20, 38))
        
    def move(self):
        self.x+=self.spdX
        self.y-=self.spdY
        
    def draw(self,scr):
        scr.blit(self.bulletPic,(self.x,self.y))
        

'''
for y in range(6):
    for x in range(32):
        bg.blit(Tree, (x * 32, y * 32 + 384))
        bg.blit(Brick, (x * 32, y * 32 + 576))
'''
class NimShootingFW(object):
    def __init__(self, tDiskNum, pIndex):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        self.clock = pygame.time.Clock()
        self.tDiskNum = tDiskNum
        self.pIndex = pIndex
        pygame.mouse.set_visible(False)
        self.gun = CLS_gun(SCREEN_W // 2, SCREEN_H // 2, 30, self.tDiskNum, self.pIndex)
        self.t0 = pygame.time.get_ticks()
        self.t1 = random.randint(0, 1000) + 300
        self.tEnd = 0
        self.finishFlag = 0

        '''
        bBrick=[0xff,0x04,0x04,0x04,0xff,0x80,0x80,0x80]
        brickClrList=[[255,127,80],[64,64,64]]
        bTree=[0x02,0x15,0x07,0x19,0x2e,0x1f,0xfb,0x6e]
        treeClrList=[[0,50,0],[0,120,0]]
        Tree = RT_get_pic(32,32,bTree, treeClrList,8, 4)
        Brick = RT_get_pic(32,32,bBrick, brickClrList,8, 4)
        '''
        self.shooter=CLS_shooter()
        self.bg=pygame.Surface((1024,768))
        self.bg.fill((0,0,0))

        self.sf_frame = pygame.image.load('SF_frame.png')
        self.sf_w, self.sf_h = 800, 600
        self.sf_frame = pygame.transform.scale(self.sf_frame, (self.sf_w, self.sf_h))
        self.sf_frame.set_colorkey((255, 255, 255))

    def play(self, cPlayer):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                i = 0
                if self.gun.bulletNum > 0:
                    self.shooter.shoot()
                self.gun.bulletNum -= 1
                if self.gun.bulletNum < -1:
                    self.gun.bulletNum = -1
                '''gun.fireTime = pygame.time.get_ticks()
                while i < len(CLS_disk.group):
                    d = CLS_disk.group[i]
                    if d.rect.collidepoint(gun.x, gun.y):
                        CLS_disk.group.pop(i)
                        gun.score += 1
                    i += 1'''
                if self.gun.bulletNum == -1:
                    if self.gun.reloadT == 0:
                        self.gun.reloadT = time.time()
                    elif time.time() - self.gun.reloadT > 1.5:
                        self.gun.bulletNum = 12
                        self.gun.reloadT = 0
            if event.type == pygame.MOUSEMOTION:
                self.gun.x, self.gun.y = event.pos
                self.shooter.rotate(event.pos[0],event.pos[1])
            if event.type == pygame.QUIT:
                pygame.quit()
                return -1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and self.finishFlag == 1:
                    return self.gun.score
                if event.key == pygame.K_ESCAPE:
                    return -3
        
        if pygame.time.get_ticks() - self.t0 > self.t1 and self.gun.diskNum > 0:
            self.gun.diskNum -= 1
            w = random.randint(40, 80)
            h = w // 2
            if random.random() < 0.5:
                disk = CLS_disk((0, SCREEN_H, w, h), (random.randint(150, 255), random.randint(0, 50), random.randint(0, 200)), \
                            random.random() + 1.5, -4.5 + random.random())
            else:
                disk = CLS_disk((SCREEN_W, SCREEN_H, w, h), (random.randint(0, 50), random.randint(150, 255), random.randint(0, 200)), \
                            random.random() - 2.5, -4.5 + random.random())
            self.t0 = pygame.time.get_ticks()
            self.t1 = random.randint(0, 1000) + 300
        if time.time() - self.gun.reloadT > 1.5 and self.gun.bulletNum == -1:
            self.gun.bulletNum = 12
            self.gun.reloadT = 0
        for i in range(len(self.shooter.bulletList)-1,-1,-1):
            self.shooter.bulletList[i].move()
            if self.shooter.bulletList[i].x > SCREEN_W or self.shooter.bulletList[i].y<0:
                self.shooter.bulletList.pop(i)
                break
            for j in range(len(CLS_disk.group)-1,-1,-1):
                if collide(self.shooter.bulletList[i].x, self.shooter.bulletList[i].y, self.shooter.bulletList[i].bulletPic.get_width(),
                           self.shooter.bulletList[i].bulletPic.get_height(), CLS_disk.group[j].rect[0], CLS_disk.group[j].rect[1], CLS_disk.group[j].rect[2], CLS_disk.group[j].rect[3]):
                    self.shooter.bulletList.pop(i)
                    CLS_disk.group.pop(j)
                    self.gun.score += 1
                    break
        self.screen.fill((0,0,0))
        self.screen.blit(self.bg,(0,0))

        self.screen.blit(self.gun.font.render(f"Player {cPlayer + 1}", True, (255, 50, 50)), (SCREEN_W - self.gun.font.size(f"Player {cPlayer + 1}")[0] - 10, SCREEN_H - self.gun.font.size(f"Player {cPlayer + 1}")[1] - 10))
        self.screen.blit(self.gun.font3.render("Press esc to return to homepage", True, (255, 255, 150)), (15, SCREEN_H - 30))
        
        for disk in CLS_disk.group:
            disk.run()
            disk.draw(self.screen)
        self.gun.draw(self.screen)
        img = self.gun.font.render('SCORE:' + str(self.gun.score) + '      DISKS:' \
                          + str(self.gun.diskNum), True, (240, 0, 140))
        self.screen.blit(img, (10, 10))
        i = 0
        for i in range(len(self.shooter.bulletList)-1,-1,-1):
            self.shooter.bulletList[i].draw(self.screen)
        while i < len(CLS_disk.group):
            if CLS_disk.group[i].rect.y<0:
                CLS_disk.group.pop(i)
            i += 1
        self.shooter.draw(self.screen)

        if self.gun.diskNum == 0:
            if self.tEnd == 0:
                self.tEnd = time.time()
            if time.time() - self.tEnd > 1.5:
                self.finishFlag = 1
        if self.finishFlag == 1:
            self.screen.blit(self.sf_frame, ((SCREEN_W - self.sf_w) // 2, (SCREEN_H - self.sf_h) // 2))
            if self.gun.score == 0:
                self.screen.blit(self.gun.font2.render("L", True, (220, 125, 25)), ((SCREEN_W - self.gun.font2.size("L")[0]) // 2, SCREEN_H * 8 // 35))
            else:
                self.screen.blit(self.gun.font2.render("CONGRATULATIONS!", True, (220, 125, 25)), ((SCREEN_W - self.gun.font2.size("CONGRATULATIONS!")[0]) // 2, SCREEN_H * 8 // 35))
            self.screen.blit(self.gun.font2.render(f"You collected {self.gun.score} disks!", True, (150, 150, 255)), ((SCREEN_W - self.gun.font2.size(f"You collected {self.gun.score} disks!")[0]) // 2, SCREEN_H * 2 // 5))
            self.screen.blit(self.gun.font.render(f"{self.gun.tDiskNum - self.gun.score} disks remaining in pile {self.gun.pIndex + 1}", True, (75, 125, 255)), ((SCREEN_W - self.gun.font.size(f"{self.gun.tDiskNum - self.gun.score} disks remaining in pile {self.gun.pIndex + 1}")[0]) // 2, SCREEN_H * 3 // 5))
            self.screen.blit(self.gun.font.render("Press Enter to Continue", True, (255, 150, 50)), ((SCREEN_W - self.gun.font.size("Press Enter to Continue")[0]) // 2, SCREEN_H * 27 // 35))
        
        pygame.display.update()
        self.clock.tick(500)
        return -2
