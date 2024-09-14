import pygame as p
import time
import random
from os import path

dir = path.dirname(__file__)
img_dir = path.join(dir)
    

class Messi(p.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.y = 660
        self.x = WIDTH / 2
        self.vel = 6
        self.width = 110
        self.height = 120

        # IMAGES

        self.messi = p.image.load(path.join(img_dir,"PARADO.png"))
        
        self.messi = p.transform.scale(self.messi, (self.width, self.height))
        

        self.image = self.messi
        self.rect = self.image.get_rect()
        self.mask = p.mask.from_surface(self.image)

    def update(self):
        self.movement()
        self.correction()
        self.checkCollision()
        self.rect.center = (self.x, self.y)

    def movement(self):
        keys = p.key.get_pressed()
        if keys[p.K_LEFT]:
            self.x -= self.vel
            self.image = self.messi

        elif keys[p.K_RIGHT]:
            self.x += self.vel
            self.image = self.messi

        if keys[p.K_UP]:
            self.y -= self.vel

        elif keys[p.K_DOWN]:
            self.y += self.vel

    def correction(self):
        if self.x - self.width / 2 < 0:
            self.x = self.width / 2

        elif self.x + self.width / 2 > WIDTH:
            self.x = WIDTH - self.width / 2

        if self.y - self.height / 2 < 0:
            self.y = self.height / 2

        elif self.y + self.height / 2 > HEIGHT:
            self.y = HEIGHT - self.height / 2

    def checkCollision(self):
        car_check = p.sprite.spritecollide(self, enemigos_group, False, p.sprite.collide_mask)
        if car_check:
            explosion.explode(self.x, self.y)


class Enemigos(p.sprite.Sprite):
    def __init__(self, number):
        super().__init__()
        if number == 1:
            self.y = 160
            self.image = p.image.load(path.join(img_dir,"virgil.png"))
            self.vel = 5
            self.width = 100
            self.height = 70
        
        elif number == 2:
            self.y = 240
            self.image = p.image.load(path.join(img_dir,"ramos.png"))
            self.vel = 2
            self.width = 100
            self.height = 70
            
        elif number == 3:
            self.y = 320
            self.image = p.image.load(path.join(img_dir,"pepe.png"))
            self.vel = 10
            self.width = 100
            self.height = 70
        
        elif number == 4:
            self.y = 400
            self.image = p.image.load(path.join(img_dir,"9.png"))
            self.vel = 6
            self.width = 100
            self.height = 80
            
        elif number == 5:
            self.y = 480
            self.image = p.image.load(path.join(img_dir,"guardiol.png"))
            self.vel = 14
            self.width = 70
            self.height = 70
        
        elif number == 6:
            self.y = 560
            self.image = p.image.load(path.join(img_dir,"rubencito.png"))
            self.vel = 10
            self.width = 90
            self.height = 60
        self.x = HEIGHT / 2
        self.image = p.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.mask = p.mask.from_surface(self.image)  
        
    

    def update(self):
        self.movement()
        self.rect.center = (self.x, self.y)

    def movement(self):
        self.x += self.vel

        if self.x - self.width / 3 < 0:
            self.x = self.width / 3
            self.vel *= -1

        elif self.x + self.width / 2 > WIDTH:
            self.x = WIDTH - self.width / 2
            self.vel *= -1


class Screen(p.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.img1 = p.image.load(path.join(img_dir,"cancha.jpg"))
        self.img2 = p.image.load(path.join(img_dir,"You Win.png"))
        self.img3 = p.image.load(path.join(img_dir,"You lose.png"))

        self.img1 = p.transform.scale(self.img1, (WIDTH, HEIGHT))
        self.img2 = p.transform.scale(self.img2, (WIDTH, HEIGHT))
        self.img3 = p.transform.scale(self.img3, (WIDTH, HEIGHT))

        self.image = self.img1
        self.x = 0
        self.y = 0

        self.rect = self.image.get_rect()

    def update(self):
        self.rect.topleft = (self.x, self.y)


class Punto(p.sprite.Sprite):
    def __init__(self, number):
        super().__init__()
        self.number = number
        

        if number == 1:
            self.y = 660
            self.image = p.image.load(path.join(img_dir,"barca.png"))
            self.visible = False

            self.width = 50
            self.height = 50

        else:
            self.y = 50
            self.image = p.image.load(path.join(img_dir,"barca.png"))
            self.visible = True
            
            self.width = 50
            self.height = 50

        
        self.x = WIDTH / 2
        self.image = p.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.mask = p.mask.from_surface(self.image)

    def update(self):
        if self.visible:
            self.collision()
            self.rect.center = (self.x, self.y)

    def collision(self):
        global SCORE, messi1, number

        toquebandera = p.sprite.spritecollide(self, messi_group, False, p.sprite.collide_mask)
        if toquebandera:
            self.visible = False

            if self.number == 1:
                barca2.visible = True
                if SCORE < 5:
                    SwitchLevel()

                else:
                    messi_group.empty()
                    DeleteOtherItems()

                    EndScreen(1)

            else:
                barca1.visible = True

class Balon(p.sprite.Sprite):
    def __init__(self,number):
        super().__init__()
        self.number = number
        if number == 1:
            
            self.image = p.image.load(path.join(img_dir,"oro3.png"))
            self.visible = True
            self.rect = self.image.get_rect()
            
            self.width = 50
            self.height = 50
            self.x= random.randrange(WIDTH-self.width)
            self.y= random.randrange(HEIGHT-self.height)
            self.image = p.transform.scale(self.image, (self.width, self.height))
            self.rect = self.image.get_rect()
            self.mask = p.mask.from_surface(self.image)

    def update(self):
        if self.visible:
            self.collision()
            self.rect.center = (self.x, self.y)


    def collision(self):
        global PUNTUACION, messi1, number

        toquebalon = p.sprite.spritecollide(self, messi_group, False, p.sprite.collide_mask)
        if toquebalon:
            self.visible = False

            if self.number == 1:
                balon.visible = True
                if PUNTUACION < 7:
                    Level()
                else:
                    messi_group.empty()
                    DeleteOtherItems()

                    EndScreen(1)
            else:
                balon.visible = True
            
                  
class Explosion(object):
    def __init__(self):
        self.costume = 1
        self.width = 140
        self.height = 140
        self.image = p.image.load(path.join(img_dir,"explosion" + str(self.costume) + '.png'))
        self.image = p.transform.scale(self.image, (self.width, self.height))

    def explode(self, x, y):
        x = x - self.width / 2
        y = y - self.height / 2
        DeleteMessi()

        while self.costume < 9:
            self.image = p.image.load(path.join(img_dir,"explosion" + str(self.costume) + '.png'))                                                             
            self.image = p.transform.scale(self.image, (self.width, self.height))
            win.blit(self.image, (x, y))
            p.display.update()

            self.costume += 1
        DeleteOtherItems()
        EndScreen(0)


def ScoreDisplay():
    global gameOn

    if gameOn:
        score_text = score_font.render(str(SCORE) + ' / 5', True, (0, 0, 0))
        win.blit(score_text, (255, 10))
        puntuacion_text = puntuacion_font.render(str(PUNTUACION) + ' / 7', True, (0, 0, 0))
        win.blit(puntuacion_text, (800, 10))


def checkPuntos():
    for Punto in Puntos:
        if not Punto.visible:
            Punto.kill()

        else:
            if not Punto.alive():
                barca_group.add(Punto)


def Level():
    global PUNTUACION

    if virgil.vel < 0:
        virgil.vel += 1
    else:
        virgil.vel -= 1

    if ramos.vel < 0:
        ramos.vel += 1
    else:
        ramos.vel -= 1

    if pepe.vel < 0:
        pepe.vel += 1
    else:
        pepe.vel -= 1

    if alexander.vel < 0:
        alexander.vel += 1
    else:
        alexander.vel -= 1

    if gvardiol.vel < 0:
        gvardiol.vel += 1
    else:
        gvardiol.vel -= 1

    if rubencito.vel < 0:
        rubencito.vel += 1
    else:
        rubencito.vel -= 1
    PUNTUACION += 1

def SwitchLevel():
    global SCORE

    if virgil.vel < 0:
        virgil.vel -= 1
    else:
        virgil.vel += 1

    if ramos.vel < 0:
        ramos.vel -= 1
    else:
        ramos.vel += 1

    if pepe.vel < 0:
        pepe.vel -= 1
    else:
        pepe.vel += 1

    if alexander.vel < 0:
        alexander.vel -= 1
    else:
        alexander.vel += 1

    if gvardiol.vel < 0:
        gvardiol.vel -= 1
    else:
        gvardiol.vel += 1

    if rubencito.vel < 0:
        rubencito.vel -= 1
    else:
        rubencito.vel += 1
    SCORE += 1
def DeleteMessi():
    global messi1


    messi1.kill()
    screen_group.draw(win)
    enemigos_group.draw(win)
    barca_group.draw(win)
    balon_group.draw(win)

    screen_group.update()
    enemigos_group.update()
    barca_group.update()
    balon_group.update()

    p.display.update()


def DeleteOtherItems():
    enemigos_group.empty()
    barca_group.empty()
    Puntos.clear()
    balon_group.empty()


def EndScreen(n):
    global gameOn

    gameOn = False

    if n == 0:
        bg.image = bg.img3

    elif n == 1:
        bg.image = bg.img2


WIDTH = 1280
HEIGHT = 720

p.init()

win = p.display.set_mode((WIDTH, HEIGHT))
p.display.set_caption('Gambetas Road')
clock = p.time.Clock()

SCORE = 0
score_font = p.font.SysFont('comicsans', 80, True)

PUNTUACION = 0
puntuacion_font = p.font.SysFont('Doppio One', 80, True)


bg = Screen()
screen_group = p.sprite.Group()
screen_group.add(bg)

messi1 = Messi()
messi_group = p.sprite.Group()
messi_group.add(messi1)

virgil = Enemigos(1)
ramos = Enemigos(2)
pepe = Enemigos(3)
alexander = Enemigos(4)
gvardiol= Enemigos(5)
rubencito= Enemigos(6)
enemigos_group = p.sprite.Group()
enemigos_group.add(virgil,ramos,pepe,alexander,gvardiol,rubencito)

barca1 = Punto(1)
barca2 = Punto(2)
barca_group = p.sprite.Group()
barca_group.add(barca1, barca2)
Puntos = [barca1, barca2]

balon = Balon(1)
balon_group = p.sprite.Group()
balon_group.add(balon)


explosion = Explosion()

gameOn = True
run = True
while run:
    clock.tick(60)
    for event in p.event.get():
        if event.type == p.QUIT:
            run = False

    screen_group.draw(win)

    ScoreDisplay()
    checkPuntos()

    enemigos_group.draw(win)
    messi_group.draw(win)
    barca_group.draw(win)
    balon_group.draw(win)

    enemigos_group.update()
    messi_group.update()
    barca_group.update()
    balon_group.update()

    screen_group.update()

    p.display.update()

p.quit()