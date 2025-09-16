from flask import Flask, render_template, request, redirect, url_for
import logic

app = Flask(__name__)

resultado_global = []
universo_global = None       
universo_str_global = ""     

@app.route("/", methods=["GET", "POST"])
def index():
    global resultado_global, universo_global, universo_str_global

    universo_str = universo_str_global

    if request.method == "POST":
        action = request.form.get("action")

        if action == "set_cantidad":
            try:
                cantidad = int(request.form.get("cantidad_vocab", 0))
            except (TypeError, ValueError):
                cantidad = 0
            resultado_global = [logic.set_cantidad_vocab(cantidad)]

        elif action == "add_vocab":
            nombre = request.form.get("nombre")
            simbolos_str = request.form.get("simbolos")
            try:
                cantidad_esperada = int(request.form.get("cantidad_signos", 0))
            except (TypeError, ValueError):
                cantidad_esperada = 0
            exito, mensaje = logic.agregar_vocabulario(nombre, simbolos_str, cantidad_esperada)
            resultado_global = [mensaje]

        elif action == "generar_cadenas":
            vocab = request.form.get("vocab")
            try:
                cantidad = int(request.form.get("cantidad_cadenas", 0))
            except (TypeError, ValueError):
                cantidad = 0
            resultado_global = logic.generar_cadenas_diferentes(vocab, cantidad)

        elif action == "generar_universo":
            vocab = request.form.get("vocab")
            # generar_universo debe devolver una lista (o None en caso de error)
            universo_global = logic.generar_universo(vocab)
            if not universo_global:
                universo_str_global = ""
                resultado_global = ["Error al generar el universo."]
            else:
                # formatear_universo debe devolver el string tipo "W(V) = {Ø, ...}"
                universo_str_global = logic.formatear_universo(vocab, universo_global)
            universo_str = universo_str_global

        elif action == "generar_lenguaje":
            vocab = request.form.get("vocab")
            props = request.form.getlist("propiedades")  # lista de IDs de propiedades
            exito, mensaje = logic.generar_lenguaje(vocab, props)
            resultado_global = [mensaje]

        elif action == "reset":
            logic.limpiar()
            # reset locales también
            resultado_global = []
            universo_global = None
            universo_str_global = ""
            return redirect(url_for("index"))

    # siempre pasamos 'universo' (string) al template; si está vacío el template debe mostrar el mensaje de 'no generado'
    return render_template(
        "index.html",
        vocabularios=logic.obtener_vocabularios(),
        resultado=resultado_global,
        universo=universo_str,
        propiedades=logic.propiedades_disponibles,
        lenguajes=logic.lenguajes
    )

if __name__ == "__main__":
    app.run(debug=True)
