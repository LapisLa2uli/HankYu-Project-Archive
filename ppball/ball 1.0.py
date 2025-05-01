import pygame, sys, random

SCREEN_W, SCREEN_H = 1024, 600
BORDER_W = 10
accuracy = 8
coefFric = 0.25


def RT_show_txt(scr, txt, font, x, y, c):
    img = font.render(txt, True, c)
    scr.blit(img, (x, y))
    return


def set_new_ball(ball):
    ball.x, ball.y = SCREEN_W // 2, 10
    ball.spdX = (random.random() * 2 + 2) * (random.randint(0, 1) * 2 - 1)
    ball.spdY = random.random() * 2 + 1
    ball.GX, ball.GY = 0, 0
    ball.Fric=0
    if StatusS == 1:
        pygame.mixer.Sound('mariocoin.wav').play()


def RT_draw(screen, pixel, x0, y0, scale):
    color = (pygame.color.THECOLORS['black'],
             pygame.color.THECOLORS['gray32'],
             pygame.color.THECOLORS['gray64'],
             pygame.color.THECOLORS['white'],
             pygame.color.THECOLORS['red'],
             pygame.color.THECOLORS['green'],
             pygame.color.THECOLORS['blue'],
             pygame.color.THECOLORS['orange'],
             pygame.color.THECOLORS['brown'],
             pygame.color.THECOLORS['purple'],
             pygame.color.THECOLORS['yellow'],
             pygame.color.THECOLORS['cyan'],
             pygame.color.THECOLORS['sienna'],
             pygame.color.THECOLORS['chocolate'],
             pygame.color.THECOLORS['coral'],
             pygame.color.THECOLORS['darkgreen'])
    for y in range(len(pixel)):
        line = pixel[y]
        for x in range(len(line)):
            if 'A' <= line[x] <= 'F':
                c = color[ord(line[x]) - 55]
            elif '0' <= line[x] <= '9':
                c = color[eval(line[x])]
            else:
                continue
            pygame.draw.rect(screen, c,
                             (int(x * scale + x0), int(y * scale + y0), scale, scale), 0)


