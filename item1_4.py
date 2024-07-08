# Francisco Salazar y Dylan Guzman

def determinar_vlan(vlan):
    if 1 <= vlan <= 1005:
        return "VLAN del rango normal"
    elif 1006 <= vlan <= 4094:
        return "VLAN del rango extendido"
    else:
        return "Número de VLAN inválido"

try:
    vlan = int(input("Ingrese el número de VLAN: "))
    resultado = determinar_vlan(vlan)
    print(resultado)
except ValueError:
    print("Por favor, ingrese un número válido.")
