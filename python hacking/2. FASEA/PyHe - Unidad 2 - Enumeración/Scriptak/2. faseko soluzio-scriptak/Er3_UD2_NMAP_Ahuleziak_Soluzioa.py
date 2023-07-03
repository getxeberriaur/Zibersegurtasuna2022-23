#****************************************************************************************************************************************
#Curso "Python para hacking ético" Tknika 2022/2023
#RESUMEN DEL SCRIPT: 
#El usuario introduce una dirección IP, dirección de red o dominio por teclado. Además, introduce uno o varios puertos (rangos aceptados)
#Obtenemos un listado con las vulnerabilidades de cada puerto abierto de cada IP solicitada. 
#****************************************************************************************************************************************
# Importamos la librería nmap, que proporciona una interfaz para interactuar con la herramienta de escaneo de puertos Nmap.
import nmap
# Librería para trabajar con expresiones regulares. La usaremos para comprobar que el dominio introducido es correcto
import re
# Librería para trabajar con direcciones IP y de red
import ipaddress
# Librería para trabajar con sockets
import socket

# Clase que representa un Host escaneado por Nmap
class NmapHost:
    def __init__(self):
        self.host = None                # Dirección IP del host
        self.estado = None              # Estado del host (up o down)
        self.razon = None               # Motivo del estado del host
        self.puertosAbiertos = []             # Lista de puertos abiertos
        self.puertosCerradosFiltrados = []   # Lista de puertos cerrados o filtrados
        self.so = None                  # Sistema operativo del host
        
 
# Clase que representa un puerto escaneado por Nmap
class NmapPuerto:
    def __init__(self):
        self.id = None                  # ID del puerto
        self.estado = None               # Estado del puerto (abierto, cerrado, filtrado, etc.)
        self.razon = None              # Motivo del estado del puerto
        self.puerto = None                # Número del puerto
        self.nombre = None                # Nombre del servicio asociado al puerto
        self.version = None             # Versión del servicio asociado al puerto
        self.scriptOutput = None        # Resultado de la ejecución de scripts de Nmap

# Función que procesa los resultados del escaneo de puertos de Nmap, dándoles un formato acorde a las clases que hemos creado
# Devuelve una lista con los datos de los hosts formateados.
def formateoNmapScan(scan):
    nmapHosts = []                      # Lista de hosts escaneados
    for host in scan.all_hosts():       # Recorremos todos los hosts escaneados
        nmapHost = NmapHost()           # Creamos una instancia de la clase NmapHost para el host actual
        nmapHost.host = host            # Asignamos la dirección IP del host a la instancia
        if 'status' in scan[host]:      # Verificamos si el estado del host está presente en los resultados del escaneo
            nmapHost.estado = scan[host]['status']['state']       # Asignamos el estado del host a la instancia
            nmapHost.razon = scan[host]['status']['reason']       # Asignamos el motivo del estado del host a la instancia
            for protocol in ["tcp", "udp", "icmp"]:               # Recorremos los protocolos encontrados en el escaneo (TCP, UDP, ICMP)
                if protocol in scan[host]:                        # Verificamos si el protocolo está presente en los resultados del escaneo
                    ports = scan[host][protocol].keys()            # Obtenemos la lista de puertos escaneados para el protocolo actual
                    for port in ports:                            # Recorremos todos los puertos escaneados para el protocolo actual
                        nmapPuerto = NmapPuerto()                      # Creamos una instancia de la clase NmapPort para el puerto actual
                        nmapPuerto.puerto = port                        # Asignamos el número del puerto a la instancia
                        nmapPuerto.nombre = scan[host][protocol][port]['name'] # Asignamos el nombre del servicio a la instancia
                        nmapPuerto.version = scan[host][protocol][port]['version'] # Asignamos la versión del servicio a la instancia
                        nmapPuerto.estado = scan[host][protocol][port]['state'] # Asignamos el estado del puerto a la instancia
                        nmapPuerto.os = scan[host]['osfingerprint'] if 'osfingerprint' in scan[host] else 'Sistema operativo no detectado'
                        nmapPuerto.os = scan[host]['osmatch'][0]['osclass'][0]['osfamily'] if 'osmatch' in scan[host] and len(scan[host]['osmatch']) > 0 else None
                        if 'script' in scan[host][protocol][port]:                # Verificamos si se ejecutaron scripts de Nmap para el puerto actual
                            nmapPuerto.scriptOutput = scan[host][protocol][port]['script']
                        if nmapPuerto.estado == 'open':
                            nmapHost.puertosAbiertos.append(nmapPuerto)
                        elif nmapPuerto.estado == 'closed' or nmapPuerto.estado == 'filtered':
                            nmapHost.puertosCerradosFiltrados.append(nmapPuerto)
            #Añadimos una entrada a la lista de hosts
            nmapHosts.append(nmapHost)
    #Devolvemos la lista
    nmapHosts.sort(key=lambda x: x.host)
    return nmapHosts