class CLS_ball(object):
    def __init__(self, x, y, spdX, spdY, scale, GX, GY):
        self.x, self.y = x, y
        self.spdX, self.spdY = spdX, spdY
        self.scale = scale
        self.w, self.h = 0, 0
        self.interval = 8
        self.counter = 0
        self.piclist = []
        self.GX, self.GY = GX, GY
        self.gamestatus = 0
        self.Fric = 0

    def add_pic(self, pixel):
        self.piclist.append(pixel)
        self.w = len(pixel[0]) * self.scale
        self.h = len(pixel) * self.scale

    def move(self):
        if -self.scale*10<=self.x<=SCREEN_W:
            self.x += self.spdX
            self.y += self.spdY
        self.spdY += self.GY / 2
        self.spdX += self.GX
        if self.y < BORDER_W:
            self.spdY *= -1
            if self.spdX > 0:
                self.spdX += self.Fric
            if self.spdX < 0:
                self.spdX -= self.Fric
            self.Fric /= 2 / coefFric
            self.GY /= 2 / coefFric
        if self.y > SCREEN_H - self.h - BORDER_W:
            self.spdY *= -1
            if self.spdX > 0:
                self.spdX -= self.Fric * coefFric
            if self.spdX < 0:
                self.spdX += self.Fric * coefFric
            self.Fric /= 2 / coefFric
            self.GY /= 2 / coefFric
        if StatusG==True and random.randint(0,50)==1:
            self.GX=random.randint(-8,8)
            self.GY=random.randint(-5,5)
            self.GX*=0.01
            self.GY*=0.01
        self.collide(paddleR, self.GX, self.GY)
        self.collide(paddleL, self.GX, self.GY)

    def draw(self, scr):
        RT_draw(scr, \
                self.piclist[int(self.counter) // self.interval % len(self.piclist)], \
                self.x, self.y, self.scale)
        self.counter += self.spdX * -0.5 * self.Fric

    def collide(self, pad, GX, GY):
        if self.spdX < 0:
            distance = abs(pad.x + pad.w - self.x)
        else:
            distance = abs(self.x + self.w - pad.x)
        if distance <= abs(self.spdX / 2):
            if pad.y-abs(self.spdX)**0.5 <= self.y + self.h // 2 <= (pad.y + pad.h)+abs(self.spdX)**0.5:
                self.spdX *= -1
                if StatusG == 1:
                    self.GX = random.randint(-8, 8)
                self.GX *= 0.01
                if StatusA == 1:
                    self.GY = -pad.friction * coefFric
                if StatusG == 1:
                    self.GY = random.randint(-5, 5)
                self.GY *= 0.01
                if StatusF == 1:
                    self.spdY += (pad.spdY + pad.friction // 2) * coefFric
                    self.Fric = pad.friction * coefFric
                if StatusS == 1:
                    pygame.mixer.Sound('hit.wav').play()
                if StatusD:
                    print('Collided with paddle! From left to right: GX, GY, ball.Fric, pad.friction, coefFric.\n', \
                          self.GX, self.GY, self.Fric, pad.friction, coefFric, '\n')
            else:

                if self.spdX < 0 and self.gamestatus == 0:
                    self.gamestatus = 1
                    paddleR.score += 1
                    if StatusS == 1:
                        pygame.mixer.Sound('mariodie.wav').play()
                elif self.spdX > 0 and self.gamestatus == 0:
                    self.gamestatus = 1
                    paddleL.score += 1
                    if StatusS == 1:
                        pygame.mixer.Sound('mariodie.wav').play()


class CLS_paddle(object):
    def __init__(self, x, y, w, h, c=(200, 200, 0)):
        self.x, self.y = x, y
        self.w, self.h = w, h
        self.spdY = 0
        self.c = c
        self.accY = 0
        self.friction = 0.5
        self.score = 0

    def move(self):
        self.spdY += self.accY
        self.friction = self.spdY / 2
        self.y += self.spdY
        if self.y < BORDER_W:
            self.y = BORDER_W
            self.spdY = 0
        if self.y > SCREEN_H - self.h - BORDER_W:
            self.y = SCREEN_H - self.h - BORDER_W
            self.spdY = 0

    def draw(self, scr):
        pygame.draw.rect(scr, self.c, (self.x, self.y, self.w, self.h), 0)

    def AI(self):
        if ball.gamestatus == 0:
            if self.x>SCREEN_W//2 and ball.spdX>0 or self.x<SCREEN_W//2 and ball.spdX<0:
                if ball.y > self.y + self.h // 2:
                    self.accY=5
                elif ball.y < self.y + self.h // 2:
                    self.accY=-5



def draw_field(scr):
    c = pygame.color.THECOLORS['brown']
    pygame.draw.rect(scr, c, (0, 0, SCREEN_W, BORDER_W), 0)
    pygame.draw.rect(scr, c, (0, SCREEN_H - BORDER_W, SCREEN_W, BORDER_W), 0)
    RT_show_txt(scr, 'SCORE:' + str(paddleL.score), font64, 20, 20, paddleL.c)
    RT_show_txt(scr, 'SCORE:' + str(paddleR.score), font64, 750, 20, paddleR.c)


# ---------main---------
pygame.init()
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("RT - PingPong Ball")
clock = pygame.time.Clock()
font64 = pygame.font.Font("simkai.ttf", 64)

ball = CLS_ball(10, 10, 2, 2, 3, 0, 0)
paddleL = CLS_paddle(0, 200, 10, 150, c=(255, 0, 0))
paddleR = CLS_paddle(SCREEN_W - BORDER_W, 200, 10, 150, c=(0, 0, 255))
scale = 4
actList = []

StatusG, StatusC, StatusA, StatusF, StatusD, StatusS, StatusR = 0, 0, 1, 1, 0, 0, 0
print('Hello from the dev!')
print('tutorial: player 1: W and S; player 2: arrow up & down; \n', \
      'g to toggle random gravity (default off);\n', \
      'i to toggle aerodynamics (default on); k to toggle friction (default on); \n', \
      'p to toggle debug mode (default off); o to reset scores; \nj to toggle audio (default off); \n', \
      'l to toggle robot (default off); \ny and h to increase and decrease the coefficient of friction respectively.\n', \
      'WARNING! INCREASING THE FRICTION COEFFICIENT GREATER THAN 1 IS NOT RECOMMENDED!')

pixel = []
pixel.append('....DD....')
pixel.append('..DDAADD..')
pixel.append('.DDDAADDD.')
pixel.append('.DDDAADDD.')
pixel.append('DDDDAADDDD')
pixel.append('DDDDAADDDD')
pixel.append('.DDDAADDD.')
pixel.append('.DDDAADDD.')
pixel.append('..DDAADD..')
pixel.append('....DD....')
ball.add_pic(pixel)
pixel = []
pixel.append('....DD....')
pixel.append('..DDDDDD..')
pixel.append('.DDDDDDAD.')
pixel.append('.DDDDDAAD.')
pixel.append('DDDDDAADDD')
pixel.append('DDDDAADDDD')
pixel.append('.DDAADDDD.')
pixel.append('.DAADDDDD.')
pixel.append('..DDDDD..')
pixel.append('....DD....')
ball.add_pic(pixel)
pixel = []
pixel.append('....DD....')
pixel.append('..DDDDDD..')
pixel.append('.DDDDDDDD.')
pixel.append('.DDDDDDDD.')
pixel.append('DAAAAAAAAD')
pixel.append('DAAAAAAAAD')
pixel.append('.DDDDDDDD.')
pixel.append('.DDDDDDDD.')
pixel.append('..DDDDDD..')
pixel.append('....DD....')
ball.add_pic(pixel)
pixel = []
pixel.append('....DD....')
pixel.append('..DDDDDD..')
pixel.append('.DADDDDDD.')
pixel.append('.DAADDDDD.')
pixel.append('DDDAADDDDD')
pixel.append('DDDDAADDDD')
pixel.append('.DDDDAADD.')
pixel.append('.DDDDDAAD.')
pixel.append('..DDDDDD..')
pixel.append('....DD....')
ball.add_pic(pixel)
x, y = 0, 0
spdX, spdY = 3, 1
counter = 0
while True:
    if StatusR == 1:
        paddleL.AI()
        #paddleR.AI()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                paddleR.accY = -0.2
            elif event.key == pygame.K_DOWN:
                paddleR.accY = 0.2
            elif event.key == pygame.K_SPACE and ball.gamestatus == 1:
                ball.gamestatus = 0
                set_new_ball(ball)
            elif event.key == ord('w'):
                paddleL.accY = -0.2
            elif event.key == ord('s'):
                paddleL.accY = 0.2

            elif event.key == ord('g'):
                StatusG = not StatusG
                print('random gravity toggled. Status: ', StatusG)
            elif event.key == ord('i'):
                StatusA = not StatusA
                print('aerodynamics toggled. Status: ', StatusA)
            elif event.key == ord('k'):
                StatusF = not StatusF
                print('Friction toggled. Status: ', StatusF)
            elif event.key == ord('p'):
                StatusD = not StatusD
                print('Debug mode toggled. Status: ', StatusD,
                      '. Variables will be shown automatically. Press u to show variables manually.')
            elif event.key == ord('o'):
                print('score resetted.')
                paddleL.score, paddleR.score = 0, 0
            elif event.key == ord('j'):
                StatusS = not StatusS
                print('Audio toggled. Status: ', StatusS)
            elif event.key == ord('l'):
                StatusR = not StatusR
                print('Robot mode toggled on Red side. Status: ', StatusR)
            elif event.key == ord('y'):
                coefFric *= 2
                print('friction coefficient increased. Value: ', coefFric)
            elif event.key == ord('h'):
                coefFric /= 2
                print('friction coefficient decreased. Value: ', coefFric)
            elif event.key == ord('u'):
                if StatusD:
                    print('Ball from left to right: x, y, spdX, spdY, GX, GY, Fric, gamestatus: \n', \
                          ball.x, ball.y, ball.spdX, ball.spdY, ball.GX, ball.GY, ball.Fric, ball.gamestatus, '\n',
                          end='\n')

        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_UP, pygame.K_DOWN):
                paddleR.spdY, paddleR.accY = 0, 0
            if event.key in (ord('w'), ord('s')):
                paddleL.spdY, paddleL.accY = 0, 0
    screen.fill((0, 64, 0))
    draw_field(screen)
    ball.move()
    ball.draw(screen)
    paddleL.move()
    paddleL.draw(screen)
    paddleR.move()
    paddleR.draw(screen)
    pygame.display.update()
    clock.tick(200)
