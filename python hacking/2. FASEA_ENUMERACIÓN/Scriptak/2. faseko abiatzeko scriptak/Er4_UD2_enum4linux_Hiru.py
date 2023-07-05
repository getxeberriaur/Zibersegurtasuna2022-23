#************************************************************************************************************
#Curso "Python para hacking ético" Tknika 2022/2023
#RESUMEN DEL SCRIPT: 
#El usuario introduce una dirección IP. Guarda en un fichero un listado con todos los usuarios del sistema. 
#***********************************************************************************************************
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
    #(◕‿−)INTRODUCIR AQUÍ el código del cuerpo del script

    #Solicitamos al usuario que introduzca una IP, dirección de red o nombre de equipo válido mientras el valor introducido
    #no lo sea
    
    #La función subbprocess.check_output() de la librería subprocessejecuta un comando en el sistema operativo y captura su salida.
    #En este caso, el comando que se ejecuta es 'enum4linux -a <direccion>'. 
    #El argumento text=True se utiliza para indicar que se desea obtener la salida del comando como una cadena de texto en
    #lugar de bytes. Esto nos permite trabajar con la salida como una cadena directamente.
    #La salida del comando se asigna a la variable stdout_texto, que contendrá el resultado de la ejecución de enum4linux.


    
    #Extraemos sólo nombres de usuario de la ingente información que contiene la variable stdout_texto, dejando el resultado en
    #una lista de strings. Utilizamos la función re.findall para ello, utilizando como patrón
    #de búsqueda el siguiente: r'user:\[(\w+)\] rid:'}
    
    #Abrimos un nuevo fichero en modo escritura
    
    #Escribimos el texto "Nombres de usuario" como cabecera
    
    #Escribimos todos los nombres de usuario que encontremos. Para ello, debemos recorrer los elementos de la
    #lista nombre_usuarios
    
    #Cerramos el fichero
  
