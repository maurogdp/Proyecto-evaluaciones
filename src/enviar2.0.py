import os
import yagmail

def enviar_correo_mgdiaz(destinatario, asunto, cuerpo, nombre_archivo):
    """
    Envía un correo electrónico utilizando la cuenta de 'mgdiaz@manquemavida.cl'.

    Parámetros:
    destinatario (str): La dirección de correo electrónico del destinatario.
    asunto (str): El asunto del correo electrónico.
    cuerpo (str): El cuerpo del mensaje del correo electrónico.
    nombre_archivo (str): La ruta del archivo a adjuntar al correo electrónico.
    """
    yag = yagmail.SMTP('mgdiaz@manquemavida.cl', 'nulfhoqbchwgpbna')
    yag.send(
        to=destinatario,
        subject=asunto,
        contents=cuerpo,
        attachments=nombre_archivo
    )
    print(f"Correo enviado a {destinatario} exitosamente.")

def listar_archivos_y_carpetas(directorio):
    """
    Lista los archivos y carpetas en un directorio específico.

    Parámetros:
    directorio (str): La ruta del directorio que se quiere listar.

    Retorno:
    tuple: Dos listas, la primera contiene los nombres de los archivos y la segunda contiene los nombres de las carpetas.
    """
    archivos = []
    carpetas = []
    for elemento in os.listdir(directorio):
        ruta_completa = os.path.join(directorio, elemento)
        if os.path.isfile(ruta_completa):
            archivos.append(elemento)
        elif os.path.isdir(ruta_completa):
            carpetas.append(elemento)
    return archivos, carpetas

def obtener_nombre_completo(archivo):
    """
    Obtiene el nombre completo de un archivo basado en su nombre.

    Parámetros:
    archivo (str): El nombre del archivo.

    Retorno:
    str: El nombre completo extraído del archivo.
    """
    nombre = archivo.split("-")[0].split("_")
    return nombre[1] + " " + nombre[0]

def obtener_destinatario(nombre_completo, correos_csv='correos_1B.csv'):
    """
    Obtiene el destinatario del correo basado en el nombre completo del estudiante.

    Parámetros:
    nombre_completo (str): El nombre completo del estudiante.
    correos_csv (str): La ruta del archivo CSV que contiene los correos electrónicos de los estudiantes.

    Retorno:
    str: La dirección de correo electrónico del destinatario.
    """
    with open(correos_csv, "r", encoding="utf-8") as mail:
        for linea in mail:
            l = linea.strip("\n").split(",")
            if l[0].strip().lower() == nombre_completo.lower():
                return l[1]
    return ""

def confirmar_envio():
    """
    Confirma si el usuario desea proceder con el envío de correos.

    Retorno:
    bool: True si el usuario confirma el envío, False en caso contrario.
    """
    confirmacion = input("Se enviarán los documentos a cada estudiante. Escribe 'ENVIAR' para confirmar. -> ")
    return confirmacion.upper() == "ENVIAR"

def enviar_resultados_a_estudiantes(archivos, nombre_evaluacion):
    """
    Envía los resultados de las evaluaciones a los estudiantes seleccionados.

    Parámetros:
    archivos (list): Lista de nombres de archivos con los resultados.
    nombre_evaluacion (str): El nombre de la evaluación.
    """
    envios = []
    for i, alum in enumerate(archivos, 1):
        nom = obtener_nombre_completo(alum)
        print(f"{i}.- {nom}")

    decision = input("Indica a qué estudiantes necesitas enviar los resultados de las evaluaciones.\nEscribe 'TODOS' para enviar el correo a todos los estudiantes.\nPara indicar los estudiantes ingresa los números correspondientes separados por comas (23,15,3,29)\n-> ")

    if decision == "TODOS":
        envios = archivos
    else:
        numeros_estudiantes = [int(e) for e in decision.split(",")]
        envios = [archivos[i-1] for i in numeros_estudiantes]

    for archivo in envios:
        nombre_completo = obtener_nombre_completo(archivo)
        destinatario = obtener_destinatario(nombre_completo)

        if destinatario == "":
            print(f"No se encontró correo para {nombre_completo}.")
            continue

        asunto = f'Resultados - {nombre_evaluacion} - {nombre_completo.upper()}'
        cuerpo = f"""
        Estimado/a {nombre_completo.upper()},

        Espero que este mensaje te encuentre bien.

        Te adjunto los resultados de la evaluación {nombre_evaluacion.upper()}. Por favor, revisa el archivo adjunto para ver tus resultados detallados.

        Si tienes alguna pregunta o necesitas más información, no dudes en ponerte en contacto conmigo.

        Saludos cordiales,
        Profesor Mauro Díaz
        """
        nombre_archivo = f"{directorio}/{archivo}"
        enviar_correo_mgdiaz(destinatario, asunto, cuerpo, nombre_archivo)

