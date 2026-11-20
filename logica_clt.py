from datetime import date

def _es_bisiesto(año):
    return (año % 4 == 0 and año % 100 != 0) or (año % 400 == 0)


def _dias_del_mes(año, mes):
    if mes in (1, 3, 5, 7, 8, 10, 12):
        return 31
    if mes in (4, 6, 9, 11):
        return 30
    if mes == 2:
        return 29 if _es_bisiesto(año) else 28
    return 0


def _avanzar_un_dia(fecha):
    año = fecha.year
    mes = fecha.month
    dia = fecha.day + 1
    if dia > _dias_del_mes(año, mes):
        dia = 1
        mes += 1
        if mes > 12:
            mes = 1
            año += 1
    return date(año, mes, dia)

class Lancha:
    registro = {}
 
    def __init__(self, nombre, cupos, fecha_inicio_registro):
        self.nombre = nombre
        self.cupos = cupos
        self.fecha_inicio_registro = fecha_inicio_registro
        self.dias = []
 
    def crear_lancha(nombre, cupos_dia, año, mes, dia):
 
        if not isinstance(nombre, str) or nombre.strip() == "":
            raise ValueError("El nombre no puede estar vacío.")
        nombre = nombre.strip()
        if nombre in Lancha.registro:
            raise ValueError(f"Ya existe una lancha llamada '{nombre}'.")
 
        if not isinstance(cupos_dia, int) or isinstance(cupos_dia, bool):
            raise ValueError("Los cupos por día deben ser un número entero.")
 
        if cupos_dia < 1:
            raise ValueError("La lancha debe ofrecer al menos un cupo por día.")
 
        if (not isinstance(año, int) or isinstance(año, bool)
                or not isinstance(mes, int) or isinstance(mes, bool)
                or not isinstance(dia, int) or isinstance(dia, bool)):
            raise ValueError("La fecha no es válida.")
        try:
            fecha = date(año, mes, dia)
        except ValueError:
            raise ValueError("La fecha no es válida, deben ser en números.")
 
        lancha = Lancha(nombre, cupos_dia, fecha)
        Lancha.registro[nombre] = lancha
        return lancha

    def buscar(nombre):
        if not isinstance(nombre, str):
            return None
        return Lancha.registro.get(nombre.strip())

    def fecha_siguiente(self):
        fecha = self.fecha_inicio_registro
        for _ in range(len(self.dias)):
            fecha = _avanzar_un_dia(fecha)
        return fecha

    def registrar_dia(self, pasajeros):
        self.dias.append(pasajeros)