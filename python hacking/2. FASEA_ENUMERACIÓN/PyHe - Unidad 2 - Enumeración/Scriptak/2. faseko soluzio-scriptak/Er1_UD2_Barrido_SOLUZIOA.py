#******************************************************************************************************************************
#Curso "Python para hacking ético" Tknika 2022/2023
#RESUMEN DEL SCRIPT: 
#El usuario introduce una dirección de red por teclado. Posteriormente, elige entre hacer un barrido ARP o barrido PING en ella.
#*******************************************************************************************************************************
# Librería para ejecutar comandos del sistema operativo
import os
# Librería para validar y manejar direcciones IP y de red
import ipaddress
# Proporciona una forma  de solicitar una contraseña al usuario . En este código, se utiliza para solicitar la contraseña
# del usuario antes de ejecutar comandos que requieran permisos de superusuario.
import getpass
#Librería para trabajar con expresiones regulares
import re

#Esta función valida que la dirección proporcionada por el usuario es correcta.
#Retorna True si la dirección es válida y False en caso contrario.
def validar_direccion(direccion):
    # Expresión regular para validar una dirección de red en formato xxx.xxx.xxx.xxx/xx
    patron = r'^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2})$'
    # Si la dirección coincide con el patrón, se trata de una IP válida
    if re.match(patron, direccion):
        return True
    else:
        return False

if __name__ == '__main__':
    direccion_valida = False
    #Mientras la dirección introducida no sea válida, se la seguimos pidiendo al usuario 
    while not direccion_valida:
        direccion = input("Introduce una dirección de red (formato CIDR): ")
        if validar_direccion(direccion):     # Valida la dirección proporcionada por el usuario
            direccion_valida = True           # Si la dirección es válida, cambia la variable a True para salir del bucle
        else:
            print("La dirección introducida no es válida. Por favor, inténtelo de nuevo.")
    funcion = input("¿Qué tipo de barrido deseas realizar (P)ing o (A)rp?: ")
    #Mientras la opción elegida no sea válida (no es ni I A ni P), se la seguimos pidiendo al usuario
    while (funcion.lower() not in ["a", "p"]):
        funcion = input("Opción incorrecta. Introduce (P)ing) o (A)rp: ")
    #direccion_red será un objeto de la clase ipaddress.IPv4Network
    direccion_red = ipaddress.ip_network(direccion, strict=False)
    primera_iteracion=True
    # Itera por las direcciones IP de la red
    for direccion_ip in direccion_red.hosts():       
        # Si el usuario deasea hacer un barrido PING
        if  (funcion.lower() == "p"):
            # Ejecuta el comando ping para cada dirección IP. Si el ping ha sido exitoso, la dirección IP está activa. La imprimimos
            respuesta = os.system(f"ping -c 1 {direccion_ip}") 
            if respuesta == 0:
                print(f"La dirección IP {direccion_ip} está activa.")
        # Si no es un barrido PING, deseará hacer un barrido ARP
        else: 
            #Pedimos la contraseña al usuario sólo la primera vez
            if primera_iteracion:
                password = getpass.getpass("Esta operación requiere permisos de superusuario. Introduce la contraseña del usuario kali: ")
                primera_iteracion=False
            # Ejecuta el comando arping para cada dirección IP. Si el arping ha sido exitoso, la dirección IP está activa. La imprimimos
            respuesta = os.system(f"echo {password} | sudo -S arping -c 1 {direccion_ip}")
            if respuesta == 0:
                print(f"La dirección IP {direccion_ip} está activa.")
                   