#Función para validar si el dato introducido es una IP correcta
def validar_ip(ip):
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False

#Función para validar si el dato introducido es una dirección de red correcta
def validar_dir_red (net_address):
    try:
        ipaddress.ip_network(net_address)
        return True
    except ValueError:
        return False

#Función para validar si el dato introducido es un dominio correcto
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

#Función que recibe una lista de vulnerabilidades e imprime la información más importante referente a ellas
def escribir_vulnerabilidades(listado_vuln):
  #Escribimos en el archivo la información inicial, la relativa a la aplicación
    archivo_salida.write ("A continuación, vulnerabilidades relativas a: "+ listado_vuln[0]+"\n")
    archivo_salida.write ("********************************************************************************\n")
    #Una vez imprimida, eliminamos la información sobre la aplicación en cuestión
    listado_vuln.pop(0)
    #Recorremos las vulnerabilidades encontradas
    for vulnerabilidad in listado_vuln:
        #Dividimos cada elemento de la lista por el carácter '\t', resultando una lista 'datos' que 
        datos= vulnerabilidad.split('\t')
        archivo_salida.write ("Vulnerabilidad: " +datos[1]+ "\n")
        archivo_salida.write ("Gravedad: " +datos[2]+ "\n")
        archivo_salida.write ("Enlace: " +datos[3]+ "\n")
        archivo_salida.write ("-----------------------------------------------------------------------------\n")
 


#Función para comprobar si los puertos introducidos por el usuario son correctos.
#Ejemplos de valores que dará por buenos: 1-80---- 1-80, 443-800----53,80,123,445,8006
def validar_puertos(puertos):
    puertos_validos=False
    #Dividimos la cadena partes en diferentes parrtes utilizando la coma como separador.
    partes = puertos.split(",")
    #Iteramos por cada uno de los rangos introducidos
    for parte in partes:
        #Si hay un guion, dividimos la parte en dos subpartes: inicio y fin.
        if "-" in parte:
            inicio, fin = parte.split("-")
            #Validamos que ambas partes sean dígitos 
            if not inicio.isdigit() or not fin.isdigit():
                puertos_validos=False
            #Además, verificamos que el valor de inicio sea menor o igual que el valor de fin.
            #También que tanto el inicio como el fin están dentro del rango válido de 1 a 65535. 
            elif int(inicio) > int(fin) or int(inicio) < 1 or int(fin) > 65535:
                puertos_validos=False
            else:
                puertos_validos=True    
        #Si no hay un guion, comprobamos que es un número entre 1 y 65535
        elif not parte.isdigit() or int(parte) < 1 or int(parte) > 65535:
            puertos_validos=False
        #En cualquier oo, caso
        else:
            puertos_validos=True
    #Devolvemos el último valor de la variable puertos_validos al final de la iteración
    return puertos_validos


