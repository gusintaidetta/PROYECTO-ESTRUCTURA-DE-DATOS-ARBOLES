class NodoTrie:
    def __init__(self):
        self.hijos = {}
        self.es_final = False

class Trie:
    def __init__(self):
        self.raiz = NodoTrie()

    def insertar(self, palabra: str):
        nodo = self.raiz
        for char in palabra:
            if char not in nodo.hijos:
                nodo.hijos[char] = NodoTrie()
            nodo = nodo.hijos[char]
        nodo.es_final = True

    def buscar_palabras_por_prefijo(self, prefijo: str):
        """Retorna una lista de palabras que empiezan con el prefijo dado."""
        nodo = self.raiz
        # 1. Navegar hasta el final del prefijo
        for char in prefijo:
            if char not in nodo.hijos:
                return [] # No hay coincidencias
            nodo = nodo.hijos[char]
        
        # 2. Recolectar todas las palabras a partir de ahí
        resultados = []
        self._recolectar(nodo, prefijo, resultados)
        return resultados

    def _recolectar(self, nodo, prefijo_actual, resultados):
        if nodo.es_final:
            resultados.append(prefijo_actual)
        
        for char, nodo_hijo in nodo.hijos.items():
            self._recolectar(nodo_hijo, prefijo_actual + char, resultados)

    def eliminar(self, palabra: str):
        """Elimina una palabra del Trie (necesario si borras/renombras archivos)"""
        def _eliminar_recursivo(nodo, palabra, profundidad):
            if profundidad == len(palabra):
                if not nodo.es_final:
                    return False # La palabra no existía
                nodo.es_final = False
                return len(nodo.hijos) == 0 # ¿Se puede borrar este nodo?

            char = palabra[profundidad]
            if char not in nodo.hijos:
                return False

            debe_borrar_hijo = _eliminar_recursivo(nodo.hijos[char], palabra, profundidad + 1)

            if debe_borrar_hijo:
                del nodo.hijos[char]
                return len(nodo.hijos) == 0 and not nodo.es_final
            
            return False

        _eliminar_recursivo(self.raiz, palabra, 0)
