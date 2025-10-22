import random

# Diccionario global de vocabularios
vocabularios = {}  # diccionario vacío
cantidad_vocab_esperada = 0
contador_vocab_ingresados = 0
universo = []

def set_cantidad_vocab(cantidad):
    global cantidad_vocab_esperada, contador_vocab_ingresados, vocabularios
    cantidad_vocab_esperada = cantidad
    contador_vocab_ingresados = 0
    vocabularios = {}  # Reiniciar por si había datos antes
    return f"Debes ingresar {cantidad} vocabularios."

def agregar_vocabulario(nombre, simbolos_str, cantidad_esperada):
    global contador_vocab_ingresados, cantidad_vocab_esperada

    if cantidad_vocab_esperada == 0:
        return False, "Primero debes indicar la cantidad de vocabularios."

    if contador_vocab_ingresados >= cantidad_vocab_esperada:
        return False, f"Ya se ingresaron los {cantidad_vocab_esperada} vocabularios permitidos."

    if nombre in vocabularios:
        return False, f"Error: Ya existe un vocabulario con el nombre '{nombre}'."

    # separar, limpiar espacios y eliminar duplicados
    simbolos = [s.strip() for s in simbolos_str.split(",") if s.strip()]
    simbolos = list(set(simbolos))  # elimina duplicados
    simbolos = sorted(simbolos)

    if not simbolos:
        return False, "Error: Debes ingresar al menos un símbolo válido."

    if len(simbolos) != cantidad_esperada:
        return False, f"Error: Dijiste {cantidad_esperada} signos, pero ingresaste {len(simbolos)} únicos."

    vocabularios[nombre] = simbolos
    contador_vocab_ingresados += 1

    if contador_vocab_ingresados == cantidad_vocab_esperada:
        return True, f"Vocabulario {nombre} agregado ({contador_vocab_ingresados}/{cantidad_vocab_esperada}). Ya completaste todos."
    else:
        return True, f"Vocabulario {nombre} agregado correctamente ({contador_vocab_ingresados}/{cantidad_vocab_esperada})."



def obtener_vocabularios():
    return vocabularios

def generar_cadenas_diferentes(nombre_vocab, cantidad):
    if nombre_vocab not in vocabularios:
        return ["Error: Vocabulario no existe"]

    simbolos = vocabularios[nombre_vocab]
    cadenas = []

    # Generamos con longitudes únicas desde 1 hasta "cantidad"
    for longitud in range(1, cantidad + 1):
        cadena_simbolos = random.choices(simbolos, k=longitud)
        cadena = "".join(cadena_simbolos)
        cadenas.append(f"'{cadena}'   (longitud: {longitud})")

    # Mezclamos las cadenas para que salgan en orden aleatorio
    random.shuffle(cadenas)

    return cadenas

def generar_universo(nombre_vocab, minimo=20):
    if nombre_vocab not in vocabularios:
        return None  

    simbolos = vocabularios[nombre_vocab]
    universo = []

    def generar_cadenas(actual, longitud):
        if len(universo) >= minimo:
            return
        if longitud == 0:
            if actual != "":
                universo.append(actual)
            return
        for s in simbolos:
            generar_cadenas(actual + s, longitud - 1)

    longitud = 1
    while len(universo) < minimo:
        generar_cadenas("", longitud)
        longitud += 1

    return universo 

def formatear_universo(nombre_vocab, universo, minimo=20):
    if not universo:
        return f"W({nombre_vocab}) = {{Ø}}"
    return f"W({nombre_vocab}) = {{Ø, {', '.join(universo[:minimo])}, ...}}"



# Diccionario de propiedades disponibles
propiedades_disponibles = {
    # Caracteres
    "empieza_con": ("Empieza con", lambda cad, arg: cad.startswith(arg)),
    "termina_con": ("Termina con", lambda cad, arg: cad.endswith(arg)),
    "contiene": ("Contiene", lambda cad, arg: arg in cad),

    # Números
    "contiene_digitos": ("Contiene dígitos", lambda cad, _: any(c.isdigit() for c in cad)),
    "empieza_numero": ("Empieza con un dígito", lambda cad, _: cad[0].isdigit()),

    # Longitud
    "longitud_exacta": ("Longitud exacta", lambda cad, arg: len(cad) == int(arg)),
    "longitud_min": ("Longitud mínima", lambda cad, arg: len(cad) >= int(arg)),
    "longitud_max": ("Longitud máxima", lambda cad, arg: len(cad) <= int(arg)),
    "longitud_par": ("Longitud par", lambda cad, _: len(cad) % 2 == 0),
    "longitud_impar": ("Longitud impar", lambda cad, _: len(cad) % 2 != 0),
}

# Lista global de lenguajes generados
lenguajes = {}

# limpiar
def limpiar():
    global vocabularios, lenguajes, universo, cantidad_vocab_esperada, contador_vocab_ingresados
    vocabularios = {}
    lenguajes = {}
    universo = None   
    cantidad_vocab_esperada = 0
    contador_vocab_ingresados = 0


# Función para generar un lenguaje
def generar_lenguaje(nombre_vocab, propiedades_ids, args_dict):
    if nombre_vocab not in vocabularios:
        return False, "Error: Vocabulario no existe."

    if len(lenguajes) >= 3:
        return False, "Ya se alcanzó el máximo de 3 lenguajes."
    
    if len(propiedades_ids) == 0:
        return False, "Debes de seleccionar al menos una propiedad."

    props_seleccionadas = set(propiedades_ids)

    # Evitar duplicados
    for lname, datos in lenguajes.items():
        if datos["props"] == props_seleccionadas and lname.endswith(f"({nombre_vocab})"):
            return False, "Ya existe un lenguaje con esas propiedades para este vocabulario."

    # Generar universo
    universo_list = generar_universo(nombre_vocab, minimo=100)
    if not universo_list:
        return False, "Error al generar el universo."

    # Aplicar filtros con argumentos
    lenguaje = []
    for cad in universo_list:
        valido = True
        for pid in props_seleccionadas:
            if pid in propiedades_disponibles:
                label, funcion = propiedades_disponibles[pid]
                arg = args_dict.get(pid, None)  # puede venir vacío
                if not funcion(cad, arg):
                    valido = False
                    break
        if valido:
            lenguaje.append(cad)

    nombre_lenguaje = f"L{len(lenguajes)+1}({nombre_vocab})"
    
    # Si no hay cadenas que cumplan, agregar el vacio
    if not lenguaje:
        lenguaje = ["Ø"]

    lenguajes[nombre_lenguaje] = {
        "vocabulario": nombre_vocab,
        "cadenas": lenguaje,
        "props": props_seleccionadas
    }

    return True, f"Lenguaje {nombre_lenguaje} generado con {len(lenguaje)} cadenas."
