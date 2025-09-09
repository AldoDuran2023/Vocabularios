from flask import Flask, render_template, request
import logic

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = []
    universo = ""

    if request.method == "POST":
        action = request.form.get("action")

        if action == "add_vocab":
            nombre = request.form.get("nombre")
            simbolos_str = request.form.get("simbolos")

            exito = logic.agregar_vocabulario(nombre, simbolos_str)
            if not exito:
                resultado = ["Error: Debes ingresar al menos un símbolo válido."]

        elif action == "generar_cadenas":
            vocab = request.form.get("vocab")
            cantidad = int(request.form.get("cantidad_cadenas", 0))
            resultado = logic.generar_cadenas_diferentes(vocab, cantidad)

        elif action == "generar_universo":
            vocab = request.form.get("vocab")
            universo = logic.generar_universo(vocab)

    return render_template(
        "index.html",
        vocabularios=logic.obtener_vocabularios(),
        resultado=resultado,
        universo=universo
    )

if __name__ == "__main__":
    app.run(debug=True)
