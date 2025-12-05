from nodo import Nodo 
# Nota: La importación de uuid está ahora en nodo.py, ¡así que mi archivo está más limpio!

class ArbolArchivos:
    """
    Esta clase maneja toda la lógica de mi sistema de archivos, usando los Nodos.
    Implementación completa de los Días 1, 2, 3, 4 y 5.
    """
    def __init__(self):
        # Siempre empiezo con el nodo raíz "/"
        self.raiz = Nodo(nombre="/", tipo="carpeta")

    # =======================================================
    # FUNCIONALIDADES DÍA 1-2 (Búsqueda e Inserción)
    # =======================================================

    def buscar_nodo_por_ruta(self, ruta: str) -> Nodo:
        """
        Esta es mi función más importante. Recorre el árbol para encontrar 
        el nodo que coincide con una ruta como '/Docs/archivo.txt'.
        """
        if ruta == "/":
            return self.raiz
        
        # Quito las barras iniciales/finales y separo la ruta en partes
        partes = [p for p in ruta.split("/") if p]
        nodo_actual = self.raiz
        
        for nombre_objetivo in partes:
            encontrado = False
            for hijo in nodo_actual.children:
                if hijo.nombre == nombre_objetivo:
                    nodo_actual = hijo
                    encontrado = True
                    break
            
            if not encontrado:
                return None # La ruta no existe, no lo encontré
                
        return nodo_actual

    def insertar(self, ruta_padre: str, nombre: str, tipo: str, contenido: str = None) -> bool:
        """Inserta un nuevo archivo o carpeta en la ruta de su padre."""
        padre = self.buscar_nodo_por_ruta(ruta_padre)
        
        if not padre:
            print(f"Error: La ruta padre '{ruta_padre}' no existe.")
            return False
            
        if not padre.es_carpeta():
            print(f"Error: '{ruta_padre}' no es una carpeta, no puedo agregar hijos aquí.")
            return False

        # Chequeo que no exista algo con el mismo nombre en esa carpeta
        for hijo in padre.children:
            if hijo.nombre == nombre:
                print(f"Error: Ya existe '{nombre}' en '{ruta_padre}'.")
                return False

        nuevo_nodo = Nodo(nombre, tipo, contenido)
        padre.agregar_hijo(nuevo_nodo)
        return True

    # =======================================================
    # FUNCIONALIDADES DÍA 3 (Eliminar, Mover, Tamaño)
    # =======================================================

    def eliminar(self, ruta: str) -> bool:
        """Elimina el nodo en la ruta, borrando todo lo que contenga."""
        if ruta == "/":
            print("Error: ¡No puedo eliminar la raíz!")
            return False

        nodo_a_eliminar = self.buscar_nodo_por_ruta(ruta)
        
        if not nodo_a_eliminar:
            print("Error: Nodo no encontrado.")
            return False
            
        padre = nodo_a_eliminar.padre
        if padre:
            padre.eliminar_hijo(nodo_a_eliminar)
            return True
        return False

    def mover(self, ruta_origen: str, ruta_destino: str) -> bool:
        """Mueve un nodo (archivo o carpeta) de un lugar a otro."""
        nodo = self.buscar_nodo_por_ruta(ruta_origen)
        nuevo_padre = self.buscar_nodo_por_ruta(ruta_destino)

        if not nodo or not nuevo_padre:
            print("Error: La ruta de origen o la de destino no son válidas.")
            return False

        if not nuevo_padre.es_carpeta():
            print("Error: El destino debe ser una carpeta para poder mover algo dentro.")
            return False

        # Evito mover una carpeta dentro de sí misma (error de ciclo)
        tmp = nuevo_padre
        while tmp:
            if tmp == nodo:
                print("Error: No puedes mover una carpeta dentro de sí misma o de un subdirectorio.")
                return False
            tmp = tmp.padre
            
        # Evito duplicados en el destino
        for hijo in nuevo_padre.children:
            if hijo.nombre == nodo.nombre:
                print(f"Error: Ya existe un elemento llamado '{nodo.nombre}' en el destino.")
                return False

        # 1. Desconectar del padre anterior
        if nodo.padre:
            nodo.padre.eliminar_hijo(nodo)
        
        # 2. Conectar al nuevo padre
        nuevo_padre.agregar_hijo(nodo)
        return True

    def calcular_tamano(self, nodo=None) -> int:
        """Calcula cuántos archivos y carpetas hay desde el punto dado (recursivo)."""
        if nodo is None:
            nodo = self.raiz
        
        total = 1 # Me cuento a mí mismo (el nodo actual)
        for hijo in nodo.children:
            total += self.calcular_tamano(hijo)
        return total

    # =======================================================
    # FUNCIONALIDADES DÍA 4 (Listar y Modificar)
    # =======================================================

    def listar_contenido(self, ruta: str) -> list:
        """
        Muestra una lista de los elementos dentro de una carpeta (simula el comando 'ls').
        """
        nodo = self.buscar_nodo_por_ruta(ruta)

        if not nodo:
            print(f"Error: La ruta '{ruta}' no existe.")
            return []
        
        if nodo.es_carpeta():
            # Devuelvo una lista de tuplas (tipo, nombre)
            return [(hijo.tipo, hijo.nombre) for hijo in nodo.children]
        else:
            # Si es un archivo, solo me muestro a mí mismo
            return [(nodo.tipo, nodo.nombre)]


    def modificar_contenido(self, ruta: str, nuevo_contenido: str) -> bool:
        """
        Me permite cambiar el texto dentro de un archivo (simula un comando 'edit').
        """
        nodo = self.buscar_nodo_por_ruta(ruta)

        if not nodo:
            print(f"Error: La ruta '{ruta}' no existe.")
            return False

        if nodo.es_carpeta():
            print(f"Error: '{ruta}' es una carpeta, no puedo modificar su contenido de texto.")
            return False

        # ¡Es un archivo! Actualizo el contenido.
        nodo.contenido = nuevo_contenido
        return True

    # =======================================================
    # FUNCIONALIDADES DÍA 5 (Leer y Renombrar)
    # =======================================================

    def leer_archivo(self, ruta: str) -> str:
        """
        Retorna el contenido completo de un archivo (simula el comando 'cat').
        """
        nodo = self.buscar_nodo_por_ruta(ruta)

        if not nodo:
            return f"Error: Archivo o ruta '{ruta}' no encontrado."

        if nodo.es_carpeta():
            return f"Error: '{ruta}' es una carpeta, no puedo leer su contenido como archivo."
        
        # Devolver el contenido del archivo
        return nodo.contenido if nodo.contenido is not None else "El archivo está vacío."

    def renombrar(self, ruta: str, nuevo_nombre: str) -> bool:
        """
        Cambia el nombre de un archivo o carpeta en la ruta especificada.
        """
        nodo = self.buscar_nodo_por_ruta(ruta)

        if not nodo or ruta == "/":
            print(f"Error: Nodo en '{ruta}' no encontrado o no se puede renombrar la raíz.")
            return False

        padre = nodo.padre
        
        # Validación: Evitar duplicados en el mismo directorio
        for hijo in padre.children:
            if hijo != nodo and hijo.nombre == nuevo_nombre:
                print(f"Error: Ya existe un elemento llamado '{nuevo_nombre}' en esta ubicación.")
                return False

        # Cambiar el nombre
        nodo.nombre = nuevo_nombre
        
        # Vuelvo a ordenar los hijos de la carpeta padre para que el 'ls' siga siendo correcto
        # (El método Nodo.agregar_hijo maneja el sort, pero como solo renombramos,
        # lo forzamos en el padre).
        padre.children.sort(key=lambda n: (n.tipo, n.nombre))
        
        return True


    # =======================================================
    # UTILIDAD: Visualización del Árbol (para depuración)
    # =======================================================

    def mostrar_arbol(self):
        """Función auxiliar que me ayuda a ver la estructura completa del árbol."""
        print("\n--- Estructura del Árbol de Archivos ---")
        self._mostrar_arbol_recursivo(self.raiz)
        print("---------------------------------------")

    def _mostrar_arbol_recursivo(self, nodo, prefijo=""):
        """Función recursiva para dibujar el árbol con indentación."""
        
        simbolo = "[CARPETA]" if nodo.es_carpeta() else "[ARCHIVO]"
        
        # Muestro el nodo actual
        linea = f"{prefijo}{simbolo} {nodo.nombre}"
        if not nodo.es_carpeta():
            # Si es archivo, muestro un pedacito de su contenido
            extracto = nodo.contenido[:30].replace('\n', ' ') + "..." if nodo.contenido and len(nodo.contenido) > 30 else nodo.contenido
            linea += f" (Contenido: '{extracto}')" if extracto else " (Vacío)"
            
        print(linea)
        
        # Recorro a los hijos
        num_hijos = len(nodo.children)
        for i, hijo in enumerate(nodo.children):
            # Calculo el prefijo para dibujar las líneas de conexión (como un árbol)
            es_ultimo = (i == num_hijos - 1)
            
            if es_ultimo:
                conexion = "└── "
                nuevo_prefijo = prefijo + "    "
            else:
                conexion = "├── "
                nuevo_prefijo = prefijo + "│   "
            
            self._mostrar_arbol_recursivo(hijo, nuevo_prefijo)

