from datetime import date
from os import system, name
from logica_clt import Lancha

class C:
    QUITAR_FORMATO = "\033[0m"
    NEGRITA = "\033[1m"
    TEXTO_ATENUADO = "\033[2m"
    ROJO = "\033[91m"
    VERDE = "\033[92m"
    AMARILLO = "\033[93m"
    CIAN = "\033[96m"
    MAGENTA = "\033[95m"

def limpiar():
    system("cls" if name == "nt" else "clear")

def linea(caracter="─"):
    print(C.TEXTO_ATENUADO + caracter * ANCHO + C.QUITAR_FORMATO)

def encabezado(texto):
    print()
    print(C.NEGRITA + C.MAGENTA + f" ◆ {texto}" + C.QUITAR_FORMATO)
    linea()

def opcion_ver_lanchas():
    encabezado("Lanchas registradas")
    if len(Lancha.registro) == 0:
        print("  (ninguna todavía)")
        return
    i = 1
    for nombre in Lancha.registro:
        lancha = Lancha.registro[nombre]
        print(f"  {i}. {lancha.nombre}  cupos: {lancha.cupos}  días: {len(lancha.dias)}")
        i = i + 1


def leer_nombre_lancha():
    if len(Lancha.registro) == 0:
        print(f"{C.TEXTO_ATENUADO}(ninguna todavía){C.QUITAR_FORMATO}")
        return None
    print(f"{C.CIAN}Lanchas disponibles:{C.QUITAR_FORMATO}")
    for nombre in Lancha.registro:
        print(f"  {C.NEGRITA}{nombre}{C.QUITAR_FORMATO}")
    texto = input(f"{C.CIAN}Nombre de la lancha: {C.QUITAR_FORMATO}").strip()
    lancha = Lancha.buscar(texto)
    if lancha is None:
        print("No hay una lancha con ese nombre.")
        return None
    return lancha


def convertir_a_entero_o_texto(texto):
    texto = texto.strip()
    try:
        return int(texto)
    except ValueError:
        return texto


def opcion_crear_lancha():
    encabezado("Crear lancha")
    hoy = date.today()
    try:
        nombre = input(f"{C.CIAN}Nombre de la lancha: {C.QUITAR_FORMATO}").strip()
        cupos = input(f"{C.CIAN}Cupos por día: {C.QUITAR_FORMATO}").strip()
        texto_año = input(f"{C.CIAN}Año de inicio [{hoy.year}]: {C.QUITAR_FORMATO}").strip()
        texto_mes = input(f"{C.CIAN}Mes de inicio (1-12) [{hoy.month}]: {C.QUITAR_FORMATO}").strip()
        texto_dia = input(f"{C.CIAN}Día de inicio [{hoy.day}]: {C.QUITAR_FORMATO}").strip()

        cupos = convertir_a_entero_o_texto(cupos)
        if texto_año == "":
            año = hoy.year
        else:
            año = convertir_a_entero_o_texto(texto_año)
        if texto_mes == "":
            mes = hoy.month
        else:
            mes = convertir_a_entero_o_texto(texto_mes)
        if texto_dia == "":
            dia = hoy.day
        else:
            dia = convertir_a_entero_o_texto(texto_dia)

        lancha = Lancha.crear_lancha(nombre, cupos, año, mes, dia)
        print(f"{C.VERDE}Lancha {lancha.nombre} creada. Inicia el {lancha.fecha_inicio_registro.day:02d}/{lancha.fecha_inicio_registro.month:02d}/{lancha.fecha_inicio_registro.year}.{C.QUITAR_FORMATO}")
    except ValueError as e:
        print(f"\nNo se creó la lancha: {e}")


