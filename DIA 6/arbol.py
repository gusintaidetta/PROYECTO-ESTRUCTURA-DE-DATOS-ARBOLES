from nodo import Nodo
from trie import Trie  

class ArbolArchivos:
    def __init__(self):
        self.raiz = Nodo(nombre="/", tipo="carpeta")
        self.trie = Trie() 

    # ... (Mantén tu método buscar_nodo_por_ruta igual) ...
    def buscar_nodo_por_ruta(self, ruta: str) -> Nodo:
        if ruta == "/":
            return self.raiz
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
                return None
        return nodo_actual

    def insertar(self, ruta_padre: str, nombre: str, tipo: str, contenido: str = None) -> bool:
        padre = self.buscar_nodo_por_ruta(ruta_padre)
        if not padre:
            print(f"Error: Ruta padre '{ruta_padre}' no existe.")
            return False
        if not padre.es_carpeta():
            print(f"Error: '{ruta_padre}' es un archivo.")
            return False
        
        # Verificar duplicados
        for hijo in padre.children:
            if hijo.nombre == nombre:
                print(f"Error: Ya existe '{nombre}' en '{ruta_padre}'.")
                return False

        nuevo_nodo = Nodo(nombre, tipo, contenido)
        padre.agregar_hijo(nuevo_nodo)
        
        # --- INTEGRACIÓN TRIE (DÍA 6) ---
        self.trie.insertar(nombre) 
        # --------------------------------
        
        return True

    def eliminar(self, ruta: str) -> bool:
        if ruta == "/":
            print("Error: No puedes eliminar la raíz.")
            return False

        nodo = self.buscar_nodo_por_ruta(ruta)
        if not nodo:
            print("Error: Nodo no encontrado.")
            return False
            
        padre = nodo.padre
        if padre:
            padre.eliminar_hijo(nodo)
            
            # --- INTEGRACIÓN TRIE (DÍA 6) ---
            # Nota: Al eliminar, borramos el nombre del índice.
            # Si hay otros archivos con el mismo nombre en otras carpetas,
            # esto podría requerir una lógica más avanzada (contador),
            # pero para este proyecto básico, eliminarlo está bien.
            self.trie.eliminar(nodo.nombre)
            # --------------------------------
            return True
        return False

    def renombrar(self, ruta: str, nuevo_nombre: str) -> bool:
        """Cambia el nombre de un nodo y actualiza el Trie."""
        nodo = self.buscar_nodo_por_ruta(ruta)
        if not nodo:
            print("Error: Nodo no encontrado.")
            return False
        
        # Verificar que el nombre no exista ya en el mismo directorio
        padre = nodo.padre
        for hijo in padre.children:
            if hijo.nombre == nuevo_nombre:
                print(f"Error: Ya existe un archivo llamado '{nuevo_nombre}' aquí.")
                return False

        # --- INTEGRACIÓN TRIE ---
        self.trie.eliminar(nodo.nombre) # Sacar el nombre viejo
        nodo.nombre = nuevo_nombre
        self.trie.insertar(nuevo_nombre) # Meter el nombre nuevo
        # ------------------------
        return True

    def autocompletar(self, prefijo: str):
        """Usa el Trie para sugerir nombres."""
        return self.trie.buscar_palabras_por_prefijo(prefijo)

    # ... (Mantén mover y calcular_tamano igual) ...
    def mover(self, ruta_origen: str, ruta_destino: str) -> bool:
        # (Copia el código de mover que te di en el día 2-3)
        # El mover no afecta al Trie porque el nombre del archivo no cambia, solo su ubicación.
        nodo = self.buscar_nodo_por_ruta(ruta_origen)
        nuevo_padre = self.buscar_nodo_por_ruta(ruta_destino)

        if not nodo or not nuevo_padre:
            return False
        if not nuevo_padre.es_carpeta():
            return False
        
        # Validación de ciclo
        tmp = nuevo_padre
        while tmp:
            if tmp == nodo:
                return False
            tmp = tmp.padre

        if nodo.padre:
            nodo.padre.eliminar_hijo(nodo)
        
        nuevo_padre.agregar_hijo(nodo)
        return True
    
    def calcular_tamano(self, nodo=None) -> int:
         # (Copia el código de calcular_tamano del día 2-3)
        if nodo is None:
            nodo = self.raiz
        total = 1 
        for hijo in nodo.children:
            total += self.calcular_tamano(hijo)
        return total
