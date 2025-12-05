from nodo import Nodo

class ArbolArchivos:
    def __init__(self):
        # Inicializa el árbol con un nodo raíz siempre existente
        self.raiz = Nodo(nombre="/", tipo="carpeta")

    def buscar_nodo_por_ruta(self, ruta: str) -> Nodo:
        """
        Recorre el árbol siguiendo una ruta estilo '/carpeta/archivo'
        Retorna el objeto Nodo si existe, o None si no.
        """
        if ruta == "/":
            return self.raiz
        
        # Separar la ruta en partes, ej: "/Docs/Tarea" -> ["Docs", "Tarea"]
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
                return None # La ruta está rota o no existe
                
        return nodo_actual

    def insertar(self, ruta_padre: str, nombre: str, tipo: str, contenido: str = None) -> bool:
        """Crea un nodo y lo agrega debajo del padre especificado."""
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
        return True

    def eliminar(self, ruta: str) -> bool:
        """Elimina el nodo en la ruta especificada y todos sus descendientes."""
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
            return True
        return False

    def mover(self, ruta_origen: str, ruta_destino: str) -> bool:
        """Mueve un nodo de una ruta a otra (cambia de padre)."""
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

        # Desconectar del padre anterior y conectar al nuevo
        if nodo.padre:
            nodo.padre.eliminar_hijo(nodo)
        
        nuevo_padre.agregar_hijo(nodo)
        return True

    def calcular_tamano(self, nodo=None) -> int:
        """Retorna la cantidad total de nodos (archivos + carpetas) desde el punto dado."""
        if nodo is None:
            nodo = self.raiz
        
        total = 1 # Contamos el nodo actual
        for hijo in nodo.children:
            total += self.calcular_tamano(hijo)
        return total
