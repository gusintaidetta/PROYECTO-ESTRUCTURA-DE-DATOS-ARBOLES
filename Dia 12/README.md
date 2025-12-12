# Sistema de Archivos: Proyecto Árboles

Este proyecto es una mini-aplicación de consola que simula las funciones básicas de un sistema de archivos, como crear carpetas, mover archivos y buscar nombres. Nuestro objetivo principal fue aplicar y entender a fondo las estructuras de **Árboles Generales** y los **Árboles Trie**.

## ¿Qué estructuras usamos y para qué sirven?

El corazón de este proyecto son tres componentes clave:

1.  **Árbol General (La Jerarquía):**
    * **Función:** Modela la relación Padre-Hijo entre carpetas y archivos. Cada elemento es un Nodo en el árbol.
    * **Beneficio:** Permite manejar operaciones de jerarquía de manera eficiente, como navegar entre directorios (`cd`) y mover subárboles completos (carpetas con todo su contenido) de una ruta a otra (`mv`).

2.  **Árbol Trie (El Índice de Búsqueda):**
    * **Función:** Mantiene un índice de todos los nombres de archivos y carpetas en el sistema.
    * **Beneficio:** Nos da una búsqueda por prefijo (autocompletado, comando `search`) extremadamente rápida. Si el usuario escribe "doc", el Trie encuentra todos los archivos que empiezan con esas tres letras sin recorrer el árbol principal.

3.  **Persistencia (JSON):**
    * **Función:** Guardar el estado completo del árbol en un archivo local (`sistema_archivos.json`) cuando cierras el programa y cargarlo al iniciar.
    * **Beneficio:** Mantiene tu trabajo entre sesiones.

## Cómo Ponerlo en Marcha

### Requisitos

Necesitas tener Python 3.x instalado.

### Ejecución

1.  Asegura que los archivos del proyecto estén en la misma carpeta.
2.  Ejecuta desde tu terminal:
    ```bash
    python main.py
    ```
3.  La aplicación intentará cargar el estado desde `sistema_archivos.json`.

### Nota Importante

**Siempre usa el comando `exit` para cerrar la aplicación.** Esto garantiza que todos los cambios que hiciste (archivos creados, movidos, etc.) se guarden correctamente en el JSON.

## Guía de Comandos

La interfaz de consola funciona con comandos directos, similares a cualquier terminal:

| Comando | Sintaxis de Uso | Lo que hace en el Sistema |
| :--- | :--- | :--- |
| **`ls`** | `ls` | Muestra los archivos y carpetas que están dentro de la ubicación actual. |
| **`cd`** | `cd <ruta>` | Te mueve a otra carpeta. Puedes usar rutas completas (absolutas) o relativas. `cd ..` te sube un nivel. |
| **`mkdir`** | `mkdir <nombre>` | Crea una nueva **carpeta**. |
| **`touch`** | `touch <nombre> [contenido]` | Crea un nuevo **archivo**. Puedes ponerle el contenido al lado, si quieres. |
| **`rm`** | `rm <ruta>` | Elimina un archivo o carpeta. |
| **`mv`** | `mv <origen> <destino>` | **Mueve** un elemento (archivo o carpeta) de una ruta a otra. |
| **`renombrar`** | *Necesitas implementar el comando* | Cambia el nombre de un archivo o carpeta. El índice de búsqueda (`Trie`) se debe actualizar. |
| **`search`** | `search <prefijo>` | Usa el **Trie** para encontrar todos los nombres que empiezan con ese texto. |
| **`exit`** | `exit` | Guarda todos los datos y cierra el programa. |

---

Con esto, el entregable del **Día 12** está listo. El siguiente paso en el cronograma es el **Día 13: Preparar demo y script de ejecución**. ¿Quieres que te ayude con el guion para la demostración?
