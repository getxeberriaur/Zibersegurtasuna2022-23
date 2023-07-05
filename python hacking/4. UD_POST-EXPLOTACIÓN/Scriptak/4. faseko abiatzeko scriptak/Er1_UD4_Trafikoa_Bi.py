#******************************************************************************************************************************************
#Curso "Python para hacking ético" Tknika 2022/2023
#RESUMEN DEL SCRIPT:
#Recibimos un fichero .pcap y lo analizamos, imprimiendo su información de manera más legible.
#En este caso imprimiremos información referente a tráfico TCP saliente hacia una IP y puerto introducidos por el usuario. 
#¡¡Atención!! Para que el script funcione, debes instalar el módulo pyshark en Python; para ello, ejecuta en la línea de comandos de Kali:
#      pip3 install pyshark
#******************************************************************************************************************************************

import time, ipaddress, os
#Libería para trabajar con Wireshark
import pyshark

# Función que recibe un paquete y guarda la información más relevante en vaiables. 
def conversacion_red(paquete):
   try:
   
      numero = str(paquete.number)
      #Obtenemos la dirección de destino del paquete
      longitud = str(paquete.length)
      #Obtenemos el puerto de destino del paquete
      fechayhora = paquete.sniff_time.strftime("%d-%m-%Y %H:%M:%S")
      #Devolvemos un mensaje formateado en el que aparece el contenido de las variables 
      resultado = f'      {numero:24} {longitud:22} {fechayhora}'
      return resultado

   except AttributeError as error:
      print (f"Error: {error}")

#Función que comprueba si un valor es una IP válida; si no lo es, comprueba si es un nombre de host válido. 
def validar_destino(direccion_destino):
    try:
        ipaddress.ip_address(direccion_destino)
        return True 
    except ValueError:
        return False

#Función que comprueba si un valor es un puerto válido: está vacío (puerto por defecto) o está entre 1 y 65535
def validar_puerto(puerto):
    if puerto=="":
        return True
    else:
        try:
            puerto_destino = int(puerto)
            if 1 <= puerto_destino <= 65535:
                return True
            else:
                return False
        except ValueError:
            return False
#Función para solicitar al usuario que introduzca los datos que vamos a necesitar para conectarnos al servidor ssh: IP, puerto de destino, y usuario. 
def solicitar_datos_usuario():
    try:
        destino_correcto=False
        puerto_correcto=False
        while not destino_correcto:
            destino = input('>> Introduce la dirección IP de destino: ')
            if validar_destino(destino):
                destino_correcto=True
        while not puerto_correcto:
            puerto = input('>> Introduce el puerto de destino, entre 1 y 65535: ')
            if validar_puerto(puerto):
                puerto_correcto=True
                
        return destino, puerto
  
    except ValueError:
        print ("Ha ocurrido un error inesperado...")

if __name__ == "__main__":
   try: 
      direccion_ip, puerto_usuario=solicitar_datos_usuario()
      fichero_correcto=False
      #Pedimos al usuario que introduzca la ruta de un archivo con la captura del tráfico. 
      while not fichero_correcto:
          ruta_fichero = input('>> Introduce la ruta al archivo de tráfico (.pcap): ')
          if ruta_fichero != "":
              if os.path.exists(ruta_fichero):          
                  fichero_correcto=True
              else:
                  print ('El archivo ' + ruta_fichero + ' no existe')
   except ValueError:
       print ("Error inesperado con el archivo")
   ##(◕‿−) A partir de aquí, introduce las líneas que faltan:
   try:
       #(◕‿−) Creamos un objeto de la clase FileCapture que contendrá toda la información del fichero.

       #(◕‿−) Inicializamos la lista para almacenar las conversaciones 

       # (◕‿−) Iteramos por cada paquete de la captura
           #Si se trata de un paquete "TCP"
           if paquete.transport_layer=="TCP":
              #(◕‿−)Si el puerto e IP introducidos por el usuario coinciden con los del paquete, añadimos a la
              #lista "conversaciones" la información correspondiente al paquete 
              
            
      #Imprimimos la cabecera
       print (f"*****Listado de paquetes hacia la IP {direccion_ip} y puerto {puerto_usuario} ******")  
       print ("------------------------------------------------------------------------------")
       print ("Nº de paquete                Longitud                Fecha y hora de emisión")
       print ("*************               **********              *************************") 
       # Ordenamos las conversaciones; después, las imprimimos. 
       for conversacion in sorted(conversaciones):
           print(conversacion)
   except Exception as error_impresion:
       print (f"Error al imprimir el contenido por pantalla: {error_impresion}")
