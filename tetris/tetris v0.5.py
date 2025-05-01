import pygame, random, sys, time

SCREEN_WIDTH, SCREEN_HEIGHT = 1008, 756
BLOCK_WIDTH, LEVEL_COUNT = 32, 20

def RT_drawr_txt(scr,fnt,clr,txt,sx,sy):
    img=fnt.render(txt,True,clr)
    scr.blit(img,(sx-img.get_width(),sy))
    return
class CLS_tetris(object):
    def __init__(self, pic, num, d, posList):
        self.gx, self.gy = (10 - d) // 2, 0
        self.pic, self.num, self.d = pic, num, d
        self.grid = [[0 for x in range(d)] for y in range(d)]
        print('tt init', self.num, self.d)
        for pos in posList:
            self.grid[pos[1]][pos[0]] = num
        return

    def draw(self, scr, x0, y0):
        for y in range(self.d):
            for x in range(self.d):
                if self.grid[y][x] == self.num:
                    sx = x0 + (self.gx + x) * BLOCK_WIDTH
                    sy = y0 + (self.gy + y) * BLOCK_WIDTH
                    print((self.gx+x)*BLOCK_WIDTH)
                    scr.blit(self.pic, (sx, sy))
        return

    def test(self, tGrid, fwGrid, gx, gy):
        for y in range(self.d):
            for x in range(self.d):
                if tGrid[y][x] > 0:
                    print(gy+y)
                    if gx + x < 0 or gx + x >= 10 or gy + y >= 20:
                        return False
                    if fwGrid[gy + y][gx + x] > 0:
                        return False
        return True

    def rotate(self, fwGrid, flag):
        nm = []
        for y in range(self.d):
            nm.append([0] * self.d)
        for i in range(self.d):
            for j in range(self.d-1,-1,-1):
                nm[i][self.d-j-1]=self.grid[j][i]
        self.grid=nm
        return

    def move(self, fwGrid, dx, dy):
        if self.test(self.grid,fwGrid,self.gx+dx,self.gy+dy)==True:
            self.gx+=dx
            self.gy+=dy
        else:
            return False
        return

    def get_nullline(self):
        line = 0
        for y in range(self.d):
            count = 0
            for x in range(self.d):
                count += self.grid[y][x]
            if count > 0:
                break
            line -= 1
        print(self.num, 'line', line)
        return line


class CLS_framework(object):
    def __init__(self, bgf, tfList, x0, y0, w, h):
        self.bgPic = pygame.image.load(bgf)
        self.tPicList = []
        for tf in tfList:
            tPic = pygame.image.load(tf)
            self.tPicList.append(tPic)
        self.x0, self.y0, self.w, self.h = x0, y0, w, h
        self.grid = [[0 for x in range(w)] for y in range(h)]
        self.tetris = self.new_tetris(random.randint(1, 7))
        self.rotate_tetris(random.randint(0, 3))
        self.nextTetris = self.new_tetris(random.randint(1, 7))
        self.level, self.tick = 0, 0
        return

    def new_tetris(self, num):
        if num == 1:
            d, posList = 4, [[1, 0], [1, 1], [1, 2], [1, 3]]
        elif num == 2:
            d, posList = 2, [[0, 0], [0, 1], [1, 0], [1, 1]]
        elif num == 3:
            d, posList = 2, [[0, 0], [0, 1], [1, 0], [1, 1]]
        elif num == 4:
            d, posList = 3, [[0, 0], [1, 0], [1, 1], [2, 1]]
        elif num == 5:
            d, posList = 3, [[1, 0], [2, 0], [1, 1], [0, 1]]
        elif num == 6:
            d, posList = 3, [[0, 0], [0, 1], [1, 1], [2, 1]]
        elif num == 7:
            d, posList = 3, [[2, 0], [0, 1], [1, 1], [2, 1]]
        tetris = CLS_tetris(self.tPicList[num], num, d, posList)
        return tetris

    def rotate_tetris(self, rFlag):
        for i in range(rFlag):
            self.tetris.rotate(self.grid, True)
        self.tetris.dy = self.tetris.get_nullline()
        return

    def draw(self, scr):
        scr.blit(self.bgPic, (0, 0))
        self.tetris.draw(scr, self.x0, self.y0)
        self.nextTetris.draw(scr, BLOCK_WIDTH * 9, BLOCK_WIDTH * 5)
        for y in range(self.h):
            for x in range(self.w):
                if self.grid[y][x] > 0:
                    sx = self.x0 + x * BLOCK_WIDTH
                    sy = self.y0 + y * BLOCK_WIDTH
                    scr.blit(self.tPicList[self.grid[y][x]], (sx, sy))
        return

    def translation(self, ty):
        return

    def rightline(self):
        return

    def play(self, scr):
        self.rightline()
        self.draw(scr)
        self.tick += 1
        if self.tick > LEVEL_COUNT - self.level:
            self.tick = 0
            if self.tetris.move(self.grid, 0, 1) == False:
                self.rightline()
                self.tetris = self.nextTetris
                self.rotate_tetris(random.randint(0, 3))
                self.nextTetris = self.new_tetris(random.randint(1, 7))
                self.nextNum = random.randint(1, 7)
                self.tetris.draw(scr, self.x0, self.y0)
                return self.tetris.move(self.grid, 0, 1)
        return True

    def event_key(self, key):
        if key == pygame.K_UP:
            self.tetris.rotate(self.grid, False)
        elif key == pygame.K_LEFT:
            self.tetris.move(self.grid, -1, 0)
        elif key == pygame.K_RIGHT:
            self.tetris.move(self.grid, 1, 0)
        elif key == pygame.K_DOWN:
            self.tetris.move(self.grid, 0, 1)
        return


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
fontFace = pygame.font.Font(None, 48)
ttFW = CLS_framework('backgroup32.png', (
'picFlr.png', 'pic1.png', 'picO.png', 'picT.png', 'picS.png',
'picZ.png', 'picJ.png', 'picL.png', 'picRight.png',
'picRight.png', 'picRight.png'),
                     32, 0, 10, 20)
while True:
    if ttFW.play(screen) == False:
        pygame.display.update()
        print('game over!!!')
        sys.exit()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            ttFW.event_key(event.key)
    pygame.display.update()
    clock.tick(50)
