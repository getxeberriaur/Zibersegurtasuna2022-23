#***********************************************************************************************************************************************************
#Curso "Python para hacking ético" Tknika 2022/2023
#RESUMEN DEL SCRIPT: 
#El usuario introduce una direccióon IP y una lista de puertos; por cada puerto, realizará un escaneo para determinar si está abierto, cerrado, filtrado...
#***********************************************************************************************************************************************************
#La librería logging se utiliza para configurar los mensajes de registro en el script
import logging
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
            #*********************************************************************************************************************
            #  A partir de aquí, introduce el código que falta. En alguno de los ejercicios puede que sobre parte del código.
            # (◕‿−)Cambiar ??. Enviamos un paquete determinado al puerto de destino y esperamos 5 segundos para recibir una respuesta
            respuesta = sr1(IP(dst=ip_destino)/TCP(sport=puerto_origen, dport=int(puerto), flags="??"), timeout=5)
            # (◕‿−)Cambiar xxxx.Comprobamos si no recibimos ninguna respuesta, en cuyo caso damos el puerto por yyyyyy (cerrado, abierto....)
            if str(respuesta) == "None":
                print(puerto + ": Puerto yyyyyy")
                

            # Comprobamos si la respuesta recibida es un paquete TCP
            elif respuesta.haslayer(TCP):
          
            # (◕‿−)Cambiar ??. Comprobamos si se ha recibido un paquete de respuesta con el flag establecido en cierto valor
                if respuesta.getlayer(TCP).flags == 0x??:
                    # (◕‿−)Cambiar ??. Enviamos un paquete determinado para cerrar la conexión. Utilizamos para ello la función scapy, pasándole la capa IP, y la capa TCP (clases IP y TCP
                    # de la propia scapy). 
                    enviar_paquete = sr1(IP(dst=ip_destino)/TCP(sport=puerto_origen, dport=int(puerto), flags="??"), timeout=5)
                    #(◕‿−)Cambiar yyyyyy.El puerto está yyyyyy
                    print(puerto + ": Puerto yyyyyy")
                # (◕‿−)Cambiar las ?? + yyyyyy. Comprobamos si se ha recibido un paquete de respuesta con el flag establecido con cierto valor, en cuyo
                # caso el puerto está yyyyyy.
                elif respuesta.getlayer(TCP).flags == 0x??:
                    print(puerto + ": Puerto yyyyyy")
                else:
                    print ("Error. (◕‿−)ESCRIBIR ERROR")
            else:
                print ("Error. La respuesta recibida no es un paquete TCP")
    except ValueError:
        print ("Ha ocurrido un error inesperado")
exit()
