#***************************************************************************************************************************
#Curso "Python para hacking ético" Tknika 2022/2023
#RESUMEN DEL SCRIPT: 
#El usuario introduce un dominio por teclado; si es correcto, realizamos una consulta WHOIS a ese dominio, imprimiendo sólo 
#la información que nos interesa. Para ello, jugamos con la variable consulta, un objeto de la clase "Domain" de whois. 
#***************************************************************************************************************************
#La librería whois permite obtener información de WHOIS de un dominio, incluyendo detalles sobre el registrador del dominio,
#la fecha de creación y expiración del dominio, y los contactos administrativos y técnicos asociados con el dominio
import whois
#Librería para la gestión de sockets
import socket
#Librería para trabajar con expresiones regulares
import re

# Función para comprobar si el nombre de dominio es correcto, y, si lo es, si existe
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
dominio_valido=False        
while not dominio_valido:
    dominio = input ("Introduce un dominio válido: ")
    if validar_dominio (dominio):
        try:
            # Realizamos la consulta al servidor WHOIS y almacenamos la información en la variable 'consulta'
            consulta = whois.query(dominio)
            # Mostramos información general del dominio
            print("[+] Información general del dominio %s:\n" % dominio)
            if consulta.name is not None:
                print("  - Nombre: %s" % consulta.name)
            if consulta.registrar is not None:
                print("  - Registrador: %s" % consulta.registrar)
            if consulta.creation_date is not None:
                print("  - Fecha de registro: %s" % consulta.creation_date)
            if consulta.expiration_date is not None:
                print("  - Fecha de caducidad: %s" % consulta.expiration_date)
            if consulta.last_updated is not None:
                print("  - Última actualización: %s" % consulta.last_updated)
            #*********************************************************************************  
            #(◕‿−)INTRODUCIR AQUÍ un bucle for para iterar sobre la lista de servidores de nombres del dominio
            #y mostramos cada uno de ellos en la salida del programa.
            if len(consulta.name_servers) == 0:
                print ("La lista de servidores está vacía")
            else:
                print ("Lista de servidores:")
                for ns in consulta.name_servers:
                    print("    - %s" % ns)
            #
            #************************************************************************
            dominio_valido=True
        except:
            print("El dominio introducido existe, pero no se encontró información sobre él relacionada con WHOIS.")

    else:
        print ("El dominio introducido no existe o es incorrecto")
exit()

