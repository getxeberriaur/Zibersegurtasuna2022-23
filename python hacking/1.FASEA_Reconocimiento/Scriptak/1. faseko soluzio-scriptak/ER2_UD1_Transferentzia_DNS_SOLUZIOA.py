#***************************************************************************************************************************
#Curso "Python para hacking ético" Tknika 2022/2023
#RESUMEN DEL SCRIPT: 
#El usuario introduce una IP y un nombre de dominio por teclado; si es correcto, solicitamos una transferencia de zona al  
#servidor DNS correspondiente, imprimiendo 
#***************************************************************************************************************************
#Esta librería proporciona herramientas para trabajar con zonas DNS. Permite leer y manipular archivos de zona DNS.
import dns.zone
#Esta librería proporciona funcionalidad para enviar consultas DNS a servidores DNS y recibir respuestas
import dns.query
#Esta librería contiene excepciones específicas relacionadas con consultas DNS y operaciones relacionadas.
import dns.exception
#Esta librería proporciona clases y funciones para manipular direcciones IP y redes
import ipaddress
#Librería para trabajar con expresiones regulares
import re

# Función para comprobar si el nombre de dominio es correcto
def validar_dominio (dom):
    #No comienza por guion, tiene caracteres válidos, la longitud máxima es 63, el TLD es válido
    patron_dom = r"^(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.[A-Za-z]{2,})+$"
    if not re.match(patron_dom,dom):
        return False
    else:
        return True

#Pedimos al usuario la IP y el dominio, y los validamos.
ip_valida = False
while not ip_valida:
    try:
        ip = input("Introduce la dirección IP del servidor DNS: ")
        ipaddress.ip_address(ip)
        ip_valida = True
    except ValueError:
        print ("IP no válida")
dominio_valido=False 
while not dominio_valido:
    dominio = input('Introduce el nombre de dominio a consultar: ')
    if validar_dominio(dominio):
        dominio_valido=True
    else:
        print ("El dominio introducido no es correcto")
    
#####################################################################
#Realizaremos una transferencia de zona (zone transfer) desde el servidor DNS primario del dominio introducido por el
#usuario. Una transferencia de zona es un mecanismo de replicación de información entre servidores DNS que permite copiar
#todos los registros de recursos (RR) de un dominio desde un servidor DNS a otro.
#------------------------------------------------------------------------
#   La función dns.query.xfr() realiza una consulta de transferencia de zona al servidor primario especificado y devuelve una
#   secuencia de registros de recursos que contienen la información de la zona solicitada. El primer argumento es la dirección
#   IP del servidor primario y el segundo argumento es el nombre de dominio a transferir.
#---------------------------------------------------
#   La función dns.zone.from_xfr() crea un objeto de la clase Zone del módulo dns.zone (es decir, un objeto dns.zone.Zone)
#   a partir de los registros de recursos devueltos por la consulta de transferencia de zona.
#   El objeto Zone resultante contiene toda la información de la zona y se puede usar para manipular y acceder a los
#   registros de recursos en el dominio transferido.

try:
    zone = dns.zone.from_xfr(dns.query.xfr(ip, dominio))
    print("Datos de la transferencia de zona para el dominio:", zone.origin)
    for name, node in zone.nodes.items():
        print(name)
        for rdataset in node.rdatasets:
            print(rdataset)

except dns.exception.SyntaxError:
    print("Error de sintaxis en la zona DNS.")
except dns.exception.FormError:
    print("Error de formato en la respuesta del servidor DNS.")
except dns.zone.NoNS:
    print(f"No se encontró ningún registro NS para el dominio {dominio}.")
except dns.query.TransferError as e:
    print(f"Error de transferencia de zona DNS: {str(e)}")
except dns.query.BadResponse:
    print("Respuesta inesperada del servidor DNS.")
except dns.exception.Timeout:
    print("Timeout al esperar la respuesta del servidor DNS.")
except Exception as e:
    print(f"Error desconocido: {str(e)}")
