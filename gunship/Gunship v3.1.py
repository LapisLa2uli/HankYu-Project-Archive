import pygame, sys, random
from math import *

SCREEN_W, SCREEN_H = 1000, 600
SPACE_UP, SPACE_DOWN = 110, 540
SPEEDY_MAX = 5
BG_COLOR, BORDOR_COLOR = (0, 0, 80), (80, 80, 80)
G = 0.5
STONE_H_MIN, STONE_H_MAX, STONE_W = 50, 200, 20
STONE_SPACE = 160
GUNSHIP_HP_MAX = 50
GUNSHIP_AMMO = 1000


def collide(x1, y1, w1, h1, x2, y2, w2, h2):
    if x1 + w1 >= x2 and x1 <= x2 + w2 and y1 + h1 >= y2 and y1 <= y2 + h2:
        return True
    else:
        return False


class CLS_gunship(object):
    def __init__(self, picFile, x, y, w, h, interval, frameNum):
        pic = pygame.image.load(picFile)
        pic.set_colorkey((0, 0, 0))
        self.pic = pic
        self.x, self.y, self.w, self.h = x, y, w, h
        self.interval, self.frameNum = interval, frameNum
        self.counter = 0
        self.spdX = 3
        self.spdY, self.accY = 0, 0
        self.hp = GUNSHIP_HP_MAX
        self.bulletList = []
        self.droneList = []
        self.ammo = GUNSHIP_AMMO
        self.wingmen = 4

    def move(self):
        self.spdY += (self.accY + G)
        if self.spdY < -SPEEDY_MAX:
            self.spdY = -SPEEDY_MAX
        elif self.spdY > SPEEDY_MAX:
            self.spdY = SPEEDY_MAX
        self.y += self.spdY
        if self.y < SPACE_UP:
            self.y = SPACE_UP
        elif self.y > SPACE_DOWN - self.h:
            self.y = SPACE_DOWN - self.h

    def draw(self, scr):
        currentNum = (self.counter // self.interval) % self.frameNum
        self.counter += 1
        if fwork.status == 1 or self.hp <= 0:
            currentNum = 4
        scr.blit(self.pic, (int(self.x), int(self.y)),
                 (0, currentNum * self.h, self.w, self.h))
        pygame.draw.rect(scr, (0, 255, 0),
                         (self.x, self.y + 36, GUNSHIP_HP_MAX, 5), 1)
        if self.hp <= 0:
            fwork.die()
            return
        lifeColor = int(self.hp / GUNSHIP_HP_MAX * 255)
        pygame.draw.rect(scr, (255 - lifeColor, lifeColor, 0),
                         (self.x, self.y + 36, self.hp, 5), 0)


class CLS_bullet(object):
    def __init__(self, picFile, x, y, spdX, spdY):
        pic = pygame.image.load(picFile)
        pic.set_colorkey((0, 0, 0))
        self.pic = pic
        self.x, self.y = x, y
        self.w, self.h = pic.get_size()
        self.spdX, self.spdY = spdX, spdY

    def move(self):
        self.x += self.spdX
        self.y += self.spdY

    def draw(self, scr):
        scr.blit(self.pic, (int(self.x), int(self.y)))


class CLS_stone(object):
    def __init__(self):
        self.x, self.w = SCREEN_W, STONE_W
        h = random.randint(STONE_H_MIN, STONE_H_MAX)
        self.h = h
        if h % 2 == 0:
            self.y = SPACE_UP
        else:
            self.y = SPACE_DOWN - h

    def move(self):
        self.x -= fwork.z10.spdX

    def draw(self, scr):
        pygame.draw.rect(scr, (80, 80, 80), (self.x, self.y, self.w, self.h), 0)


class CLS_drone(object):
    def __init__(self, picFile, x, y, w, h, interval, frameNum):
        pic = pygame.image.load(picFile)
        pic.set_colorkey((0, 0, 0))
        self.pic = pic
        self.x, self.y, self.w, self.h = x, y, w, h
        self.interval, self.frameNum = interval, frameNum
        self.counter = 0
        self.spdX = 3
        self.spdY, self.accY = 0, 0
        self.hp = GUNSHIP_HP_MAX // 2
        self.bulletList = []
        self.destY = random.randint(0, SCREEN_H)

    def move(self):
        if self.hp <= 0:
            self.x -= fwork.z10.spdX
        if self.destY < self.y:
            self.accY = -1
        else:
            self.accY = 0
        self.spdY += (self.accY + G)
        if self.spdY < -SPEEDY_MAX:
            self.spdY = -SPEEDY_MAX
        elif self.spdY > SPEEDY_MAX:
            self.spdY = SPEEDY_MAX
        self.y += self.spdY
        if self.y < SPACE_UP:
            self.y = SPACE_UP
        elif self.y > SPACE_DOWN - self.h:
            self.y = SPACE_DOWN - self.h
        if self.x == 90:
            self.bulletList.append(CLS_bullet('bullet.bmp', self.x + 62, self.y + 26, 15, random.random()))
            pygame.mixer.Sound('bullet.wav').play()

    def draw(self, scr):
        currentNum = (self.counter // self.interval) % self.frameNum
        self.counter += 1
        if fwork.status == 1 or self.hp <= 0:
            currentNum = 4
        scr.blit(self.pic, (int(self.x), int(self.y)),
                 (0, currentNum * self.h, self.w, self.h))
        pygame.draw.rect(scr, (0, 255, 0),
                         (self.x, self.y + 36, GUNSHIP_HP_MAX // 2, 5), 1)
        lifeColor = int(self.hp / (GUNSHIP_HP_MAX // 2) * 255)
        if lifeColor >= 0:
            pygame.draw.rect(scr, (255 - lifeColor, lifeColor, 0),
                             (self.x, self.y + 36, self.hp, 5), 0)


class CLS_ammo(object):
    def __init__(self, picfile, scale):
        pic = pygame.image.load(picfile)
        pic = pygame.transform.scale(pic, (pic.get_width() * scale, pic.get_height() * scale))
        self.pic = pic
        self.x, self.y = SCREEN_W, random.randint(SPACE_UP, SPACE_DOWN - pic.get_height())
        self.w, self.h = pic.get_width(), pic.get_height()
        while True:
            flag = 0
            for stone in fwork.stoneList:
                if collide(self.x, self.y, self.w, self.h, stone.x, stone.y, stone.w, stone.h):
                    flag = 1
                    break
            if flag == 0:
                break
            else:
                self.x, self.y = SCREEN_W, random.randint(SPACE_UP, SPACE_DOWN - pic.get_height())

    def draw(self, scr):
        if -self.w < self.x < SCREEN_W:
            scr.blit(self.pic, (self.x, self.y))


class CLS_boss(object):
    def __init__(self, picFile, x, y, w, h, interval, frameNum, hp):
        pic = pygame.image.load(picFile)
        pic = pygame.transform.flip(pic, True, False)
        pic.set_colorkey((0, 0, 0))
        self.pic = pic
        self.x, self.y, self.w, self.h = x, y, w, h
        self.interval, self.frameNum = interval, frameNum
        self.counter = 0
        self.spdX = 3
        self.spdY, self.accY = 0, 0
        self.hp = hp
        self.HP_MAX = hp
        self.missileList = []
        self.alt = SPACE_UP // 2 + SPACE_DOWN // 2
        self.tick = 0
        self.missileStatus = True
        self.dieStatus = False

    def move(self):
        range = 20
        if fwork.z10.y - range <= self.y <= fwork.z10.y + range:
            self.alt = random.randint(SPACE_UP, SPACE_DOWN - self.w)
        if self.y < self.alt:
            self.accY = 0
        else:
            self.accY = -1
        self.spdY += (self.accY + G)
        if self.spdY < -SPEEDY_MAX:
            self.spdY = -SPEEDY_MAX
        elif self.spdY > SPEEDY_MAX:
            self.spdY = SPEEDY_MAX
        self.y += self.spdY
        if self.y < SPACE_UP:
            self.y = SPACE_UP
        elif self.y > SPACE_DOWN - self.h:
            self.y = SPACE_DOWN - self.h

    def dieMove(self):
        self.accY = 0
        self.spdX = -fwork.z10.spdX
        self.spdY += (self.accY + G)
        if self.spdY < -SPEEDY_MAX:
            self.spdY = -SPEEDY_MAX
        elif self.spdY > SPEEDY_MAX:
            self.spdY = SPEEDY_MAX
        self.y += self.spdY
        self.x += self.spdX
        if self.y < SPACE_UP:
            self.y = SPACE_UP
        elif self.y > SPACE_DOWN - self.h:
            self.y = SPACE_DOWN - self.h

    def draw(self, scr):
        currentNum = (self.counter // self.interval) % self.frameNum
        self.counter += 1
        if self.dieStatus == True:
            currentNum = 4
        scr.blit(self.pic, (int(self.x), int(self.y)),
                 (0, currentNum * self.h, self.w, self.h))
        pygame.draw.rect(scr, (0, 255, 0),
                         (self.x, self.y + 36, GUNSHIP_HP_MAX, 5), 1)
        lifeColor = int(self.hp / self.HP_MAX * 255)
        if lifeColor < 0:
            lifeColor = 0
        pygame.draw.rect(scr, (255 - lifeColor, lifeColor, 0),
                         (self.x, self.y + 36, self.hp / self.HP_MAX * GUNSHIP_HP_MAX, 5), 0)

    def fire(self):
        self.missileList.append(CLS_missile())


class CLS_smoke(object):
    def __init__(self, x, y):
        self.pic = pygame.image.load('smoke.png')
        self.pic = pygame.transform.scale(self.pic, (self.pic.get_width() * 0.02, self.pic.get_height() * 0.02))
        self.x, self.y = x, y
        self.counter = 0
        self.pic.set_colorkey((255, 255, 255))

    def move(self):
        self.x -= fwork.z10.spdX

    def draw(self, scr):
        new_pic = pygame.transform.scale(self.pic,
                                         (self.pic.get_width() + self.counter, self.pic.get_height() + self.counter))
        new_pic.set_alpha(255 - self.counter * 7)
        scr.blit(new_pic, (self.x, self.y))
        self.counter += 1


class CLS_missile(object):
    def __init__(self):
        self.pic = pygame.image.load('missile.png')
        self.pic = pygame.transform.scale(self.pic, (self.pic.get_width() * 0.1, self.pic.get_height() * 0.1))
        self.x, self.y = fwork.boss.x, fwork.boss.y
        self.w, self.h = self.pic.get_width(), self.pic.get_height()
        self.direction = 270
        self.spdX, self.spdY, self.accX, self.accY = 0, 0, 0, 0
        self.thrust = 1
        self.max_speed = 10
        self.smokeList = []
        self.counter = 0
        self.hp = 10

    def get_direction(self):
        ratio = (fwork.z10.y - self.y) / (fwork.z10.x - self.x)

        Min = 100000
        dir = 0
        for i in range(180, 360,2 ):
            Fx = -abs(sin(360 - i) * self.thrust)
            Fy = -cos(radians(360 - i)) * self.thrust - G
            if Min > abs(Fy / Fx - ratio):
                Min = abs(Fy / Fx - ratio)
                dir = i
        self.direction = dir
        self.accY = (-cos(radians(360 - dir)) * self.thrust - G) / 2
        self.accX = (-abs(sin(360 - dir) * self.thrust)) / 2

    def move(self):
        # if self.accX != 0:
        # print(self.direction, self.x, self.y, self.spdX, self.spdY, self.accX, self.accY, self.accY / self.accX)
        self.get_direction()
        # calculating air resistance
        new_pic = pygame.transform.rotate(self.pic, 360 - self.direction)
        w = new_pic.get_width()
        h = new_pic.get_height()
        if self.spdY > 0:
            self.accY -= max(0, 0.0001 * w * abs(self.spdY) ** 2)
        if self.spdY < 0:
            self.accY += max(0, 0.0001 * w * abs(self.spdY) ** 2)
        if self.spdX > 0:
            self.accX -= max(0, 0.0001 * h * abs(self.spdX) ** 2)
        if self.spdX < 0:
            self.accX += max(0, 0.0001 * h * abs(self.spdX) ** 2)
        self.spdX += self.accX
        self.spdY += self.accY
        '''if self.spdY < -self.max_speed:
            self.spdY = -self.max_speed
        elif self.spdY > self.max_speed:
            self.spdY = self.max_speed
        if self.spdX < -self.max_speed:
            self.spdX = -self.max_speed
        elif self.spdX > self.max_speed:
            self.spdX = self.max_speed'''
        self.x += self.spdX
        self.y += self.spdY
        print(self.accY, self.accX, self.spdX, self.spdY, self.x, self.y)
        if self.counter % 3 == 0:
            self.smokeList.append(CLS_smoke(self.x + self.w, self.y + self.h // 2))
        self.counter += 1

    def draw(self, scr):
        new_pic = pygame.transform.rotate(self.pic, 360 - self.direction)
        self.w = new_pic.get_width()
        self.h = new_pic.get_height()
        scr.blit(new_pic, (self.x, self.y))
        for smoke in self.smokeList:
            smoke.move()
            smoke.draw(scr)
        for i in range(len(self.smokeList)):
            if self.smokeList[i].x + self.smokeList[i].pic.get_width() + self.smokeList[i].counter < 0 or \
                    self.smokeList[i].counter == 250:
                self.smokeList.pop(i)
            if i == len(self.smokeList) - 1:
                break


class CLS_explosion(object):
    def __init__(self, x, y, scale, duration, pic):
        self.pic = pygame.image.load(pic)
        self.pic = pygame.transform.scale(self.pic, (self.pic.get_width() * scale, self.pic.get_height() * scale))
        self.x, self.y = x - self.pic.get_width() / 2, y - self.pic.get_height() / 2
        self.counter = 0
        self.duration = duration

    def move(self):
        self.x -= fwork.z10.spdX
        self.duration -= 1

    def draw(self, scr):
        if self.counter > self.duration:
            return False
        scr.blit(self.pic, (self.x, self.y))


class CLS_framework(object):
    def __init__(self):
        pygame.init()
        self.scr = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption('RT GUNSHIP')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('simkai.ttf', 32)
        self.score = 2000000
        self.z10 = CLS_gunship('gunship.bmp', 40, 100, 84, 30, 3, 4)
        self.stoneList = []
        self.status = 0
        self.face = pygame.image.load('face.bmp')
        self.hiScore = 0
        self.userName = ''
        self.droneList = []
        self.bStatus = 0
        self.ammoList = []
        self.frequency = 600
        self.bossStatus = False
        self.boss = CLS_boss('gunship.bmp', SCREEN_W - 84 - 20, (SPACE_UP + SPACE_DOWN) // 2, 84, 30, 3, 4,
                             self.score // 10000)
        self.prevScore = 0
        self.explosionList = []

    def play(self):
        if self.status == 1:
            return

        self.draw_field()

        self.ammo_do()
        self.stone_do()
        self.z10.move()
        self.z10.draw(self.scr)
        self.bullet_do()
        self.drone_do()
        self.boss_do()
        self.explosion_do()
        pygame.display.update()
        self.clock.tick(100)

    def draw_field(self):
        self.scr.fill((0, 0, 0))
        pygame.draw.rect(self.scr, BG_COLOR, (0, SPACE_UP, SCREEN_W, SPACE_DOWN - SPACE_UP), 0)
        pygame.draw.rect(self.scr, BORDOR_COLOR, (0, SPACE_DOWN, SCREEN_W, 10), 0)
        pygame.draw.rect(self.scr, BORDOR_COLOR, (0, SPACE_UP - 10, SCREEN_W, 10), 0)
        img = self.font.render('SCORE:' + str(self.score), True, (160, 180, 0))
        self.scr.blit(img, (SCREEN_W - 300, 10))
        self.scr.blit(self.face, (0, 0))
        img = self.font.render('Hi-SCORE: ' + str(self.hiScore), True, (255, 0, 0))
        self.scr.blit(img, (SCREEN_W - 300, 50))
        if self.z10.ammo > 0:
            img = self.font.render('Ammo:' + str(self.z10.ammo), True, (255, 0, 0))
            self.scr.blit(img, (10, SCREEN_H - 30))
        else:
            img = self.font.render('No Ammo!', True, (255, 0, 0))
            self.scr.blit(img, (10, SCREEN_H - 30))

    def ammo_do(self):
        if len(self.ammoList) > 0:
            if self.ammoList[0].x + self.ammoList[0].w < 0:
                self.ammoList.pop(0)
        if random.randint(self.frequency, 1000) == 1000:
            self.ammoList.append(CLS_ammo("ammo.png", 0.1))
        for ammo in self.ammoList:
            ammo.draw(self.scr)
            ammo.x -= self.z10.spdX
        for i in range(len(self.ammoList)):
            if collide(self.z10.x, self.z10.y, self.z10.w, self.z10.h, self.ammoList[i].x, self.ammoList[i].y,
                       self.ammoList[i].w, self.ammoList[i].h):
                self.z10.ammo += 100
                self.ammoList.pop(i)
            if i == len(self.ammoList) - 1:
                break

    def stone_do(self):
        lastStoneX = 0
        for stone in self.stoneList:
            stone.move()
            stone.draw(self.scr)
            lastStoneX = stone.x
            if stone.x + stone.w < 0:
                self.stoneList.pop(0)
            if (self.z10.x + self.z10.w >= stone.x) and (self.z10.x <= stone.x + stone.w):
                if (self.z10.y + self.z10.h >= stone.y) and (self.z10.y <= stone.y + stone.h):
                    self.z10.hp -= 1
                    if self.z10.hp <= 0:
                        self.die()
                else:
                    self.score += abs(stone.h) * self.z10.spdX
                    if self.score > self.hiScore:
                        self.hiScore = self.score
        if SCREEN_W - lastStoneX > random.randint(STONE_SPACE, int(STONE_SPACE * 1.5)) and self.bossStatus == False:
            stone = CLS_stone()
            self.stoneList.append(stone)

    def bullet_do(self):
        if self.bStatus == 1 and self.z10.ammo > 0:
            self.z10.bulletList.append(CLS_bullet('bullet.bmp', self.z10.x + 62, self.z10.y + 26, 20, random.random()))
            self.z10.ammo -= 1

            pygame.mixer.stop()
            pygame.mixer.Sound('bullet.wav').play()
        for bullet in self.z10.bulletList:
            bullet.move()
            bullet.draw(self.scr)
            for stone in self.stoneList:
                w, h = bullet.pic.get_size()
                if collide(bullet.x, bullet.y, bullet.w, bullet.h,
                           stone.x, stone.y, stone.w, stone.h):
                    self.explosionList.append(CLS_explosion(bullet.x - 20, bullet.y - 20, 0.05, 3, 'explosion.png'))
                    stone.h -= 20
                    if stone.y > SPACE_UP:
                        stone.y += 20
                    bullet.x = SCREEN_W
            if collide(bullet.x, bullet.y, bullet.w, bullet.h,
                       self.boss.x, self.boss.y, self.boss.w, self.boss.h) and self.bossStatus == True:
                self.explosionList.append(CLS_explosion(bullet.x - 20, bullet.y - 20, 0.05, 3, 'explosion.png'))
                # print('collide')
                self.boss.hp -= 1
        for i in range(len(self.z10.bulletList)):
            if i >= len(self.z10.bulletList):
                break
            if self.z10.bulletList[i].x > SCREEN_W + 100 or self.z10.bulletList[i].y < SPACE_UP or self.z10.bulletList[
                i].y > SPACE_DOWN:
                if self.z10.bulletList[i].y > SPACE_DOWN:
                    self.explosionList.append(
                        CLS_explosion(self.z10.bulletList[i].x, self.z10.bulletList[i].y - 10, 0.05, 3,
                                      'explosion_grnd.png'))
                self.z10.bulletList.pop(i)

        for drone in self.z10.droneList:
            for bullet in drone.bulletList:
                bullet.move()
                bullet.draw(self.scr)
                for stone in self.stoneList:
                    w, h = bullet.pic.get_size()
                    if collide(bullet.x, bullet.y, bullet.w, bullet.h,
                               stone.x, stone.y, stone.w, stone.h):
                        self.explosionList.append(CLS_explosion(bullet.x, bullet.y, 0.05, 5, 'explosion.png'))
                        stone.h -= 10
                        if stone.y > SPACE_UP:
                            stone.y += 10
                        bullet.x = SCREEN_W

    def drone_do(self):
        for drone in self.z10.droneList:
            drone.move()
            for stone in self.stoneList:
                if collide(drone.x, drone.y, drone.w, drone.h, stone.x, stone.y, stone.w, stone.h):
                    drone.hp -= 20
                    stone.h -= 30
                    if stone.y > SPACE_UP:
                        stone.y += 30
            i = 0
            while i < len(drone.bulletList):
                if drone.bulletList[i].x > SCREEN_W or drone.bulletList[i].y > SPACE_DOWN:
                    drone.bulletList.pop(i)
                i += 1
            drone.draw(self.scr)
        for i in range(len(self.z10.droneList)):
            if i >= len(self.z10.droneList):
                break
            if self.z10.droneList[i].x <= 0:
                self.z10.droneList.pop(i)

    def boss_do(self):
        if self.bossStatus == False:
            if (
                    self.score // 1000000) % 2 == 0 and self.score // 1000000 != 0 and self.score // 1000000 > self.prevScore // 1000000:
                self.prevScore = self.score
                self.bossStatus = True
                self.boss = CLS_boss('gunship.bmp', SCREEN_W - 84 - 20, (SPACE_UP + SPACE_DOWN) // 2, 84, 30, 3, 4,
                                     self.score // 10000)
        elif self.bossStatus == True:
            for drone in self.z10.droneList:
                drone.hp = 0
            if self.boss.hp <= 0:
                self.boss.dieStatus = True
            if self.boss.dieStatus == False:
                self.boss.move()
                self.boss.draw(self.scr)
                if (self.boss.tick // 100) % 2 == 1 and self.stoneList == []:
                    if self.boss.missileStatus == True:
                        self.boss.fire()
                        self.boss.missileStatus = False
                else:
                    self.boss.missileStatus = True
                self.boss.tick += 1
                self.missile_do()
            else:
                self.boss.dieMove()
                self.boss.move()
                self.boss.draw(self.scr)
                if self.boss.x + self.boss.w < 0:
                    self.bossStatus = False

    def missile_do(self):
        for missile in self.boss.missileList:
            missile.move()
            missile.draw(self.scr)

        for i in range(len(self.boss.missileList)):
            if self.boss.missileList[i].x < 0 or self.boss.missileList[i].y < SPACE_UP or self.boss.missileList[i].y + \
                    self.boss.missileList[i].h > SPACE_DOWN or self.boss.missileList[i].hp <= 0:
                self.boss.missileList.pop(i)
                print()
            if i == len(self.boss.missileList):
                break
            if collide(self.boss.missileList[i].x, self.boss.missileList[i].y, self.boss.missileList[i].w,
                       self.boss.missileList[i].h, self.z10.x, self.z10.y, self.z10.w, self.z10.h):
                self.z10.hp -= 40
                self.boss.missileList.pop(i)
            if i == len(self.boss.missileList) - 1:
                break

    def explosion_do(self):
        for i in range(len(self.explosionList)):
            try:
                if self.explosionList[i].x <= -self.explosionList[i].pic.get_width() or self.explosionList[
                    i].duration <= 0:
                    self.explosionList.pop(i)
            except:
                break
        for i in range(len(self.explosionList)):
            self.explosionList[i].move()
            self.explosionList[i].draw(self.scr)

    def die(self):
        self.status = 1
        img = self.font.render('Press ENTER to Continue', True, (255, 0, 0))
        self.scr.blit(img, (200, 300))

    def keydown(self, key):
        if event.key == pygame.K_UP:
            self.z10.accY = -1
        if event.key == pygame.K_LEFT:
            self.z10.spdX -= 1
        if event.key == pygame.K_RIGHT:
            self.z10.spdX += 1
        if event.key == pygame.K_RETURN:
            self.status, self.score = 0, 0
            self.stoneList = []
            self.z10.droneList = []
            self.z10.bulletList = []
            self.z10.hp = GUNSHIP_HP_MAX
            self.z10.ammo = GUNSHIP_AMMO
            self.bossStatus = False
            self.prevScore = 0
        if event.key == ord(' '):
            self.bStatus = 1
        if event.key == ord('a'):
            if self.z10.wingmen > 0:
                self.z10.droneList.append(CLS_drone('gunship.bmp', self.z10.x + 50, self.z10.y, 84, 30, 3, 4))
                self.z10.wingmen -= 1
                print('a')

    def keyup(self, key):
        if event.key == ord(' '):
            self.bStatus = 0
        if event.key == pygame.K_UP:
            self.z10.accY = 0


fwork = CLS_framework()
# pygame.mixer.Sound('bg1.mp3').play(loops=-1)
try:
    f = open('score.txt', 'r')
    fwork.hiScore = eval(f.read())
    f.close()
except:
    f = open('score.txt', 'w')
    f.write('0')
    f.close()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            f = open('score.txt', 'w')
            f.write(str(fwork.hiScore))
            f.close()
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            fwork.keydown(event.key)
        elif event.type == pygame.KEYUP:
            fwork.keyup(event.key)
    fwork.play()
