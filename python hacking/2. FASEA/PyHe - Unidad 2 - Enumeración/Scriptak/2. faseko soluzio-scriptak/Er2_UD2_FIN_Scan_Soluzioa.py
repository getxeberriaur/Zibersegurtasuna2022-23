#************************************************************************************************************************************************************
#Curso "Python para hacking ético" Tknika 2022/2023
#RESUMEN DEL SCRIPT: 
#El usuario introduce una direccióon IP y una lista de puertos; por cada puerto, realizaremos un FIN Scan, y se nos mostrá si está abierto-filtrado o cerrado
#************************************************************************************************************************************************************
#La librería logging se utiliza para configurar los mensajes de registro en el script
#import logging
#Scapy es una biblioteca de manipulación y generación de paquetes de red,y se utiliza en este script para enviar y recibir paquetes.
#Importamos todas las clases y funciones disponibles en el módulo all dentro del paquete Scapy. El módulo all contiene una selección de las clases y funciones más comunes y utilizadas de Scapy.
#Al usar *, todas las clases y funciones se importan directamente en el espacio de nombres actual, lo que significa que se pueden acceder directamente sin necesidad de utilizar el prefijo scapy.
from scapy.all import *

import ipaddress

# Establecemos el nivel de registro de errores en Scapy a "ERROR", que es el nivel más bajo y sólo muestra mensajes de error (no warnings ni otra información)
# Dejamos comentado la línea. Es importante conocerla, pero muestra mucha información que dificulta la visualización en salida. 
#logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

#Establecemos el Verbose de scapy a 0, con lo cual no muestra nada en salida. Si queremos que se muestre información, habrá que comentar esta línea y decomentar la de encima
conf.verb=0

#Función para comprobar si los puertos introducidos por el usuario son correctos. Deben estar separados por una coma
def validar_puertos(puertos):
    patron = r"^\d+(?:,\d+)*$"
    if re.match(patron, puertos):
        return True
    else:
        return False


if __name__ == "__main__":   
    ip_valida = False
    while not ip_valida:
        try:
            ip_destino = input('Introduce una dirección IP válida: ')
            ipaddress.ip_address(ip_destino)
            ip_valida = True
        except ValueError:
            print ('La IP introducida no es correcta')
    puertos_ok=False
    while not puertos_ok:
        try:
            puertos_destino = input("Introduce la lista de puertos separados por ',' (ejemplo: 80,443,8080): ")
            if validar_puertos(puertos_destino):
                #Quitamos posibles espacios 
                puertos_destino = puertos_destino.replace(" ", "")
                #puertos pasa a ser una lista con todos los puertos introducidos por el usuario
                puertos_destino = puertos_destino.strip().split(',')
                puertos_ok=True
            else:
                print ("Error al introducir los puertos")
        except ValueError:
            print("Error inesperado") 

    try:    
        # Generamos un número de puerto de origen aleatorio
        puerto_origen = RandShort()
    
        # Iteramos por cada puerto a escanear
        for puerto in puertos_destino:

            # Enviamos un paquete ACK al puerto de destino y esperamos 5 segundos para recibir una respuesta
            respuesta = sr1(IP(dst=ip_destino)/TCP(sport=puerto_origen, dport=int(puerto), flags="F"), timeout=10)
            # Comprobamos si no recibimos ninguna respuesta, en cuyo caso damos el puerto por cerrado
            if str(respuesta) == "None":
                print(puerto + ": Indeterminado. Puerto abierto o filtrado")

            #************************************
            #VALOR FLAGS. DECIMAL Y HEXADECIMAL *
            #FIN: Decimal: 1  Hexadecimal:  0x01*
            #SYN: Decimal: 2  Hexadecimal:  0x02*
            #RST: Decimal: 4  Hexadecimal:  0x04*
            #PSH: Decimal: 8  Hexadecimal:  0x08*
            #ACK: Decimal: 16 Hexadecimal:  0x10*
            #URG: Decimal: 32 Hexadecimal:  0x20*
            #************************************
            # Comprobamos si la respuesta recibida es un paquete TCP
            elif respuesta.haslayer(TCP):
                # Comprobamos si se ha recibido un paquete de respuesta con el flag establecido en 0x14 (RST--0x10--+ACK--0x04--) activado, en cuyo
                # caso el puerto está cerrado
                if respuesta.getlayer(TCP).flags == 0x14:
                    print(puerto + ": Puerto cerrado")
                else:
                    print ("Error. No se puede determinar si el puerto está filtrado o no")
            else:
                print ("Error. No se puede determinar si el puerto está filtrado o no")
    except ValueError:
        print ("Error inesperado. Fin de la ejecución")


