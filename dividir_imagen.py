from PIL import Image
import os

def dividir_guardar_imagen(ruta_imagen, carpeta_destino, divisiones_por_columna):
    #cargar imagen
    with Image.open(ruta_imagen) as img:
        #obtener dimensiones
        ancho, alto = img.size
        #calcular tamaño de la división
        ancho_division = ancho // divisiones_por_columna

        os.makedirs(carpeta_destino, exist_ok=True)

        contador = 0
        #iterar sobre las divisiones 
        for i in range(divisiones_por_columna):
            for j in range(divisiones_por_columna):
                izquierda = i * ancho_division
                arriba = j * ancho_division
                derecha = izquierda + ancho_division
                abajo = arriba + ancho_division

                #recortar la imagen
                img_recortada = img.crop((izquierda, arriba, derecha, abajo))
                nombre_archivo = f"tile_{contador+1}.png"
                contador += 1
                #guardar la imagen  
                img_recortada.save(os.path.join(carpeta_destino, nombre_archivo))


dividir_guardar_imagen("assets//Tiles//Tilemap_Flat.png", "assets//Tiles", 10)