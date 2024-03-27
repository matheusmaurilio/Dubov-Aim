import pygame as pg
import random 
import sys

## TAMANHO DA TELA ##
WIDTH = 1280
HEIGHT = 720

## ARQUIVOS ##
BG = 'assets/imgs/bg.png'
FONT = 'assets/fonts/PixelGameFont.ttf'
TARGET = 'assets/imgs/target.png'
AIM = 'assets/imgs/mouse.png'
SHOOT = 'assets/audio/disparo.mp3'

## PONTUAÇÃO ##
POINTS = 0
RECORD = 0

## TEMPORIZADOR ##
TIMER = 1800   # 1800/60 = 30 segundos

## PAUSAR E FECHAR ##
GAME_PAUSED = False
CLOSE = False

## ALVO ##

class Target(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = pg.image.load(TARGET).convert_alpha()
        self.image = pg.transform.scale(self.image, (200, 150))
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(0, HEIGHT - self.rect.height)

class Aim(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load(AIM).convert_alpha()
        self.image = pg.transform.scale(self.image, (25, 25))
        self.rect = self.image.get_rect()
        self.sound = pg.mixer.Sound(SHOOT)

    def update(self):
        self.rect.center = pg.mouse.get_pos()

    def shoot(self):
        global POINTS
        self.sound.play()

        colisions = pg.sprite.spritecollide(aim,target_group, False)
        for colision in colisions:
            POINTS +=1
            colision.kill()
            alvo = Target(random.randrange(0,WIDTH),random.randrange(0,HEIGHT)) 
            target_group.add(alvo)

pg.init()

screen = pg.display.set_mode((WIDTH, HEIGHT))

bg = pg.image.load(BG).convert()
bg = pg.transform.scale(bg, (WIDTH, HEIGHT))

clock = pg.time.Clock()

font = pg.font.Font(FONT, 30)

pg.display.set_caption('DUBOV AIM')

target_group = pg.sprite.Group()

aim = Aim()
group_aim = pg.sprite.Group()
group_aim.add(aim)

for i in range(1):
    target = Target(random.randint(0, WIDTH - 200), random.randint(0, HEIGHT - 150))
    target_group.add(target)


while not CLOSE:
    if not GAME_PAUSED:
        pg.mouse.set_visible(False)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE: #esc
                    GAME_PAUSED = not GAME_PAUSED

            if event.type == pg.MOUSEBUTTONDOWN:
                aim.shoot()

            screen.blit(bg, (0,0))

            target_group.draw(screen)
            group_aim.draw(screen)
            group_aim.update()
    else:
        screen.fill((252, 132, 3))
        pg.mouse.set_visible(True)
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE: #esc
                    GAME_PAUSED = not GAME_PAUSED

            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        
        pause = font.render(f'PRESSIONE ESC PARA INICIAR   ', True, (255,255,255))
        points = font.render(f'RECORDE: {RECORD}', True, (255,255,255))

        pause_rect = pause.get_rect(center = (WIDTH/2, HEIGHT/2))
        points_rect = points.get_rect(center = (WIDTH/2, HEIGHT/2-50))

        screen.blit(pause, pause_rect)
        screen.blit(points, points_rect)

    pg.display.flip()
    clock.tick(120)