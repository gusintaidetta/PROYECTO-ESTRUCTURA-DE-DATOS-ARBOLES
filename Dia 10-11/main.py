import os
from arbol import ArbolArchivos

class TerminalShell:
    def __init__(self):
        self.arbol = ArbolArchivos()
        self.ruta_actual = "/"
        self.papelera = []

    def obtener_ruta_absoluta(self, nombre_o_ruta):
        if nombre_o_ruta == "/": return "/"
        if nombre_o_ruta.startswith("/"): return nombre_o_ruta
        if self.ruta_actual == "/": return f"/{nombre_o_ruta}"
        return f"{self.ruta_actual}/{nombre_o_ruta}"

    def cmd_ls(self):
        nodo = self.arbol.buscar_nodo_por_ruta(self.ruta_actual)
        if not nodo: 
            print("Error de ruta.")
            return
        print(f"Contenido de {self.ruta_actual}:")
        if not nodo.children: print("  (Vacío)")
        for hijo in nodo.children:
            tipo = "[D]" if hijo.es_carpeta() else "[F]"
            print(f"  {tipo} {hijo.nombre}")

    def iniciar(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=== SISTEMA DE ARCHIVOS HERMAN ===")
        
        # 1. CARGAR DATOS AL INICIAR
        self.arbol.cargar_json()
        
        while True:
            try:
                entrada = input(f"\n{self.ruta_actual} $ ").strip().split()
            except KeyboardInterrupt:
                break
                
            if not entrada: continue
            cmd = entrada[0].lower()
            args = entrada[1:]

            if cmd == "exit":
                # 2. GUARDAR DATOS AL SALIR
                self.arbol.guardar_json()
                break
            
            elif cmd == "ls": self.cmd_ls()
            
            elif cmd == "mkdir" and args:
                self.arbol.insertar(self.ruta_actual, args[0], "carpeta")
            
            elif cmd == "touch" and args:
                cont = " ".join(args[1:]) if len(args) > 1 else ""
                self.arbol.insertar(self.ruta_actual, args[0], "archivo", cont)
            
            elif cmd == "cd" and args:
                if args[0] == "..":
                    partes = self.ruta_actual.split("/")
                    self.ruta_actual = "/".join(partes[:-1]) or "/"
                else:
                    ruta = self.obtener_ruta_absoluta(args[0])
                    nodo = self.arbol.buscar_nodo_por_ruta(ruta)
                    if nodo and nodo.es_carpeta(): self.ruta_actual = ruta
                    else: print("Ruta inválida.")
            
            elif cmd == "rm" and args:
                ruta = self.obtener_ruta_absoluta(args[0])
                if self.arbol.eliminar(ruta): print("Eliminado.")
            
            elif cmd == "search" and args:
                res = self.arbol.autocompletar(args[0])
                print("Resultados:", res)
                
            elif cmd == "help":
                print("Comandos: ls, cd, mkdir, touch, rm, search, exit")
            else:
                print("Comando desconocido.")

if __name__ == "__main__":
    app = TerminalShell()
    app.iniciar()
