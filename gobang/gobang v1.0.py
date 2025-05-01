import pygame, sys, time, random

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 800
BOARD_ORDER, BOARD_SIZE = 19, 30
BOARD_X0, BOARD_Y0 = 15, 15
GRID_NULL, GRID_BLACK, GRID_WHITE = 0, 1, 2
SPEED_X = [1,0,-1,-1]
SPEED_Y = [0,1,-1,1]

def RT_show_txt(scr, txt, font, x, y, c):
    img = font.render(txt, True, c)
    scr.blit(img, (x, y))
    return
def is_five(grid, x, y, flag):
    Dir=0
    for Dir in (0,1,2,3):
        x0,y0=x,y
        x1,y1=x,y
        yList=[]
        cnt=0
        while 0<=x0<len(grid) and 0<=y0<len(grid) or 0<=x1<len(grid) and 0<=y1<len(grid):
            if (x0,y0)==(x1,y1):
                yList.append(flag)
                x0 += SPEED_X[Dir]
                y0 += SPEED_Y[Dir]
                x1 -= SPEED_X[Dir]
                y1 -= SPEED_Y[Dir]
            elif 0<=x0<len(grid) and 0<=y0<len(grid) and grid[y0][x0]==flag:
                yList.append(grid[y0][x0])

                x0 += SPEED_X[Dir]
                y0 += SPEED_Y[Dir]
            elif 0<=x1<len(grid) and 0<=y1<len(grid) and grid[y1][x1]==flag:
                yList.append(grid[y1][x1])

                x1 -= SPEED_X[Dir]
                y1 -= SPEED_Y[Dir]
            if yList==[flag,flag,flag,flag,flag]:
                return True
            cnt+=1
            if cnt>=10:
                break
            print(x0,y0,x1,y1,yList)
    return False


class CLS_gobang(object):
    def __init__(self, fPic, bPic, wPic, x0, y0):
        self.facePic, self.bMan, self.wMan = fPic, bPic, wPic
        self.x0, self.y0 = x0, y0
        self.board = pygame.Surface((570, 570))
        self.draw_board()
        self.grid = []
        for y in range(BOARD_ORDER):
            line = [GRID_NULL] * BOARD_ORDER
            self.grid.append(line)
        self.flag = GRID_BLACK
        self.font = pygame.font.Font(None, 32)
        self.Status=0
        return

    def draw_board(self):
        self.board.fill((240, 200, 0))
        L = BOARD_X0 + (BOARD_ORDER - 1) * BOARD_SIZE
        for i in range(BOARD_X0, SCREEN_HEIGHT, BOARD_SIZE):
            pygame.draw.line(self.board, (0, 0, 0), (BOARD_X0, i), (L, i), 1)
            pygame.draw.line(self.board, (0, 0, 0),
                             (i, BOARD_Y0), (i, L), 1)
        pygame.draw.rect(self.board, (0, 0, 0),
                         (BOARD_X0 - 1, BOARD_Y0 - 1, L + 3 - BOARD_Y0, L + 3 - BOARD_Y0), 1)
        return
    def draw(self,scr):
        scr.fill((180,140,0))
        scr.blit(self.facePic,(0,0))
        scr.blit(self.board,(self.x0,self.y0))
        for y in range(BOARD_ORDER):
            for x in range(BOARD_ORDER):
                if self.grid[y][x]==GRID_BLACK:
                    scr.blit(self.bMan, \
                             (self.x0+x*BOARD_SIZE,self.y0+y*BOARD_SIZE))
                elif self.grid[y][x]==GRID_WHITE:
                    scr.blit(self.wMan, \
                             (self.x0+x*BOARD_SIZE,self.y0+y*BOARD_SIZE))
        x=self.x0+BOARD_X0+BOARD_ORDER*BOARD_SIZE+50
        txt=self.font.render('Next',True,(225,220,0))
        scr.blit(txt,(x,self.y0+BOARD_Y0+20))
        if self.flag==GRID_BLACK:
            scr.blit(self.bMan,(x+15,self.y0+BOARD_Y0+50))
        else:
            scr.blit(self.wMan,(x+15,self.y0+BOARD_Y0+50))
        return
    def mouse_down(self, mx, my):
        gx = (mx-30)//BOARD_SIZE
        gy = (my-80)//BOARD_SIZE
        if 0 <= gx < BOARD_ORDER and 0 <= gy < BOARD_ORDER and self.Status==0:
            if self.grid[gy][gx] == GRID_NULL:
                print(self.grid)
                self.grid[gy][gx] = self.flag
                print(self.grid)
                if is_five(self.grid, gx, gy, self.flag):
                    print(self.flag, 'WIN!!!')
                    self.Status=1
                self.flag = GRID_BLACK + GRID_WHITE - self.flag
        return


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
fPic = pygame.image.load('face01.bmp')
fPic.set_colorkey((0, 0, 0))
wPic = pygame.image.load('WCMan.bmp')
wPic.set_colorkey((255, 0, 0))
bPic = pygame.image.load('BCMan.bmp')
bPic.set_colorkey((255, 0, 0))
gobang = CLS_gobang(fPic, bPic, wPic, 30, 80)
print(gobang.grid)
while True:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button != 1:
                continue
            mx, my = event.pos
            gobang.mouse_down(mx, my)
        if event.type==pygame.KEYDOWN:
            gobang.grid = []
            for y in range(BOARD_ORDER):
                line = [GRID_NULL] * BOARD_ORDER
                gobang.grid.append(line)
            gobang.Status=0
            print(gobang.grid)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    gobang.draw(screen)
    pygame.display.update()
