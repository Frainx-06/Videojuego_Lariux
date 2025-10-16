import pygame
import constante
import math

class BastonMorado():
    def __init__(self, image, imagen_bala):
        self.imagen_bala = imagen_bala
        # Bastón
        self.imagen_original = image
        self.update_time = pygame.time.get_ticks()
        self.angulo = 180
        self.imagen = pygame.transform.rotate(self.imagen_original, self.angulo)
        self.forma = self.imagen.get_rect()
        self.distancia_minima = None  
    
    def cambiar_imagen(self, arma1, arma2, tipo_arma): 
        if tipo_arma == 1:
            self.imagen_bala = arma1
        elif tipo_arma == 2:
            self.imagen_bala = arma2

    def cambiar_arma(self, tipo_Arma, arma1, arma2):
        if self.angulo is None:
            self.angulo = 180
        if tipo_Arma == 1:
            self.imagen_original = arma1
            self.imagen = pygame.transform.rotate(self.imagen_original, self.angulo)
            self.distancia_minima = float(500)
        else:
            self.imagen_original = arma2
            self.imagen = pygame.transform.rotate(self.imagen_original, self.angulo)
            self.distancia_minima = float(200)



    def obtener_objetivo_mas_cercano(self, enemigos):
        # Buscar el enemigo más cercano
        enemigo_cercano = None
        
        for enemigo in enemigos:
            # Calculamos la distancia entre el proyectil y el enemigo
            dx = enemigo.forma.centerx - self.forma.centerx
            dy = enemigo.forma.centery - self.forma.centery
            distancia = math.sqrt(dx**2 + dy**2)

            if distancia < self.distancia_minima:
                enemigo_cercano = enemigo
                self.distancia_minima = distancia

        return enemigo_cercano

    def update(self, personaje, enemigos, grados, tipo_Arma,bonusDaño):
        bala = None

        self.forma.center = personaje.forma.center
        self.forma.x += personaje.forma.width - 40
        self.forma.y -= personaje.forma.height - 60

        # Mover la rotación del arma
        self.angulo = grados

        # Disparar
        if tipo_Arma == 2:
            cooldown_animacion = 300
        else: 
            cooldown_animacion = 1000
        
        if pygame.time.get_ticks() - self.update_time >= cooldown_animacion:
            # Obtener el enemigo más cercano
            enemigo_cercano = self.obtener_objetivo_mas_cercano(enemigos)

            if enemigo_cercano:
                # Crear el proyectil y darle la posición inicial y objetivo
                if tipo_Arma == 1:
                    bala = Pro(self.imagen_bala, self.forma.centerx, self.forma.centery, enemigo_cercano.forma.center, 5, bonusDaño)  
                else:
                    bala = Pro(self.imagen_bala, self.forma.centerx, self.forma.centery, enemigo_cercano.forma.center, 10, bonusDaño) 
                #print("Se creó un proyectil en:", self.forma.centerx, self.forma.centery, "Ángulo hacia enemigo:", enemigo_cercano.forma.center)
                self.update_time = pygame.time.get_ticks()
            else:
                return None
            
        return bala
    
    def dibujar(self, ventana, validacion):
        #pygame.draw.rect(ventana, constante.NEGRO, self.forma, 1)
        if self.angulo is None:
            self.angulo = 180
        if validacion == None:
            self.imagen = pygame.transform.rotate(self.imagen_original, 32)
        else:
            self.imagen = pygame.transform.rotate(self.imagen_original, 360 - self.angulo)
        ventana.blit(self.imagen, self.forma)

class Pro(pygame.sprite.Sprite):
    def __init__(self, image, x, y, objetivo, velocidad, bonusDaño):
        pygame.sprite.Sprite.__init__(self)
        self.imagen_ori = image
        self.image = self.imagen_ori
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocidad = velocidad  # Velocidad del movimiento
        self.objetivo = objetivo  # El objetivo al que se dirige el proyectil (una posición)
        self.bonusDaño = bonusDaño

    def calcular_angulo(self):
        # Calculamos el ángulo entre la posición actual y la posición del objetivo
        dx = self.objetivo[0] - self.rect.centerx
        dy = self.objetivo[1] - self.rect.centery
        angulo = math.degrees(math.atan2(dy, dx))  # Convertimos de radianes a grados
        return angulo 

    def update(self, lista_enemigos, proyectiles, posicion_pantalla, personaje, tipo_arma, sonido_impacto):
        damage = 0
        pos_daño = None
        # Calculamos el ángulo hacia el objetivo
        angulo = self.calcular_angulo()

        # Animación para que el proyectil suba y baje en el eje y como si flotara
        if tipo_arma == 1:
            tiempo_actual = pygame.time.get_ticks()
            amplitud = 3  # La amplitud del movimiento de flotación
            frecuencia = 0.005  # La frecuencia del movimiento de flotación
            # Calculamos el desplazamiento en y usando una función seno para el efecto de flotación
            desplazamiento_y = amplitud * math.sin(frecuencia * tiempo_actual)
        else:
            desplazamiento_y = 0
        self.rect.y += desplazamiento_y

        # Calculamos las componentes del movimiento en x e y
        delta_x = math.cos(math.radians(angulo)) * self.velocidad
        delta_y = math.sin(math.radians(angulo)) * self.velocidad

        # Actualizamos la posición
        self.rect.x += delta_x
        self.rect.y += delta_y

        # Ajustar la posición del proyectil según la posición de la pantalla
        self.rect.x += posicion_pantalla[0]
        self.rect.y += posicion_pantalla[1]

        # Verificar si el proyectil sale de la pantalla y eliminarlo
        if (self.rect.right < 0 or self.rect.left > constante.ANCHO_VENTANA or
            self.rect.bottom < 0 or self.rect.top > constante.ALTO_VENTANA):
            self.kill()
            return damage, pos_daño

        # Verificar si el proyectil ha alcanzado el objetivo
        if math.hypot(self.rect.centerx - self.objetivo[0], self.rect.centery - self.objetivo[1]) < self.velocidad:
            self.kill()
            return damage, pos_daño

        # Verificar si hay colisión
        for enemigo in lista_enemigos:
            if self.rect.colliderect(enemigo.forma):
                
                if tipo_arma == 1:
                    damage = 40 + self.bonusDaño
                elif tipo_arma == 2:
                    damage = 20 + self.bonusDaño

                pos_daño = enemigo.forma
                sonido_impacto.play()
                enemigo.vida -= damage
                #print("El enemigo ha recibido", damage, "de daño. Vida restante:", enemigo.vida)
                if enemigo.vida <= 0:
                    lista_enemigos.remove(enemigo)
                    personaje.monedas += 1
                    for proyectil in proyectiles:
                        if proyectil.objetivo == enemigo.forma.center:
                            proyectil.kill()
                    self.kill()
                    break
                else:
                    self.kill()  # Eliminar el proyectil después de causar daño
                    break
        return damage, pos_daño

    def dibujar(self, ventana):
        ventana.blit(self.image, (self.rect.centerx - self.image.get_width() // 2, 
                                  self.rect.centery - self.image.get_height() // 2))
