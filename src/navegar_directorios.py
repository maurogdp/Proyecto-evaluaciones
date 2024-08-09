import os

def listar_contenido(directorio):
    """Lista las carpetas y archivos en el directorio dado."""
    try:
        contenido = os.listdir(directorio)
        carpetas = [d for d in contenido if os.path.isdir(os.path.join(directorio, d))]
        archivos = [f for f in contenido if os.path.isfile(os.path.join(directorio, f))]
        return carpetas, archivos
    except FileNotFoundError:
        print(f"El directorio {directorio} no existe.")
        return [], []

def mostrar_contenido(directorio, carpetas, archivos):
    """Muestra el contenido del directorio con numeración."""
    print(f"\nContenido de: {directorio}")
    print("Carpetas:")
    for i, carpeta in enumerate(carpetas):
        print(f"{i+1}. [Carpeta] {carpeta}")
    print("Archivos:")
    for i, archivo in enumerate(archivos, len(carpetas)):
        print(f"{i+1}. [Archivo] {archivo}")

def navegar_directorio(directorio_actual):
    """Navega por los directorios y permite seleccionar archivos."""
    while True:
        carpetas, archivos = listar_contenido(directorio_actual)
        mostrar_contenido(directorio_actual, carpetas, archivos)

        # Mostrar opciones de navegación
        print("\nOpciones:")
        print("0. Subir un nivel")
        for i, carpeta in enumerate(carpetas):
            print(f"{i+1}. Entrar en la carpeta '{carpeta}'")
        for i, archivo in enumerate(archivos, len(carpetas)):
            print(f"{i+1}. Seleccionar archivo '{archivo}'")

        # Leer la opción del usuario
        opcion = input("\nElige una opción (número): ").strip()
        elegir=False
        if not opcion.isdigit():
            if opcion[0]=="e":
                elegir=True
                if opcion[1:].isdigit():
                    opcion=opcion[1:]
                else:
                    elegir=False
                    print("Por favor, introduce un número válido.")
                    continue
                
            else:        
                print("Por favor, introduce un número válido.")
                continue

        opcion = int(opcion)

        if opcion == 0:
            # Subir un nivel
            directorio_actual = os.path.dirname(directorio_actual)
        elif 1 <= opcion <= len(carpetas):
            # Entrar en una subcarpeta
            carpeta_selecionada=carpetas[opcion-1]
            ruta_carpeta_selecionada = os.path.join(directorio_actual, carpeta_selecionada)
            if not elegir:
                directorio_actual = ruta_carpeta_selecionada
            else:

                return ruta_carpeta_selecionada,carpeta_selecionada
        elif len(carpetas) < opcion <= len(carpetas) + len(archivos):
            # Seleccionar un archivo
            archivo_seleccionado = archivos[opcion - len(carpetas) - 1]
            archivo_seleccionado_sin_extension=archivo_seleccionado.split(".")[0]
            ruta_archivo_seleccionado = os.path.join(directorio_actual, archivo_seleccionado)
            print(f"\nArchivo seleccionado: {ruta_archivo_seleccionado}")
            return ruta_archivo_seleccionado,archivo_seleccionado,archivo_seleccionado_sin_extension
        else:
            print("Opción no válida, intenta de nuevo.")

def main():
    directorio_inicial = r"C:\Users\mauro\Desktop\Proyecto Evaluaciones"
    archivo_seleccionado = navegar_directorio(directorio_inicial)
    print(f"\nEl archivo seleccionado es: {archivo_seleccionado}")
    return archivo_seleccionado

if __name__ == "__main__":
    main()
