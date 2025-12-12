import os
from arbol import ArbolArchivos

# Nombre del archivo donde se guardará el estado del sistema
ARCHIVO_ESTADO = "filesystem_state.pickle"

class TerminalShell:
    def __init__(self):
        # Cargar el estado al iniciar (Día 9-10)
        self.arbol = ArbolArchivos.cargar_estado(ARCHIVO_ESTADO)
        self.ruta_actual = "/"     
        self.papelera = []         

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
        if self.arbol.insertar(self.ruta_actual, nombre, "carpeta"):
            print(f"Carpeta '{nombre}' creada.")

    def cmd_touch(self, nombre, contenido=""):
        """Crear archivo."""
        if self.arbol.insertar(self.ruta_actual, nombre, "archivo", contenido):
            print(f"Archivo '{nombre}' creado.")

    def cmd_rm(self, nombre):
        """Eliminar nodo (Mover a papelera)."""
        ruta_completa = self.obtener_ruta_absoluta(nombre)
        nodo = self.arbol.buscar_nodo_por_ruta(ruta_completa)
        
        if nodo:
            # En lugar de borrarlo permanentemente, lo guardamos en la papelera
            if self.arbol.eliminar(ruta_completa):
                self.papelera.append(nodo)
                print(f"'{nombre}' movido a la papelera.")
            else:
                print("Error al intentar eliminar.")
        else:
            print("Elemento no encontrado.")

    def cmd_mv(self, origen, destino):
        """Mover archivo/carpeta."""
        ruta_origen = self.obtener_ruta_absoluta(origen)
        ruta_destino = self.obtener_ruta_absoluta(destino)
        
        if self.arbol.mover(ruta_origen, ruta_destino):
            print(f"Movido exitosamente a {ruta_destino}")

    def cmd_rn(self, ruta, nuevo_nombre):
        """Renombrar archivo/carpeta."""
        ruta_completa = self.obtener_ruta_absoluta(ruta)
        
        if self.arbol.renombrar(ruta_completa, nuevo_nombre):
            print(f"Renombrado '{ruta}' a '{nuevo_nombre}'")

    def cmd_search(self, prefijo):
        """Buscar usando el Trie."""
        resultados = self.arbol.autocompletar(prefijo)
        if resultados:
            print(f"Resultados para '{prefijo}':")
            for res in resultados:
                print(f" - {res}")
        else:
            print("No se encontraron coincidencias.")

    def cmd_papelera(self):
        """Mostrar y vaciar papelera."""
        if not self.papelera:
            print("La papelera está vacía.")
            return

        print("--- PAPELERA DE RECICLAJE ---")
        for i, nodo in enumerate(self.papelera):
            print(f"{i+1}. {nodo.nombre} ({nodo.tipo}) [ID: {nodo.id[:8]}]")
        
        opcion = input("Escribe 'vaciar' para eliminar todo permanentemente, o 'restaurar [número]' para recuperar un archivo: ")
        
        if opcion.lower() == "vaciar":
            self.papelera.clear()
            print("Papelera vaciada permanentemente.")
        elif opcion.lower().startswith("restaurar"):
            try:
                indice = int(opcion.split()[1]) - 1
                if 0 <= indice < len(self.papelera):
                    # NOTA: Restauramos a la raíz por simplicidad.
                    nodo_a_restaurar = self.papelera.pop(indice)
                    
                    # Reinsertar en la raíz
                    if self.arbol.insertar("/", nodo_a_restaurar.nombre, nodo_a_restaurar.tipo, nodo_a_restaurar.contenido):
                        # Reinsertar el nombre en el Trie (ya que se eliminó en cmd_rm)
                        self.arbol.trie.insertar(nodo_a_restaurar.nombre)
                        print(f"'{nodo_a_restaurar.nombre}' restaurado a la raíz (/)")
                    else:
                        # Si falla (ej: ya existe un archivo con ese nombre en /), lo volvemos a poner en la papelera
                        self.papelera.insert(indice, nodo_a_restaurar)
                        print("Error al restaurar: Ya existe un archivo con ese nombre en la raíz.")
                else:
                    print("Número de archivo inválido.")
            except (ValueError, IndexError):
                print("Comando de restauración inválido. Usa: restaurar [número]")


    def cmd_export_preorden(self):
        """Muestra el árbol en recorrido Preorden (Raíz -> Hijos)."""
        print("\n--- EXPORTAR ARBOL (PREORDEN) ---")
        self._recorrido_preorden_recursivo(self.arbol.raiz, 0)
        print("---------------------------------")

    def _recorrido_preorden_recursivo(self, nodo, nivel):
        indentacion = "  " * nivel
        print(f"{indentacion}- {nodo.nombre} ({nodo.tipo}) [ID: {nodo.id[:8]}]")
        for hijo in nodo.children:
            self._recorrido_preorden_recursivo(hijo, nivel + 1)

    def iniciar(self):
        self.limpiar_pantalla()
        print("=== SISTEMA DE ARCHIVOS CONSOLA ===")
        print(f"Estado inicial: {self.ruta_actual}")
        print("Comandos: ls, cd, mkdir, touch, rm, mv, rn, search, papelera, export, exit")
        
        while True:
            # Input estilo terminal: /Docs/Tarea $ 
            entrada = input(f"\n{self.ruta_actual} $ ").strip().split()
            
            if not entrada: continue
            
            comando = entrada[0].lower()
            args = entrada[1:]

            if comando == "exit":
                # Guardar el estado al salir (Día 9-10)
                self.arbol.guardar_estado(ARCHIVO_ESTADO)
                print("Guardando estado y saliendo. ¡Adiós!")
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
            elif comando == "rn" and len(args) == 2:
                self.cmd_rn(args[0], args[1])
            elif comando == "search" and len(args) > 0:
                self.cmd_search(args[0])
            elif comando == "papelera":
                self.cmd_papelera()
            elif comando == "export":
                self.cmd_export_preorden()
            elif comando == "help":
                 print("Ayuda: mkdir [nombre], touch [nombre], rm [nombre], cd [ruta], ls, rn [ruta] [nuevo_nombre], search [prefijo]")
            else:
                print("Comando no reconocido o argumentos faltantes. Escribe 'help' para ver la lista.")

if __name__ == "__main__":
    app = TerminalShell()
    app.iniciar()
