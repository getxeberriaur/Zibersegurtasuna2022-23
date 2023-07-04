#***************************************************************************************************************************
#Curso "Python para hacking ético" Tknika 2022/2023
#RESUMEN DEL SCRIPT: 
#El usuario introduce un dominio por teclado; si es correcto, realizamos una consulta DNS a ese dominio, imprimiendo sólo 
#el valor de algunos de los registros más relevantes. 
#***************************************************************************************************************************

#La librería dns.resolver simplifica la interacción con los servidores DNS y ofrece métodos para realizar consultas
#y obtener respuestas estructuradas con la información solicitada. Proporciona una interfaz más amigable y de más alto
#nivel que la funcionalidad incorporada de la librería estándar socket de Python.
import dns.resolver
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
#Si el dominio es correcto, mostramos la información correspondiente a él
    dominio = input("Introduce un dominio: ")
    if validar_dominio(dominio):
    # Realizamos diferentes consultas a los registros del dominio introducido
        try:
            registroA = dns.resolver.resolve(dominio, 'A')
            registroNS = dns.resolver.resolve(dominio, 'NS')
            registroAAAA = dns.resolver.resolve(dominio, 'AAAA')
            registroMX = dns.resolver.resolve(dominio, 'MX')
            # Imprimimos la respuesta de cada consulta
            print(registroA.response.to_text())
            print(registroNS.response.to_text())
            print(registroAAAA.response.to_text())
            #*********************************************************************************  
            #(◕‿−)INTRODUCIR AQUÍ una instruccion para imprimir el contenido del registro MX
            #
            print(registroMX.response.to_text())
            #************************************************************************
        except dns.resolver.NoAnswer:
            print(f"No se encontró un registro completo para el dominio: {dominio}")
        dominio_valido=True
    else:
        print ("El dominio introducido no es correcto o no existe")
exit()
