from geopy.geocoders import OpenCage
from geopy.distance import geodesic
import requests

def obtener_coordenadas(ciudad, pais, api_key):
    geolocator = OpenCage(api_key)
    location = geolocator.geocode(f"{ciudad}, {pais}")
    return (location.latitude, location.longitude)

def obtener_distancia(ciudad_origen, ciudad_destino, api_key, medio_transporte):
    coord_origen = obtener_coordenadas(ciudad_origen, "Chile", api_key)
    coord_destino = obtener_coordenadas(ciudad_destino, "Argentina", api_key)
    distancia_km = geodesic(coord_origen, coord_destino).kilometers
    distancia_millas = distancia_km * 0.621371
    duracion = obtener_duracion_viaje(coord_origen, coord_destino, medio_transporte)
    return distancia_km, distancia_millas, duracion

def obtener_duracion_viaje(coord_origen, coord_destino, medio_transporte):
    url = f"http://router.project-osrm.org/route/v1/{medio_transporte}/{coord_origen[1]},{coord_origen[0]};{coord_destino[1]},{coord_destino[0]}?overview=false"
    response = requests.get(url).json()
    duracion_segundos = response['routes'][0]['duration']
    duracion_minutos = duracion_segundos / 60
    return duracion_minutos

def mostrar_narrativa(ciudad_origen, ciudad_destino, distancia_km, distancia_millas, duracion):
    print(f"\nEl viaje desde {ciudad_origen} hasta {ciudad_destino} es de aproximadamente:")
    print(f"{distancia_km:.2f} kilómetros")
    print(f"{distancia_millas:.2f} millas")
    print(f"Duración estimada del viaje: {duracion:.2f} minutos")

def main():
    api_key = "9a281429d9ee407bb738ba33c87eec04"
    while True:
        ciudad_origen = input("Ingrese la Ciudad de Origen (o 's' para salir): ")
        if ciudad_origen.lower() == 's':
            break

        ciudad_destino = input("Ingrese la Ciudad de Destino: ")
        if ciudad_destino.lower() == 's':
            break

        print("Seleccione el medio de transporte:")
        print("1. Conducir")
        print("2. Bicicleta")
        print("3. Caminando")

        opcion_transporte = input("Ingrese el número correspondiente al medio de transporte: ")

        if opcion_transporte == '1':
            medio_transporte = 'driving'
        elif opcion_transporte == '2':
            medio_transporte = 'bicycling'
        elif opcion_transporte == '3':
            medio_transporte = 'walking'
        else:
            print("Opción no válida, usando 'Conducir' por defecto.")
            medio_transporte = 'driving'

        distancia_km, distancia_millas, duracion = obtener_distancia(ciudad_origen, ciudad_destino, api_key, medio_transporte)
        mostrar_narrativa(ciudad_origen, ciudad_destino, distancia_km, distancia_millas, duracion)

if __name__ == "__main__":
    main()
