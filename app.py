# app.py
from flask import Flask, url_for, render_template
import sqlite3
from random import randint

app = Flask(__name__)

# ----------------------
# Rutas básicas
# ----------------------

@app.route("/")
def home():
    """Página principal con enlaces a otras secciones."""
    url_saludo = url_for("mostrar_saludo")
    return f'''
        <a href="{url_saludo}">Saludo</a>
        <br>
        <a href="{url_for("mostrar_despedida")}">Despedida</a>
    '''

@app.route("/saludo")
def mostrar_saludo():
    return "<h2>¡Saludos, persona amable!</h2>"

@app.route("/despedida")
def mostrar_despedida():
    return "<h2>¡Nos vemos, persona agradable!</h2>"

@app.route("/saludo/<string:nombre>")
def saludo_personalizado(nombre):
    return f"<h2>¡Saludos, {nombre}!</h2>"

@app.route("/despedida/<string:nombre>")
def despedida_personalizada(nombre):
    return f"<h2>¡Nos vemos, {nombre}!</h2>"

@app.route("/dado/<int:caras>")
def tirar_dado(caras):
    resultado = randint(1, caras)
    return f"<h2>El dado de {caras} caras dio: {resultado}</h2>"

@app.route("/sumar/<int:n1>/<int:n2>")
def sumar(n1, n2):
    return f"<h2>La suma de {n1} y {n2} es {n1+n2}</h2>"

@app.route("/division/<int:n1>/<int:n2>")
def dividir(n1, n2):
    if n2 == 0:
        return "<h2>No se puede dividir por cero</h2>"
    return f"<h2>La división de {n1} entre {n2} es {n1/n2}</h2>"

@app.route("/espalindromo/<string:palabra>")
def es_palindromo(palabra):
    palabra = palabra.lower()
    palabra = ''.join(filter(str.isalnum, palabra))
    if palabra == palabra[::-1]:
        return f"<h2>La palabra {palabra} es palindromo</h2>"
    else:
        return f"<h2>La palabra {palabra} no es palindromo</h2>"
    

# ----------------------
# Funciones auxiliares de SQLite
# ----------------------

def obtener_conexion():
    conexion = sqlite3.connect("instance/datos.sqlite", timeout=5.0)
    conexion.row_factory = sqlite3.Row
    return conexion

# ----------------------
# Rutas SQLite
# ----------------------

@app.route("/sqlite/usuarios")
def listar_usuarios():
    with obtener_conexion() as conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM usuarios")
        filas = cursor.fetchall()
        usuarios = [dict(fila) for fila in filas]
    return str(usuarios)

@app.route("/sqlite/registro")
def contar_registros():
    with obtener_conexion() as conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT COUNT(*) AS cantidad FROM usuarios")
        cantidad = cursor.fetchone()["cantidad"]
    return f"Hay {cantidad} registros en la tabla usuarios."

@app.route("/sqlite/agregar/<string:usuario>/<string:email>")
def agregar_usuario(usuario, email):
    with obtener_conexion() as conexion:
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO usuarios (usuario, email) VALUES (?, ?)", (usuario, email))
        conexion.commit()
        cursor.execute("SELECT COUNT(*) AS cantidad FROM usuarios")
        cantidad = cursor.fetchone()["cantidad"]
    return f"Se insertó a {usuario} con email {email}. Total: {cantidad} registros."

@app.route("/sqlite/actualizar/<string:usuario>/<string:nuevo_email>")
def actualizar_email(usuario, nuevo_email):
    with obtener_conexion() as conexion:
        cursor = conexion.cursor()
        cursor.execute("UPDATE usuarios SET email=? WHERE usuario=?", (nuevo_email, usuario))
        conexion.commit()
    return f"Correo de {usuario} actualizado a {nuevo_email}."

@app.route("/sqlite/eliminar/<int:usuario_id>")
def eliminar_usuario(usuario_id):
    with obtener_conexion() as conexion:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id=?", (usuario_id,))
        conexion.commit()
    return f"Usuario con ID {usuario_id} eliminado."

@app.route("/sqlite/usuario/<int:usuario_id>")
def obtener_usuario_por_id(usuario_id):
    with obtener_conexion() as conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE id=?", (usuario_id,))
        fila = cursor.fetchone()
    return str(dict(fila)) if fila else "Usuario no encontrado"

# ----------------------
# Templates
# ----------------------


# with ... as ...: : es una forma elegante de cerrar automaticamente un proceso

@app.route("/sqlite/detalle/<int:usuario_id>")
def mostrar_datos_template(usuario_id):
    with obtener_conexion() as conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT id, usuario, email, telefono, direccion FROM usuarios WHERE id=?", (usuario_id,))
        usuario = cursor.fetchone()
    if usuario:
        return render_template("template1.html", **usuario) 
    return "Usuario no encontrado"

# **usuario: Hace que cada clave del diccionario se transforme
# en una variable dentro del template

@app.route("/sqlite/enlaces")
def mostrar_links_usuarios():
    with obtener_conexion() as conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT id, usuario FROM usuarios")
        lista_de_usuarios = cursor.fetchall()
    return render_template("template2.html", usuarios=lista_de_usuarios)

# 'usuarios' (a la izquierda del igual) es el nombre de la 
# variable que se usará dentro del HTML template.
# 'lista_de_usuarios' (a la derecha) es la variable de Python
# que ya tenés en tu código.

# if __name__ == '__main__':
#     app.run(debug=True, threaded=False)