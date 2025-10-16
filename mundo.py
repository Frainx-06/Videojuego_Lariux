import pygame
import constante

obstaculos = [39]

class Mundo():
    def __init__(self):
        self.map_tiles = []
        self.obstaculos = []
        self.Ronda= 1


    def process_data(self, data, tile_list):
        self.level_length = len(data)
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile_list[tile] is not None:  # Verificar que la imagen no sea None
                    image = tile_list[tile]
                    image_rect = image.get_rect()
                    image_x = x * constante.TILE_SIZE
                    image_y = y * constante.TILE_SIZE
                    image_rect.center = (image_x, image_y)
                    tile_data = (image, image_rect, image_x, image_y)
                    if tile in obstaculos:
                        self.obstaculos.append(tile_data)
                    self.map_tiles.append(tile_data)               

    def update(self, posicion_pantalla):
        nuevos_tiles = []

        for tile in self.map_tiles:
            tile = list(tile)  # Convertir en lista para modificar
            tile[2] += posicion_pantalla[0]
            tile[3] += posicion_pantalla[1]
            tile[1].center = (tile[2], tile[3])  # Actualizar rect
            nuevos_tiles.append(tuple(tile))  # Convertir de nuevo a tupla y guardar
        self.map_tiles = nuevos_tiles  # Reemplazar la lista original

    def draw(self, ventana):
        for tile in self.map_tiles:
            ventana.blit(tile[0], tile[1])
