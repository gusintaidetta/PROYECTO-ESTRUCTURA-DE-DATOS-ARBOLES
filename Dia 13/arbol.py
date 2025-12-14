import json
from nodo import Nodo
from trie import Trie

class ArbolArchivos:
    def __init__(self):
        self.raiz = Nodo(nombre="/", tipo="carpeta")
        self.trie = Trie()

    # --- NAVEGACIÓN ---
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

    # --- OPERACIONES ---
    def insertar(self, ruta_padre: str, nombre: str, tipo: str, contenido: str = None) -> bool:
        padre = self.buscar_nodo_por_ruta(ruta_padre)
        if not padre: return False
        if not padre.es_carpeta(): return False

        for hijo in padre.children:
            if hijo.nombre == nombre: return False

        nuevo_nodo = Nodo(nombre, tipo, contenido)
        padre.agregar_hijo(nuevo_nodo)
        self.trie.insertar(nombre) 
        return True

    def eliminar(self, ruta: str) -> bool:
        if ruta == "/": return False
        nodo = self.buscar_nodo_por_ruta(ruta)
        if not nodo: return False
        
        padre = nodo.padre
        if padre:
            padre.eliminar_hijo(nodo)
            self.trie.eliminar(nodo.nombre)
            return True
        return False

    def mover(self, ruta_origen: str, ruta_destino: str) -> bool:
        nodo = self.buscar_nodo_por_ruta(ruta_origen)
        nuevo_padre = self.buscar_nodo_por_ruta(ruta_destino)
        if not nodo or not nuevo_padre: return False
        if not nuevo_padre.es_carpeta(): return False
        
        tmp = nuevo_padre
        while tmp:
            if tmp == nodo: return False
            tmp = tmp.padre

        if nodo.padre:
            nodo.padre.eliminar_hijo(nodo)
        nuevo_padre.agregar_hijo(nodo)
        return True

    def renombrar(self, ruta: str, nuevo_nombre: str) -> bool:
        nodo = self.buscar_nodo_por_ruta(ruta)
        if not nodo: return False
        
        for hijo in nodo.padre.children:
            if hijo.nombre == nuevo_nombre: return False

        self.trie.eliminar(nodo.nombre)
        nodo.nombre = nuevo_nombre
        self.trie.insertar(nuevo_nombre)
        return True

    def autocompletar(self, prefijo: str):
        return self.trie.buscar_palabras_por_prefijo(prefijo)

    # --- PERSISTENCIA (JSON) ---
    def a_diccionario(self, nodo):
        return {
            "id": nodo.id,
            "nombre": nodo.nombre,
            "tipo": nodo.tipo,
            "contenido": nodo.contenido,
            "children": [self.a_diccionario(hijo) for hijo in nodo.children]
        }

    def guardar_json(self, nombre_archivo="sistema_archivos.json"):
        try:
            datos = self.a_diccionario(self.raiz)
            with open(nombre_archivo, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=4)
            print("Datos guardados exitosamente.")
            return True
        except Exception as e:
            print(f"Error al guardar: {e}")
            return False

    def cargar_json(self, nombre_archivo="sistema_archivos.json"):
        try:
            with open(nombre_archivo, 'r', encoding='utf-8') as f:
                datos = json.load(f)
            self.raiz = self._reconstruir_nodo(datos)
            self.trie = Trie() 
            self._reconstruir_trie(self.raiz)
            print("Datos cargados exitosamente.")
            return True
        except FileNotFoundError:
            print("Iniciando con sistema vacío.")
            return False

    def _reconstruir_nodo(self, datos):
        nodo = Nodo(datos["nombre"], datos["tipo"], datos["contenido"])
        nodo.id = datos["id"]
        for hijo_datos in datos["children"]:
            nodo.agregar_hijo(self._reconstruir_nodo(hijo_datos))
        return nodo

    def _reconstruir_trie(self, nodo):
        self.trie.insertar(nodo.nombre)
        for hijo in nodo.children:
            self._reconstruir_trie(hijo)
