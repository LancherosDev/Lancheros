# 🚤 Gestor de Lanchas

Sistema de consola en Python para registrar lanchas, simular o cargar el flujo diario de pasajeros y generar informes estadísticos de ocupación.

> Trabajo de fin de curso · **Fundamentos de Programación** · Ingeniería en Ciencia de Datos · Universidad del Magdalena
> Docente: Brayan Carbono

---

## 📋 Descripción

Llevar el control diario de capacidad, demanda y aprovechamiento de embarcaciones de pasajeros de forma manual genera inconsistencias en fechas, errores de digitación fuera de los cupos permitidos y demoras al consolidar indicadores.

**Gestor de Lanchas** resuelve este problema con una aplicación de consola orientada a objetos, sin dependencias externas, que permite:

- Crear y administrar múltiples lanchas, cada una con nombre único, cupos diarios y fecha de inicio de operación.
- Registrar pasajeros día a día (la fecha siguiente se calcula automáticamente) o simular días de operación de forma aleatoria.
- Generar informes con métricas estadísticas, distribución por niveles de ocupación y gráfico de barras en consola.
- Comparar lanchas según su factor de ocupación promedio.
- Cargar lanchas y pasajeros de forma masiva desde archivos de texto delimitados por `;`.

---

## ✨ Funcionalidades

| Funcionalidad | Detalle |
|---|---|
| **Gestión de lanchas** | Crear con fecha personalizada o la fecha actual del sistema, listar (tecla `v`) y seleccionar por nombre exacto. |
| **Registro diario** | Valida que el número de pasajeros sea un entero entre `0` y el cupo máximo de la lancha. |
| **Simulación** | Genera `n` días aleatorios dentro de un rango mínimo y máximo válido. |
| **Informe detallado** | Total de pasajeros, promedio diario, ocupación promedio (%), desviación estándar, fechas de máxima y mínima afluencia, niveles de ocupación con gráfico de barras, racha más larga en nivel crítico y último día registrado. |
| **Comparación** | Lancha con mayor y menor factor de ocupación promedio (ignora lanchas sin días). |
| **Carga desde archivos** | Importa lanchas y pasajeros reportando cada error con su número de línea, sin detener la lectura de las líneas válidas. |
| **Menú interactivo** | Ciclo continuo con 7 opciones numeradas más el listado rápido `v`, validando entradas no reconocidas. |

### Niveles de ocupación

| Nivel | Rango de ocupación |
|---|---|
| 🔴 Crítico | menor a 50 % |
| 🟡 Bajo | desde 50 % y menor a 70 % |
| 🟢 Adecuado | desde 70 % y menor a 90 % |
| 🔵 Lleno | 90 % o más |

---

## 🗂️ Estructura del repositorio

```
Lancheros/
├── logica_clt.py             # Lógica de negocio: clase Lancha, fechas y estadísticas
├── interface_usuario_clt.py  # Interfaz de consola: menú, entradas y presentación
├── lanchas.csv               # Datos de ejemplo: lanchas (nombre;cupos;año;mes;día)
└── pasajero.csv              # Datos de ejemplo: pasajeros (nombre_lancha;pasajeros)
```

El proyecto separa la **lógica de negocio** (`logica_clt.py`) de la **interfaz de usuario** (`interface_usuario_clt.py`), de modo que los cálculos no dependen de cómo se presentan.

---

## ⚙️ Requisitos

- Python 3
- No requiere instalar paquetes: usa únicamente la biblioteca estándar (`datetime`, `random`, `os`).
- Una terminal con soporte de códigos ANSI para visualizar los colores (Windows Terminal, VS Code, Linux/macOS).

---

## ▶️ Cómo ejecutar

```bash
# 1. Clonar el repositorio
git clone https://github.com/viloriadaniel199/Lancheros.git
cd Lancheros

# 2. Ejecutar el programa
python interface_usuario_clt.py
```

### Menú principal

| Opción | Acción |
|---|---|
| `1` | Crear lancha |
| `2` | Registrar pasajeros del día siguiente |
| `3` | Simular días de operación |
| `4` | Generar informe de una lancha |
| `5` | Mostrar lanchas con mayor y menor factor de ocupación |
| `6` | Cargar lanchas y pasajeros desde archivos |
| `7` | Salir |
| `v` | Ver lanchas registradas |

---

## 📁 Formato de los archivos de carga

La opción `6` solo funciona cuando **no hay lanchas cargadas** en memoria. Ambos archivos son UTF-8, delimitados por punto y coma (`;`); la primera línea (encabezado) y las líneas vacías se omiten.

