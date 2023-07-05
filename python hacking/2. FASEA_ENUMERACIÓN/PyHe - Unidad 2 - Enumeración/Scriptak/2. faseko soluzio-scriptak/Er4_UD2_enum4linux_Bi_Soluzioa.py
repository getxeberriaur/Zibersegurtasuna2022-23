#****************************************************************************************************
#Curso "Python para hacking ético" Tknika 2022/2023
#RESUMEN DEL SCRIPT: 
#El usuario introduce una dirección IP. Imprime por pantalla información sobre el sistema operativo
#***************************************************************************************************
#Utilizamos la librería subprocess se utiliza para ejecutar comandos externos y obtener su salida
import subprocess
#Esta librería proporciona clases y funciones para manipular direcciones IP y redes
import ipaddress
#Usamos esta librería para trabajar con expresiones regulares
import re

#Esta función valida que la dirección proporcionada por el usuario es correcta.
#Retorna True si la dirección es válida y False en caso contrario.
def validar_direccion(direccion):
    try:
        ipaddress.ip_network(direccion)
        return True
    except ValueError:
        try:
            ipaddress.ip_address(direccion)
            return True
        except ValueError:
            return False

if __name__ == '__main__':
    #Solicitamos al usuario que introduzca una IP válida mientras el valor introducido no lo sea
    while True:
        direccion = input("Introduce la dirección del equipo cuyo sistema operativo deseas conocer: ")
        if validar_direccion(direccion):
            break
        else:
            print("La dirección introducida no es válida. Por favor, inténtalo de nuevo: ")
    try:
        #La función subbprocess.check_output() de la librería subprocessejecuta un comando en el sistema operativo y captura su salida.
        #En este caso, el comando que se ejecuta es 'enum4linux -a <direccion>'. 
        #El argumento text=True se utiliza para indicar que se desea obtener la salida del comando como una cadena de texto en
        #lugar de bytes. Esto nos permite trabajar con la salida como una cadena directamente.
        #La salida del comando se asigna a la variable stdout_texto, que contendrá el resultado de la ejecución de enum4linux.
        stdout_texto = subprocess.check_output(["enum4linux", direccion], text=True)
        
        # Extraemos información del sistema operativo de la ingente información que contiene la variable stdout_texto
        lineas = stdout_texto.strip().split('\n')
        hay_info_so=False
        #Recorremos las líneas de salida hasta que encontramos en una cadena "Got OS"; entonces, imprimimos la línea
        #posterior, que es la que recoge información sobre el sistema operativo. Usamos range para generar un iterable, ya que no se puede
        #iterar directamente sobre un entero. 
        for i in range(len(lineas)):
            if "Got OS" in lineas[i]:
                sistema_operativo = lineas[i+1].strip()
                hay_info_so=True
                break
        #Si no hemos obtenido información sobre el sistema operativo, informamos por pantalla de ello; si la hemos obtenido, la escribimos en
        #pantalla
        if not hay_info_so:
            print ("No se ha encontrado información sobre el sistema operativo")
        else: 
            print ("Información sobre el sistema operativo")
            print (sistema_operativo)
    except subprocess.CalledProcessError:
        print (f"No se ha podido obtener la información solicitada para la IP {direccion}")