def opcion_registrar_dia():
    encabezado("Registrar un día")
    lancha = leer_nombre_lancha()
    
    if lancha is None:
        return
    
    fecha = lancha.fecha_siguiente()
    print(f"{C.CIAN}Registrando pasajeros del día {fecha.isoformat()}{C.QUITAR_FORMATO}")
    
    while True:
        texto = input(f"{C.CIAN}Ingrese los pasajeros del día: {C.QUITAR_FORMATO}").strip()
        try:
            pasajeros = int(texto)
        except ValueError:
            print(f"{C.ROJO}Los pasajeros deben ser un número entero.{C.QUITAR_FORMATO}")
            continue
        if pasajeros < 0 or pasajeros > lancha.cupos:
            print(f"{C.ROJO}Los pasajeros van de 0 a {lancha.cupos}.{C.QUITAR_FORMATO}")
            continue
        
        lancha.registrar_dia(pasajeros)
        print(f"{C.VERDE}Día registrado. Total de días: {len(lancha.dias)}{C.QUITAR_FORMATO}")
        break

def opcion_simular_dias():
    lancha = leer_nombre_lancha()
    if lancha is None:
        return
    try:
        texto = input(f"{C.CIAN}Número de días a simular: {C.QUITAR_FORMATO}").strip()
        try:
            num_dias = int(texto)
        except ValueError:
            raise ValueError(f"{C.ROJO}El número de días debe ser un número entero.{C.QUITAR_FORMATO}")
        if num_dias < 1:
            raise ValueError(f"{C.ROJO}Se debe simular al menos un día.{C.QUITAR_FORMATO}")
        texto = input(f"{C.CIAN}Pasajeros mínimos (0 - {lancha.cupos}): {C.QUITAR_FORMATO}").strip()

        try:
            minimo = int(texto)
        except ValueError:
            raise ValueError(f"{C.ROJO}Los pasajeros deben ser un número entero.{C.QUITAR_FORMATO}")
        if minimo < 0 or minimo > lancha.cupos:
            raise ValueError(f"{C.ROJO}Los pasajeros van de 0 a {lancha.cupos}.{C.QUITAR_FORMATO}")
        texto = input(f"{C.CIAN}Pasajeros máximos (0 - {lancha.cupos}): {C.QUITAR_FORMATO}").strip()
            
        try:
            maximo = int(texto)
        except ValueError:
            raise ValueError(f"{C.ROJO}Los pasajeros deben ser un número entero.{C.QUITAR_FORMATO}")
        if maximo < 0 or maximo > lancha.cupos:
            raise ValueError(f"{C.ROJO}Los pasajeros van de 0 a {lancha.cupos}.{C.QUITAR_FORMATO}")
        if minimo > maximo:
            raise ValueError(f"{C.ROJO}El mínimo no puede ser mayor que el máximo.{C.QUITAR_FORMATO}")
            
        lancha.simular_dias(num_dias, minimo, maximo)
        print(f"{C.VERDE}Se agregaron {num_dias} días simulados. Total de días: {len(lancha.dias)}{C.QUITAR_FORMATO}")
    except ValueError as e:
            print(f"{C.ROJO}No se simuló ningún día: {e}{C.QUITAR_FORMATO}")

ANCHO = 30

def banner():
    print(C.NEGRITA + C.CIAN)
    print(" ╔" + "═" * (ANCHO - 2) + "╗")
    print(" ║" + "GESTOR DE LANCHAS".center(ANCHO - 2) + "║")
    print(" ║" + "control de pasajeros".center(ANCHO - 2) + "║")
    print(" ╚" + "═" * (ANCHO - 2) + "╝" + C.QUITAR_FORMATO)