**Archivo de lanchas** (5 campos): `nombre;cupos;año;mes;día`

```
nombre;cupos;año;mes;día
Caracola;40;2026;11;1
```

**Archivo de pasajeros** (2 campos): `nombre_lancha;pasajeros`

```
nombre_lancha;pasajeros
Caracola;26
```

Si una línea tiene un error de formato, de tipo de dato o de validación, se informa en rojo con su número de línea y se continúa con el resto.

---

## 🧠 Diseño y algoritmos

El proyecto implementa sus cálculos sin librerías estadísticas externas (NumPy, pandas), de modo que cada operación puede auditarse paso a paso.

**Aritmética de fechas.** Aunque se almacenan como `datetime.date`, el avance de un día se programó manualmente con `_es_bisiesto`, `_dias_del_mes` y `_avanzar_un_dia`, controlando cambios de mes y de año. Sobre esto se construyen `fecha_siguiente` y `fecha_del_indice`.

**Indicadores.** Sea `n` el número de días registrados, `pᵢ` los pasajeros del día `i` y `C` el cupo diario:

- Total: `T = Σ pᵢ`
- Promedio diario: `x̄ = T / n`
- Factor de ocupación (%): `FO = (x̄ / C) × 100`
- Desviación estándar poblacional: `σ = √[ (1/n) · Σ (pᵢ − x̄)² ]`

Todos los valores se muestran redondeados a 2 decimales. Para comparar lanchas se usa `factor_ocupacion_sin_redondear`, evitando empates artificiales por redondeo prematuro.

**Extremos diarios.** `dia_max_min` recorre la serie una sola vez (O(n)) con comparaciones estrictas; ante empates conserva la primera fecha registrada.

**Racha crítica.** `racha_mas_larga_critico` recorre la serie en O(n) manteniendo la longitud y el inicio de la racha actual y de la mejor encontrada. Un día con 50 % o más de ocupación reinicia la racha; si ningún día fue crítico, devuelve `None`.

### Validaciones principales

- Nombres de lancha únicos y no vacíos.
- Cupos enteros positivos.
- Fechas reales de calendario (por ejemplo, se rechaza el 30 de febrero).
- Pasajeros dentro del intervalo cerrado `[0, cupos]`.
- Se descartan valores booleanos al validar enteros (en Python `bool` hereda de `int`).

---

## 🧪 Pruebas

La verificación se hizo sobre la versión final con la siguiente matriz de casos:

| Caso | Funcionalidad | Resultado esperado |
|---|---|---|
| CP-01 | Creación de lancha válida | Se registra con 0 días y confirmación en verde. |
| CP-02 | Validación de creación | Nombre repetido, cupos inválidos o fecha inexistente → error controlado sin alterar el registro. |
| CP-03 | Registro de pasajeros | Rechaza lancha inexistente, texto y valores fuera de rango; registra el valor válido. |
| CP-04 | Simulación de días | Agrega `n` valores válidos; rechaza `mínimo > máximo`. |
| CP-05 | Informe estadístico | Lancha vacía → «No tiene días registrados.»; con datos → métricas, barras, racha y último día. |
| CP-06 | Factores extremos | Ignora lanchas sin días y muestra la mayor y la menor ocupación. |
| CP-07 | Carga desde archivos | Carga líneas válidas, reporta las erróneas y bloquea la recarga si ya hay lanchas. |
| CP-08 | Navegación del menú | Ejecuta las opciones 1–7 y `v`; muestra «Opción no válida.» ante entradas incorrectas. |

---

## 👥 Equipo

| Integrante | GitHub |
|---|---|
| Ivan Reales | [@SirIvanRo](https://github.com/SirIvanRo) |
| Daniel Viloria | [@viloriadaniel199](https://github.com/viloriadaniel199) |
| Jehiver Nieto | [@jehivern](https://github.com/jehivern) |

El desarrollo fue incremental y colaborativo, en 14 implementaciones registradas en el historial de commits de la rama `main`.

---

## 🛠️ Tecnologías

Python 3 · Git · GitHub · Visual Studio Code

---

## 🤖 Uso de inteligencia artificial generativa

Se usó Gemini como apoyo en la configuración del entorno (Git, Python, VS Code), la ejecución de comandos de control de versiones, la revisión conceptual de los módulos y la redacción del informe. La integración en el repositorio, la verificación en terminal y la revisión final fueron realizadas por los integrantes del equipo, quienes responden por el funcionamiento y la sustentación del proyecto.

---

## 🎥 Video explicativo

<!-- Reemplazar con el enlace público del video -->
[Ver video](ENLACE_AL_VIDEO)
