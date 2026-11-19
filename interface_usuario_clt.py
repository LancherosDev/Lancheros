from logica_clt import Lancha


def convertir_a_entero_o_texto(texto):
    texto = texto.strip()
    try:
        return int(texto)
    except ValueError:
        return texto


try:
    nombre = input("Ingrese el nombre de la lancha: ")
    cupos = input("Ingrese la cantidad de cupos por día: ")
    año = input("Ingrese el año de inicio del registro: ")
    mes = input("Ingrese el mes de inicio del registro (1-12): ")
    dia = input("Ingrese el día de inicio del registro: ")

    cupos = convertir_a_entero_o_texto(cupos)
    año = convertir_a_entero_o_texto(año)
    mes = convertir_a_entero_o_texto(mes)
    dia = convertir_a_entero_o_texto(dia)

    lancha = Lancha.crear_lancha(nombre, cupos, año, mes, dia)
    print(f"\nLancha '{lancha.nombre}' creada. Días registrados: {len(lancha.dias)}")
except ValueError as e:
    print(f"\nNo se creó la lancha: {e}")