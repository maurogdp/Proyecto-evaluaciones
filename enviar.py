import yagmail
import os

def enviar_correo(destinatario, asunto, cuerpo, nombre_archivo):
    yag = yagmail.SMTP('mgdiaz@manquemavida.cl', 'nulfhoqbchwgpbna')
    yag.send(
        to=destinatario,
        subject=asunto,
        contents=cuerpo,
        attachments=nombre_archivo
    )
    print("Correo enviado exitosamente.")


def listar_archivos_en_carpeta():

    # Obtener la lista de archivos en la carpeta actual
    archivos = os.listdir()
    # Imprimir cada nombre de archivo
    
    lista_de_nombres=[]
    for archivo in archivos:
        
        if "quiz" in archivo:
            #print(archivo)
            a=archivo.split("-")[1]
            if a not in lista_de_nombres:
                lista_de_nombres.append(a)
    # for nombre in lista_de_nombres:
        # print(nombre.lower())

def verificar_existencia_de_archivos_csv(nombre):
    # Obtener la lista de archivos en la carpeta actual
    archivos = os.listdir()
    #print("--------------------------------------------------------------")
    #print(archivos)
    #print("--------------------------------------------------------------")
    arxiv=[a.lower() for a in archivos]
    #print("--------------------------------------------------------------")
    #print(arxiv)
    #print("--------------------------------------------------------------")
    # Imprimir cada nombre de archivo
    nombres_de_archivos=[f"quiz-{nombre}-full.csv".lower(),f"quiz-{nombre}-quizStudentTagDetailCSV.csv".lower(),f"quiz-{nombre}-quizStudentTagSummaryCSV.csv".lower()]
    archivos_faltantes=[]
    for a in nombres_de_archivos:
        if a not in arxiv:
            archivos_faltantes.append(a)
            #print(archivos_faltantes)
    #print("--------------------------------------------------------------")
    #print(archivos_faltantes)
    #print("--------------------------------------------------------------")
    
    if len(archivos_faltantes)>0:
        print("--------------------------------------------------------------")
        print("Faltan los siguientes arvhivos par poder generar los informes:")
        for xiv in archivos_faltantes:
            print(xiv)
        print("--------------------------------------------------------------")
        exit()


import os

def listar_archivos_y_carpetas(directorio):
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







#listar_archivos_en_carpeta()

enviar_a_alumnos=input("Quieres enviar los correos a los alumnos? (s/n) -> ")

nombre_evaluacion="Reducción de términos semejantes y valorización"

enviar_prueba=input("Quieres enviar el documento de prueba?(s/n) -> ")
if enviar_prueba!="s":
    confirmacion=input("Se enviarán los documentos a cada estudiante. Escribe 'ENVIAR' para confirmar. -> ")

if enviar_a_alumnos.lower()=="s":

    for archivo in archivos:
        nombre=archivo.split("-")[0].split("_")
        
        nombre_completo=nombre[1]+" "+nombre[0]
        
        # Ejemplo de uso
        destinatario=""
        
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

        if destinatario=="":
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
        # print(destinatario)
        # print(asunto)
        # print(cuerpo)
        # print(nombre_archivo)
        enviar_correo(destinatario, asunto, cuerpo, nombre_archivo)