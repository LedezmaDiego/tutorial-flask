from flask import Flask

app = Flask(__name__)

@app.route("/")
def principal():
    return """
    <a href="/hola">Hola</a>
    <a href="/chau">Chau</a>
    <button>waos</button>
"""

@app.route("/hola")
def saludar():
    return "<h2>Hola</h2>"

@app.route("/chau")
def despedida():
    return "<h2>Chau</h2>"