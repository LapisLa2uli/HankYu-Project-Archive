import pygame, random, sys, time

SCREEN_WIDTH, SCREEN_HEIGHT = 1008, 756
BLOCK_WIDTH, LEVEL_COUNT = 32, 20
PLAY_STAT, PAUSE_STAT, STOP_STAT = 0, 1, 2
SCORE_LIST = [0, 10, 30, 60, 100]


def RT_drawr_txt(scr, fnt, clr, txt, sx, sy):
    img = fnt.render(txt, True, clr)
    scr.blit(img, (sx - img.get_width(), sy))
    return
class CLS_tetris(object):
    def __init__(self, pic, num, d, posList):
        self.gx, self.gy = (10 - d) // 2, 0
        self.pic, self.num, self.d = pic, num, d
        self.grid = [[0 for x in range(d)] for y in range(d)]
        for pos in posList:
            self.grid[pos[1]][pos[0]] = num
        return

    def draw(self, scr, x0, y0):
        for y in range(self.d):
            for x in range(self.d):
                if self.grid[y][x] == self.num:
                    sx = x0 + (self.gx + x) * BLOCK_WIDTH
                    sy = y0 + (self.gy + y) * BLOCK_WIDTH
                    scr.blit(self.pic, (sx, sy))
        return

    def test(self, tGrid, fwGrid, gx, gy):
        for y in range(self.d):
            for x in range(self.d):
                if tGrid[y][x] > 0:
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
            for j in range(self.d - 1, -1, -1):
                nm[i][self.d - j - 1] = self.grid[j][i]
        if self.test(nm, fwGrid, self.gx, self.gy) == True \
                or flag == True:
            self.grid = nm
        return

    def move(self, fwGrid, dx, dy):
        if self.test(self.grid, fwGrid, self.gx + dx, self.gy + dy) == True:
            self.gx += dx
            self.gy += dy
            return True
        if dy == 0:
            return False
        for y in range(self.d):
            for x in range(self.d):
                if self.grid[y][x] > 0:
                    fwGrid[self.gy + y][self.gx + x] = self.num
        return False

    def get_nullline(self):
        line = 0
        for y in range(self.d):
            count = 0
            for x in range(self.d):
                count += self.grid[y][x]
            if count > 0:
                break
            line -= 1
        return line


class CLS_field(object):
    def __init__(self, picList, x0, y0, w, h):
        self.tPicList = picList
        self.x0, self.y0, self.w, self.h = x0, y0, w, h
        self.AI = CLS_AI()
        self.new_game()

    def new_game(self):
        self.stat, self.tick = PLAY_STAT, 0
        self.score, self.lines, self.level = 0, 0, 0
        self.grid = [[0 for x in range(self.w)] for y in range(self.h)]
        self.tetris = self.new_tetris(random.randint(1, 7))
        self.rotate_tetris(random.randint(0, 3))
        self.nextTetris = self.new_tetris(random.randint(1, 7))

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
        if self.stat!=PLAY_STAT:
            return
        for i in range(rFlag):
            self.tetris.rotate(self.grid, True)
        self.tetris.dy = self.tetris.get_nullline()
        return

    def draw(self, scr):
        self.tetris.draw(scr, self.x0, self.y0)
        self.nextTetris.draw(scr, BLOCK_WIDTH * 9, BLOCK_WIDTH * 5)
        for y in range(self.h):
            for x in range(self.w):
                if self.grid[y][x] > 0:
                    sx = self.x0 + x * BLOCK_WIDTH
                    sy = self.y0 + y * BLOCK_WIDTH
                    scr.blit(self.tPicList[self.grid[y][x]], (sx, sy))
        return

    def fullline(self):
        for line in self.grid:
            if (8 in line) or (9 in line) or (10 in line):
                for p in range(len(line)):
                    line[p] += 1
        for i in range(len(self.grid)):
            if self.grid[i] == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]:
                self.grid.pop(i)
                newline = [0] * len(self.grid[0])
                self.grid.insert(0, newline)
        return

    def scanline(self):
        crtLines = 0
        print(self.grid)
        for line in self.grid:
            if 0 in line:
                continue
            if (8 in line) or (9 in line) or (10 in line):
                continue
            crtLines += 1
            for p in range(len(line)):
                line[p] = 0
        self.lines += crtLines
        self.score += SCORE_LIST[crtLines]
        self.level = self.lines // 30
        return

    def play(self, scr):
        self.fullline()
        self.draw(scr)
        # print(self.stat)
        if self.stat != PLAY_STAT:
            return
        self.tick += 2
        if self.tick > LEVEL_COUNT - self.level:
            self.tick = 0
            if self.tetris.move(self.grid, 0, 1) == False:
                self.scanline()
                print('AI', self.AI.score_situation(self.grid), self.grid)
                self.tetris = self.nextTetris
                self.rotate_tetris(random.randint(0, 3))
                self.nextTetris = self.new_tetris(random.randint(1, 7))
                self.nextNum = random.randint(1, 7)
                self.tetris.draw(scr, self.x0, self.y0)
                self.stat = (1 - self.tetris.move(self.grid, 0, 1)) * 2
                print(self.stat)
        return
    def event_key(self, cmd):
        if cmd == 0:
            self.tetris.rotate(self.grid, False)
        elif cmd == 1:
            self.tetris.move(self.grid, -1, 0)
        elif cmd == 2:
            self.tetris.move(self.grid, 1, 0)
        elif cmd == 3:
            self.tetris.move(self.grid, 0, 1)
        elif cmd == 4:
            if self.stat != STOP_STAT:
                self.stat = 1 - self.stat
        elif cmd == 5:
            if self.stat == STOP_STAT:
                self.new_game()
        return
    def grid_encode(self):
        codeStr=''
        codeStr+=str(self.score)+','
        codeStr+=str(self.lines)+','
        codeStr+=str(self.level)+','
        for y in range(self.h):
            for x in range(self.w):
                if self.grid[y][x]>9:
                    codeStr+='A'
                else:
                    codeStr+=str(self.grid[y][x])
        return codeStr
    def grid_decode(self,codeStr):
        codeList=codeStr.split(',')
        self.score=eval(codeList[1])
        self.lines=eval(codeList[2])
        self.level=eval(codeList[3])
        cStr,p=codeList[4],0
        for y in range(self.h):
            for x in range(self.w):
                if cStr[p]=='A':
                    self.grid[y][x]=10
                else:
                    self.grid[y][x]=eval(cStr[p])
                p+=1
        return
    def tetris_encode(self,tetris):
        codeStr=''
        codeStr+=str(tetris.d)+','
        codeStr+=str(tetris.cCode)+','
        codeStr+=str(tetris.gx)+','
        codeStr+=' '+str(tetris.gy)+','
        for y in range(tetris.d):
            for x in range(tetris.d):
                codeStr+=str(tetris.grid[y][x])
        return codeStr
    def tetris_decode(self,tetris,codeStr):
        codeList=codeSt.split(',')
        d=eval(codeList[1])
        cCode=eval(codeList[2])
        gx=eval(codeList[3])
        gy=eval(codeList[4])
        if tetris.cCode!=cCode:
            tetris=self.new_tetris(cCode)
        tetris.gx,tetris.gy=gx,gy
        cStr,p=codeList[5],0
        for y in range(tetris.d):
            for x in range(tetris.d):
                tetris.grid[y][x]=eval(cStr[p])
                p+=1
        return tetris

