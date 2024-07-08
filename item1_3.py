# Francisco Salazar y Dylan Guzman

def obtener_integrantes():
    integrantes = []
    while True:
        nombre = input("Ingrese el nombre y apellido del integrante (o 's' para salir): ")
        if nombre.lower() == 's':
            break
        integrantes.append(nombre)
    return integrantes

def mostrar_integrantes(integrantes):
    print("\nLista de integrantes del grupo:")
    for integrante in integrantes:
        print(integrante)

if __name__ == "__main__":
    integrantes = obtener_integrantes()
    mostrar_integrantes(integrantes)
