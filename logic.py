import random

# Diccionario global de vocabularios
vocabularios = {}  # diccionario vacío

def agregar_vocabulario(nombre, simbolos_str, cantidad_esperada):
    # separar, limpiar espacios y eliminar duplicados
    simbolos = [s.strip() for s in simbolos_str.split(",") if s.strip()]
    simbolos = list(dict.fromkeys(simbolos))  # elimina duplicados, mantiene orden
    simbolos = sorted(simbolos)  # para consistencia

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

    for _ in range(cantidad):
        # Elegimos una longitud aleatoria de cadena (ej: entre 1 y 5 símbolos)
        longitud = random.randint(1, 5)

        # La cadena se forma concatenando símbolos del vocabulario
        cadena_simbolos = random.choices(simbolos, k=longitud)

        # Guardamos tanto la cadena unida como su "longitud lógica"
        cadena = "".join(cadena_simbolos)
        cadenas.append(f"{cadena}   (longitud: {len(cadena_simbolos)})")

    return cadenas

def generar_universo(nombre, cantidad=20):
    """
    Genera al menos 'cantidad' cadenas únicas para el universo del discurso W(v).
    """
    if nombre not in vocabularios:
        return f"W({nombre}) = {{}}"

    simbolos = vocabularios[nombre]
    universo = set()
    longitud_actual = 1

    # generar cadenas incrementando longitudes
    while len(universo) < cantidad:
        cadena = "".join(random.choice(simbolos) for _ in range(longitud_actual))
        universo.add(cadena)
        longitud_actual += 1

    universo_str = ", ".join(sorted(universo))
    return f"W({nombre}) = {{ {universo_str} }}"
