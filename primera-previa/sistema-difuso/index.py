import sqlite3  # Importo librería para manejo de bases de datos

con = sqlite3.connect("mydatabase.db")  # Definir conexión a una base de datos
cursor = con.cursor()  # Cursor para interactuar con la base de datos

# Creación de las tablas
cursor.execute("CREATE TABLE hechos(id_h INTEGER PRIMARY KEY, nombre TEXT)")
cursor.execute(
    """CREATE TABLE reglas(id_r INTEGER PRIMARY KEY, id_anteced INTEGER, id_consec INTEGER, difuso FLOAT,
                FOREIGN KEY(id_anteced) REFERENCES hechos(id_h),FOREIGN KEY(id_consec) REFERENCES hechos(id_h) )"""
)

# Adicionar información en la tabla de hechos
cursor.execute("INSERT INTO hechos VALUES(1,'fiebre')")
cursor.execute("INSERT INTO hechos VALUES(2,'malestar')")
cursor.execute("INSERT INTO hechos VALUES(3,'dolor_garganta')")
cursor.execute("INSERT INTO hechos VALUES(4,'faringitis')")
cursor.execute("INSERT INTO hechos VALUES(5,'gripa')")

# Adicionar información en la tabla de reglas
cursor.execute("INSERT INTO reglas VALUES(1,1,5,0.2)")
cursor.execute("INSERT INTO reglas VALUES(2,2,5,0.7)")
cursor.execute("INSERT INTO reglas VALUES(3,3,4,0.8)")
cursor.execute("INSERT INTO reglas VALUES(4,2,4,0.6)")


# Vista contenido tabla hechos
cursor.execute("SELECT * FROM hechos")
result = cursor.fetchall()
print(result)


# Vista contenido tabla reglas
cursor.execute("SELECT * FROM reglas")
result = cursor.fetchall()
print(result)
[(1, 1, 5, 0.2), (2, 2, 5, 0.7), (3, 3, 4, 0.8), (4, 2, 4, 0.6)]

# Generación de agenda
agenda = {}


# Busco el consecuente (enfermedad) y lleno la agenda
def manejoAgenda(sintoma):
    # Tomo la enfermedad
    cursor.execute("SELECT id_consec FROM reglas WHERE id_anteced = '%i'" % sintoma)
    enfermedad_id = cursor.fetchall()
    # Tomo el identificador de la(s) reglas en donde se cumple el sintoma, esto es para poder acceder al valor difuso
    cursor.execute("SELECT id_r FROM reglas WHERE id_anteced = '%i'" % sintoma)
    index_enfermedad = cursor.fetchall()

    # Si el sintoma solo conduce a una enfermedad
    if len(enfermedad_id) == 1:
        # Nombre de la enfermedad
        cursor.execute(
            "SELECT nombre FROM hechos WHERE id_h = '%i'" % enfermedad_id[0][0]
        )
        nomb_enfermedad = cursor.fetchall()
        # Valor difuso asignado a enfermedad
        cursor.execute(
            "SELECT difuso FROM reglas WHERE id_r = '%f'" % index_enfermedad[0][0]
        )
        valor_difuso = cursor.fetchall()

        if nomb_enfermedad[0][0] in agenda:
            acumulado_difuso = agenda.get(nomb_enfermedad[0][0])
            agenda[nomb_enfermedad[0][0]] = acumulado_difuso + (
                (1 - acumulado_difuso) * valor_difuso[0][0]
            )
        else:
            agenda[nomb_enfermedad[0][0]] = valor_difuso[0][0]

    # Si el sintoma se presenta en ambas enfermedades
    if len(enfermedad_id) == 2:

        # Primer enfermedad
        cursor.execute(
            "SELECT nombre FROM hechos WHERE id_h = '%i'" % enfermedad_id[0][0]
        )
        nomb_enfermedad = cursor.fetchall()
        # Valor difuso asignado a enfermedad
        cursor.execute(
            "SELECT difuso FROM reglas WHERE id_r = '%f'" % index_enfermedad[0][0]
        )
        valor_difuso = cursor.fetchall()

        if nomb_enfermedad[0][0] in agenda:
            acumulado_difuso = agenda.get(nomb_enfermedad[0][0])
            agenda[nomb_enfermedad[0][0]] = acumulado_difuso + (
                (1 - acumulado_difuso) * valor_difuso[0][0]
            )
        else:
            agenda[nomb_enfermedad[0][0]] = valor_difuso[0][0]

        # Segunda enfermedad
        cursor.execute(
            "SELECT nombre FROM hechos WHERE id_h = '%i'" % enfermedad_id[1][0]
        )
        nomb_enfermedad = cursor.fetchall()
        # Valor difuso asignado a enfermedad
        cursor.execute(
            "SELECT difuso FROM reglas WHERE id_r = '%f'" % index_enfermedad[1][0]
        )
        valor_difuso = cursor.fetchall()

        if nomb_enfermedad[0][0] in agenda:
            acumulado_difuso = agenda.get(nomb_enfermedad[0][0])
            agenda[nomb_enfermedad[0][0]] = acumulado_difuso + (
                (1 - acumulado_difuso) * valor_difuso[0][0]
            )
        else:
            agenda[nomb_enfermedad[0][0]] = valor_difuso[0][0]

    print(agenda)


# Tomo el identificador del sintoma proporcionado
def sistema(entrada):
    cursor.execute("SELECT id_h FROM hechos WHERE nombre = '%s'" % entrada)
    sintoma = cursor.fetchall()
    if len(sintoma) == 1:
        valor_sintoma = sintoma[0][0]
        manejoAgenda(valor_sintoma)


# Ciclo de pregunta
while True:
    entrada = input("Ingrese un sintoma: ")
    if entrada != "nada":
        sistema(entrada)
    else:
        break

    # Revisión de Agenda
num = list(agenda.values())
nombres = list(agenda.keys())

# Caso de agenda sin sintomas
if len(num) == 0:
    print("Agenda vacía")

elif len(num) > 0:
    # Sintoma con mayor valor y ver si hay empate
    maximo = max(num)
    cantidad = num.count(maximo)
    if cantidad > 1:
        print("No está definida la enfermedad, hay empate")
    elif cantidad == 1:
        enfermedad_pos = num.index(maximo)
        enfermedad_nombre = nombres[enfermedad_pos]
        print("El paciente tiene {} en un {}%".format(enfermedad_nombre, maximo * 100))


agenda.clear()
