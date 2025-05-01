import pygame, sys, random

SCREEN_W, SCREEN_H = 1000, 600
SPACE_UP, SPACE_DOWN = 110, 540
SPEEDY_MAX = 5
BG_COLOR, BORDOR_COLOR = (0, 0, 80), (80, 80, 80)
G = 0.5
STONE_H_MIN, STONE_H_MAX, STONE_W = 50, 200, 20
STONE_SPACE = 160


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
        if fwork.status == 1:
            currentNum = 4
        scr.blit(self.pic, (int(self.x), int(self.y)),
                 (0, currentNum * self.h, self.w, self.h))


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


class CLS_framework(object):
    def __init__(self):
        pygame.init()
        self.scr = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption('RT GUNSHIP')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('simkai.ttf', 32)
        self.score = 0
        self.z10 = CLS_gunship('gunship.bmp', 40, 100, 84, 30, 3, 4)
        self.stoneList = []
        self.status = 0
        self.face = pygame.image.load('face.bmp')

    def play(self):
        if self.status == 1:
            return
        self.draw_field()
        self.stone_do()
        self.z10.move()
        self.z10.draw(self.scr)
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
                    self.status = 1
                else:
                    self.score += stone.h * self.z10.spdX
        if SCREEN_W - lastStoneX > random.randint(STONE_SPACE, int(STONE_SPACE * 1.5)):
            stone = CLS_stone()
            self.stoneList.append(stone)

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

    def keyup(self, key):
        if event.key == pygame.K_UP:
            self.z10.accY = 0


fwork = CLS_framework()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            fwork.keydown(event.key)
        elif event.type == pygame.KEYUP:
            fwork.keyup(event.key)
    fwork.play()
