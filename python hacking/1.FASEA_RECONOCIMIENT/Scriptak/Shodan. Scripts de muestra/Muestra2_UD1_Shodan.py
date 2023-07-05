#********************************************************************************************
#Curso "Python para hacking ético" Tknika 2022/2023
#RESUMEN DEL SCRIPT: 
#Se realiza una búsqueda completa sobre un destino (dominio o IP) introducido por el usuario
#********************************************************************************************
#Importamos las librerías "shodan" y "socket"
import shodan
import socket
import re

# Credenciales de la API de Shodan
# (◕‿−)Cambia "xxxxxxxxxxxxxxxx" por tu API_KEY
SHODAN_API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxx"
api = shodan.Shodan(SHODAN_API_KEY)

# Función para buscar información de un host
def busqueda_informacion(valor_destino):
    # Busca información del host en Shodan
    
    try:
        #Obtenemos la dirección IP asociada al valor introducido por el usuario. Si ya era una IP, no la convertirá
        ip_asociada=socket.gethostbyname(valor_destino)
        #La variable host contendrá un objeto de la API de Shodan
        host = api.host(ip_asociada)
        # Imprime información del host
        print(f"IP: {host['ip_str']}")
        print(f"Organización: {host.get('org', 'N/A')}")
        print(f"Sistema operativo: {host.get('os', 'N/A')}")
        print(f"Países: {', '.join(host.get('countries', []))}")
        # Imprime información de los puertos abiertos
        print("Puertos abiertos:")
        for servicio in host['data']:
            print(f"- {servicio['port']}/{servicio['transport']} - {servicio.get('product', 'unknown')} {servicio.get('version', 'unknown')}")
        
        # Imprime información sobre vulnerabilidades
        if 'vulns' in host and len(host['vulns']) > 0:
            print("Vulnerabilidades:")
            for vulnerabilidad in host['vulns']:
                print(f"Vulnerabilidad: {vulnerabilidad}")
        else:
            print ("No se han detectado vulnerabilidades conocidas")
    except shodan.APIError as e:
        print("Error al hacer la consulta a Shodan:", e)
    exit()
#Función para comprobar si una ip es válida
def validar_ip(ip):
    patron_ip = r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
    if re.match(patron_ip, ip):
        return True
    else:
        return False

    
#Función para comprobar si un dominio es válido
def validar_dominio (dom):
    #No comienza por guion, tiene caracteres válidos, la longitud máxima es 63, el TLD es válido
    patron_dom = r"^(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.[A-Za-z]{2,})+$"
    if not re.match(patron_dom,dom):
        return False
    try:
        socket.gethostbyname(dom)
        return True
    except socket.error:
        return False



if __name__ == '__main__':
    #Pedimos al usuario que introduzca una IP o dominio sobre los que realizar la búsqueda
    #Comprobamos si lo que introduce es una IP o un dominio válido. Mientras no lo sea, se lo
    #seguimos pidiendo
    entrada_ok=False
    while not entrada_ok:
        destino = input("Introduce una IP o dominio: ")
        if validar_ip(destino):
            entrada_ok=True
        elif validar_dominio(destino):
            entrada_ok=True
        else:
            print(f"{destino} no es una IP o dominio válido.")   
    busqueda_informacion(destino)
