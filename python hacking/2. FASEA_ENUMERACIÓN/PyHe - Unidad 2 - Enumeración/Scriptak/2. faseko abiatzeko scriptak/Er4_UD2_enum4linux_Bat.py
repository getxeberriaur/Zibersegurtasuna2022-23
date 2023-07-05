#******************************************************************************************************************
#Curso "Python para hacking ético" Tknika 2022/2023
#RESUMEN DEL SCRIPT: 
#El usuario introduce una dirección IP. Imprime por pantalla la política de contraseñas del equipo correspondiente.
#******************************************************************************************************************
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
        return False

if __name__ == '__main__':
    #Solicitamos al usuario que introduzca una IP, dirección de red o nombre de equipo válido mientras el valor introducido
    #no lo sea
    direccion_ok=False
    while not direccion_ok:
        direccion = input("Introduce la dirección del equipo cuyos usuarios deseas conocer: ")
        if validar_direccion(direccion):
            direccion_ok=True
        else:
            print("La dirección introducida no es válida. Por favor, inténtalo de nuevo.")
    try:
        #La función subbprocess.check_output() de la librería subprocessejecuta un comando en el sistema operativo y captura su salida.
        #En este caso, el comando que se ejecuta es 'enum4linux -a <direccion>'. 
        #El argumento text=True se utiliza para indicar que se desea obtener la salida del comando como una cadena de texto en
        #lugar de bytes. Esto nos permite trabajar con la salida como una cadena directamente.
        #La salida del comando se asigna a la variable stdout_texto, que contendrá el resultado de la ejecución de enum4linux.
        stdout_texto = subprocess.check_output(["enum4linux", "-a", direccion], text=True)
        # Extraemos la política de complejidad de las contraseñas de la ingente información que contiene la variable stdout_texto
        #(◕‿−)ICambiar XXXXXXX
        informacion_complejidad = re.findall(r'Password Complexity: (.+)', XXXXXXX)
       
        #********************************************************
        #Escribimos el texto "Información sobre la política de complejidad de la password:" como cabecera
        #Escribimos la línea con informaciómn obtenida
        #(◕‿−)INTRODUCIR AQUÍ el código correspondiente a las líneas de encima




        #************************
    except subprocess.CalledProcessError:
        print (f"No se ha podido obtener la información solicitada para la IP {direccion}")
