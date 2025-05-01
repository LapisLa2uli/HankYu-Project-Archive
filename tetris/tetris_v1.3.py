import pygame, random, sys, time

SCREEN_WIDTH, SCREEN_HEIGHT = 1008, 756
BLOCK_WIDTH, LEVEL_COUNT = 32, 20
PLAY_STAT, PAUSE_STAT, STOP_STAT = 0, 1, 2
SCORE_LIST = [0, 10, 30, 60, 100]


def RT_drawr_txt(scr, fnt, clr, txt, sx, sy):
    img = fnt.render(txt, True, clr)
    scr.blit(img, (sx - img.get_width(), sy))
    return


def print_matrix(List):
    for row in List:
        for ele in row:
            print(ele, end=' ')
        print()


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


class CLS_AI(object):
    def __init__(self):
        self.offset, self.rotate = 0, 0
        self.decision = (0, 0, 0)
        self.rotateCount = 0
        return

    def score_situation(self, grid):
        '''memo = [(0, 0)]
        newGrid = []
        for line in grid:
            newGrid.append(line[:])
        while len(memo) > 0:
            coor = memo[0]
            memo.pop(0)
            if coor[1] + 1 < len(newGrid[0]):
                if newGrid[coor[0]][coor[1] + 1] == 0:
                    newGrid[coor[0]][coor[1] + 1] = -1
                    memo.append((coor[0], coor[1] + 1))
            if newGrid[coor[0]][coor[1] - 1] == 0 and coor[1] - 1 >= 0:
                newGrid[coor[0]][coor[1] - 1] = -1
                memo.append((coor[0], coor[1] - 1))
            if coor[0] + 1 < len(newGrid):
                if newGrid[coor[0] + 1][coor[1]] == 0:
                    newGrid[coor[0] + 1][coor[1]] = -1
                    memo.append((coor[0] + 1, coor[1]))
            if newGrid[coor[0] - 1][coor[1]] == 0 and coor[0] - 1 >= 0:
                newGrid[coor[0] - 1][coor[1]] = -1
                memo.append((coor[0] - 1, coor[1]))
        score = 0
        for y in range(len(newGrid)):
            for x in range(len(newGrid[0])):
                if newGrid[y][x] == -1:
                    score += 1
                elif newGrid[y][x] == 0:
                    score -= 2
        return score'''
        '''testList = [True] * 10
        score = 0
        height=0
        flag=0
        for y in range(len(grid)):
            for x in range(len(grid[0])):
                if grid[y][x] != 0:
                    testList[x] = False
                    flag=1
                if testList[x] == True:
                    score += 1
                if flag==0:
                    height+=1'''
        score = 0
        filled = 0
        for line in grid:
            for element in line:
                if element != 0:
                    filled += 1
        probeList = [0] * 10
        flagList = [1] * 10
        for i in range(len(grid) - 1):
            for x in range(len(probeList)):
                if grid[i + 1][x] != 0:
                    flagList[x] = 0
                else:
                    if flagList[x] == 1:
                        probeList[x] += 1
                        score += 1
            # print('probeList: ', probeList)
        # print('probeList: ',probeList)
        score += 10
        for i in range(len(probeList)):
            probeList[i] += 1
        columns=0
        for i in range(len(probeList)-1):
            if abs(probeList[i]-probeList[i+1])>4:
                columns+=1
        cnt = 0
        for y in range(len(grid)):
            for x in range(len(grid[0])):
                if grid[y][x] == 0:
                    cnt += 1

        print('unfilled squares', len(grid) * len(grid[0]) - (sum(probeList) + 10) - filled, probeList, cnt, score,
              filled)
        print('closed squares: ', cnt - score)
        '''try:
            return score*min(probeList)//(len(grid)*len(grid[0])-(sum(probeList)+10)-filled)
        except ZeroDivisionError:
            return score*min(probeList)*2'''
        try:
            return score - ((cnt - score)*40) - (max(probeList)-min(probeList))*30 -(columns-1)*50  # /((max(probeList)-min(probeList))/2)
        except ZeroDivisionError:
            try:
                return score / (cnt - score) * min(probeList)-columns
            except ZeroDivisionError:
                return score * min(probeList)-columns

    def make_decision(self, grid):
        x = 0
        BestDecision = (0, 0, -10000)  # first: offset; second: rotate
        tetris = ttFW.field0.tetris
        for rotation in range(0, 3):
            tetris = ttFW.field0.tetris
            tetris.rotate(ttFW.grid, rotation)
            for offset in range(-1, 20):
                fwGrid = []
                for line in ttFW.field0.grid:
                    fwGrid.append(line[:])
                print('init')
                print_matrix(fwGrid)
                tGrid = tetris.grid[:][:]
                if ttFW.field0.tetris.test(tGrid, fwGrid, offset, 0):
                    offy = 0
                    while tetris.test(tGrid, fwGrid, offset, offy) == True:
                        offy += 1
                    offy -= 1
                    for y in range(ttFW.field0.tetris.d):
                        for x in range(ttFW.field0.tetris.d):
                            if tGrid[y][x] > 0:
                                fwGrid[offy + y][offset + x] = tetris.num
                    crtLines = 0
                    for line in fwGrid:
                        if 0 in line:
                            continue
                        if (8 in line) or (9 in line) or (10 in line):
                            continue
                        crtLines += 1
                        for p in range(len(line)):
                            line[p] = 0
                    for line in fwGrid:
                        if (8 in line) or (9 in line) or (10 in line):
                            for p in range(len(line)):
                                line[p] += 1
                    for i in range(len(fwGrid)):
                        if fwGrid[i] == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]:
                            fwGrid.pop(i)
                            newline = [0] * len(fwGrid[0])
                            fwGrid.insert(0, newline)
                    print('p1', offset, offy, self.score_situation(fwGrid) * (crtLines + 1))
                    print_matrix(fwGrid)
                    if BestDecision[2] < self.score_situation(fwGrid) ** (crtLines + 1):
                        BestDecision = (offset, rotation, self.score_situation(fwGrid))
        print('Best Decision: ', BestDecision)
        self.decision = BestDecision

    def excecute(self):
        print('current', self.rotate, ttFW.field0.tetris.gx, self.decision)
        if self.rotate != self.decision[1] + 2:
            print('rotate', self.rotate, self.decision)
            ttFW.field0.event_key(0)
            self.rotate += 1
        if ttFW.field0.tetris.gx < self.decision[0]:
            ttFW.field0.event_key(2)
        elif ttFW.field0.tetris.gx > self.decision[0]:
            ttFW.field0.event_key(1)


