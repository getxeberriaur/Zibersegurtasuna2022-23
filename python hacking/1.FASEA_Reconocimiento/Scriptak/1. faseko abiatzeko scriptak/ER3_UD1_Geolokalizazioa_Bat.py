#***************************************************************************************************************************
#Curso "Python para hacking ético" Tknika 2022/2023
#RESUMEN DEL SCRIPT: 
#El usuario introduce unas coordenadas, y obtenemos la ciudad que les corresponde.   
#***************************************************************************************************************************

#El módulo geocoders proporciona herramientas para geocodificación, es decir, para convertir una ubicación en coordenadas
#geográficas (latitud y longitud) y viceversa.
#La clase Nominatim es una implementación de un geocodificador que utiliza el servicio web Nominatim para buscar
#ubicaciones geográficas.
from geopy.geocoders import Nominatim


# Función que obtiene el nombre de la ciudad a partir de las coordenadas de latitud y longitud y
# lo devuelve como una cadena de texto
def obtener_ciudad(latit, longit):
    # Creamos una cadena de texto con las coordenadas introducidas
    geolocalizador = Nominatim(user_agent="python_hacking_tknika")
    localizacion_str = f"{latit}, {longit}"
    #Se utiliza el método reverse de la clase geolocator para obtener la información de la ubicación correspondiente a las
    #coordenadas especificadas.
    localizacion = geolocalizador.reverse(localizacion_str)
    #Si se ha obtenido la ubicación, la función devuelve la ciudad correspondiente a las coordenadas
    #Primero, accede al diccionario location.raw['address'] que contiene información detallada de la dirección encontrada en la
    #ubicación. Luego, utiliza el método get() para buscar el valor de la clave 'city' (ciudad) en el diccionario.
    #Si no se encuentra una clave 'city', busca la clave 'town' (pueblo), luego 'village' (aldea).
    #La función get() devuelve el valor de la clave buscada si se encuentra, y si no se encuentra, devuelve None.
    #Utilizando el operador or, el código verifica cada clave en orden y devuelve el primer valor que no sea None.
    #De esta forma, si la clave 'city' no existe en el diccionario, se intentará buscar la ciudad en las otras claves
    #mencionadas. Si ninguna de ellas existe, se devuelve None. Si no se encuentra la ubicación, se debe indicar por pantalla. 
    #************************************************************************
    if localizacion is not None:
        ciudad = localizacion.raw['address'].get('city', None) or localizacion.raw['address'].get('town', None) or localizacion.raw['address'].get('village', None)
        return ciudad
    else:
        return None

#****************************************************************
#(◕‿−)Definir las funciones latitud_correcta y longitud_correcta
#Una latitud correcta debe estar entre -90 y +90
#Una longitud correcta debe estar entre -180 y +180

#Función para comprobar si el valor de la latitud es correcto


#Función para comprobar si el valor de la longitud es correcto

      
        
if __name__ == '__main__':
    # Definimos una variable booleana para controlar si el formato del valor introducido por el usuario es correcto
    es_decimal_latitud = False
    es_decimal_longitud = False
    # Utilizamos un bucle while para solicitar al usuario la latitud y longitud de la ubicación
    latitud = 99999.9
    longitud = 99999.9
    #Mientras el usuario no introduzca un valor decimal para la latitud, se lo pedimos
    while not es_decimal_latitud:
        try:
            # Solicitamos al usuario la latitud y la convertimos a float. Si no es correcta, se la volvemos a pedir    
            latitud = float(input("Introduce la latitud. Utiliza el punto como separador decimal: "))
            while not latitud_correcta(latitud):
                latitud = float(input("Valor erróneo para la latitud. Vuelve a introducirlo: "))
            es_decimal_latitud = True
        except ValueError:
            print ("El valor introducido para la latitud no es un número decimal válido")
    #Mientras el usuario no introduzca un valor decimal para la longitud, se lo pedimos
    while not es_decimal_longitud:
        try:
            # Solicitamos al usuario la longitud y la convertimos a float. Si no es correcta, se la volvemos a pedir
            longitud =float(input("Introduce la longitud. Utiliza el punto como separador decimal: "))
            while not longitud_correcta(longitud):
                longitud =float(input("Valor erróneo para la longitud. Vuelve a introducirlo: "))
            es_decimal_longitud = True
        except ValueError:
            print ("El valor introducido para la longitud no es un número decimal válido") 
    #******************************************************************************************************************
    #(◕‿−)INTRODUCIR AQUÍ el código para imprimir el nombre de la ciudad que corresponde a las coordenadas introducidas
    #por el usuario. Si no se ha podido obtener la ciudad, imprimir un mensaje indicándolo
    


