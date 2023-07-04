#***************************************************************
#Curso "Python para hacking ético" Tknika 2022/2023
#RESUMEN DEL SCRIPT: 
#Se realizan dos búsquedas de muestra utilizando varios flitros
#**************************************************************

import shodan

# Credenciales de la API de Shodan
# (◕‿−)Cambia "xxxxxxxxxxxxxxxx" por tu API_KEY
SHODAN_API_KEY = "xxxxxxxxxxxxxxxxxxx"

# Inicializar la API de Shodan

api = shodan.Shodan(SHODAN_API_KEY)

# Definir los filtros de búsqueda (en este caso se buscan dispositivos con el puerto 22 abierto y que contengan "OpenSSH" en el banner)
consulta = 'port:22 "OpenSSH"'

# Realizar la búsqueda y guardar los resultados en una variable
try:
    resultados_busqueda = api.search(consulta)
    # Imprimir el número de resultados encontrados
    print ("Listado de IPs con puerto ssh abierto y OpenSSH en marcha:")
    print ("**********************************************************")
    print(f"Se encontraron {len(resultados_busqueda['matches'])} resultados:")
    # Iterar sobre los resultados e imprimimos la IP
    for resultado in resultados_busqueda['matches']:
        print(f"IP: {resultado['ip_str']}")
    print ("###Fin del listado###")       
     

except shodan.APIError as e:
    print('Error al realizar la búsqueda: ', e)

# Ejemplo de búsqueda con múltiples filtros
try:
    #Definir los filtros de búsqueda (en este caso se buscan dispositivos Windows con el puerto 3389 abierto, y con
    #capturas de pantalla disponibles)
    consulta = 'port:3389 os:"Windows" has_screenshot:true'
    # Realizar la búsqueda y guardar los resultados en una variable
    resultados_busqueda = api.search(consulta)
    # Imprimir el número de resultados encontrados  
    print ("Listado de IPs de dispositivos Windows con capturas de pantalla disponibles :")
    print ("*****************************************************************************")
    print(f"Se encontraron {len(resultados_busqueda['matches'])} resultados:")
    # Iterar sobre los resultados e imprimir información relevante de cada dispositivo encontrado
    for resultado in resultados_busqueda['matches']:
        print(f"IP: {resultado['ip_str']}")
        print(f"Hostnames: {resultado['hostnames']}")
        print(f"Organización: {resultado['org']}")
    print ("###Fin del listado###")       
except shodan.APIError as e:
    print('Error al realizar la búsqueda: ', e)






