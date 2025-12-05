import uuid # Genera identificadores únicos universales(Ids)

class Nodo:
    def __init__(self, nombre: str, tipo: str, contenido: str = None, padre=None):
        
        # Atributos de identificación
        self.id = str(uuid.uuid4())  # ID
        self.nombre = nombre         # Nombre del archivo o carpeta.
        self.tipo = tipo             # 'carpeta' o 'archivo'.
        self.contenido = contenido   
        
        # Atributos de la estructura del árbol (sus jerarquías)
        self.children = []           # Nodos/hijos directos
        self.padre = padre           # Referencia al nodo padre (donde esta)

    def __repr__(self):
        """Método para mostrar de manera legible"""
        return f"<{self.tipo.upper()}: {self.nombre} (ID: {self.id[:8]})>"

    # Métodos auxiliares del árbol 

    def agregar_hijo(self, hijo):
        """Añade un nodo a la lista de children y establece la referencia inversa al padre."""
        hijo.padre = self            # Establece que este nodo es el padre del hijo
        self.children.append(hijo)
        
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
