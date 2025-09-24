from flask import Flask, render_template, request, redirect, url_for, jsonify
import logic

app = Flask(__name__)

resultado_global = []
universo_global = None       
universo_str_global = ""     

@app.route("/", methods=["GET", "POST"])
def index():
    global resultado_global, universo_global, universo_str_global

    universo_str = universo_str_global
    mensaje_alerta = None  # 🔹 nuevo

    if request.method == "POST":
        action = request.form.get("action")

        if action == "set_cantidad":
            try:
                cantidad = int(request.form.get("cantidad_vocab", 0))
            except (TypeError, ValueError):
                cantidad = 0
            mensaje_alerta = logic.set_cantidad_vocab(cantidad)

        elif action == "add_vocab":
            nombre = request.form.get("nombre")
            simbolos_str = request.form.get("simbolos")
            try:
                cantidad_esperada = int(request.form.get("cantidad_signos", 0))
            except (TypeError, ValueError):
                cantidad_esperada = 0
            exito, mensaje = logic.agregar_vocabulario(nombre, simbolos_str, cantidad_esperada)
            mensaje_alerta = mensaje 

        elif action == "generar_cadenas":
            vocab = request.form.get("vocab")
            try:
                cantidad = int(request.form.get("cantidad_cadenas", 0))
            except (TypeError, ValueError):
                cantidad = 0
            resultado_global = logic.generar_cadenas_diferentes(vocab, cantidad)
            mensaje_alerta = f"Se generaron {len(resultado_global)} cadenas."

        elif action == "generar_universo":
            vocab = request.form.get("vocab")
            universo_global = logic.generar_universo(vocab)
            if not universo_global:
                universo_str_global = ""
                mensaje_alerta = "Error al generar el universo."
            else:
                universo_str_global = logic.formatear_universo(vocab, universo_global)
                mensaje_alerta = f"Universo generado para el vocabulario {vocab}."
            universo_str = universo_str_global

        elif action == "generar_lenguaje":
            vocab = request.form.get("vocab")
            props = request.form.getlist("propiedades")

            # Capturamos los argumentos adicionales
            args_dict = {}
            for pid in props:
                arg_val = request.form.get(f"arg_{pid}", None)
                if arg_val and arg_val.strip():
                    args_dict[pid] = arg_val.strip()

            exito, mensaje = logic.generar_lenguaje(vocab, props, args_dict)
            mensaje_alerta = mensaje


        elif action == "reset":
            logic.limpiar()
            resultado_global = []
            universo_global = None
            universo_str_global = ""
            return redirect(url_for("index"))

    return render_template(
        "index.html",
        vocabularios=logic.obtener_vocabularios(),
        resultado=resultado_global,
        universo=universo_str,
        propiedades=logic.propiedades_disponibles,
        lenguajes=logic.lenguajes,
        mensaje_alerta=mensaje_alerta, 
        cantidad_vocab_esperada=logic.cantidad_vocab_esperada,
        contador_vocab_ingresados=logic.contador_vocab_ingresados 
    )


@app.route("/get_simbolos/<vocab>")
def get_simbolos(vocab):
    simbolos = logic.obtener_vocabularios().get(vocab, [])
    return jsonify({"simbolos": simbolos})


if __name__ == "__main__":
    app.run(debug=True)
