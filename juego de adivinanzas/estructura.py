from flask import Flask, render_template, request
import random

app = Flask(__name__)

class JuegoAdivinanza:
    def __init__(self):
        self.palabras = ["manzana", "pera", "plátano", "uva"]
        self.jugadores = {}
        self.respuestas_posibles = ["si", "no", "Tal vez"]

    def asignar_palabra(self, jugador_id):
        palabra = random.choice(self.palabras)
        self.jugadores[jugador_id] = {"palabra": palabra, "turnos_restantes": 3}

    def validar_pregunta(self, jugador_id, pregunta):
        if jugador_id not in self.jugadores:
            return "Jugador no registrado"
        
        palabra_secreta = self.jugadores[jugador_id]["palabra"]
        if pregunta.lower() == palabra_secreta:
            return "si"
        else:
            return random.choice(["no", "Tal vez"])

juego = JuegoAdivinanza()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/iniciar_juego', methods=['POST'])
def iniciar_juego():
    num_jugadores = int(request.form.get('num_jugadores', 1))  # Obtener la cantidad de jugadores del formulario
    for i in range(1, num_jugadores + 1):
        jugador_id = f"jugador_{i}"
        juego.asignar_palabra(jugador_id)
    return "Juego iniciado"

@app.route('/enviar_pregunta', methods=['POST'])
def enviar_pregunta():
    jugador_id = request.form.get('jugador_id')
    pregunta = request.form.get('pregunta')
    if not jugador_id or not pregunta:
        return "Falta información del jugador o la pregunta."
    respuesta = juego.validar_pregunta(jugador_id, pregunta)
    if respuesta == "si":
        juego.jugadores.pop(jugador_id)  # Eliminar al jugador si adivina
    else:
        if jugador_id in juego.jugadores:
            juego.jugadores[jugador_id]["turnos_restantes"] -= 1
    return respuesta

if __name__ == '__main__':
    app.run(debug=True)
