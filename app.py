# Importa el framework Flask para crear rutas web y url_for para generar URLs dinámicas
from flask import Flask, url_for
import sqlite3  # Módulo estándar para interactuar con bases de datos SQLite

app = Flask(__name__)  # Instancia principal de la aplicación Flask

db = None  # Variable global para mantener la conexión activa con SQLite

# Convierte cada fila obtenida de la base en un diccionario con clave=nombre_columna
# Esto facilita el acceso a los datos como si fueran objetos tipo JSON
def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}

# Abre la conexión a la base de datos y configura la devolución de filas como objetos tipo dict
def abrirConexion():
    global db
    db = sqlite3.connect("instance/datos.sqlite")  # Se conecta al archivo SQLite
    db.row_factory = sqlite3.Row  # Habilita el acceso por nombre de columna
    return db

# Cierra la conexión abierta a la base de datos
def cerrarConexion():
    global db
    if db is not None:
        db.close()
        db = None

# ------------------------- RUTAS Y FUNCIONES RELACIONADAS A SQLITE -------------------------

# Prueba básica: cuenta cuántos registros hay en la tabla "usuarios"
@app.route("/sqlite/test-db")
def testDB():
    conexion = abrirConexion()
    cursor = conexion.cursor()  # Crea un cursor para ejecutar sentencias SQL
    cursor.execute("SELECT COUNT(*) AS cant FROM usuarios; ")  # Ejecuta consulta SQL
    res = cursor.fetchone()  # Obtiene una única fila del resultado (espera un COUNT)
    registros = res["cant"]  # Accede al campo "cant" desde el dict retornado
    cerrarConexion()
    return f"Hay {registros} registros en la tabla usuarios"

# Devuelve todos los usuarios registrados en la base
@app.route("/sqlite/usuarios/")
def obterGente():
    conexion = abrirConexion()
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM usuarios')  # Trae todas las filas de la tabla "usuarios"
    resultado = cursor.fetchall()  # Recupera todas las filas del resultado
    cerrarConexion()
    fila = [dict(row) for row in resultado]  # Convierte cada fila a diccionario
    return str(fila)  # Devuelve como string para visualización en navegador

# Inserta un nuevo usuario con su email
@app.route("/sqlite/insert/<string:usuario>/<string:email>")
def testInsert(usuario, email):
    conexion = abrirConexion()
    cursor = conexion.cursor()
    db.execute("INSERT INTO usuarios (usuario, email) VALUES (?, ?);", (usuario, email,))
    # Usa placeholders (?) para prevenir inyecciones SQL
    db.commit()  # Confirma los cambios en la base (necesario para INSERT/DELETE/UPDATE)
    cursor.execute("SELECT COUNT(*) AS cant FROM usuarios; ")
    res = cursor.fetchone()
    registros = res["cant"]
    cerrarConexion()
    return f"Se insertó a '{usuario}' con email '{email}'. Ahora hay '{registros}' usuarios"

# Elimina un usuario por ID
@app.route("/sqlite/delete/<int:id>")
def testDelete(id):
    conexion = abrirConexion()
    cursor = conexion.cursor()
    db.execute("DELETE FROM usuarios WHERE id=?", (id,))
    db.commit()  # Aplica los cambios de forma permanente
    cursor.execute("SELECT COUNT(*) AS cant FROM usuarios; ")
    res = cursor.fetchone()
    registros = res["cant"]
    cerrarConexion()
    return f"Se borro el id '{id}' en la tabla usuarios. Ahora hay '{registros}' usuarios"

@app.route("/sqlite/cambiar-mail/<string:usuario>/<string:nuevo_email>")
def testUpdate(usuario, nuevo_email):
    conexion = abrirConexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT email FROM usuarios WHERE usuario=?", (usuario,))
    res = cursor.fetchone()
    email_antiguo = res["email"] if res else "No encontrado"
    db.execute("UPDATE usuarios SET email=? WHERE usuario=?", (nuevo_email, usuario,))
    db.commit()  # Guarda los cambios
    cursor.execute("SELECT email FROM usuarios WHERE usuario=?", (usuario,))
    res = cursor.fetchone()
    email_actualizado = res["email"] if res else "No encontrado"
    cerrarConexion()
    return f"Se actualizó el email de '{usuario}': de '{email_antiguo}' a '{email_actualizado}'"
#by papu

# Devuelve los datos de un usuario por ID
@app.route("/sqlite/detalle/<int:id>")
def testDetalle(id):
    conexion = abrirConexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE id=?", (id,))
    resultado = cursor.fetchone()
    cerrarConexion()
    fila = dict(resultado)  # Convierte la fila individual en dict
    return str(fila)

# ------------------------- OTRAS RUTAS UTILITARIAS -------------------------

# Página principal con enlaces generados dinámicamente
@app.route("/")
def main():
    url_hola = url_for("saludar")
    url_dado = url_for("dado", caras = 6)
    url_logo = url_for("static", filename="img/golang-tonoto.png")
    url_sumar = url_for("suma", n1 = 1, n2 = 9)
    url_palindromo = url_for("es_palindromo", palabra = "spinetta")

    return f"""
    <a href=\"{url_hola}\">Hola</a><br>
    <a href=\"{url_for("despedida")}\">Chau</a><br>
    <a href=\"{url_logo}\">Logo</a><br>
    <a href=\"{url_dado}\">Tirar Dado</a><br>
    <a href=\"{url_sumar}\">Sumar Dos Números</a><br>
    <a href=\"{url_palindromo}\">Saber si una palabra es palíndromo o no</a>
    """

# Devuelve "Hola" plano
@app.route("/hola")
def saludar():
    return "<h2>Hola</h2>"

# Devuelve saludo personalizado
@app.route("/hola/<string:nombre>")
def saludar_con_nombre(nombre):
    return f"<h2>Hola {nombre}</h2>"

# Devuelve "Chau" plano
@app.route("/chau")
def despedida():
    return "<h2>Chau</h2>"

# Devuelve despedida personalizada
@app.route("/chau/<string:nombre>")
def despedir_con_nombre(nombre):
    return f"<h2>Chau {nombre} </h2>"

# Simula el lanzamiento de un dado
@app.route("/dado/<int:caras>")
def dado(caras):
    from random import randint
    numero = randint(1, caras)  # Número aleatorio entre 1 y el número de caras
    return f"<h2>Dado de {caras} caras, salio '{numero}'</h2>"

# Suma dos números enteros
@app.route("/sumar/<int:n1>/<int:n2>")
def suma(n1, n2):
    suma = n1 + n2
    return f"<h2>{n1} mas {n2} da '{suma}'</h2>"

# Verifica si una palabra es palíndromo
@app.route("/palindromo/<string:palabra>")
def es_palindromo(palabra):
    palabra = palabra.lower().replace(" ", "")  # Ignora mayúsculas y espacios
    verificacion = palabra == palabra[::-1]  # Compara la palabra con su reverso
    verificarPalindromo = "es" if verificacion else "no es"
    return f"<h2>La palabra '{palabra}' {verificarPalindromo} un palíndromo.</h2>"