import random

# Diccionario global de vocabularios
vocabularios = {}  # diccionario vacío
cantidad_vocab_esperada = 0
contador_vocab_ingresados = 0

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
        cadenas.append(f"{cadena}   (longitud: {longitud})")

    # Mezclamos las cadenas para que salgan en orden aleatorio
    random.shuffle(cadenas)

    return cadenas

def generar_universo(nombre_vocab, minimo=20):
    if nombre_vocab not in vocabularios:
        return "Error: Vocabulario no existe"

    simbolos = vocabularios[nombre_vocab]
    universo = ["Ø"]

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

    return f"W({nombre_vocab}) = {{{', '.join(universo[:minimo])}, ...}}"