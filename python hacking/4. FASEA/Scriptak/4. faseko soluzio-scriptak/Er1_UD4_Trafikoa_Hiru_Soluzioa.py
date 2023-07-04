#******************************************************************************************************************************************
#Curso "Python para hacking ético" Tknika 2022/2023
#RESUMEN DEL SCRIPT:
#Recibimos un fichero .pcap y lo analizamos, imprimiendo su información de manera más legible.
#En este caso imprimiremos información referente a tráfico TCP  desde una IP y hacia un puerto determinados
#Utilizaremos principalmente la librería Scapy 
#******************************************************************************************************************************************

from scapy.all import *
import time, ipaddress

# Función para analizar y mostrar información de los paquetes TCP
def analizar_paquetes(paquetes, ip_src, puerto_dst):
    print(f"***** Listado de paquetes desde la IP {ip_src} y puerto {puerto_dst} ******")
    print("------------------------------------------------------------------------------")
    print("Nº de paquete            IP de destino                Fecha/hora de emisión")
    print("*************           ****************           *************************")
    #Recorremos los paquetes, de tal manera que se asigne el índice a la variable numero_paquete
    for numero_paquete, paquete in enumerate(paquetes, start=1):
        #Si el paquete es TCP/IP
        if paquete.haslayer(IP) and paquete.haslayer(TCP):
            #Asignamos a las variables ip y tcp la extracción de las capasip y tcp respectivamente. 
            ip = paquete[IP]
            tcp = paquete[TCP]
            #Si la IP de origen y el puerto de destino son los introducidos por el usuario, obtenemos la información que vamos a imprimir
            if ip.src == ip_src and tcp.dport == int(puerto_dst):
                fecha_hora = paquete.time
                fecha_hora_str = time.strftime("%d-%m-%Y %H:%M:%S", time.localtime(int(fecha_hora)))
                destino=ip.dst
                print(f"{numero_paquete:<25}{destino:<28}{fecha_hora_str}")
#Función que comprueba si un valor es una IP válida; si no lo es, comprueba si es un nombre de host válido. 
def validar_destino(direccion_destino):
    try:
        ipaddress.ip_address(direccion_destino)
        return True 
    except ValueError:
        return False

#Función que comprueba si un valor es un puerto válido: está vacío (puerto por defecto) o está entre 1 y 65535
def validar_puerto(puerto):
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
            destino = input('>> Introduce la dirección IP de origen: ')
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
   try:
      #Asignamos a una variable la captura del fichero. Utilizamos la función rdpcap para ello. 
      captura = rdpcap(ruta_fichero)
      #Llamamos a la función "analizar_paquetes"
      analizar_paquetes(captura, direccion_ip, puerto_usuario)
   except Exception as error_impresion:
       print (f"Error al imprimir el contenido por pantalla: {error_impresion}")

       
