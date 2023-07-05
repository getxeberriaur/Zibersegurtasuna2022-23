#*************************************************************************************************
#Curso "Python para hacking ético" Tknika 2022/2023
#RESUMEN DEL SCRIPT: 
#El usuario introduce la ruta de una imagen, y obtenemos el modelo de cámara con el que fue tomada   
#*************************************************************************************************

#El módulo PIL proporciona funciones y clases para manipular imágenes. Importamos su clase Image
from PIL import Image
#Importamos las constantes TAGS y GPSTAGS del módulo ExifTags en el paquete PIL. Estas constantes contienen los nombres de las
#etiquetas EXIF estándar y etiquetas GPS respectivamente.
from PIL.ExifTags import TAGS, GPSTAGS
#Importamos este módulo para interactuar con el sistema operativo. En este ejercicio en concreto, para comprobar si el archivo
#introducido por el usuario existe
import os

#Función que obtiene los datos EXIF de una imagen, devolviéndolos en una tupla
def obtener_datos_exif(imagen):
    diccionario_exif = {}
    try:
        img = Image.open(imagen)
        diccionario_exif = img._getexif()
        return diccionario_exif
    except:
        print ("Error inesperado al obtener los datos de la imagen proporcionada")

# Función que obtiene los datos de geolocalización a partir de los datos EXIF de una imagen y los devuelve en una tupla
def obtener_modelo_camara(datos_exif):
    if not datos_exif:
        print ("No se encontraron metadatos EXIF")
    else:
        modelo = None
        clave_modelo = None
        #Iteramos sobre las claves y valores del diccionario TAGS. En cada iteración, key representa la clave actual y
        #value representa el valor correspondiente. clave_modelo almacenará el valor del código de la etiqueta Model. Podríamos
        #haber asumido como clave la que tiene en la actualizad (272), pero, ¿y si varía?
        for clave, valor in TAGS.items():
            if valor == 'Model':
                clave_modelo = clave
        #Si hay datos del modelo de la cámara y la clave encontrada está dentro del diccionario recibido, guardamos el elemento correspondiente
        #del diccionario en la variable "modelo"
        if clave_modelo is not None and clave_modelo in datos_exif:
            modelo = datos_exif[clave_modelo]
        return modelo

#(◕‿−) Escribir el cuerpo del script
if __name__ == '__main__':
    #Pedimos al usuario que introduzca la ruta de un archivo. Mientras el archivo introducido no exista, se lo volveremos a
    #solicitar. 

    
    #Obtenemos los metadatos del archivo

    #Obtenemos el modelo de la cámara

    #Si la variable 'modelo_camara'no está vacía, imprimimos su valor; si no, señal de que no se ha podido obtener el modelo.
      
