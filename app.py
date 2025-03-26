from flask import Flask

app = Flask(__name__)

@app.route("/")
def principal():
    return """
    <a href="/hola">Hola</a>
    <a href="/chau">Chau</a>
    <button>
    <a href="https://www.google.com/url?sa=t&source=web&rct=j&opi=89978449&url=https://www.youtube.com/watch%3Fv%3DN6ns-_Eo-ns&ved=2ahUKEwjYxMvW_aeMAxV4rpUCHWDCDhUQ78AJegQIDBAB&usg=AOvVaw2TFc-j3m981XdDhOGQJz-l">waos</a>
    </button>
"""

@app.route("/hola")
def saludar():
    return "<h2>Hola</h2>"

@app.route("/hola/<string:nombre>")
def saludar_con_nombre(nombre):
    return f"<h2>Hola {nombre}</h2>"


@app.route("/dado/<int:caras>")
def dado(caras):
    from random import randint
    numero = randint(1, caras)
    return f"<h2>Dado de {caras} caras, salio {numero}</h2>"

@app.route("/sumar/<int:n1>/<int:n2>")
def suma(n1, n2):
    suma = n1 + n2
    return f"<h2>{n1} mas {n2} da {suma}</h2>"

@app.route("/chau")
def despedida():
    return "<h2>Chau</h2>"

@app.route("/palindromo/<string:palabra>")
def es_palindromo(palabra):
    palabra = palabra.lower().replace(" ", "")
    verificacion = palabra == palabra[::-1]
    if verificacion == True:
        verificarPalindromo = "es un palíndromo."
    elif verificacion == False:
        verificarPalindromo = "no es un palíndromo"
    return f"<h2>La palabra {palabra} {verificarPalindromo}</h2>"


