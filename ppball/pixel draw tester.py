import pygame,sys
SCREEN_W,SCREEN_H=1024,600
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
pixel=[]
pixel.append('.......4.......')
pixel.append('......444......')
pixel.append('.....44444.....')
pixel.append('....4444444....')
pixel.append('....3333333....')
pixel.append('....3333333....')
pixel.append('....3333333....')
pixel.append('....3333333....')
pixel.append('....3333333....')
pixel.append('....3333333....')
pixel.append('...433333334...')
pixel.append('..44333433344..')
pixel.append('..44444.44444..')
pixel.append('..44444.44444..')
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    RT_draw(screen,pixel,500,300,2)
    pygame.display.update()
    clock.tick(200)
