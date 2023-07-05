#************************************************************************************
#Curso "Python para hacking ético" Tknika 2022/2023
#RESUMEN DEL SCRIPT: 
#El usuario introduce una dirección, y obtenemos las coordenadas que le corresponden   
#************************************************************************************
#El módulo geocoders proporciona herramientas para geocodificación, es decir, para convertir una ubicación en coordenadas
#geográficas (latitud y longitud) y viceversa.
#La clase Nominatim es una implementación de un geocodificador que utiliza el servicio web Nominatim para buscar
#ubicaciones geográficas.
from geopy.geocoders import Nominatim

# Creamos una instancia de Nominatim con un user_agent personalizado
geolocator = Nominatim(user_agent="tknika12345")

# Definimos una variable booleana para controlar la validez de la dirección
direccion_valida = False

while not direccion_valida:
    direccion = input("Introduce una dirección: ")
    try:
        # Utilizamos el método geocode para obtener la ubicación basada en la dirección ingresada
        localizacion = geolocator.geocode(direccion)
        if localizacion is None:
            print("La dirección no es válida. Introduce una dirección existente.")
        else:
            # Si la ubicación es válida, establecemos la variable direccion_valida en True para salir del bucle
            direccion_valida = True
    except Exception as e:
        # Si ocurre un error durante la geocodificación, lo mostramos en pantalla
        print(f"Ocurrió un error: {e}")


#************************************************************************
## Si se encontró una ubicación, obtenemos las coordenadas de latitud y longitud
#y las imprimimos or pantalla
# (◕‿−)INTRODUCIR AQUÍ el trozo de código para realizar lo explicado encima
#
if localizacion is not None:
    latitud = localizacion.latitude
    longitud = localizacion.longitude
    print(f"Las coordenadas de la dirección introducida son: Latitud {latitud}, Longitud {longitud}")
else:
    print("No se pudo encontrar coordenadas para la dirección especificada.")
exit()