# =======================================================
# EJEMPLO DE USO Y PRUEBA COMPLETA DE DÍAS 1-5
# =======================================================
if __name__ == "__main__":
    fs = ArbolArchivos()
    print("Iniciando mis pruebas del Sistema de Archivos (Días 1-5)")

    # 1. Creamos mi estructura de archivos inicial (Día 1-2)
    fs.insertar("/", "Documentos", "carpeta")
    fs.insertar("/Documentos", "Reporte.txt", "archivo", "Primer borrador del informe. Faltan detalles.")
    fs.insertar("/Documentos", "Fotos", "carpeta")
    fs.insertar("/Documentos/Fotos", "perro.jpg", "archivo", "Una foto del perro salchicha.")
    fs.insertar("/", "Apps", "carpeta")
    fs.insertar("/Apps", "main.py", "archivo", "print('Hola mundo')")
    
    fs.mostrar_arbol()

    # --- PRUEBAS DEL DÍA 5 ---

    # 2. Prueba de Leer Archivo (Día 5)
    print("\n--- Prueba de Leer Archivo (cat) ---")
    print(f"Contenido de '/Apps/main.py':\n{fs.leer_archivo('/Apps/main.py')}")

    # Pruebo casos de error al leer
    print(fs.leer_archivo('/Documentos')) # Error: Es carpeta
    print(fs.leer_archivo('/Inexistente')) # Error: No existe

    # 3. Prueba de Renombrar (Día 5)
    print("\n--- Prueba de Renombrar ---")
    
    # Renombrar un archivo
    fs.renombrar("/Documentos/Reporte.txt", "Informe_Final.txt")
    print("Renombrado '/Documentos/Reporte.txt' a 'Informe_Final.txt'.")
    
    # Renombrar una carpeta
    fs.renombrar("/Apps", "Programas")
    print("Renombrado '/Apps' a 'Programas'.")

    # Pruebo caso de error al renombrar un duplicado
    fs.renombrar("/Documentos/Fotos", "Informe_Final.txt") # ¡Debe fallar!

    # 4. Verifico la estructura final después de renombrar y listado (Día 4)
    print("\n--- Estructura final (Verificación) ---")
    fs.mostrar_arbol()
    
    # Pruebo el listado en la nueva carpeta renombrada
    print("\n--- Listado en '/Programas' ---")
    print(fs.listar_contenido("/Programas"))
