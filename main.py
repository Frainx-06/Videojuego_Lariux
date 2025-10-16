import pygame
import constante
import random
from textos import DamageTexto
from Personaje import Personaje
from bastonMorado import BastonMorado
from mundo import Mundo
import csv

pygame.init()

pygame.mixer.init()
ventana = pygame.display.set_mode((constante.ANCHO_VENTANA,constante.ALTO_VENTANA))

pygame.display.set_caption("Lariux")

#inicializar la fuente
font = pygame.font.Font("Assets//Fuente//m3x6.ttf", 25)
font_GameOver = pygame.font.Font("Assets//Fuente//m3x6.ttf", 74)
font_Monedas = pygame.font.Font("Assets//Fuente//m3x6.ttf", 60)
font_Rondas = pygame.font.Font("Assets//Fuente//m3x6.ttf", 50)

#textos de los objetos
font_objetos = pygame.font.Font("Assets//Fuente//m3x6.ttf", 40)                 
GameOver_Text = font_GameOver.render('Has doblao servilleta', True, constante.BLANCO)

#variables
posicion_pantalla = [0 , 0]


def escalar_img(image, escala):
    w = image.get_width()
    h = image.get_height()

    nueva_imagen = pygame.transform.scale(image, (w * escala, h * escala))
    return nueva_imagen

#Importar imagenes
#monedas
monedas = pygame.image.load("Assets//Monedas//G_Idle.png")
monedas = escalar_img (monedas, 1)

#objetos
obj_agilidad = pygame.image.load("Assets//Objetos//Agilidad.png")
obj_daño = pygame.image.load("Assets//Objetos//Daño.png")
obj_velocidad = pygame.image.load("Assets//Objetos//Velocidad.png")
obj_dash  = pygame.image.load("Assets//Objetos//Dash.png")

#vida
vida1 = pygame.image.load("Assets//Vida//vida1.png")
vida2 = pygame.image.load("Assets//Vida//vida2.png")
vida3 = pygame.image.load("Assets//Vida//vida3.png")
vida4 = pygame.image.load("Assets//Vida//vida4.png")

vida1 = escalar_img(vida1, 3.5)
vida2 = escalar_img(vida2, 3.5)
vida3 = escalar_img(vida3, 3.5)
vida4 = escalar_img(vida4, 3.5)

#personaje
# Cargar las animaciones del personaje
animaciones_quieto = []
for i in range(2):
    img = pygame.image.load(f"Assets//Personaje{i}.png")
    img = escalar_img(img, constante.ESCALA_PERSONAJE)
    animaciones_quieto.append(img)

animaciones_andar = []
for i in range(4):
    img = pygame.image.load(f"Assets//Andar{i}.png")
    img = escalar_img(img, constante.ESCALA_PERSONAJE)
    animaciones_andar.append(img)

quieto = True

#enemigos
animaciones_enemigos = []
for i in range (10):
     img_enemigos = pygame.image.load(f"Assets//Enemigos//Golem{i}walk.png")
     img_enemigos = escalar_img(img_enemigos, constante.ESCALA_ENEMIGO)
     animaciones_enemigos.append(img_enemigos)

#arma
img_b_Morado = pygame.image.load(f"Assets//Armas//B_Morado.png")
img_H_Aire = pygame.image.load(f"Assets//Armas//30.png")
animaciones = animaciones_quieto    

#vida del jugador
def ui(personaje, mundo):
    ventana.blit(monedas,(constante.ANCHO_VENTANA - 100, 10))
    monedas_text = font_Monedas.render(f":{personaje.monedas}", True, constante.AMARILLO)
    ventana.blit(monedas_text, ((constante.ANCHO_VENTANA - 55, 10)))
    rondas = font_Rondas.render(f"rondas: {mundo.Ronda}", True, constante.BLANCO)
    ventana.blit(rondas, (10, 30))
    for i in range(4):
        if jugador.vida == 100:
            ventana.blit(vida1, (10, 10))
        if jugador.vida == 75:
            ventana.blit(vida2, (10, 10))
        if jugador.vida == 50:
            ventana.blit(vida3, (10, 10))
        if jugador.vida == 25:
            ventana.blit(vida4, (10, 10))

#crear un jugador de la clase personaje
jugador = Personaje(1000,500,animaciones, 100, 1)

world_data = []

for i in range(constante.FILAS):
    filas = [10] * constante.COLUMNAS
    world_data.append(filas)


#cargar las imagenes del mapa
tile_list = []
for i in range(constante.TILE_TYPE):
    img = pygame.image.load(f"Assets//Tiles//tile_{i}.png")
    img = pygame.transform.scale(img, (constante.TILE_SIZE, constante.TILE_SIZE))
    tile_list.append(img)


