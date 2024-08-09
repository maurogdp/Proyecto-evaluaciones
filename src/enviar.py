import yagmail
import os

def enviar_correo_mgdiaz(destinatario, asunto, cuerpo, nombre_archivo):
    """
    Envía un correo electrónico utilizando la cuenta de 'mgdiaz@manquemavida.cl'.

    Parámetros:
    destinatario (str): La dirección de correo electrónico del destinatario.
    asunto (str): El asunto del correo electrónico.
    cuerpo (str): El cuerpo del mensaje del correo electrónico.
    nombre_archivo (str): La ruta del archivo a adjuntar al correo electrónico.

    Esta función utiliza la biblioteca yagmail para enviar un correo electrónico
    desde la cuenta 'mgdiaz@manquemavida.cl' a la dirección de correo proporcionada.
    Incluye el asunto, el cuerpo del mensaje y un archivo adjunto especificado.

    Ejemplo de uso:
    enviar_correo_mgdiaz('destinatario@example.com', 'Asunto del correo', 'Cuerpo del correo', 'ruta/al/archivo.txt')

    """
    yag = yagmail.SMTP('mgdiaz@manquemavida.cl', 'nulfhoqbchwgpbna')
    yag.send(
        to=destinatario,
        subject=asunto,
        contents=cuerpo,
        attachments=nombre_archivo
    )
    print("Correo enviado exitosamente.")

def listar_archivos_en_carpeta():
    """
    Lista los archivos en la carpeta actual que contienen la palabra 'quiz' en su nombre,
    y extrae partes específicas de sus nombres.

    Esta función realiza las siguientes acciones:
    1. Obtiene la lista de archivos en la carpeta actual.
    2. Filtra los archivos que contienen la palabra 'quiz'.
    3. Extrae la parte del nombre del archivo que sigue al primer guión ('-').
    4. Agrega la parte extraída a una lista, asegurándose de no incluir duplicados.
    5. Devuelve la lista de nombres únicos.

    Retorno:
    lista_de_nombres (list): Una lista de nombres extraídos de los archivos que contienen 'quiz' en su nombre.
    """

    # Obtener la lista de archivos en la carpeta actual
    archivos = os.listdir()

    # Inicializar una lista para almacenar los nombres únicos
    lista_de_nombres = []

    # Iterar sobre los archivos y filtrar los que contienen 'quiz'
    for archivo in archivos:
        if "quiz" in archivo:
            # Extraer la parte del nombre después del primer guión
            a = archivo.split("-")[1]
            # Agregar a la lista si no está ya presente
            if a not in lista_de_nombres:
                lista_de_nombres.append(a)

    return lista_de_nombres

def verificar_existencia_de_archivos_csv(nombre):
    """
    Verifica la existencia de archivos CSV necesarios en la carpeta actual.

    Parámetros:
    nombre (str): El nombre base que se utilizará para formar los nombres de los archivos CSV a verificar.

    Esta función realiza las siguientes acciones:
    1. Obtiene la lista de archivos en la carpeta actual y los convierte a minúsculas.
    2. Genera una lista de nombres de archivos CSV que deben existir, basados en el nombre proporcionado.
    3. Verifica si cada uno de los archivos requeridos está presente en la lista de archivos.
    4. Si alguno de los archivos requeridos falta, imprime una lista de los archivos faltantes y finaliza la ejecución del programa.

    Los archivos requeridos son:
    - 'quiz-{nombre}-full.csv'
    - 'quiz-{nombre}-quizStudentTagDetailCSV.csv'
    - 'quiz-{nombre}-quizStudentTagSummaryCSV.csv'

    Ejemplo de uso:
    verificar_existencia_de_archivos_csv('test')

    """
    # Obtener la lista de archivos en la carpeta actual
    archivos = os.listdir()

    # Convertir todos los nombres de archivos a minúsculas para una comparación insensible a mayúsculas/minúsculas
    arxiv = [a.lower() for a in archivos]

    # Lista de nombres de archivos requeridos
    nombres_de_archivos = [
        f"quiz-{nombre}-full.csv".lower(),
        f"quiz-{nombre}-quizStudentTagDetailCSV.csv".lower(),
        f"quiz-{nombre}-quizStudentTagSummaryCSV.csv".lower()
    ]

    # Lista para almacenar los nombres de archivos faltantes
    archivos_faltantes = []

    # Verificar la existencia de cada archivo requerido
    for a in nombres_de_archivos:
        if a not in arxiv:
            archivos_faltantes.append(a)

    # Si faltan archivos, imprimir la lista de archivos faltantes y finalizar la ejecución del programa
    if archivos_faltantes:
        print("--------------------------------------------------------------")
        print("Faltan los siguientes archivos para poder generar los informes:")
        for xiv in archivos_faltantes:
            print(xiv)
        print("--------------------------------------------------------------")
        exit()

