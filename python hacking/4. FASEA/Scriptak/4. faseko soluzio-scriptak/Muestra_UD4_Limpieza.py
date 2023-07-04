#******************************************************************************************************************
#Curso "Python para hacking ético" Tknika 2022/2023
#RESUMEN DEL SCRIPT:
#Se trata de un script genérico que serviría para realizar tareas básicas de
#limpieza en un sistema GNU/Linux 
#*******************************************************************************
import os
import datetime
#librería que proporciona funciones para trabajar con la base de datos de contraseñas del sistema.
import pwd
import pam

# Función para eliminar archivos potencialmente maliciosos en un directorio y subdirectorios
#
def eliminar_archivos_maliciosos(directorio, fecha_limite):
    #Utilizamos os.walk para recorrer el directorio y sus subdirectorios
    print (f"Borrando archivos del directorio {directorio}")
    for ruta, dirs, ficheros in os.walk(directorio):
        for fichero in ficheros:
                ruta_archivo = os.path.join(ruta, fichero)
                if os.path.exists(ruta_archivo):
                    fecha_creacion = datetime.datetime.fromtimestamp(os.path.getctime(ruta_archivo)).date()
                    if fecha_creacion >= fecha_limite and (fichero.endswith('.exe') or fichero.endswith('.py')):
                        print(f"Eliminando archivo malicioso: {ruta_archivo}")
                        os.remove(ruta_archivo)

# Función para borrar el historial de comandos del usuario actual
def borrar_historial():
    print ("Borrando el historial")
    
    if os.path.exists('/etc/os-release'):
        with open('/etc/os-release') as f:
            content = f.read()
            if 'kali' in content.lower():
               os.system("rm ~/.zsh_history && touch ~/.zsh_history")     

    #Eliminamos el archivo de historial de comandos existente y lo volvemos a crear vacío
    os.system("rm ~/.bash_history && touch ~/.bash_history")     
        
    
# Función para desinstalar software no deseado
def desinstalar_software_no_deseado(software):
    for programa in software:
        print(f"Desinstalando: {programa}")
        os.system(f"apt-get purge {programa} -y")

# Función para limpiar registros de eventos
def limpiar_registros_eventos():
    print("Limpiando registros de eventos...")
    os.system("echo '' > /var/log/syslog")
    os.system("echo '' > /var/log/auth.log")
    # Agrega aquí otros registros de eventos que desees limpiar

def obtener_fecha_creacion_usuario(usuario):
    fecha_creacion = None
    try:
        fecha_creacion_str = os.popen(f"sudo passwd -S {usuario}").read().split()[2]
        fecha_creacion = datetime.datetime.strptime(fecha_creacion_str, "%Y-%m-%d").date()
    except Exception as e:
        print(f"No se pudo obtener la fecha de creación del usuario {usuario}: {str(e)}")
    return fecha_creacion

#Función para eliminar todos los usuarios creados a partir de la fecha introducida por el usuario
def eliminar_usuarios(fecha_limite):
    #Recuperamos todos los usuarios del sistema y dejarlos en la variable "usuarios", que es una lista de de objetos
    #"pwd.struct_passwd". 
    usuarios = pwd.getpwall()
    #Iteramos por la lista de usuarios
    for usuario in usuarios:
        nombre_usuario = usuario.pw_name
        try:
            fecha_creacion = obtener_fecha_creacion_usuario(nombre_usuario)
            if fecha_creacion and fecha_creacion >= fecha_limite:
                print(f"Eliminando usuario: {nombre_usuario}")
                os.system(f"userdel {nombre_usuario}")
        except Exception as e:
            print (f"Error {e}")
                
#Función para validar si la fecha introducida por el usuario es correcta
def validar_fecha(fecha):
    try:
        datetime.datetime.strptime(fecha, "%d-%m-%Y")
        return True
    except ValueError:
        return False
    
# Obtener la fecha que introduce el usuario como límite
fecha_correcta = False
while not fecha_correcta:
    fecha_usuario_str = input("Introduce la fecha límite (formato: dd-mm-yyyy): ")
    if validar_fecha(fecha_usuario_str):
        fecha_correcta=True        
fecha_usuario = datetime.datetime.strptime(fecha_usuario_str, '%d-%m-%Y').date()

# Función para eliminar tareas de cron
def eliminar_tareas_cron():
    os.system("crontab -r")

# Ejecutar la eliminación de archivos maliciosos en todo el sistema
eliminar_archivos_maliciosos("/home/kali/Escritorio/Ariketak/UD4zaborra", fecha_usuario)

# Ejecutar el borrado del historial
borrar_historial()

# Ejecutar la eliminación de usuarios
eliminar_usuarios(fecha_usuario)

# Ejecutar la desinstalación de software no deseado
#desinstalar_software_no_deseado(["nombre_software1", "nombre_software2"]) 

# Ejecutar la limpieza de registros de eventos
limpiar_registros_eventos()

# Ejecutar la eliminación de tareas de cron
eliminar_tareas_cron()


