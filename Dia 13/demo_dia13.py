import time
import os
import sys
from arbol import ArbolArchivos

# Colores para que la consola se vea profesional
COLOR_TITULO = '\033[95m'
COLOR_ACCION = '\033[94m'
COLOR_EXITO = '\033[92m'
COLOR_RESET = '\033[0m'

def limpiar():
    os.system('cls' if os.name == 'nt' else 'clear')

def narrar(texto):
    """Imprime el texto con una pausa para que puedas hablar."""
    print(f"\n{COLOR_ACCION}>>> {texto}{COLOR_RESET}")
    time.sleep(1.5) # Tiempo para que leas el título
    
def paso_exitoso(mensaje):
    print(f"{COLOR_EXITO}  ✔ {mensaje}{COLOR_RESET}")
    time.sleep(1.0)

def ejecutar_demo():
    limpiar()
    print(f"{COLOR_TITULO}============================================")
    print(" DEMOSTRACIÓN AUTOMATIZADA: PROYECTO HERMAN")
    print("============================================" + COLOR_RESET)
    time.sleep(2)

    # 1. INICIALIZACIÓN
    narrar("PASO 1: Inicializando el Sistema de Archivos...")
    arbol = ArbolArchivos()
    # Limpiamos memoria por si acaso cargó algo viejo
    arbol.raiz.children = [] 
    arbol.trie.raiz.hijos = {}
    paso_exitoso("Sistema iniciado. Raíz creada '/'")

    # 2. CREACIÓN (MKDIR / TOUCH)
    narrar("PASO 2: Creando estructura de carpetas y archivos (Árbol General)...")
    
    # Lista de cosas a crear
    elementos = [
        ("/", "Semestre_1", "carpeta", None),
        ("/", "Juegos", "carpeta", None),
        ("/Semestre_1", "Programacion", "carpeta", None),
        ("/Semestre_1/Programacion", "Proyecto_Arboles.py", "archivo", "print('Hola Mundo')"),
        ("/Semestre_1/Programacion", "Apuntes.txt", "archivo", "Tema: Grafos"),
        ("/Juegos", "Minecraft.exe", "archivo", None),
        ("/Juegos", "Valorant.lnk", "archivo", None)
    ]

    for ruta, nombre, tipo, contenido in elementos:
        arbol.insertar(ruta, nombre, tipo, contenido)
        print(f"  + Creando {tipo}: {ruta}/{nombre}")
        time.sleep(0.3)
    
    paso_exitoso("Estructura base generada.")

    # 3. MOSTRAR PREORDEN
    narrar("PASO 3: Visualización del Árbol (Recorrido Preorden)...")
    print("  (Estructura jerárquica actual):")
    
    def mostrar_preorden(nodo, nivel):
        indent = "    " * nivel
        icono = "📁" if nodo.es_carpeta() else "📄"
        print(f"{indent}{icono} {nodo.nombre}")
        for hijo in nodo.children:
            mostrar_preorden(hijo, nivel + 1)
            
    mostrar_preorden(arbol.raiz, 0)
    time.sleep(3) # Pausa larga para que el profe vea el árbol

    # 4. BÚSQUEDA (TRIE)
    narrar("PASO 4: Probando el Buscador Rápido (Trie)...")
    prefijo = "Pro"
    print(f"  🔍 Buscando archivos que inicien con: '{prefijo}'")
    time.sleep(1)
    
    resultados = arbol.autocompletar(prefijo)
    print(f"  Resultados encontrados: {resultados}")
    
    if "Programacion" in resultados and "Proyecto_Arboles.py" in resultados:
        paso_exitoso("El Trie encontró carpeta y archivo correctamente.")

    # 5. MOVER (MOVE)
    narrar("PASO 5: Moviendo archivos (Cambiando referencias de padres)...")
    print("  Moviendo '/Juegos/Minecraft.exe' a '/Semestre_1' (para esconderlo)")
    arbol.mover("/Juegos/Minecraft.exe", "/Semestre_1")
    
    # Verificar movimiento
    nodo = arbol.buscar_nodo_por_ruta("/Semestre_1/Minecraft.exe")
    if nodo:
        paso_exitoso("Movimiento verificado. Minecraft ahora está en Semestre_1.")

    # 6. ELIMINAR Y PAPELERA
    narrar("PASO 6: Eliminando archivos (Gestión de Papelera)...")
    print("  Eliminando carpeta '/Juegos'...")
    arbol.eliminar("/Juegos")
    
    nodo_borrado = arbol.buscar_nodo_por_ruta("/Juegos")
    if nodo_borrado is None:
        paso_exitoso("Carpeta eliminada del árbol principal.")
        print("  (Nota: El Trie también se actualizó eliminando 'Valorant.lnk')")

    # 7. PERSISTENCIA
    narrar("PASO 7: Guardando estado final (JSON)...")
    arbol.guardar_json("demo_dia13.json")
    paso_exitoso("Archivo 'demo_dia13.json' generado en disco.")

    print(f"\n{COLOR_TITULO}=== DEMOSTRACIÓN FINALIZADA CON ÉXITO ==={COLOR_RESET}")

if __name__ == "__main__":
    ejecutar_demo()