class CLS_field(object):
    def __init__(self, picList, x0, y0, w, h,aStatus):
        self.tPicList = picList
        self.x0, self.y0, self.w, self.h = x0, y0, w, h
        self.aStatus=aStatus
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
            d, posList = 3, [[0, 0], [0, 1], [0, 2], [1, 1]]
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
        if self.stat != PLAY_STAT:
            return
        for i in range(rFlag):
            self.tetris.rotate(self.grid, True)
        self.tetris.dy = self.tetris.get_nullline()
        return

    def draw(self, scr):
        self.tetris.draw(scr, self.x0, self.y0)
        self.nextTetris.draw(scr, BLOCK_WIDTH * 9, BLOCK_WIDTH * (5+(self.x0-BLOCK_WIDTH)//(BLOCK_WIDTH*2)))
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
        self.tick += 1
        if self.tick > LEVEL_COUNT - self.level:
            self.tick = 0
            # self.AI.make_decision(self.grid)
            if self.aStatus:
                self.AI.excecute()
            print(self.tetris.gx, self.tetris.gy)
            if self.tetris.move(self.grid, 0, 1) == False:
                self.scanline()
                self.tetris = self.nextTetris
                self.rotate_tetris(random.randint(0, 3))
                self.nextTetris = self.new_tetris(random.randint(1, 7))
                self.nextNum = random.randint(1, 7)
                self.tetris.draw(scr, self.x0, self.y0)
                self.stat = (1 - self.tetris.move(self.grid, 0, 1)) * 2
                self.AI.rotate = 0
                print('AI', self.AI.make_decision(self.grid), self.grid)
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
        self.field0 = CLS_field(self.tPicList, BLOCK_WIDTH, BLOCK_WIDTH * 3, 10, 20,True)
        self.field1=CLS_field(self.tPicList,BLOCK_WIDTH*17,BLOCK_WIDTH*3,10,20,False)
        self.fontScore = pygame.font.Font('c:\\Windows\\Fonts\\Arial.ttf', 16)
        return

    def play(self, scr):
        scr.blit(self.bgPic, (0, 0))
        self.field0.play(scr)
        self.field1.play(scr)
        RT_drawr_txt(scr, self.fontScore, (200, 200, 200),
                     str(self.field0.score), 340, 10)
        RT_drawr_txt(scr, self.fontScore, (200, 200, 200),
                     str(self.field0.lines), 340, 42)
        RT_drawr_txt(scr, self.fontScore, (200, 200, 200),
                     str(self.field0.level + 1), 340, 74)
        RT_drawr_txt(scr, self.fontScore, (200, 200, 200),
                     str(self.field1.score), 565, 10)
        RT_drawr_txt(scr, self.fontScore, (200, 200, 200),
                     str(self.field1.lines), 565, 42)
        RT_drawr_txt(scr, self.fontScore, (200, 200, 200),
                     str(self.field1.level + 1), 565, 74)
        return

    def event_key(self, key):
        if key == pygame.K_UP:
            self.field1.event_key(0)
        elif key == pygame.K_LEFT:
            self.field1.event_key(1)
        elif key == pygame.K_RIGHT:
            self.field1.event_key(2)
        elif key == pygame.K_DOWN:
            self.field1.event_key(3)
        elif key == pygame.K_p:
            self.field1.event_key(4)
        elif key == pygame.K_SPACE:
            self.field1.event_key(5)
        elif key == ord('W'):
            self.field1.event_key(0)
        elif key == ord('A'):
            self.field1.event_key(1)
        elif key == ord('S'):
            self.field1.event_key(2)
        elif key == ord('D'):
            self.field1.event_key(3)
        elif key == pygame.K_p:
            self.field1.event_key(4)
        elif key == pygame.K_SPACE:
            self.field1.event_key(5)
            self.field0.event_key(5)

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
    ttFW.play(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            ttFW.event_key(event.key)
    pygame.display.update()
    # clock.tick(50)
