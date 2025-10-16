import random
import pygame
import math
import constante

class Personaje():
    def __init__(self, x, y, animaciones, vida, tipo):
        self.monedas = 5
        self.vida = vida
        self.vivo = True
        self.flip = False
        self.animaciones = animaciones
        #Animaciones del personaje
        self.frame_index = 0
        #Aqui se almacena la hora actual (en milisegundos desde que se inicio 'pygame')
        self.update_time = pygame.time.get_ticks()
        self.image = animaciones[self.frame_index]
        self.forma = pygame.Rect(x, y, self.image.get_width(), self.image.get_height())
        self.tipo = tipo
        self.golpe = False
        self.ultimo_golpe = pygame.time.get_ticks()
        self.velocidad = 2
        self.agilidad = 0

    def movimiento(self, delta_x, delta_y, obstaculos):
        posicion_pantalla = [0,0]
        if delta_x < 0:
            self.flip = True
        if delta_x > 0:
            self.flip = False

        self.forma.x += delta_x
        for obstaculo in obstaculos:
            if obstaculo[1].colliderect(self.forma):
                if delta_x > 0:
                    self.forma.right = obstaculo[1].left
                if delta_x < 0:
                    self.forma.left = obstaculo[1].right
        self.forma.y += delta_y
        for obstaculo in obstaculos:
            if obstaculo[1].colliderect(self.forma):
                if delta_y > 0:
                    self.forma.bottom = obstaculo[1].top
                if delta_y < 0:
                    self.forma.top = obstaculo[1].bottom

        if self.tipo == 1:
            if self.forma.right >(constante.ANCHO_VENTANA - constante.LIMITE_PANTALLA):
                posicion_pantalla[0] = (constante.ANCHO_VENTANA - constante.LIMITE_PANTALLA) - self.forma.right
                self.forma.right = constante.ANCHO_VENTANA - constante.LIMITE_PANTALLA
            if self.forma.left < constante.LIMITE_PANTALLA:
                posicion_pantalla[0] = constante.LIMITE_PANTALLA - self.forma.left
                self.forma.left = constante.LIMITE_PANTALLA
            if self.forma.bottom >(constante.ALTO_VENTANA - constante.LIMITE_PANTALLA):
                posicion_pantalla[1] = (constante.ALTO_VENTANA - constante.LIMITE_PANTALLA) - self.forma.bottom
                self.forma.bottom = constante.ALTO_VENTANA - constante.LIMITE_PANTALLA
            if self.forma.top < constante.LIMITE_PANTALLA:
                posicion_pantalla[1] = constante.LIMITE_PANTALLA - self.forma.top
                self.forma.top = constante.LIMITE_PANTALLA
            return posicion_pantalla
    
    def enemigo(self, posicion_pantalla, obstaculo, jugador):
        ene_dx = 0
        ene_dy = 0

        self.forma.x += posicion_pantalla[0]
        self.forma.y += posicion_pantalla[1]

        #seguir al jugador por el eje x
        if self.forma.centerx > jugador.forma.centerx:
            ene_dx = -constante.VELOCIDAD_ENEMIGO
        if self.forma.centerx < jugador.forma.centerx:
            ene_dx = constante.VELOCIDAD_ENEMIGO
        
        #seguir al jugador por el eje y
        if self.forma.centery > jugador.forma.centery:
            ene_dy = -constante.VELOCIDAD_ENEMIGO
        if self.forma.centery < jugador.forma.centery:
            ene_dy = constante.VELOCIDAD_ENEMIGO
        
        #atacar al jugador
        if self.forma.colliderect(jugador.forma) and jugador.golpe == False:
            if jugador.agilidad > 8:
                jugador.agilidad = 8 

            prob = random.randint (jugador.agilidad, 10)
            
            if prob < 10 :
                jugador.vida -= 25
            jugador.golpe = True
            jugador.ultimo_golpe = pygame.time.get_ticks()
            
            
        self.movimiento(ene_dx, ene_dy, obstaculo)

    def update(self, quieto):
        if self.vida <= 0:
            self.vida = 0
            self.vivo = False

        cooldown_animacion = 200  # Ajusta el cooldown a un valor más bajo
        cooldown_golpe = 1000
        if self.tipo == 1:
            if self.golpe == True:
                if pygame.time.get_ticks() - self.ultimo_golpe > cooldown_golpe:
                    self.golpe = False

        if quieto == True:
            if self.frame_index > 1:
                self.frame_index = 0
            cooldown_animacion = 400
        self.image = self.animaciones[self.frame_index]
        if pygame.time.get_ticks() - self.update_time >= cooldown_animacion:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animaciones):
            self.frame_index = 0 

    def autoaim(self, enemigos):
        if enemigos:
            # Encontrar el enemigo más cercano basado en la distancia
            closest_enemy = min(enemigos, key=lambda enemigos: math.dist((self.forma.x, self.forma.y), (enemigos.forma.x, enemigos.forma.y)))
            
            # Obtener coordenadas del enemigo (por ejemplo, golem)
            enemy_x, enemy_y = closest_enemy.forma.x, closest_enemy.forma.y
            
            # Calcular el ángulo hacia ese enemigo
            dx = enemy_x - self.forma.x
            dy = enemy_y - self.forma.y
            angle = math.degrees(math.atan2(dy, dx))  # Ángulo en radianes
            return angle
        return None
    
    def dibujar(self, ventana):
       #pygame.draw.rect(ventana, constante.ROJO, self.forma, 1)
        imagen_dibujar=pygame.transform.flip(self.image, self.flip, False)
        ventana.blit(imagen_dibujar, self.forma)