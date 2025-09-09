import random

# Diccionario global de vocabularios
vocabularios = {} # diccionario vacio

def agregar_vocabulario(nombre, simbolos_str):
    simbolos = [s.strip() for s in simbolos_str.split(",") if s.strip()]
    simbolos = list(set(simbolos))  # elimina duplicados
    if not simbolos:
        return False
    vocabularios[nombre] = simbolos
    return True

def obtener_vocabularios():
    return vocabularios

def generar_cadenas_diferentes(nombre, cantidad):
    if nombre not in vocabularios:
        return []
    
    max_longitud = cantidad * 2 

    simbolos = vocabularios[nombre]
    cadenas = []
    longitudes_usadas = set()

    while len(cadenas) < cantidad:
        longitud = random.randint(1, max_longitud)
        if longitud in longitudes_usadas:
            continue
        cadena = "".join(random.choice(simbolos) for _ in range(longitud))
        if cadena not in cadenas:
            cadenas.append(cadena)
            longitudes_usadas.add(longitud)

    return cadenas

def generar_universo(nombre, cantidad=21):
    if nombre not in vocabularios:
        return "U = {}"

    max_longitud = cantidad * 2 
    
    simbolos = vocabularios[nombre]
    universo = set()

    while len(universo) < cantidad:
        longitud = random.randint(1, max_longitud)
        cadena = "".join(random.choice(simbolos) for _ in range(longitud))
        universo.add(cadena)

    universo_str = ", ".join(sorted(universo))
    return f"U = {{ {universo_str} }}"
