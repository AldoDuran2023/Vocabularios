import random

# Diccionario global de vocabularios
vocabularios = {}  # diccionario vacío

def agregar_vocabulario(nombre, simbolos_str, cantidad_esperada):
    # separar, limpiar espacios y eliminar duplicados
    simbolos = [s.strip() for s in simbolos_str.split(",") if s.strip()]
    simbolos = list(set(simbolos)) # elimina duplicados
    simbolos = sorted(simbolos)

    if not simbolos:
        return False, "Error: Debes ingresar al menos un símbolo válido."

    if len(simbolos) != cantidad_esperada:
        return False, f"Error: Dijiste {cantidad_esperada} signos, pero ingresaste {len(simbolos)} únicos."

    vocabularios[nombre] = simbolos
    return True, f"Vocabulario {nombre} agregado correctamente."


def obtener_vocabularios():
    return vocabularios

def generar_cadenas_diferentes(nombre_vocab, cantidad):
    if nombre_vocab not in vocabularios:
        return ["Error: Vocabulario no existe"]

    simbolos = vocabularios[nombre_vocab]
    cadenas = []

    # Aseguramos longitudes únicas desde 1 hasta "cantidad"
    for longitud in range(1, cantidad + 1):
        # Se construye una cadena con "longitud" símbolos
        cadena_simbolos = random.choices(simbolos, k=longitud)
        cadena = "".join(cadena_simbolos)
        cadenas.append(f"{cadena}   (longitud: {longitud})")

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

    return f"W({nombre_vocab}) = {{" + ",".join(universo[:minimo]) + "}}"