def listar_archivos_y_carpetas(directorio):
    """
    Lista los archivos y carpetas en un directorio específico.

    Parámetros:
    directorio (str): La ruta del directorio que se quiere listar.

    Esta función realiza las siguientes acciones:
    1. Itera sobre los elementos en el directorio especificado.
    2. Clasifica los elementos en archivos y carpetas.
    3. Devuelve dos listas: una con los nombres de los archivos y otra con los nombres de las carpetas.

    Retorno:
    tuple: Dos listas, la primera contiene los nombres de los archivos y la segunda contiene los nombres de las carpetas.

    Ejemplo de uso:
    archivos, carpetas = listar_archivos_y_carpetas('/ruta/al/directorio')
    """
    archivos = []
    carpetas = []

    # Iterar sobre los elementos en el directorio
    for elemento in os.listdir(directorio):
        ruta_completa = os.path.join(directorio, elemento)
        if os.path.isfile(ruta_completa):
            archivos.append(elemento)
        elif os.path.isdir(ruta_completa):
            carpetas.append(elemento)

    return archivos, carpetas


# Ejemplo de uso


directorio = 'C:/Users/mauro/Desktop/Notas desde zip/RTS y Val_Matemática 1C'
archivos, carpetas = listar_archivos_y_carpetas(directorio)

# print("Archivos:")
# for archivo in archivos:
#     print(type(archivo))

# print("\nCarpetas:")
# for carpeta in carpetas:
#     print(carpeta)


# listar_archivos_en_carpeta()

enviar_a_alumnos = input("Quieres enviar los correos a los alumnos? (s/n) -> ")

nombre_evaluacion = "Reducción de términos semejantes y valorización"

enviar_prueba = input("Quieres enviar el documento de prueba?(s/n) -> ")
if enviar_prueba != "s":
    confirmacion = input(
        "Se enviarán los documentos a cada estudiante. Escribe 'ENVIAR' para confirmar. -> ")

if enviar_a_alumnos.lower() == "s":
    i = 1
    envios = []
    for alum in archivos:

        nom = alum.split("-")[0].split("_")[0]+" " + \
            alum.split("-")[0].split("_")[1]
        print(f"{i}.- {nom}")
        i += 1
    decision = input("Indica a que estudiantes necesitas enviar los resultados de las evaluaciones.\nEscribe 'TODOS' para envar el correoa todos los estudiantes.\nPara indicar los estudiantes ingresa los numeros correspondientes separados por comas (23,15,3,29)\n->")
    if decision == "TODOS":
        envios = archivos
    else:
        numeros_estudiantes = [int(e) for e in decision.split(",")]
        for i in numeros_estudiantes:
            envios.append(archivos[i-1])
    for archivo in envios:

        nombre = archivo.split("-")[0].split("_")

        nombre_completo = nombre[1]+" "+nombre[0]

        # Ejemplo de uso
        destinatario = ""

       # Configurar destinatario
        if enviar_prueba.lower() == "s":
            destinatario = 'mauro.gdp@gmail.com'
        elif enviar_prueba.lower() != "s" and confirmacion == "ENVIAR":
            with open("correos_1C.csv", "r", encoding="utf-8") as mail:
                lineas = mail.readlines()
                for linea in lineas:
                    l = linea.strip("\n").split(",")
                    if l[0].strip().lower() == nombre_completo.lower():
                        destinatario = l[1]
                        break

        if destinatario == "":
            print(f"No se encontró correo para {nombre_completo}.")
            continue
        asunto = f'Resultados - {nombre_evaluacion} - {nombre_completo.upper()}'
        cuerpo = f"""
                    Estimado/a {nombre_completo.upper()},

                    Espero que este mensaje te encuentre bien.

                    Te adjunto los resultados de la evaluación {nombre_evaluacion.upper()} . Por favor, revisa el archivo adjunto para ver tus resultados detallados.

                    Si tienes alguna pregunta o necesitas más información, no dudes en ponerte en contacto conmigo.

                    Saludos cordiales,
                    Profesor Mauro Díaz
                    """
        nombre_archivo = f"RTS y Val_Matemática 1C/{archivo}"

        print("-----------------------------------------------------------------")
        print(f"Enviar correo: {nombre_completo.upper()}")
        print(destinatario)
        print(asunto)
        print(cuerpo)
        print(nombre_archivo)
        enviar_correo_mgdiaz(destinatario, asunto, cuerpo, nombre_archivo)
