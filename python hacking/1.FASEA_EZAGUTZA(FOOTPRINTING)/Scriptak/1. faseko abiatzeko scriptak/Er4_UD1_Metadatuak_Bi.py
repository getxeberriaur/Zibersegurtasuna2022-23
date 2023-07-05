#*************************************************************************************************
#Curso "Python para hacking ético" Tknika 2022/2023
#RESUMEN DEL SCRIPT: 
#El usuario introduce la ruta de una imagen, y obtenemos la ciudad en la que fue tomada   
#*************************************************************************************************

#El módulo PIL proporciona funciones y clases para manipular imágenes. Importamos su clase Image
from PIL import Image
#Importamos las constantes TAGS y GPSTAGS del módulo ExifTags en el paquete PIL. Estas constantes contienen los nombres de las
#etiquetas EXIF estándar y etiquetas GPS respectivamente.
from PIL.ExifTags import TAGS, GPSTAGS
#Importamos este módulo para interactuar con el sistema operativo. En este ejercicio en concreto, para comprobar si el archivo
#introducido por el usuario existe
import os

#(◕‿−)OPCIONAL: Importamos las funciones obtener_ciudad, latitud_correcta y longitud_correcta del script ER3_UD1_Geolokalizazioa_Bat

#Función que obtiene los datos EXIF de una imagen, devolviéndolos en una tupla
def obtener_datos_exif(imagen):
    diccionario_exif = {}
    try:
        img = Image.open(imagen)
        diccionario_exif = img._getexif()
    except:
        print ("Error inesperado al obtener los datos de la imagen proporcionada")
    return diccionario_exif

# Función que obtiene los datos de geolocalización a partir de los datos EXIF de una imagen y los devuelve en una tupla
def obtener_geolocalizacion(datos_exif):
    if not datos_exif:
        raise ValueError("No se encontraron metadatos EXIF")
    geolocalizacion = {}
    clave_gps_info = None
    #Estamos iterando sobre las claves y valores del diccionario TAGS. En cada iteración, key representa la clave actual y
    #value representa el valor correspondiente. clave_gps_info almacenará el valor del código de la etiqueta GPSInfo. Podríamos
    #haber asumido como clave la que tiene en la actualizad (34853), pero, ¿y si varía?
    for clave, valor in TAGS.items():
        if valor == 'GPSInfo':
            clave_gps_info = clave
    #Si hay datos de geolocalización y la clave encontrada está dentro del diccionario recibido, formamos una tupla ("geolocalizacion")
    #sólo con la información que nos interesa.    
    if clave_gps_info is not None and clave_gps_info in datos_exif:
        gps_info = datos_exif[clave_gps_info]
        for clave_gps, valor_gps in gps_info.items():
            if clave_gps in GPSTAGS:
                geolocalizacion[GPSTAGS[clave_gps]] = valor_gps
    #El contenido de la tupla "geolocalizacion" será algo así como:
    #{'GPSVersionID': b'\x02\x02\x00\x00', 'GPSLatitudeRef': 'N', 'GPSLatitude': (40.0, 41.0, 21.12),
    # 'GPSLongitudeRef': 'W', 'GPSLongitude': (74.0, 2.0, 40.2), 'GPSAltitudeRef': b'\x00', 'GPSAltitude': 10.0,
    # 'GPSTimeStamp': (0.0, 0.0, 0.0), 'GPSProcessingMethod': '', 'GPSDateStamp': '00:00:00'}
    return geolocalizacion

# Función que obtiene las coordenadas GPS de latitud y longitud a partir de los datos de geolocalización y los devuelve en
# dos variables
def obtener_coordenadas(geolocalizacion):
    latit = None
    longit = None
    #Dentro de la tupla, iteramos sólo sobre las claves que nos interesan para obtener sus valores. 
    #Convertimos el valor de esas claves a coordenada decimal. Por ejemplo, GPSLatitude lo pasaremos de (40.0, 41.0, 21.12)
    #a 40.6892
    for key in ['GPSLatitude', 'GPSLongitude', 'GPSLatitudeRef', 'GPSLongitudeRef']:
        if key in geolocalizacion:
            if key == 'GPSLatitude':
                latit = convertir_a_decimal(geolocalizacion[key])
            if key == 'GPSLongitude':
                longit = convertir_a_decimal(geolocalizacion[key])
            if key == 'GPSLatitudeRef' and geolocalizacion[key] == 'S':
                latit = 0 - latit
            if key == 'GPSLongitudeRef' and geolocalizacion[key] == 'W':
                longit = 0 - longit
    return latit, longit

# Función que convierte los valores GPS de grados, minutos y segundos a valores decimales
def convertir_a_decimal(coordenada):
    grados = float(coordenada[0])
    minutos = float(coordenada[1])
    segundos = float(coordenada[2])
    return grados + minutos / 60 + segundos / 3600

#(◕‿−) Escribir el cuerpo del script
if __name__ == '__main__':
    #Pedimos al usuario que introduzca la ruta de un archivo. Mientras el archivo introducido no exista, se lo volveremos a
    #solicitar. 
    
    #Obtenemos los metadatos del archivo

    #Creamos una tupla sólo con los metadatos relativos a la geolocalización

    #Creamos una tupla sólo con los metadatos relativos a la geolocalización

    #Comprobamos si la latitud y la longitud tienen  valores crrectos. Si los tienen, obtenemos la ciudad. Para ello,
    #podemos utilizar funciones del script ER3_UD1_Geolokalizazioa_Bat
    
