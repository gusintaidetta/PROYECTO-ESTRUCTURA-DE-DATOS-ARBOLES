import uuid # Esto me ayuda a darle un ID único a cada cosa

class Nodo:
    """
    Esta es mi clase fundamental. Representa un archivo o una carpeta individual
    en mi sistema (Funcionalidades de los Días 1-4).
    """
    def __init__(self, nombre: str, tipo: str, contenido: str = None, padre=None):
        
        # Atributos de identificación
        self.id = str(uuid.uuid4())  # ID único para cada nodo (¡Buena idea mía!)
        self.nombre = nombre          # Nombre del archivo o carpeta.
        self.tipo = tipo.lower()      # 'carpeta' o 'archivo'.
        self.contenido = contenido    # Aquí guardo el texto (solo si soy un archivo).
        
        # Atributos de la estructura del árbol (sus jerarquías)
        self.children = []            # Nodos/hijos directos
        self.padre = padre            # Referencia al nodo padre

    def __repr__(self):
        """Representación simple para cuando imprimo el objeto."""
        return f"<{self.tipo.upper()}: {self.nombre} (ID: {self.id[:8]})>"

    # Métodos auxiliares del árbol
    
    def agregar_hijo(self, hijo):
        """
        Añade un nodo a la lista de children, establece el padre, y ¡ORDENA! 
        (Es la corrección clave para que el 'ls' del Día 4 funcione alfabéticamente).
        """
        hijo.padre = self            
        self.children.append(hijo)
        # Aquí ordeno los hijos alfabéticamente (primero carpetas, luego archivos)
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
