import uuid # Genera identificadores únicos universales(Ids)

class Nodo:
    """
    Esta es mi clase fundamental. Representa un archivo o una carpeta individual
    en mi sistema (Funcionalidades de los Días 1-4).
    """
    def __init__(self, nombre: str, tipo: str, contenido: str = None, padre=None):
        
        # Atributos de identificación
        self.id = str(uuid.uuid4())  # ID único para cada nodo
        self.nombre = nombre         # Nombre del archivo o carpeta.
        self.tipo = tipo.lower()     # 'carpeta' o 'archivo'.
        self.contenido = contenido   
        
        # Atributos de la estructura del árbol (sus jerarquías)
        self.children = []           # Nodos/hijos directos
        self.padre = padre           # Referencia al nodo padre

    def __repr__(self):
        """Método para mostrar de manera legible"""
        return f"<{self.tipo.upper()}: {self.nombre} (ID: {self.id[:8]})>"

    # Métodos auxiliares del árbol 

    def agregar_hijo(self, hijo):
        """
        Añade un nodo a la lista de children, establece el padre, y ordena la lista.
        (Crucial para que el listado sea alfabético, corrección del Día 4).
        """
        hijo.padre = self            # Establece que este nodo es el padre del hijo
        self.children.append(hijo)
        # Ordeno los hijos alfabéticamente (por tipo y luego por nombre)
        self.children.sort(key=lambda n: (n.tipo, n.nombre)) 
        
    def eliminar_hijo(self, hijo):
        """Elimina un nodo hijo de la lista"""
        if hijo in self.children:
            self.children.remove(hijo)
            hijo.padre = None        # El nodo eliminado ya no tiene padre
            return True
        return False
    
    def es_carpeta(self) -> bool:
        """Comprueba si el nodo es de tipo 'carpeta'."""
        return self.tipo == 'carpeta'