def imprimir_consola_enviar_resultados_a_estudiantes(archivos, nombre_evaluacion):
    """
    Imprime en la consola los mensaje que serian enviados a cada estudiante de los seleccionados.

    Parámetros:
    archivos (list): Lista de nombres de archivos con los resultados.
    nombre_evaluacion (str): El nombre de la evaluación.
    """
    envios = []
    for i, alum in enumerate(archivos, 1):
        nom = obtener_nombre_completo(alum)
        print(f"{i}.- {nom}")

    decision = input("Indica a qué estudiantes necesitas enviar los resultados de las evaluaciones.\nEscribe 'TODOS' para enviar el correo a todos los estudiantes.\nPara indicar los estudiantes ingresa los números correspondientes separados por comas (23,15,3,29)\n-> ")

    if decision == "TODOS":
        envios = archivos
    else:
        numeros_estudiantes = [int(e) for e in decision.split(",")]
        envios = [archivos[i-1] for i in numeros_estudiantes]

    for archivo in envios:
        nombre_completo = obtener_nombre_completo(archivo)
        destinatario = obtener_destinatario(nombre_completo)

        if destinatario == "":
            print(f"No se encontró correo para {nombre_completo}.")
            continue

        asunto = f'Resultados - {nombre_evaluacion} - {nombre_completo.upper()}'
        cuerpo = f"""
        Estimado/a {nombre_completo.upper()},

        Espero que este mensaje te encuentre bien.

        Te adjunto los resultados de la evaluación {nombre_evaluacion.upper()}. Por favor, revisa el archivo adjunto para ver tus resultados detallados.

        Si tienes alguna pregunta o necesitas más información, no dudes en ponerte en contacto conmigo.

        Saludos cordiales,
        Profesor Mauro Díaz
        """
        nombre_archivo = f"{directorio}/{archivo}"
        
        print("--------------------------------------------------------")
        print(destinatario)
        print()
        print(asunto)
        print()
        print(cuerpo)
        print()
        print(nombre_archivo)
        print("--------------------------------------------------------")

        
        #enviar_correo_mgdiaz(destinatario, asunto, cuerpo, nombre_archivo)


def enviar_correo_prueba(archivo, nombre_evaluacion):
    """
    Envía un correo de prueba a la dirección personal para verificar el envío.

    Parámetros:
    archivo (str): El nombre del archivo de prueba.
    nombre_evaluacion (str): El nombre de la evaluación.
    """
    nombre_completo = obtener_nombre_completo(archivo)
    destinatario = 'mauro.gdp@gmail.com'

    asunto = f'Prueba - Resultados - {nombre_evaluacion} - {nombre_completo.upper()}'
    cuerpo = f"""
    Estimado/a {nombre_completo.upper()},

    Espero que este mensaje te encuentre bien.

    Te adjunto los resultados de la evaluación {nombre_evaluacion.upper()}. Por favor, revisa el archivo adjunto para ver tus resultados detallados.

    Si tienes alguna pregunta o necesitas más información, no dudes en ponerte en contacto conmigo.

    Saludos cordiales,
    Profesor Mauro Díaz
    """
    nombre_archivo = f"{directorio}/{archivo}"
    enviar_correo_mgdiaz(destinatario, asunto, cuerpo, nombre_archivo)




def listar_directorios(directorio):
    """Lista las carpetas en el directorio dado."""
    try:
        return [d for d in os.listdir(directorio) if os.path.isdir(os.path.join(directorio, d))]
    except FileNotFoundError:
        print("El directorio no existe.")
        return []
    
def seleccionar_directorio(directorios):
    """Permite al usuario seleccionar una carpeta de la lista."""
    print("\nSelecciona una carpeta:")
    for i, dir in enumerate(directorios):
        print(f"{i + 1}. {dir}")

    while True:
        try:
            eleccion = int(input("\nIntroduce el número de la carpeta que deseas seleccionar: "))
            if 1 <= eleccion <= len(directorios):
                return directorios[eleccion - 1]
            else:
                print("Número no válido. Intenta de nuevo.")
        except ValueError:
            print("Entrada no válida. Introduce un número.")

def iniciar_directorio():
    directorio_actual = os.getcwd()
    print(f"\nEstás en el directorio: {directorio_actual}")

    directorios = listar_directorios(directorio_actual)

    if not directorios:
        print("No se encontraron carpetas en el directorio actual.")
        return

    directorio_seleccionado = seleccionar_directorio(directorios)
    print(f"\nHas seleccionado la carpeta: {directorio_seleccionado}")

iniciar_directorio()


# Ejemplo de uso
directorio = 'C:/Users/mauro/Desktop/Notas desde zip/RTS y Val_Matemática 1B'
archivos, carpetas = listar_archivos_y_carpetas(directorio)

enviar_prueba = input("¿Quieres enviar el documento de prueba a tu correo personal? (s/n) -> ")

nombre_evaluacion = "Reducción de términos semejantes y valorización"


if enviar_prueba.lower() == "s":
    if archivos:
        enviar_correo_prueba(archivos[0], nombre_evaluacion)  # Enviar un correo de prueba con el primer archivo
else:
    imprimir_en_consola = input("¿Deseas imprimir en consola los mensajes que se enviarán? (s/n) -> ")
    
    if imprimir_en_consola.lower() == "s":
        imprimir_consola_enviar_resultados_a_estudiantes(archivos, nombre_evaluacion)
    else:
        enviar_a_alumnos = input("¿Quieres enviar los correos a los alumnos? (s/n) -> ")
        if enviar_a_alumnos.lower() == "s" and confirmar_envio():
            enviar_resultados_a_estudiantes(archivos, nombre_evaluacion)
