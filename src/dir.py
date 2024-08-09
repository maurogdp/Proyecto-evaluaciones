import os

def listar_directorios(directorio):
    """Lista las carpetas en el directorio dado."""
    try:
        return [d for d in os.listdir(directorio) if os.path.isdir(os.path.join(directorio, d))]
    except FileNotFoundError:
        print(f"El directorio {directorio} no existe.")
        return []

def obtener_red_de_carpetas(directorio_actual):
    """Obtiene la red de carpetas desde el directorio actual, incluyendo hasta 2 niveles de carpetas padres."""
    red_de_carpetas = {}

    # Nivel 0: Directorio actual
    red_de_carpetas[directorio_actual] = listar_directorios(directorio_actual)

    # Nivel 1: Directorio padre
    directorio_nivel_1 = os.path.dirname(directorio_actual)
    if directorio_nivel_1:
        red_de_carpetas[directorio_nivel_1] = listar_directorios(directorio_nivel_1)

        # Nivel 2: Directorio abuelo
        directorio_nivel_2 = os.path.dirname(directorio_nivel_1)
        if directorio_nivel_2:
            red_de_carpetas[directorio_nivel_2] = listar_directorios(directorio_nivel_2)

    return red_de_carpetas

def mostrar_red_de_carpetas(red_de_carpetas):
    """Muestra la red de carpetas."""
    for directorio, subdirectorios in red_de_carpetas.items():
        print(f"\nDirectorio: {directorio}")
        for subdirectorio in subdirectorios:
            print(f"  - {subdirectorio}")

def main():
    directorio_actual = os.getcwd()
    print(f"Directorio actual: {directorio_actual}")

    red_de_carpetas = obtener_red_de_carpetas(directorio_actual)
    mostrar_red_de_carpetas(red_de_carpetas)

if __name__ == "__main__":
    main()
