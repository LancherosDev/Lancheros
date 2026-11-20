from logica_clt import Lancha


def convertir_a_entero_o_texto(texto):
    texto = texto.strip()
    try:
        return int(texto)
    except ValueError:
        return texto


def leer_nombre_lancha():
    nombre = input("Ingrese el nombre de la lancha: ").strip()
    lancha = Lancha.buscar(nombre)
    if lancha is None:
        print(f"No hay una lancha con el nombre '{nombre}'.")
        return None
    return lancha


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

lancha = leer_nombre_lancha()
if lancha is not None:
    fecha = lancha.fecha_siguiente()
    print(f"Registrando pasajeros del día {fecha.isoformat()}")

    while True:
        texto = input("Ingrese los pasajeros del día: ").strip()
        try:
            pasajeros = int(texto)
        except ValueError:
            print("Los pasajeros deben ser un número entero.")
            continue
        if pasajeros < 0 or pasajeros > lancha.cupos:
            print(f"Los pasajeros van de 0 a {lancha.cupos}.")
            continue
        lancha.registrar_dia(pasajeros)
        print(f"Día registrado. Total de días: {len(lancha.dias)}")
        break

    lancha = leer_nombre_lancha()
    if lancha is not None:
        try:
            texto = input("Número de días a simular: ").strip()
            try:
                num_dias = int(texto)
            except ValueError:
                raise ValueError("El número de días debe ser un número entero.")
            if num_dias < 1:
                raise ValueError("Se debe simular al menos 1 día.")

            texto = input("Pasajeros mínimos por día: ").strip()
            try:
                minimo = int(texto)
            except ValueError:
                raise ValueError("Los pasajeros deben ser un número entero.")
            if minimo < 0 or minimo > lancha.cupos:
                raise ValueError(f"Los pasajeros van de 0 a {lancha.cupos}.")

            texto = input("Pasajeros máximos por día: ").strip()
            try:
                maximo = int(texto)
            except ValueError:
                raise ValueError("Los pasajeros deben ser un número entero.")
            if maximo < 0 or maximo > lancha.cupos:
                raise ValueError(f"Los pasajeros van de 0 a {lancha.cupos}.")
            if minimo > maximo:
                raise ValueError("El mínimo no puede ser mayor que el máximo.")

            lancha.simular_dias(num_dias, minimo, maximo)
            print(f"\nSse agregaron {num_dias} días simulados. Total de dias: {len(lancha.dias)}")
        except ValueError as e:
            print(f"\nNo se simularon días: {e}")    

    lancha = leer_nombre_lancha()
    if lancha is not None:
        print()
        print(lancha.generar_informe())