#  Jumpy - Juego de plataforma

import pygame as pyg, random, sys
from os import path

ANCHO = 500
ALTO = 800

pantalla = pyg.display.set_mode((ANCHO, ALTO))
dir = path.dirname(__file__)
img_dir = path.join(dir, 'img')

class Juego:
   
    def __init__(self):
        # Inicializar pygame y crear una ventana:

        pyg.init() 
        pyg.mixer.init() 
        
        pyg.display.set_caption(TITULO) # Para agregar texto
        """icono = pyg.image.load(path.join(img_dir, "icono.ico"))
        pyg.display.set_icon(icono) #Cargar imagen de icono:"""
        self.reloj = pyg.time.Clock()
        self.ejecucion = True # variable para el ciclo del juego
        self.nom_fuente = pyg.font.match_font(NOMBRE_FUENTE)
        self.cargar_datos()

    def cargar_datos(self):
        # cargar la puntuacion más alta
        self.ubicacion_archivo = ""
        self.nombre_archivo = r"C:\Users\Usuario\OneDrive\Documentos\TRABAJOS COLE\2022\Programacion\Pygame_V2\Juego_7\juego\puntaje_mas_alto.txt"
        self.archivo_txt = self.nombre_archivo
        
        with open(self.archivo_txt, "r") as f:
            try:
                self.puntajemasalto = int(f.read())
            except:
                self.puntajemasalto = 0
        f.close()

        # Cargar las imagenes u objetos
        self.imagenes = Objetos(path.join(img_dir, "sprites_juntos.png"))
        
        # Plataformas
        self.plataformas2 = []
        for i in range(1, 2):
            self.plataformas2.append(pyg.image.load(path.join\
            (img_dir, "plataforma{}.png".format(i))).convert())

        # Cargar demás imágenes:
        self.jugador = []
        for i in range(1, 6):
            self.jugador.append(pyg.image.load(path.join\
            (img_dir, "jugador{}.png".format(i))).convert())

        # Cargar la música y sonidos
        self.snd_dir = path.join(dir, 'snd')
        self.salto_sonido = pyg.mixer.Sound(path.join(self.snd_dir, 'Jump33.wav'))
        self.poten_sonido = pyg.mixer.Sound(path.join(self.snd_dir, 'Boost16.wav'))

        #Cargar las imagenes de fondos: 
        self.fondo_inicio = pyg.image.load(path.join(img_dir, "imagen_inicio_v2.jpg"))
        self.fondo_durante = pyg.image.load(path.join(img_dir, "imagen_durante_v2.jpg"))
        self.fondo_final = pyg.image.load(path.join(img_dir, "imagen_final.jpg")) 

    def nuevo(self):   
        # Comienzo o nuevo juego:

        self.puntaje = 0
        # grupos de objetos
        self.grupo_objetos = pyg.sprite.LayeredUpdates()
        self.plataformas = pyg.sprite.Group()
        self.potenciador = pyg.sprite.Group()
        self.enemigo = pyg.sprite.Group()
        self.nubes = pyg.sprite.Group()
        self.jugador = Jugador(self) 
         
        # Plataformas:
        for plat in LISTA_PLATAFORMA:
            Plataforma(self, *plat) # utilizar todos sus elementos
        self.tiempo_enemi = 0

        # Musica:
        pyg.mixer.music.load(path.join(self.snd_dir, 'desarrollo.mp3'))
        self.run()

    def run(self):
        # Bucle del juego, comprueba si hay...

        pyg.mixer.music.play(loops=-1) # repetir infinitas veces
        self.jugando = True
        while self.jugando:
            self.reloj.tick(FPS)
            self.eventos()
            self.update()
            self.dibujar()
        pyg.mixer.music.fadeout(500) # así la música se desvanece gradualmente

    def update(self):
        # Bucle del juego - Acualizacion:

        self.grupo_objetos.update()

        # Cuando se mueve
        nuevo = pyg.time.get_ticks()
        if nuevo - self.tiempo_enemi > 5000 + \
            random.choice([-1000, -500, 0, 500, 1000]):
            self.tiempo_enemi = nuevo
            Enemigo(self)

        # colision con el enemigo
        sobre_enemi = pyg.sprite.spritecollide(self.jugador, self.enemigo, False, pyg.sprite.collide_mask)
        if sobre_enemi:
            self.jugando = False

        # verificacion de colision entre el jugador y la plataforma
        if self.jugador.vel.y > 0:
            colision = pyg.sprite.spritecollide(self.jugador, self.plataformas, False)
            # cuando choquen, se detenga el objeto o judador
            if colision:
                # si llegamos a una plataforma, entonces el primero es el mas bajo "bajito" 
                bajito = colision[0]
                for coli in colision:
                    if coli.rect.bottom > bajito.rect.bottom:# si alguno de la lisa es mas bajo que el primero
                        bajito = coli
                
                if self.jugador.pos.x < bajito.rect.right + 10 and \
                   self.jugador.pos.x > bajito.rect.left - 10:
                    # si la posicion del jugador en x es menor que la plataforma que estamos 
                    # a la derecha y si la posicion del jugador en x es mayor que 
                    # el rectangulo más bajo a la izquierda
                    if self.jugador.pos.y < bajito.rect.centery:
                        # solo saltar a la plataforma de abajo, cuando los pies 
                        # esten por encima de la parte inferior de la plataforma
                        self.jugador.pos.y = bajito.rect.top
                        self.jugador.vel.y = 0
                        self.jugador.saltando = False
                

        # cuando el jugador alcanze 1/4 superior de la pantalla
        elif self.jugador.rect.top <= ALTO / 4:
            # subir la pantalla para que el jugador siempre se aprecie
            self.jugador.pos.y += max(abs(self.jugador.vel.y), 2)
            for nub in self.nubes:
                nub.rect.y += max(abs(self.jugador.vel.y / 2), 2)
            for enemi in self.enemigo:
                enemi.rect.y += max(abs(self.jugador.vel.y), 2)
            for plat in self.plataformas:
                plat.rect.y += max(abs(self.jugador.vel.y), 2)
                # eliminar a las plataformas que ya no se ven
                if plat.rect.top >= ALTO:
                    plat.kill()
                    # sumar puntos al ir superando las plataformas
                    self.puntaje += 10

        # si el jugador esta sobre un potenciador, colisionen
        sobre_pot = pyg.sprite.spritecollide(self.jugador, self.potenciador, True)
        for pot in sobre_pot:
            if pot.type == "boost":
                self.poten_sonido.play() 
                self.jugador.vel.y = -POTENCIADORES
                self.jugador.saltando = False

        # Pierde / muere
        if self.jugador.rect.bottom > ALTO:
            for sprite in self.grupo_objetos:
                # cae en una velocidad adecuada
                sprite.rect.y -= max(self.jugador.vel.y, 10)
                # cuando se salga de la pantalla, hay que eliminarlo / matarlo
                if sprite.rect.bottom < 0:
                    sprite.kill()
                    
        # cuando se acaben las plataformas, termina el juego
        if len(self.plataformas) == 0:
            self.jugando = False

        # generar nuevas plataformas para mantener el número de ellas
        while len(self.plataformas) < 9:
            ancho = random.randrange(50, 100)
            Plataforma(self, random.randrange(0, ANCHO-ancho),
                       random.randrange(-75, -30))
            
    def eventos(self):
        # Procesos de entrada - eventos:

        for evento in pyg.event.get():
            # Controlar para cerrar la ventana:
            if evento.type == pyg.QUIT:
                if self.jugando:
                    self.jugando = False
                self.ejecucion = False
            # para saltar, con espacio o flecha
            if evento.type == pyg.KEYDOWN:
                if evento.key == pyg.K_UP or evento.key == pyg.K_SPACE:
                    self.jugador.saltar() # salto largo
            elif evento.type == pyg.KEYUP: # mantener presionado
                if evento.key == pyg.K_UP or evento.key == pyg.K_SPACE:
                    self.jugador.salto_corto() # salto corto
            
    def dibujar(self):
        # Bucle del juego - Dibujos:

        pantalla.blit(self.fondo_durante,(0,0))
        self.grupo_objetos.draw(pantalla)

        # insertar el texto puntaje y ubicarlo en la ventana
        self.insertar_texto(str(self.puntaje), 25, ROJO, ANCHO/2, 15)

        # despues de dibujar simepre, dar vuelta
        pyg.display.flip()

    def pantalla_inicio(self):
        # Pantalla de inicio del juego: 
        
        pyg.mixer.music.load(path.join(self.snd_dir, "intro.ogg"))
        pyg.mixer.music.play(loops=-1)
        pantalla.blit(self.fondo_inicio,(0,0))
        self.insertar_texto(str(self.puntajemasalto), \
                            25, NEGRO, 230, 625)
        pyg.display.flip()
        self.presionar_tecla()
        pyg.mixer.music.fadeout(500)
       
    def pantalla_final(self):
        # Pantalla del final del juego:

        if not self.ejecucion:
            return
        pyg.mixer.music.load(path.join(self.snd_dir, "gameover.ogg"))
        pyg.mixer.music.play(loops=-1)
        pantalla.blit(self.fondo_final,(0,0))

        # ubicacion de los textos
        self.insertar_texto("Puntaje: " + str(self.puntaje), 40, NEGRO, \
                            ANCHO/2+5, 580)
        self.insertar_texto("Puntaje: " + str(self.puntaje), 40, BLANCO, \
                            ANCHO/2, 580)
        # mostrar puntuación más alta:
        if self.puntaje > self.puntajemasalto:
            self.puntajemasalto = self.puntaje
            self.insertar_texto("NUEVA PUNTUACIÓN MÁS ALTA!", 30, NEGRO, \
                                ANCHO/2+5, 620)
            self.insertar_texto("NUEVA PUNTUACIÓN MÁS ALTA!", 30, BLANCO, \
                                ANCHO/2, 620)
            with open(self.archivo_txt, 'w') as f:
                f.write(str(self.puntaje))
        else:
            self.insertar_texto("Puntuación más alta: " + str(self.puntajemasalto), \
                                40, NEGRO, ANCHO/2 +5, 620)
            self.insertar_texto("Puntuación más alta: " + str(self.puntajemasalto), \
                                40, BLANCO, ANCHO/2, 620)
        self.insertar_texto("Presione una tecla", \
                            40, NEGRO, ANCHO/2 +5, 700)
        self.insertar_texto("Presione una tecla", \
                            40, VIOLETA, ANCHO/2, 700)
        self.insertar_texto("para volver a jugar", \
                            40, NEGRO, ANCHO/2 +5, 730)
        self.insertar_texto("para volver a jugar", \
                            40, VIOLETA, ANCHO/2, 730)
        pyg.display.flip()
        self.presionar_tecla()
        pyg.mixer.music.fadeout(500)

    def presionar_tecla(self):
        espera = True
        while espera:
            self.reloj.tick(FPS)
            # controlar los eventos
            for evento in pyg.event.get():
                # si es salir, no espera ninguna tecla y se cierra
                if evento.type == pyg.QUIT:
                    espera = False
                    self.ejecucion = False
                # si es ya presiono la tecla, no espera más.
                elif evento.type == pyg.KEYUP:
                    espera = False

    def insertar_texto(self, texto, tamano, color, x, y):
        fuente = pyg.font.Font(self.nom_fuente, tamano)
        superfi_texto = fuente.render(texto, True, color)
        # para ubicarlo mejor, armo un rectangulo para el texto
        rectan_texto = superfi_texto.get_rect()
        rectan_texto.midtop = (x, y) # ubicacion, arriba al centro
        pantalla.blit(superfi_texto, rectan_texto) # mostar por pantalla


