from datetime import date
import random

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

    def simular_dias(self, num_dias, minimo, maximo):
        if not isinstance(num_dias, int) or isinstance(num_dias, bool):
            raise ValueError("El número de días debe ser un número entero.")
        if num_dias < 1:
            raise ValueError("Se debe simular al menos un día.")
        if not isinstance(minimo, int) or isinstance(minimo, bool):
            raise ValueError("Los pasajeros deben ser un número entero.")
        if minimo < 0 or minimo > self.cupos:
            raise ValueError(f"Los pasajeros van de 0 a {self.cupos}.")
        if not isinstance(maximo, int) or isinstance(maximo, bool):
            raise ValueError("Los pasajeros deben ser un número entero.")
        if maximo < 0 or maximo > self.cupos:
            raise ValueError(f"Los pasajeros van de 0 a {self.cupos}.")
        if minimo > maximo:
            raise ValueError("El mínimo no puede ser mayor que el máximo.")
        for _ in range(num_dias):
            self.dias.append(random.randint(minimo, maximo))

    def dia_max_min(self):
        indice_max = 0
        indice_min = 0
        for i in range(len(self.dias)):
            if self.dias[i] > self.dias[indice_max]:
                indice_max = i
            if self.dias[i] < self.dias[indice_min]:
                indice_min = i
        return self.fecha_del_indice(indice_max), self.fecha_del_indice(indice_min)
    
    
    def fecha_del_indice(self, indice):
        fecha = self.fecha_inicio_registro
        for _ in range(indice):
          fecha = _avanzar_un_dia(fecha)
        return fecha
    
    def contar_niveles_ocupacion(self):
        critico = 0
        bajo = 0
        adecuado = 0
        lleno = 0
        for p in self.dias:
            porcentaje = (p / self.cupos) * 100
        if porcentaje < 50:
            critico = critico + 1
        elif porcentaje < 70:
            bajo = bajo + 1
        elif porcentaje < 90:   
            adecuado = adecuado + 1
        else:
            lleno = lleno + 1
        return critico, bajo, adecuado, lleno

    def racha_mas_larga_critico(self):
        mejor_longitud = 0
        mejor_inicio = 0
        longitud_actual = 0
        inicio_actual = 0
        
        for i in range(len(self.dias)):
            porcentaje = (self.dias[i] / self.cupos) * 100
            if porcentaje < 50:
                if longitud_actual == 0:
                    inicio_actual = i
                longitud_actual = longitud_actual + 1
                if longitud_actual > mejor_longitud:
                    mejor_longitud = longitud_actual
                    mejor_inicio = inicio_actual
            else:
                longitud_actual = 0
        if mejor_longitud == 0:
            return None
        return mejor_longitud, self.fecha_del_indice(mejor_inicio)


def generar_informe(self):
    informe = f"Lancha: {self.nombre}\n"
    informe += f"Cupos por día: {self.cupos}\n"
    
    if len(self.dias) == 0:
        informe += "No tiene días registrados.\n"
        return informe
    
    total_pasajeros = sum(self.dias)
    promedio = round(total_pasajeros / len(self.dias), 2)
    factor_ocupacion = round((promedio / self.cupos) * 100, 2)
    
    suma_cuadrados = 0
    for p in self.dias:
        diferencia = p - promedio
        suma_cuadrados = suma_cuadrados + diferencia * diferencia
    
    desviacion = round((suma_cuadrados / len(self.dias)) ** 0.5, 2)
    
    fecha_max, fecha_min = self.dia_max_min()
    
    informe += f"Días registrados: {len(self.dias)}\n"
    informe += f"Pasajeros totales: {total_pasajeros}\n"
    informe += f"Promedio de pasajeros por día: {promedio}\n"
    informe += f"Desviación estándar: {desviacion}\n"
    informe += f"Factor de ocupación: {factor_ocupacion}\n"
    informe += f"Día con más pasajeros: {fecha_max}\n"
    informe += f"Día con menos pasajeros: {fecha_min}\n"
    
    critico, bajo, adecuado, lleno = self.contar_niveles_ocupacion()
    informe += f"Días en nivel crítico: {critico}\n"
    informe += f"Días en nivel bajo: {bajo}\n"
    informe += f"Días en nivel adecuado: {adecuado}\n"
    informe += f"Días en nivel lleno: {lleno}\n"
    
    resultado_racha = self.racha_mas_larga_critico()
    if resultado_racha is None:
        informe += "No tuvo ningún día en nivel crítico.\n"
    else:
        longitud_racha, fecha_inicio_racha = resultado_racha
        informe += f"Racha más larga en nivel crítico: {longitud_racha} días\n"
        informe += f"Inicio de la racha más larga en nivel crítico: {fecha_inicio_racha}\n"
    return informe