def opcion_generar_informe():
    lancha = leer_nombre_lancha()
    if lancha is None:
        return
    
    print()
    if len(lancha.dias) == 0:
        print(f"{C.NEGRITA}{lancha.nombre}{C.QUITAR_FORMATO} · {lancha.cupos} cupos · 0 días registrados")
        print(f"\n{C.TEXTO_ATENUADO}No tiene días registrados.{C.QUITAR_FORMATO}")
        return
    
    print(f"{C.NEGRITA}{lancha.nombre}{C.QUITAR_FORMATO} · {lancha.cupos} cupos · {len(lancha.dias)} días registrados")
    print()
    
    total_pasajeros = sum(lancha.dias)
    promedio = round(total_pasajeros / len(lancha.dias), 2)
    factor_ocupacion = round((promedio / lancha.cupos) * 100, 2)
    
    suma_cuadrados = 0
    for p in lancha.dias:
        diferencia = p - promedio
        suma_cuadrados = suma_cuadrados + diferencia * diferencia
    desviacion = round((suma_cuadrados / len(lancha.dias)) ** 0.5, 2)
    
    fecha_max, fecha_min = lancha.dia_max_min()
    fecha_max_txt = f"{fecha_max.day:02d}/{fecha_max.month:02d}/{fecha_max.year}"
    fecha_min_txt = f"{fecha_min.day:02d}/{fecha_min.month:02d}/{fecha_min.year}"
    
    print(f"Total de pasajeros {total_pasajeros}")
    print(f"Promedio por día {promedio}")
    print(f"Ocupación promedio {factor_ocupacion} %")
    print(f"Desviación estándar {desviacion}")
    print(f"Día con más pasajeros {fecha_max_txt}")
    print(f"Día con menos pasajeros {fecha_min_txt}")
    print()
    
    critico, bajo, adecuado, lleno = lancha.contar_niveles_ocupacion()
    print(f"{C.NEGRITA}Niveles de ocupación{C.QUITAR_FORMATO}")
    
    mayor = critico
    if bajo > mayor:
        mayor = bajo
    if adecuado > mayor:
        mayor = adecuado
    if lleno > mayor:
        mayor = lleno
    
    ANCHO_BARRA = 40
    
    def barra(n):
        if mayor == 0:
            return ""
        largo = int((n / mayor) * ANCHO_BARRA)
        return "█" * largo

    print(f"{C.ROJO}crítico {barra(critico)} {critico}{C.QUITAR_FORMATO}")
    print(f"{C.AMARILLO}bajo {barra(bajo)} {bajo}{C.QUITAR_FORMATO}")
    print(f"{C.VERDE}adecuado {barra(adecuado)} {adecuado}{C.QUITAR_FORMATO}")
    print(f"{C.CIAN}lleno {barra(lleno)} {lleno}{C.QUITAR_FORMATO}")
    print()
    
    resultado_racha = lancha.racha_mas_larga_critico()
    if resultado_racha is None:
        print(f"{C.TEXTO_ATENUADO}No tuvo ningún día en nivel crítico.{C.QUITAR_FORMATO}")
    else:
        longitud_racha, fecha_inicio_racha = resultado_racha
        fecha_racha_txt = f"{fecha_inicio_racha.day:02d}/{fecha_inicio_racha.month:02d}/{fecha_inicio_racha.year}"
        print(f"{C.ROJO}Racha más larga en nivel crítico: {longitud_racha} días desde el {fecha_racha_txt}{C.QUITAR_FORMATO}")
    
    ultimo = lancha.fecha_del_indice(len(lancha.dias) - 1)
    ultimo_txt = f"{ultimo.day:02d}/{ultimo.month:02d}/{ultimo.year}"
    print(f"{C.VERDE}Al día: último registro {ultimo_txt}.{C.QUITAR_FORMATO}")

def opcion_factores_extremos():
    encabezado("Factor de ocupación más alto y más bajo")
    
    max_factor = None
    max_nombre = None
    min_factor = None
    min_nombre = None
    
    for nombre in Lancha.registro:
        lancha = Lancha.registro[nombre]
        factor = lancha.factor_ocupacion_sin_redondear()
        if factor is None:
            continue
    
        if max_factor is None or factor > max_factor:
            max_factor = factor
            max_nombre = nombre
    
        if min_factor is None or factor < min_factor:
            min_factor = factor
            min_nombre = nombre
        
    if max_factor is None:
        print("Ninguna lancha tiene días registrados.")
        return
    print(f"{C.NEGRITA}{C.CIAN}Lancha con factor de ocupación más alto: {C.QUITAR_FORMATO}{C.NEGRITA}{max_nombre} ({round(max_factor, 2)} %){C.QUITAR_FORMATO}")
    print(f"{C.NEGRITA}{C.CIAN}Lancha con factor de ocupación más bajo: {C.QUITAR_FORMATO}{C.NEGRITA}{min_nombre} ({round(min_factor, 2)} %){C.QUITAR_FORMATO}")