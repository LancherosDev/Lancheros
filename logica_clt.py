from datetime import date


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