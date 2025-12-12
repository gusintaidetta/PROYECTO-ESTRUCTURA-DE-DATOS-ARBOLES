import time
import random
import string
from arbol import ArbolArchivos

def generar_nombre_random(longitud=8):
    """Genera un nombre aleatorio como 'xkjhqwei'"""
    letras = string.ascii_lowercase
    return ''.join(random.choice(letras) for i in range(longitud))

def prueba_stress():
    print("=== INICIANDO PRUEBA DE PERFORMANCE (DÍA 10-11) ===")
    arbol = ArbolArchivos()
    
    CANTIDAD_NODOS = 5000 # Puedes subirlo a 10000 o más
    
    print(f"1. Generando {CANTIDAD_NODOS} archivos en memoria...")
    
    start_time = time.time()
    
    # Creamos una estructura plana para estresar la inserción
    # Insertaremos todo en la raíz para probar colisiones y velocidad de lista
    for i in range(CANTIDAD_NODOS):
        nombre = f"archivo_{i}_{generar_nombre_random(5)}.txt"
        arbol.insertar("/", nombre, "archivo", "contenido prueba")
        
        # Cada 1000 nodos imprimimos progreso
        if i % 1000 == 0:
            print(f"   Creados {i} nodos...")
            
    end_time = time.time()
    duracion = end_time - start_time
    print(f"-> Tiempo de Inserción: {duracion:.4f} segundos")
    print(f"-> Promedio: {duracion/CANTIDAD_NODOS:.6f} seg/nodo")

    print("\n2. Probando Búsqueda Exacta (Hash Map / Recorrido)...")
    objetivo = arbol.raiz.children[-1].nombre # Buscar el último creado
    
    start_time = time.time()
    nodo = arbol.buscar_nodo_por_ruta(f"/{objetivo}")
    end_time = time.time()
    
    if nodo:
        print(f"-> Encontrado: {nodo.nombre}")
        print(f"-> Tiempo de Búsqueda: {end_time - start_time:.6f} segundos")
    else:
        print("Error: No se encontró el nodo.")

    print("\n3. Probando Autocompletado (Trie)...")
    prefijo = "archivo_100" # Debería traer varios
    start_time = time.time()
    resultados = arbol.autocompletar(prefijo)
    end_time = time.time()
    
    print(f"-> Coincidencias encontradas: {len(resultados)}")
    print(f"-> Tiempo de Trie: {end_time - start_time:.6f} segundos")
    
    print("\n=== PRUEBA FINALIZADA ===")

if __name__ == "__main__":
    prueba_stress()
