import os
from arbol import ArbolArchivos

class TerminalShell:
    def __init__(self):
        self.arbol = ArbolArchivos()
        self.ruta_actual = "/"     # Siempre empezamos en la raíz.
        self.papelera = []         # Lista temporal para archivos borrados (Papelera)

    def limpiar_pantalla(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def obtener_ruta_absoluta(self, nombre_o_ruta):
        """Ayuda a convertir 'archivo.txt' en '/carpeta/archivo.txt' basado en donde estemos."""
        if nombre_o_ruta == "/":
            return "/"
        
        # Si ya es una ruta absoluta (empieza con /), la dejamos así
        if nombre_o_ruta.startswith("/"):
            return nombre_o_ruta
        
        # Si es relativa, la unimos a la ruta actual
        if self.ruta_actual == "/":
            return f"/{nombre_o_ruta}"
        else:
            return f"{self.ruta_actual}/{nombre_o_ruta}"

    def cmd_ls(self):
        """Listar hijos del directorio actual."""
        nodo_actual = self.arbol.buscar_nodo_por_ruta(self.ruta_actual)
        if not nodo_actual:
            print("Error: Ruta actual no existe.")
            return

        print(f"Contenido de {self.ruta_actual}:")
        if not nodo_actual.children:
            print("  (Vacío)")
        else:
            for hijo in nodo_actual.children:
                tipo_icono = "[D]" if hijo.es_carpeta() else "[F]" # D=Directory, F=File
                print(f"  {tipo_icono} {hijo.nombre}")

    def cmd_cd(self, destino):
        """Cambiar directorio (Change Directory)."""
        if destino == "..":
            # Ir al padre (subir nivel)
            if self.ruta_actual == "/":
                print("Ya estás en la raíz.")
                return
            # Lógica para quitar el último segmento de la ruta
            partes = self.ruta_actual.split("/")
            # partes[:-1] quita el último, luego join une todo de nuevo
            nueva_ruta = "/".join(partes[:-1])
            if nueva_ruta == "": nueva_ruta = "/" # Corrección si volvemos a raiz
            self.ruta_actual = nueva_ruta
        else:
            # Ir a una carpeta hija
            ruta_destino = self.obtener_ruta_absoluta(destino)
            nodo = self.arbol.buscar_nodo_por_ruta(ruta_destino)
            
            if nodo and nodo.es_carpeta():
                self.ruta_actual = ruta_destino
            else:
                print(f"Error: '{destino}' no es una carpeta válida o no existe.")

    def cmd_mkdir(self, nombre):
        """Crear carpeta."""
        self.arbol.insertar(self.ruta_actual, nombre, "carpeta")
        print(f"Carpeta '{nombre}' creada.")

    def cmd_touch(self, nombre, contenido=""):
        """Crear archivo."""
        self.arbol.insertar(self.ruta_actual, nombre, "archivo", contenido)
        print(f"Archivo '{nombre}' creado.")

    def cmd_rm(self, nombre):
        """Eliminar nodo (Mover a papelera)."""
        ruta_completa = self.obtener_ruta_absoluta(nombre)
        nodo = self.arbol.buscar_nodo_por_ruta(ruta_completa)
        
        if nodo:
            # En lugar de borrarlo permanentemente, lo guardamos en la papelera
            # Primero lo desconectamos del árbol real
            if self.arbol.eliminar(ruta_completa):
                self.papelera.append(nodo)
                print(f"'{nombre}' movido a la papelera.")
            else:
                print("Error al eliminar.")
        else:
            print("Elemento no encontrado.")

    def cmd_papelera(self):
        """Mostrar y vaciar papelera."""
        if not self.papelera:
            print("La papelera está vacía.")
            return

        print("--- PAPELERA DE RECICLAJE ---")
        for i, nodo in enumerate(self.papelera):
            print(f"{i+1}. {nodo.nombre} ({nodo.tipo})")
        
        opcion = input("Escribe 'vaciar' para eliminar todo o enter para salir: ")
        if opcion.lower() == "vaciar":
            self.papelera.clear()
            print("Papelera vaciada permanentemente.")

    def cmd_mv(self, origen, destino):
        """Mover archivo/carpeta."""
        ruta_origen = self.obtener_ruta_absoluta(origen)
        ruta_destino = self.obtener_ruta_absoluta(destino)
        
        if self.arbol.mover(ruta_origen, ruta_destino):
            print(f"Movido exitosamente a {ruta_destino}")
        else:
            print("Error al mover. Verifica las rutas.")

    def cmd_search(self, prefijo):
        """Buscar usando el Trie."""
        resultados = self.arbol.autocompletar(prefijo)
        if resultados:
            print(f"Resultados para '{prefijo}':")
            for res in resultados:
                print(f" - {res}")
        else:
            print("No se encontraron coincidencias.")

    def cmd_export_preorden(self):
        """Muestra el árbol en recorrido Preorden (Raíz -> Hijos)."""
        print("\n--- EXPORTAR ARBOL (PREORDEN) ---")
        self._recorrido_preorden_recursivo(self.arbol.raiz, 0)
        print("---------------------------------")

    def _recorrido_preorden_recursivo(self, nodo, nivel):
        indentacion = "  " * nivel
        print(f"{indentacion}- {nodo.nombre} ({nodo.tipo})")
        for hijo in nodo.children:
            self._recorrido_preorden_recursivo(hijo, nivel + 1)

    def iniciar(self):
        self.limpiar_pantalla()
        print("=== SISTEMA DE ARCHIVOS HERMAN - CONSOLA ===")
        print("Comandos: ls, cd, mkdir, touch, rm, mv, search, papelera, export, exit")
        
        while True:
            # Input estilo terminal: /Docs/Tarea $ 
            entrada = input(f"\n{self.ruta_actual} $ ").strip().split()
            
            if not entrada: continue
            
            comando = entrada[0].lower()
            args = entrada[1:]

            if comando == "exit":
                break
            elif comando == "ls":
                self.cmd_ls()
            elif comando == "pwd":
                print(self.ruta_actual)
            elif comando == "cd" and len(args) > 0:
                self.cmd_cd(args[0])
            elif comando == "mkdir" and len(args) > 0:
                self.cmd_mkdir(args[0])
            elif comando == "touch" and len(args) > 0:
                # Permite contenido opcional: touch nota.txt "hola mundo"
                nombre = args[0]
                contenido = " ".join(args[1:]) if len(args) > 1 else ""
                self.cmd_touch(nombre, contenido)
            elif comando == "rm" and len(args) > 0:
                self.cmd_rm(args[0])
            elif comando == "mv" and len(args) == 2:
                self.cmd_mv(args[0], args[1])
            elif comando == "search" and len(args) > 0:
                self.cmd_search(args[0])
            elif comando == "papelera":
                self.cmd_papelera()
            elif comando == "export":
                self.cmd_export_preorden()
            elif comando == "help":
                 print("Ayuda: mkdir [nombre], touch [nombre], rm [nombre], cd [ruta], ls, search [prefijo]")
            else:
                print("Comando no reconocido o argumentos faltantes.")

if __name__ == "__main__":
    app = TerminalShell()
    app.iniciar()