class CLS_framework(object):
    def __init__(self, bgf, tfList, x0, y0, w, h):
        self.bgPic = pygame.image.load(bgf)
        self.tPicList = []
        for tf in tfList:
            tPic = pygame.image.load(tf)
            tPic = pygame.transform.scale(tPic, (BLOCK_WIDTH, BLOCK_WIDTH))
            self.tPicList.append(tPic)
        self.x0, self.y0 = 0, 0
        self.grid = [[0 for x in range(w)] for y in range(h)]
        self.field0 = CLS_field(self.tPicList, BLOCK_WIDTH, BLOCK_WIDTH * 3, 10, 20)
        self.fontScore = pygame.font.Font('c:\\Windows\\Fonts\\Arial.ttf', 16)
        return

    def play(self, scr):
        scr.blit(self.bgPic, (0, 0))
        self.field0.play(scr)
        RT_drawr_txt(scr, self.fontScore, (200, 200, 200),
                     str(self.field0.score), 340, 10)
        RT_drawr_txt(scr, self.fontScore, (200, 200, 200),
                     str(self.field0.lines), 340, 42)
        RT_drawr_txt(scr, self.fontScore, (200, 200, 200),
                     str(self.field0.level + 1), 340, 74)
        return

    def event_key(self, key):
        if key == pygame.K_UP:
            self.field0.event_key(0)
        elif key == pygame.K_LEFT:
            self.field0.event_key(1)
        elif key == pygame.K_RIGHT:
            self.field0.event_key(2)
        elif key == pygame.K_DOWN:
            self.field0.event_key(3)
        elif key == pygame.K_p:
            self.field0.event_key(4)
        elif key == pygame.K_SPACE:
            self.field0.event_key(5)
        return


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
fontFace = pygame.font.Font(None, 48)
sct=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sct.bind(('127.0.0.1',6005))
sct.setblocking(0)
sct.settimeout(0.001)
svraddr=('127.0.0.1',6000)
timeOut=0
ttFW = CLS_framework('backgroup32.png', (
    'picFlr.png', 'pic1.png', 'picO.png', 'picT.png', 'picS.png',
    'picZ.png', 'picJ.png', 'picL.png', 'picRight.png',
    'picRight.png', 'picRight.png'),
                     32, 0, 10, 20)
while True:
    if ttFW.stat==DISCONNECTED_STAT:
        sct.sendt(b'connect',svraddr)
        print('connecting......')
        clock.tick(10)
    try:

    ttFW.play(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            ttFW.event_key(event.key)
    pygame.display.update()
    clock.tick(50)