if __name__ == '__main__':
    #Pedimos al usuario que introduzca una IP, dirección de red o dominio sobre los que realizar el escaneo.
    #Comprobamos si lo que introduce es una IP, dirección de red y dominio válido. Mientras no lo sea, se lo
    #seguimos pidiendo
    dir_ok=False
    while not dir_ok:
        destino = input("Introduce una IP, dirección de red (formato CIDR) o dominio: ")
        if validar_ip(destino):
            dir_ok=True
        elif validar_dir_red(destino):
            dir_ok=True
        elif validar_dominio(destino):
            dir_ok=True
        else:
            print(f"{destino} no es una IP, dirección de red o dominio válido.")

    puertos_ok=False        
    while not puertos_ok:
        try:
            puertos_destino = input("Introduce la lista de puertos separados por ',' (ejemplo: 80,443,8080) o un rango de puertos (ejemplo: 80-200): ")
            if validar_puertos(puertos_destino):
                puertos_destino = puertos_destino.replace(" ", "")
                puertos_ok=True
            else:
                print ("Error al introducir los puertos")
        except ValueError:
            print("Error inesperado")
    
    try:  
        #Creamos una instancia de la clase PortScanner del módulo nmap. Esta instancia se utiliza posteriormente para realizar el escaneo de puertos en el host de destino.
        #PortScanner es una clase en este módulo que permite realizar escaneos de puertos en hosts remotos.
        #Al crear una instancia de PortScanner estamos preparando un objeto que se utilizará para realizar operaciones de escaneo de puertos en el host objetivo       
        #utilizando la biblioteca nmap.
        nm = nmap.PortScanner()
        # Escaneamos el host destino, en el rango de puertos introducido por el usuario, con argumentos adicionales para obtener información
        #detallada de cada puerto.
        # '-sV' indica que se realice detección de versiones de servicios.
        # '-n' indica que no se realice resolución de DNS inversa
        # '-T5' indica que se utilice el nivel de agresividad 5 (mayor velocidad pero más ruido en la red)
        # '--script vulners': ejecutará el script 'vulners' del NSE
        nm.scan(destino, puertos_destino, arguments="--script vulners -sV -n -T5")  
        #Creamos una lista que contenga los datos formateados que nos devuelve la función formateoNmapscan. La ordenamos por IP
        estructuraNmap = formateoNmapScan(nm)
        estructuraNmap.sort(key=lambda x: x.host)
        print("Guardando los datos en el fichero 'resultados_vulnerabilidades.txt'...")
        archivo_salida = open("resultados_vulnerabilidades.txt", "w")
        #Tratamos cada host guardado en la lista
        for host in estructuraNmap:
            #Escribimos la dirección IP escaneada
            archivo_salida.write("                                   " + "\n")
            archivo_salida.write("Host:" + host.host + "\n")
            archivo_salida.write("-----------------------------------" + "\n")
            #Dentro de cada host, tratamos uno por uno cada puerto
            for puertoOpen in host.puertosAbiertos:
                #Escribimos el número del puerto, el nombre del servicio y la versión del servicio
                archivo_salida.write("Puerto: " + str(puertoOpen.puerto)+'  Servicio: '+puertoOpen.nombre+'   Versión: '+puertoOpen.version+"\n")
                if puertoOpen.scriptOutput is not None: 
                    #Creamos una lista a partir de la clave 'vulners' del diccionario generado como salida del script ejecutado. Le quitamos los espacios a la lista y
                    #la dividimos en elementos que separamos por el carácter \n
                    lista_vulnerabilidades=puertoOpen.scriptOutput['vulners'].strip().split('\n')
                    #Llamamos a la función escribir_vulnerabilidades
                    escribir_vulnerabilidades(lista_vulnerabilidades)
        archivo_salida.close()
            
    except ValueError:
        print ("Error inesperado")
exit()
             





   
        
