from flask import Flask, render_template, request
import logic

app = Flask(__name__)

# Variables globales para mantener estado
resultado_global = []
universo_global = ""

@app.route("/", methods=["GET", "POST"])
def index():
    global resultado_global, universo_global  # usamos las globales

    if request.method == "POST":
        action = request.form.get("action")

        if action == "add_vocab":
            nombre = request.form.get("nombre")
            simbolos_str = request.form.get("simbolos")
            cantidad_esperada = int(request.form.get("cantidad_signos", 0))

            exito, mensaje = logic.agregar_vocabulario(nombre, simbolos_str, cantidad_esperada)
            if not exito:
                resultado_global = [mensaje]
            else:
                resultado_global = [mensaje]

        elif action == "generar_cadenas":
            vocab = request.form.get("vocab")
            cantidad = int(request.form.get("cantidad_cadenas", 0))
            resultado_global = logic.generar_cadenas_diferentes(vocab, cantidad)

        elif action == "generar_universo":
            vocab = request.form.get("vocab")
            universo_global = logic.generar_universo(vocab)

    return render_template(
        "index.html",
        vocabularios=logic.obtener_vocabularios(),
        resultado=resultado_global,
        universo=universo_global
    )

if __name__ == "__main__":
    app.run(debug=True)
