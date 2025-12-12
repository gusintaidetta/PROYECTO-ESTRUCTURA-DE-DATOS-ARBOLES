from nodo import Nodo
from trie import Trie 
import pickle # Necesario para guardar y cargar el estado (Días 9-10)

class ArbolArchivos:
    def __init__(self):
        self.raiz = Nodo(nombre="/", tipo="carpeta")
        self.trie = Trie() 

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
            print(f"Error: '{ruta_padre}' es un archivo, no puede tener hijos.")
            return False

        # Verificar duplicados
        for hijo in padre.children:
            if hijo.nombre == nombre:
                print(f"Error: Ya existe '{nombre}' en '{ruta_padre}'.")
                return False

        nuevo_nodo = Nodo(nombre, tipo, contenido)
        padre.agregar_hijo(nuevo_nodo)
        
        # Sincronización con el Trie para la búsqueda
        self.trie.insertar(nombre)
        return True

    def eliminar(self, ruta: str) -> bool:
        if ruta == "/":
            print("Error: No puedes eliminar la raíz.")
            return False

        nodo_a_eliminar = self.buscar_nodo_por_ruta(ruta)
        
        if not nodo_a_eliminar:
            print("Error: Nodo no encontrado.")
            return False
            
        padre = nodo_a_eliminar.padre
        if padre:
            padre.eliminar_hijo(nodo_a_eliminar)
            # Sincronización con el Trie
            self.trie.eliminar(nodo_a_eliminar.nombre)
            return True
        return False

    def mover(self, ruta_origen: str, ruta_destino: str) -> bool:
        nodo = self.buscar_nodo_por_ruta(ruta_origen)
        nuevo_padre = self.buscar_nodo_por_ruta(ruta_destino)

        if not nodo or not nuevo_padre:
            print("Error: Origen o destino no válidos.")
            return False

        if not nuevo_padre.es_carpeta():
            print("Error: El destino debe ser una carpeta.")
            return False

        # Validación básica para no mover una carpeta dentro de sí misma
        tmp = nuevo_padre
        while tmp:
            if tmp == nodo:
                print("Error: No puedes mover una carpeta dentro de sí misma.")
                return False
            tmp = tmp.padre

        # Evitar duplicados en el destino
        for hijo in nuevo_padre.children:
            if hijo.nombre == nodo.nombre:
                print(f"Error: Ya existe un elemento llamado '{nodo.nombre}' en el destino.")
                return False

        if nodo.padre:
            nodo.padre.eliminar_hijo(nodo)
        
        nuevo_padre.agregar_hijo(nodo)
        return True

    def renombrar(self, ruta: str, nuevo_nombre: str) -> bool:
        """Cambia el nombre de un nodo y actualiza el Trie."""
        nodo = self.buscar_nodo_por_ruta(ruta)
        if not nodo or ruta == "/":
            print("Error: Nodo no encontrado o no se puede renombrar la raíz.")
            return False
        
        # Verificar que el nombre no exista ya en el padre
        padre = nodo.padre
        for hijo in padre.children:
            if hijo != nodo and hijo.nombre == nuevo_nombre:
                print(f"Error: Ya existe un elemento llamado '{nuevo_nombre}' en esta ubicación.")
                return False

        # Actualizar Trie: Borrar nombre viejo, poner nombre nuevo
        self.trie.eliminar(nodo.nombre)
        nodo.nombre = nuevo_nombre
        self.trie.insertar(nuevo_nombre)
        
        # Reordenar el padre para que el listado siga correcto
        padre.children.sort(key=lambda n: (n.tipo, n.nombre))
        
        return True

    def autocompletar(self, prefijo: str):
        """Devuelve sugerencias para el prefijo dado."""
        return self.trie.buscar_palabras_por_prefijo(prefijo)

    def calcular_tamano(self, nodo=None) -> int:
        if nodo is None:
            nodo = self.raiz
        total = 1
        for hijo in nodo.children:
            total += self.calcular_tamano(hijo)
        return total

    # --- FUNCIONALIDADES DÍA 9-10: PERSISTENCIA ---

    def guardar_estado(self, nombre_archivo="filesystem_state.pickle"):
        """Guarda el objeto ArbolArchivos completo en un archivo usando pickle."""
        try:
            with open(nombre_archivo, 'wb') as f:
                pickle.dump(self, f)
        except Exception as e:
            print(f"Error al guardar el estado: {e}")

    @staticmethod
    def cargar_estado(nombre_archivo="filesystem_state.pickle"):
        """Carga el objeto ArbolArchivos desde un archivo, o crea uno nuevo si no existe."""
        try:
            with open(nombre_archivo, 'rb') as f:
                print("Estado del sistema de archivos cargado exitosamente.")
                return pickle.load(f)
        except FileNotFoundError:
            print("Archivo de estado no encontrado. Creando nuevo sistema de archivos.")
            return ArbolArchivos()
        except Exception as e:
            print(f"Error al cargar el estado: {e}. Creando nuevo sistema de archivos.")
            return ArbolArchivos()
