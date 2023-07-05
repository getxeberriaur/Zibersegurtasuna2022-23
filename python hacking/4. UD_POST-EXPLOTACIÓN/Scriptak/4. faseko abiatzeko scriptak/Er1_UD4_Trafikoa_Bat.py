#******************************************************************************************************************************************
#Curso "Python para hacking ético" Tknika 2022/2023
#RESUMEN DEL SCRIPT:
#Recibimos un fichero .pcap y lo analizamos, imprimiendo su información de manera más legible.
#En este caso imprimiremos información referente a paquetes ICMP.
#¡¡Atención!! Para que el script funcione, debes instalar el módulo pyshark en Python; para ello, ejecuta en la línea de comandos de Kali:
#      pip3 install pyshark
#**********************************************************************************************************************************
import time,ipaddress, os
#Libería para trabajar con Wireshark
import pyshark


# Función que recibe un paquete y guarda la información más relevante en vaiables. 
def conversacion_red(paquete):
   try:
      #Obtenemos la dirección de origen del paquete
      direccion_origen = paquete.ip.src
      #Obtenemos la dirección de destino del paquete
      direccion_destino = paquete.ip.dst
      #Obtenemos la fecha y hora del paquete llamando al método strftime de la librería 
      fechayhora = paquete.sniff_time.strftime("%d-%m-%Y %H:%M:%S")
      #Devolvemos un mensaje formateado en el que aparece el contenido de las variables 
      return f'{direccion_origen:<24}  {direccion_destino:<26}  {fechayhora}'
   except AttributeError as error:
      print ("Error: {error}")

if __name__ == "__main__": 
   try: 
      fichero_correcto=False
      #Pedimos al usuario que introduzca la ruta de un archivo que contenga las contraseñas. Debe ser un archivo con una contraseña por línea.
      while not fichero_correcto:
          ruta_fichero = input('>> Introduce la ruta al archivo de contraseñas (una contraseña por línea): ')
          if ruta_fichero != "":
              if os.path.exists(ruta_fichero):          
                  fichero_correcto=True
              else:
                  print ('El archivo ' + ruta_fichero + ' no existe')
   except ValueError:
       print ("Error inesperado con el archivo")
  ##(◕‿−) A partir de aquí, introduce las líneas que faltan: 
   try: 
       #Creamos un objeto de la clase FileCaptura que contendrá toda la información del fichero.
       captura = pyshark.FileCapture(ruta_fichero)
       ##(◕‿−)Inicializamos la lista para almacenar las conversaciones 
       
       #(◕‿−)Iteramos por cada elemento de la captura
           #Si dentro del paquete aparece la palabra icmp:
           if 'icmp' in paquete:
              #(◕‿−)Guardamos en la variable "resultado" la cadena de caracteres generada por la función "conversacion_red"
              
              #(◕‿−)Si el string "resultado" no está vacío
              
                 #(◕‿−)Añadimos el string a la lista "conversaciones"

       #Imprimimos la cabecera
       print ("************************Listado de paquetes ICMP *****************************")
       print ("------------------------------------------------------------------------------")
       print ("Dirección de origen     Dirección de destino         Fecha y hora de emisión")
       print ("********************   **********************       *************************")
       # Iteramos por la lista ordenada de conversaciones para imprimirlas; después, las imprimimos. 
       for conversacion in sorted(conversaciones):
            #(◕‿−)Imprimir la conversación
   except Exception as error_impresion:
        print (f"Error al imprimir el contenido por pantalla: {error_impresion}")