#cargar el mapa
with open("Assets//Tiles//Mapa_Def.csv", newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)



#crear un mundo
mundo = Mundo()
mundo.process_data(world_data, tile_list)

#crear un arma de la clase bastonMorado
#Bonus de daño por los objetos
bonusDaño = 0

img_proyectil = pygame.image.load(f"Assets//Armas//Proyectil_Bas_Morado//001.png")
img_proyectil = escalar_img(img_proyectil, constante.ESCALA_PROYECTIL)

img_pro_aire = pygame.image.load(f"Assets//Armas//Wind//001.png")
img_pro_aire = escalar_img(img_pro_aire, constante.ESCALA_PROYECTIL)
basMorado = BastonMorado(img_b_Morado,img_proyectil)

#crear grupo de proyectiles
grupo_damage_text = pygame.sprite.Group()
grupo_proyectiles = pygame.sprite.Group()


#Tienda
  # Lista de todas las posibles mejoras con sus imágenes y textos
mejoras_disponibles = [
    {"imagen": escalar_img(obj_daño, 2), "texto": "+ Daño", "Dinero" : 5},
    {"imagen": escalar_img(obj_velocidad, 2), "texto": "+ Velocidad", "Dinero" : 5},
    {"imagen": escalar_img(obj_agilidad, 2), "texto": "+ Agilidad", "Dinero" : 5},
]

mejoras_tienda = []

tienda_abierta = False
tienda = False

run = True


#definir las variables de movimiento del jugador
mover_arriba = False;
mover_abajo = False;
mover_izquierda = False;
mover_derecha = False;


tipo_Arma = 1

 #Calcular el movimiento del jugador, velocidad
delta_x = 0
delta_y = 0

#crear lista de enemigos
def lista_enemigos(numeroMin, numeroMax):
    enemigos = []
    for i in range(random.randint(numeroMin, numeroMax)):
        enemigo = Personaje(random.randint(200, constante.ANCHO_VENTANA), random.randint(200, constante.ALTO_VENTANA), animaciones_enemigos, 100, 2)
        enemigos.append(enemigo)
    return enemigos

enemigos = lista_enemigos(1,2)

reloj = pygame.time.Clock()

#Sonidos
sonido_muerte = pygame.mixer.Sound("Assets//Sonidos//Muerte.wav")
pygame.mixer.music.load("Assets//Sonidos//time_for_adventure.mp3")
pygame.mixer.music.play(-1)

sonido_impacto = pygame.mixer.Sound("Assets//Sonidos//hurt.wav")