vec = pyg.math.Vector2 # agregar un vector

class Objetos():
    # para cargar y poder dividir los objetos
    def __init__(self, nombrearch):
        self.objetos = pyg.image.load(path.join(img_dir, nombrearch)).convert()
    def obtener_imagen(self, x, y, ancho, alto):
        # tomar una imagen de la hoja de calculo
        image = pyg.Surface((ancho, alto)) # tamaño especificado
        image.blit(self.objetos, (0, 0), (x, y, ancho, alto)) # seleccionar, el trozo de imagen especificado
        image = pyg.transform.scale(image, (ancho // 2, alto // 2)) # cambiar tamaño.
        return image

class Jugador(pyg.sprite.Sprite):   
    def __init__(self, juego):
        self._layer = CAPA_JUGADOR
        self.groups = juego.grupo_objetos
        pyg.sprite.Sprite.__init__(self, self.groups)
        self.juego = juego
        self.caminando = False
        self.saltando = False
        self.imagen_actual = 0
        self.ultima_actual = 0
        self.cargar_imagenes()
        self.image = self.parado[0]
        self.rect = self.image.get_rect()
        self.rect.center = (40, ALTO-100)
        self.pos = vec(40, ALTO-100)
        self.vel = vec(0, 0) # vector de velocidad
        self.ace = vec(0, 0) # vector de aceleracion
    
    def cargar_imagenes(self):
        # cargar la imagenes en la pantalla

        self.parado = [self.juego.imagenes.obtener_imagen(617,164,132,163),
                       self.juego.imagenes.obtener_imagen(617,0,133,163)]
        for marco in self.parado:
            marco.set_colorkey(NEGRO) # transparente, eliminar fondo negro

        self.camina_der = [self.juego.imagenes.obtener_imagen(0,664,120,161),
                           self.juego.imagenes.obtener_imagen(121,664,120,161)]
        for marco in self.camina_der:
            marco.set_colorkey(NEGRO)

        self.camina_iz = [self.juego.imagenes.obtener_imagen(617,491,120,162),
                          self.juego.imagenes.obtener_imagen(617,328,120,162)]
        for marco in self.camina_iz:
            marco.set_colorkey(NEGRO)

        self.salta = self.juego.imagenes.obtener_imagen(266,499,132,164)
        self.salta.set_colorkey(NEGRO)
    
    def salto_corto(self):
        # salto corto
        if self.saltando:
            if self.vel.y < -2: # mueve para arriba
                self.vel.y = -2

    def saltar(self):
        # saltar solo si estas sobre una plataforma
        self.rect.y += 2
        colision = pyg.sprite.spritecollide(self, self.juego.plataformas, False)
        self.rect.y -= 2
        if colision and not self.saltando:
            self.juego.salto_sonido.play() # reproducir el sonido de salto
            self.saltando = True
            self.vel.y = -JUGADOR_SALTO

    def update(self):
        self.animacion()
        self.ace = vec(0, JUGADOR_GRAV)
        # al presionar una flecha, acelera en esa direccion:
        teclas = pyg.key.get_pressed()
        if teclas[pyg.K_LEFT]:
            self.ace.x = -JUGADOR_ACE
        if teclas[pyg.K_RIGHT]:
            self.ace.x = JUGADOR_ACE
        
        # Aplicar friccion: Ajustar velocidad a la friccion, 
        self.ace.x += self.vel.x * JUGADOR_FRICC

        # Ecuaciones de movimiento:
        self.vel += self.ace # aceleracion se suma a la velocidad
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0 # para que deje de caminar al costado
        self.pos += self.vel + 0.5 * self.ace # lo anterior se suma a la posicion, para una nueva

        # para mantenerse dentro de la ventana. 
        if self.pos.x > ANCHO + self.rect.width / 2:
            self.pos.x = 0 - self.rect.width / 2
        if self.pos.x < 0 - self.rect.width / 2:
            self.pos.x = ANCHO + self.rect.width / 2
        
        # para una plataforma
        self.rect.midbottom = self.pos

    def animacion(self):
        ahora = pyg.time.get_ticks()
        if self.vel.x != 0:
            self.caminando = True
        else:
            self.caminando = False
        # animacion cuando camina
        if self.caminando:
            if ahora - self.ultima_actual > 180:
                self.ultima_actual = ahora
                self.imagen_actual = (self.imagen_actual + 1) % len(self.camina_iz)
                debajo = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.camina_der[self.imagen_actual]
                else:
                    self.image = self.camina_iz[self.imagen_actual]
                self.rect = self.image.get_rect()
                self.rect.bottom = debajo
        # animacion al estar quieto
        if not self.saltando and not self.caminando:
            if ahora - self.ultima_actual > 350:
                self.ultima_actual = ahora
                self.imagen_actual = (self.imagen_actual + 1) % len(self.parado)
                debajo = self.rect.bottom
                self.image = self.parado[self.imagen_actual]
                self.rect = self.image.get_rect()
                self.rect.bottom = debajo

        # crear una mascara para la colision perfecta de los objetos
        self.mascara = pyg.mask.from_surface(self.image)

class Plataforma(pyg.sprite.Sprite):
    # Parametros para la ubicacion de la imagen u objeto
    def __init__(self, juego, x, y):
        self._layer = CAPA_PLATAFORMA
        self.groups = juego.grupo_objetos, juego.plataformas
        pyg.sprite.Sprite.__init__(self, self.groups)
        self.juego = juego
        self.image = random.choice(self.juego.plataformas2)
        ancho = random.randrange(100, 170)
        self.image = pyg.transform.scale(self.image, (ancho, 50))
        self.rect = self.image.get_rect()
        self.image.set_colorkey(NEGRO)
        self.rect.x = x
        self.rect.y = y
        if random.randrange(80) < APARECE_POT:
            Potenciador(self.juego, self)

class Potenciador(pyg.sprite.Sprite):
    # definir y agregar los potenciadores de salto
    def __init__(self, juego, plat):
        self._layer = CAPA_POTEN
        self.groups = juego.grupo_objetos, juego.potenciador
        pyg.sprite.Sprite.__init__(self, self.groups)
        self.juego = juego
        self.plat = plat
        self.type = random.choice(["boost"])
        self.image = self.juego.imagenes.obtener_imagen(591,749,70,70)
        self.image.set_colorkey(NEGRO)
        self.image = pyg.transform.scale(self.image, (50,50))
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top - 5
    def update(self):
        # parte inferior del potenciador arriba de la plataforma
        self.rect.bottom = self.plat.rect.top - 5
        # eliminarlo, cuando la plataforma ya no exista
        if not self.juego.plataformas.has(self.plat): 
            # devuelve True o False, si esta o no
            self.kill() 

class Enemigo(pyg.sprite.Sprite):
    # definir a enemigo
    def __init__(self, juego):
        self._layer = CAPA_ENEMIGOS
        self.groups = juego.grupo_objetos, juego.enemigo
        pyg.sprite.Sprite.__init__(self, self.groups)
        self.juego = juego
        self.imagen_1 = self.juego.imagenes.obtener_imagen(242,664,114,155)
        self.imagen_1.set_colorkey(NEGRO)
        self.imagen_2 = self.juego.imagenes.obtener_imagen(357,664,90,155)
        self.imagen_2.set_colorkey(NEGRO)
        self.image = self.imagen_1
        self.rect = self.image.get_rect()
        self.rect.centerx = random.choice([-100, ANCHO + 100])
        self.vx = random.randrange(1, 4)
        if self.rect.centerx > ANCHO:
            self.vx *= -1
        self.rect.y = random.randrange(ALTO / 2)
        self.vy = 0
        self.normaly = 0.5

    def update(self):
        # actualizacion del enemigo
        self.rect.x += self.vx
        self.vy += self.normaly
        if self.vy > 3 or self.vy < -3:
            self.normaly *= -1
        # para ubicar bien las imagenes
        centro = self.rect.center
        if self.normaly < 0:
            self.image = self.imagen_1
        else:
            self.image = self.imagen_2
        self.rect = self.image.get_rect()
        # crear una mascara para la colision perfecta de los objetos
        self.mascara = pyg.mask.from_surface(self.image)
        self.rect.center = centro
        self.rect.y += self.vy
        # cuando salga de la pantalla, lo eliminamos
        if self.rect.left > ANCHO + 100 or self.rect.right < -100:
            self.kill()

# OPCIONES Y CONFIGURACIONES DEL JUEGO:

# Constantes del juego:
TITULO = " EL TURBOPIOJO"

FPS = 60
NOMBRE_FUENTE = "impact"
IMAGENES = "sprites_juntos.png"
ARCHIVO_PMA = "puntaje_mas_alto.txt"

#Propiedades del jugador:
JUGADOR_ACE = 0.5
JUGADOR_FRICC = -0.12
JUGADOR_GRAV = 0.8
JUGADOR_SALTO = 20

# Propiedades del juego
POTENCIADORES = 60
APARECE_POT = 8
APARECE_ENEMI = 1000 # cada 1 segundo

CAPA_JUGADOR = 2
CAPA_PLATAFORMA = 1
CAPA_POTEN = 1.5
CAPA_ENEMIGOS = 2
CAPA_NUBES = 0

# Plataformas de inicio
LISTA_PLATAFORMA = [(0, ALTO - 60),
                    (ANCHO / 2, 650),
                    (30, 550),
                    (300, 430),
                    (360, 300),
                    (175, 200),
                    (400, 100),
                    (125, 50)]
#                    x,   y

# Definiendo colores:
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
AMARILLO = (255, 255, 0)
NARANJA = (224, 125, 67)
GRIS = (38, 38, 37)
VIOLETA = (221, 169, 245)
BGCOLOR_ANTERIOR = (133, 199, 192)
BGCOLOR = (111, 222, 218)


g = Juego()
g.pantalla_inicio() 

while g.ejecucion:
    g.nuevo()
    g.pantalla_final()

pyg.quit() 