#While del juego
while run == True:
    if not jugador.vivo and not hasattr(jugador, 'sonido_muerte_reproducido'):
        sonido_muerte.play()
        jugador.sonido_muerte_reproducido = True
    #Controlar los frames 
    reloj.tick(constante.FPS)

    ventana.fill(constante.BG_NEGRO)

    if jugador.vivo:

        #Calcular el movimiento del jugador, velocidad
        delta_x = 0
        delta_y = 0

        if mover_derecha == True:
            delta_x = jugador.velocidad
        if mover_izquierda == True:
            delta_x = -jugador.velocidad
        if mover_arriba == True:
            delta_y = -jugador.velocidad
        if mover_abajo == True:
            delta_y = jugador.velocidad

        if quieto:
            jugador.animaciones = animaciones_quieto
        else:
            jugador.animaciones = animaciones_andar

        #actualiza jugador
        jugador.update(quieto)

        #actualizar enemigo
        for personajes in enemigos:
            personajes.enemigo(posicion_pantalla, mundo.obstaculos, jugador)
            personajes.update(quieto)

        #actualiza el estado del arma
        grados = jugador.autoaim(enemigos) #Autoapuntado
        proyectil = basMorado.update(jugador,enemigos ,grados, tipo_Arma, bonusDaño)

        if proyectil:
            grupo_proyectiles.add(proyectil)
        for proyectil in grupo_proyectiles:
            damage, pos_damage = proyectil.update(enemigos, grupo_proyectiles, posicion_pantalla, jugador, tipo_Arma, sonido_impacto)
            if damage:
                damageText = DamageTexto(pos_damage.centerx, pos_damage.centery, str(damage), font, constante.ROJO)
                grupo_damage_text.add(damageText)

        if mover_abajo == False and mover_arriba == False and mover_izquierda == False and mover_derecha == False:
            quieto = True
        else:
            quieto = False

        #mover al jugador
        posicion_pantalla = jugador.movimiento(delta_x, delta_y, mundo.obstaculos)

        #actualizar la posición del jugador
        mundo.update(posicion_pantalla)

        #actualizar el daño
        grupo_damage_text.update(posicion_pantalla)

    #dibujar el mundo
    mundo.draw(ventana)

    #dibujar al enemigo
    for personaje in enemigos:
        personaje.dibujar(ventana)
        
    #dibuja al jugador
    jugador.dibujar(ventana)

    #dibuja arma
    basMorado.dibujar(ventana, proyectil)

    # Cronómetro para pasar tiempo antes de rellenar la lista de enemigos 
    if not enemigos and jugador.vivo:        
        # Darle al boton de continuar
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:

                if boton_comprar_1.collidepoint(event.pos):
                    mejora = mejoras_tienda[0]
                    print(f"{mejora['texto']}")
                    if jugador.monedas >= mejora["Dinero"]:
                        imagen_objeto_escalada = None
                        if mejora["texto"] == "+ Daño":
                            bonusDaño += 10
                            jugador.monedas -= (mejora["Dinero"] + mundo.Ronda)
                        elif mejora["texto"] == "+ Velocidad":
                            jugador.velocidad += 0.5
                            jugador.monedas -= (mejora["Dinero"] + mundo.Ronda)
                        elif mejora["texto"] == "+ Agilidad":
                            jugador.agilidad += 1
                            jugador.monedas -= (mejora["Dinero"] + mundo.Ronda)
                        jugador.monedas - mejora["Dinero"] + mundo.Ronda

                if boton_comprar_2.collidepoint(event.pos):
                    mejora = mejoras_tienda[1]
                    print(f"{mejora['texto']}")
                    if jugador.monedas >= mejora["Dinero"]:
                        imagen_objeto_escalada = None
                        if mejora["texto"] == "+ Daño":
                            bonusDaño += 10
                            jugador.monedas -= (mejora["Dinero"] + mundo.Ronda)
                        elif mejora["texto"] == "+ Velocidad":
                            jugador.velocidad += 0.5
                            jugador.monedas -= (mejora["Dinero"] + mundo.Ronda)
                        elif mejora["texto"] == "+ Agilidad":
                            jugador.agilidad += 1
                            jugador.monedas -= (mejora["Dinero"] + mundo.Ronda)
                        jugador.monedas - mejora["Dinero"] + mundo.Ronda

                if boton_comprar_3.collidepoint(event.pos):
                    mejora = mejoras_tienda[2]
                    print(f"{mejora['texto']}")
                    if jugador.monedas >= mejora["Dinero"]:
                        imagen_objeto_escalada = None
                        if mejora["texto"] == "+ Daño":
                            bonusDaño += 10
                            jugador.monedas -= (mejora["Dinero"] + mundo.Ronda)
                        elif mejora["texto"] == "+ Velocidad":
                            jugador.velocidad += 0.5
                            jugador.monedas -= (mejora["Dinero"] + mundo.Ronda)
                        elif mejora["texto"] == "+ Agilidad":
                            jugador.agilidad += 1
                            jugador.monedas -= mejora["Dinero"]
                        jugador.monedas - (mejora["Dinero"] + mundo.Ronda)
                


                if rect_continuar.collidepoint(event.pos):
                    mundo.Ronda += 1
                    enemigos = lista_enemigos(mundo.Ronda + 2, mundo.Ronda + 4)
                    del mundo.tiempo_espera
                    tienda = False
                    tienda_abierta = False

    
        if not hasattr(mundo, 'tiempo_espera'):
            mundo.tiempo_espera = pygame.time.get_ticks()
            tienda = False

        tiempo_actual = pygame.time.get_ticks()
        tiempo_espera = tiempo_actual - mundo.tiempo_espera

        if tiempo_espera > constante.TIEMPO_ENTRE_RONDAS:
            mundo.Ronda += 1
            enemigos = lista_enemigos(mundo.Ronda + 2, mundo.Ronda + 4)
            del mundo.tiempo_espera
        else:
            tienda = True
            
        if tienda:
            if not tienda_abierta:
                mejoras_tienda = random.sample(mejoras_disponibles, 3)
                tienda_abierta = True  # Evita repetir la selección en cada frame
        # Crear una superposición semitransparente para el fondo
        overlay = pygame.Surface((constante.ANCHO_VENTANA, constante.ALTO_VENTANA))
        overlay.set_alpha(128)  # Ajustar la transparencia (0-255)
        overlay.fill(constante.NEGRO)  # Fondo oscuro
        ventana.blit(overlay, (0, 0))

        # Desactivar movimiento del personaje mientras la tienda está abierta
        mover_abajo = False
        mover_arriba = False
        mover_derecha = False
        mover_izquierda = False

        # Tamaño del rectángulo principal (tienda)
        ancho_tienda = 700  
        alto_tienda = 250  

        # Posición centrada de la tienda
        x_centro = (constante.ANCHO_VENTANA - ancho_tienda) // 2
        y_centro = (constante.ALTO_VENTANA - alto_tienda) // 2

        # Crear el rectángulo principal (fondo de la tienda)
        rect_tienda = pygame.Rect(x_centro, y_centro, ancho_tienda, alto_tienda)

        # Dibujar el rectángulo principal
        pygame.draw.rect(ventana, constante.GRIS, rect_tienda)

        # Dimensiones de las secciones internas
        margen = 20  
        ancho_seccion = (ancho_tienda - margen * 4) // 3  
        alto_seccion = alto_tienda - 60  

        # Dimensiones del botón "Comprar"
        alto_boton = 30
        ancho_boton = ancho_seccion - 20  

        # Dibujar las tres secciones en una fila dentro de la tienda con sus botones
        for i in range(3):
            rect_seccion = pygame.Rect(
                x_centro + margen + i * (ancho_seccion + margen),
                y_centro + margen,
                ancho_seccion,
                alto_seccion
            )

            pygame.draw.rect(ventana, constante.BLANCO, rect_seccion)

            # Obtener la imagen y el texto de la mejora aleatoria
            mejora = mejoras_tienda[i]
            imagen_objeto_escalada = mejora["imagen"]
            dinero_mejora = mejora['Dinero'] + mundo.Ronda
            texto_mejora = (f"{mejora['texto']} | {dinero_mejora}")
            
            
            # Obtener dimensiones de la imagen
            ancho_imagen = imagen_objeto_escalada.get_width()
            alto_imagen = imagen_objeto_escalada.get_height()

            # Calcular la posición para centrar la imagen en la sección
            x_imagen = rect_seccion.x + (ancho_seccion - ancho_imagen) // 2
            y_imagen = rect_seccion.y + 10  

            # Dibujar la imagen en la sección
            ventana.blit(imagen_objeto_escalada, (x_imagen, y_imagen))

            # Agregar texto descriptivo debajo de la imagen
            fuente_texto = pygame.font.Font(None, 24)
            texto_render = fuente_texto.render(texto_mejora, True, constante.NEGRO)
            ventana.blit(texto_render, (rect_seccion.x + (ancho_seccion - texto_render.get_width()) // 2, 
                                        y_imagen + alto_imagen + 5))  

            # Agregar texto "Comprar" en el botón
            texto_boton = fuente_texto.render("comprar", True, constante.NEGRO)
        
            # Botón de comprar debajo del cuadro correspondiente
            if i == 0:
                boton_comprar_1 = pygame.Rect(
                rect_seccion.x + 10, 
                rect_seccion.bottom + 5,  
                ancho_boton,
                alto_boton
                )
                pygame.draw.rect(ventana, constante.BLANCO, boton_comprar_1)
                ventana.blit(texto_boton, (boton_comprar_1.x + (ancho_boton - texto_boton.get_width()) // 2,
                            boton_comprar_1.y + (alto_boton - texto_boton.get_height()) // 2))
            elif i == 1:
                boton_comprar_2 = pygame.Rect(
                rect_seccion.x + 10, 
                rect_seccion.bottom + 5,  
                ancho_boton,
                alto_boton
                )
                pygame.draw.rect(ventana, constante.BLANCO, boton_comprar_2)
                ventana.blit(texto_boton, (boton_comprar_2.x + (ancho_boton - texto_boton.get_width()) // 2,
                            boton_comprar_2.y + (alto_boton - texto_boton.get_height()) // 2))
            elif i == 2:
                boton_comprar_3 = pygame.Rect(
                rect_seccion.x + 10, 
                rect_seccion.bottom + 5,  
                ancho_boton,
                alto_boton
                )
                pygame.draw.rect(ventana, constante.BLANCO, boton_comprar_3)
                ventana.blit(texto_boton, (boton_comprar_3.x + (ancho_boton - texto_boton.get_width()) // 2,
                            boton_comprar_3.y + (alto_boton - texto_boton.get_height()) // 2))

        # Crear el rectángulo para el botón "Continuar" debajo del rectángulo principal
        ancho_continuar = 200  # Ancho ajustado para el botón continuar
        alto_continuar = 50    # Altura del botón continuar
        x_continuar = (constante.ANCHO_VENTANA - ancho_continuar) // 2  # Centrado horizontalmente
        y_continuar = (constante.ALTO_VENTANA - alto_tienda - 100) // 2  # Colocarlo justo debajo del rectángulo principal

        rect_continuar = pygame.Rect(x_continuar, y_continuar, ancho_continuar, alto_continuar)

        # Dibujar el rectángulo "Continuar"
        pygame.draw.rect(ventana, constante.BLANCO, rect_continuar)

        # Añadir borde gris fino alrededor del rectángulo
        pygame.draw.rect(ventana, (169, 169, 169), rect_continuar, 2)

        # Agregar texto "Continuar" en el rectángulo
        texto_continuar = font_objetos.render("Continuar", True, constante.NEGRO)
        ventana.blit(texto_continuar, (rect_continuar.x + (ancho_continuar - texto_continuar.get_width()) // 2,
                                    rect_continuar.y + (alto_continuar - texto_continuar.get_height()) // 2))


    #cargar la ui 
    ui(jugador, mundo)

    #dibujar balas
    for proyectil in grupo_proyectiles:
         proyectil.dibujar(ventana)
    
    #dibujar los textos
    grupo_damage_text.draw(ventana)


    #Cerrar el juego y manejar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        #Inputs para moverse
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                mover_izquierda = True
            if event.key == pygame.K_d:
                mover_derecha = True
            if event.key == pygame.K_w:
                mover_arriba = True
            if event.key == pygame.K_s:
                mover_abajo = True 
            if event.key == pygame.K_COMMA:
                tipo_Arma = 2
            if event.key == pygame.K_PERIOD:
                tipo_Arma = 1
            if event.key == pygame.K_0:
                jugador.monedas = 1000

        #Para cuando se suelta la tecla 
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                mover_izquierda = False
            if event.key == pygame.K_d:
                mover_derecha = False
            if event.key == pygame.K_w:
                mover_arriba = False
            if event.key == pygame.K_s:
                mover_abajo = False

    basMorado.cambiar_arma(tipo_Arma, img_b_Morado, img_H_Aire)
    basMorado.cambiar_imagen(img_proyectil, img_pro_aire, tipo_Arma)

    if jugador.vivo == False:
        ventana.fill(constante.NEGRO)
        text_rect = GameOver_Text.get_rect(center=(constante.ANCHO_VENTANA/2, constante.ALTO_VENTANA/2))
        ventana.blit(GameOver_Text, text_rect)

        # Crear el rectángulo para el botón "Reiniciar"
        ancho_reiniciar = 200
        alto_reiniciar = 50
        x_reiniciar = (constante.ANCHO_VENTANA - ancho_reiniciar) // 2
        y_reiniciar = (constante.ALTO_VENTANA - alto_reiniciar) // 2 + 100  # Ajustar la posición vertical
        rect_reiniciar = pygame.Rect(x_reiniciar, y_reiniciar, ancho_reiniciar, alto_reiniciar)

        # Dibujar el botón "Reiniciar"
        pygame.draw.rect(ventana, constante.BLANCO, rect_reiniciar)

        # Añadir borde gris fino alrededor del rectángulo
        pygame.draw.rect(ventana, (169, 169, 169), rect_reiniciar, 2)

        # Agregar texto "Reiniciar" en el rectángulo
        texto_reiniciar = font_objetos.render("Reiniciar", True, constante.NEGRO)
        ventana.blit(texto_reiniciar, (rect_reiniciar.x + (ancho_reiniciar - texto_reiniciar.get_width()) // 2,
                                    rect_reiniciar.y + (alto_reiniciar - texto_reiniciar.get_height()) // 2))
        
        # Verificar si el jugador hace clic en el botón "Reiniciar"
        if event.type == pygame.MOUSEBUTTONDOWN:
            if rect_reiniciar.collidepoint(event.pos) or texto_reiniciar.collidepoint(event.pos):  # Comprobar si el clic está dentro del botón
                # Aquí reiniciamos todo el juego
                jugador = Personaje(1000, 500, animaciones, 100, 1)  # Reiniciar el jugador
                mundo.Ronda = 1  # Reiniciar ronda
                enemigos = lista_enemigos(1, 2)  # Reiniciar enemigos
                grupo_damage_text.empty()  # Limpiar los textos de daño
                grupo_proyectiles.empty()  # Limpiar los proyectiles
                tienda_abierta = False  # Cerrar la tienda
                tienda = False  # Desactivar tienda
                run = True  # Reiniciar el ciclo del juego

    pygame.display.update()

pygame.quit()