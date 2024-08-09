import os
import csv
import pandas as pd
from openpyxl import Workbook

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter

from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph

from reportlab.graphics import renderPDF

from reportlab.pdfgen import canvas

import PyPDF2
import time

import navegar_directorios

alumnos_PIE = []

nombres_archivos_graficos = []

nombres_y_notas = []


def reorder_list(original_list, order):
    """
    Reordena una lista según los valores especificados en otra lista.

    Parameters:
    original_list (list): La lista original a reordenar.
    order (list): Una lista de índices que indica el nuevo orden.

    Returns:
    list: La lista reordenada.
    """
    # Crear un diccionario para mapear índices a valores de la lista original
    index_to_value = {index: original_list[index] for index in range(len(original_list))}
    print(index_to_value)
    # Reordenar la lista original según los valores en 'order'
    reordered_list = [index_to_value[str(i)] for i in order]
    return reordered_list

### SE OCUPA
def tablas_iniciales(nombre_ensayo, curso):
    global nombres_y_notas
    nombre_quiz = nombre_ensayo
    encabezado = []
    contenido = []
    with open(f"quiz-{nombre_quiz}-full.csv", "r", encoding='utf-8') as archivo:
        lineas = archivo.readlines()
        lista_lineas = []
        for l in lineas:
            lista_lineas.append(l.strip("\n").split(","))
        encabezado = lista_lineas[0]
        con = lista_lineas[1:]
        contenido = [c for c in con if c[1].strip('"') == curso]
    #print(contenido)

    # print(encabezado)
    # print("--------------------------------------------------------------------------------")
    # for c in contenido:
    #     print(c)
    #     print("--------------------------------------------------------------------------------")
    # Extraer datos del estudiante

    col_evaluacion = encabezado.index("QuizName")
    col_clase = encabezado.index("QuizClass")
    col_nombre = encabezado.index("FirstName")
    col_apellido = encabezado.index("LastName")
    col_id = encabezado.index("StudentID")
    col_run = encabezado.index("CustomID")
    col_correctas = encabezado.index("Earned Points")
    col_totales = encabezado.index("Possible Points")
    col_porcentaje = encabezado.index("PercentCorrect")
    col_fecha_creacion = encabezado.index("QuizCreated")
    col_fecha_exportacion = encabezado.index("DataExported")
    col_key_version = encabezado.index("Key Version")
    encabezado_preguntas = ["Pregunta", "Tú respuesta",
                            "Clave", "C/I", "Número de correctas", "% de correctas"]

    datos_y_respuestas_por_alumno = []
    print("La evaluación tiene un total de", int(
        float(contenido[1][col_totales].strip('"'))), "preguntas válidas.")

    max = {}

    for a in contenido:
        if a[col_clase].strip('"') not in max.keys():
            max[a[col_clase].strip('"')] = []
    cursos = list(max.keys())
    for c in cursos:
        max[c].append(int(input(f"Puntaje maximo para {c} regular -> ")))
        max[c].append(int(input(f"Puntaje maximo para {c} PIE -> ")))
    # print(max)
    lista_pie = guardar_alumnos_PIE(contenido, col_nombre, col_apellido)
    exigencia = float(
        input("Ingresa el porcentaje de exigencia en una escala de 0 a 1 -> "))
    # print(lista_pie)
    for alumno in contenido:
        #print(alumno)
        total = 0
        porcentaje = 0
        for a in lista_pie:
            if alumno[col_apellido].strip('"') == a[0] and alumno[col_nombre].strip('"') == a[1]:
                total = max[alumno[col_clase].strip('"')][1]
                break
            total = max[alumno[col_clase].strip('"')][0]
        porcentaje = str(
            round(int(float(alumno[col_correctas].strip('"')))*100/total, 2))+"%"
        buenas = int(float(alumno[col_correctas].strip('"')))
        puntaje_aprobacion = total*exigencia
        nota = 0
        if buenas >= puntaje_aprobacion:
            nota = round((3/(total-puntaje_aprobacion)) *
                         (buenas-puntaje_aprobacion)+4, 1)
        else:
            nota = round((3/puntaje_aprobacion)*buenas+1, 1)

        datos = [["Evaluación", alumno[col_evaluacion].strip('"')],
                 ["Clase", alumno[col_clase].strip('"')],
                 ["Nombre", alumno[col_nombre].strip('"')],
                 ["Apellido", alumno[col_apellido].strip('"')],
                 ["ID", alumno[col_id].strip('"')],
                 ["RUN", alumno[col_run].strip('"')],
                 ["Forma", alumno[col_key_version].strip('"')],
                 ["Buenas", buenas],
                 ["Total", total],
                 ["Porcentaje", porcentaje],
                 ["Nota", nota],
                 ["Fecha de creación", alumno[col_fecha_creacion].strip('"')],
                 ]
        # ["Fecha de exportación",alumno[col_fecha_exportacion].strip('"')]
        # ]
        # print(datos[1],datos[2],datos[3],datos[8])
        # print(datos)
        # print("----------------------------------------------------------------------------")

        # Guardar nombres y notas en la lista
        nombres_y_notas.append([alumno[col_apellido].strip(
            '"')+" "+alumno[col_nombre].strip('"'), nota])

        # Crear la lista para la tabla de respuestas
        respuestas = [encabezado_preguntas]
        numero_de_preguntas = len(contenido[0][col_key_version+1:])//4
        for i in range(numero_de_preguntas):
            r = [i+1, alumno[col_key_version+1+i *
                             4].strip('"'), alumno[col_key_version+2+i*4].strip('"')]
            if alumno[col_key_version+4+i*4] == "C":
                r.append("Correcta")
            elif alumno[col_key_version+4+i*4] == "X":
                r.append("Incorrecta")
            elif alumno[col_key_version+4+i*4] == "" and alumno[col_key_version+1+i*4].strip('"') == alumno[col_key_version+2+i*4].strip('"'):
                r.append("Correcta (P)")
            elif alumno[col_key_version+4+i*4] == "" and alumno[col_key_version+1+i*4].strip('"') != alumno[col_key_version+2+i*4].strip('"'):
                r.append("Incorrecta (P)")
            respuestas.append(r)
        # print(respuestas)
        # print("-----------------------------------------------------------")

        # Identificar el porcentaje de correctas
        # for resp in respuestas:

        datos_y_respuestas_por_alumno.append([alumno[col_apellido].strip(
            '"'), alumno[col_nombre].strip('"'), datos, respuestas])

    # Identificar el porcentaje de correctas
    cantidad_preguntas=len(datos_y_respuestas_por_alumno[0][3][1:])
    contador_correctas = [0 for i in range(cantidad_preguntas)]
    print("contador correctas largo ",len(contador_correctas))
    print(contador_correctas)
    
    
    for detalle in datos_y_respuestas_por_alumno:
        #time.sleep(3)
        forma=f"{detalle[2][6][0]} {detalle[2][6][1]}"
        #print(forma)
        #time.sleep(3)
        form=[]
        nombre_arch=f"mapeos_{nombre_quiz}.csv"
        with open(nombre_arch,"r",encoding="utf-8") as maps:
            m=["Forma A","Forma B","Forma C","Forma D","Forma E"]
            indice=m.index(forma)
            form=[(int(l.strip("\n").split(",")[0]),int(l.strip("\n").split(",")[1]),int(l.strip("\n").split(",")[2]),int(l.strip("\n").split(",")[3]),int(l.strip("\n").split(",")[4])) for l in maps.readlines()[1:]]
        
            reord = sorted(form, key=lambda x: x[indice])

        
        #print(form)
        #print(detalle[1])
        for idx,resp in enumerate(detalle[3][1:]):
            if resp[1] == resp[2]:
                contador_correctas[form[idx][indice]-1] += 1
        
        #print(contador_correctas)
    numero_alumnos = len(datos_y_respuestas_por_alumno)
    porcentaje_correctas_por_pregunta = []
    for c in range(len(contador_correctas)):
        porcentaje_correctas_por_pregunta.append(
            round(contador_correctas[c]*100/numero_alumnos, 1))
    # print(porcentaje_correctas_por_pregunta)

    for detalle in datos_y_respuestas_por_alumno:
        #time.sleep(3)
        forma=f"{detalle[2][6][0]} {detalle[2][6][1]}"
        #print(forma)
        #time.sleep(3)
        form=[]
        nombre_arch=f"mapeos_{nombre_quiz}.csv"
        with open(nombre_arch,"r",encoding="utf-8") as maps:
            m=["Forma A","Forma B","Forma C","Forma D","Forma E"]
            indice=m.index(forma)
            form=[(int(l.strip("\n").split(",")[0]),int(l.strip("\n").split(",")[1]),int(l.strip("\n").split(",")[2]),int(l.strip("\n").split(",")[3]),int(l.strip("\n").split(",")[4])) for l in maps.readlines()[1:]]
        
            reord = sorted(form, key=lambda x: x[indice])

        
        #print(form)
        for i in range(len(detalle[3][1:])):
            print(form[i][indice])
            detalle[3][1:][i].append(contador_correctas[form[i][indice]-1])
            detalle[3][1:][i].append(porcentaje_correctas_por_pregunta[form[i][indice]-1])
            # print(detalle[3][1:][i])

    # for k in datos_y_respuestas_por_alumno:
    #     print(k)
    #     print("----------------------------------------")
    for a in datos_y_respuestas_por_alumno:
        for c in a:
            for b in c:
                pass
                # print(b)
    return datos_y_respuestas_por_alumno

### SE OCUPA
def listar_archivos_en_carpeta():
    
    # Obtener la lista de archivos en la carpeta actual
    archivos = os.listdir()
    # Imprimir cada nombre de archivo

    lista_de_nombres = []
    for archivo in archivos:

        if "quiz" in archivo:
            # print(archivo)
            a = archivo.split("-")[1]
            if a not in lista_de_nombres:
                lista_de_nombres.append(a)
    for nombre in lista_de_nombres:
        print(nombre.lower())

### SE OCUPA
def crear_2tabla(filas1, filas2, nombre_archivo):
    # Crear el archivo PDF

    pdf_filename = f"{nombre_archivo}-Tablas_datos_y_respuestas.pdf"

    # Definir los márgenes (en puntos, donde 1 pulgada = 72 puntos)
    left_margin = 20
    right_margin = 20
    top_margin = 20
    bottom_margin = 20

    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        leftMargin=left_margin,
        rightMargin=right_margin,
        topMargin=top_margin,
        bottomMargin=bottom_margin
    )

    # doc = SimpleDocTemplate(pdf_filename, pagesize=letter)

    # prueba=""
    # if "m2" in nombre_archivo.lower():
    #     prueba="m2"
    # elif "m1" in nombre_archivo.lower():
    #     prueba="m1"
    # puntaje_paes=agregar_puntaje(filas1,prueba)
    # filas1.append(["Puntaje PAES",str(puntaje_paes)])

    # Definir estilos

    estilo_respuestas_estudiante = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#00A200")),
                                               ('TEXTCOLOR', (0, 0),
                                                (-1, 0), colors.whitesmoke),
                                               ('ALIGN', (0, 0),
                                                (-1, -1), 'CENTER'),
                                               ('VALIGN', (0, 0),
                                                (-1, -1), 'MIDDLE'),
                                               ('FONTNAME', (0, 0),
                                                (-1, 0), 'Helvetica-Bold'),
                                               ('FONTSIZE', (0, 0), (-1, -1), 10),
                                               ('BOTTOMPADDING',
                                                (0, 0), (-1, 0), 5),
                                               ('BACKGROUND', (0, 1), (-1, -1),
                                                colors.HexColor("#DDFFDD")),
                                               ('GRID', (0, 0), (-1, -1), 1, colors.black)])

    estilo_datos_estudiante = TableStyle([('BACKGROUND', (0, 0), (0, -1), colors.HexColor("#00A200")),
                                          ('TEXTCOLOR', (0, 0),
                                           (0, -1), colors.whitesmoke),
                                          ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                          ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                                          ('FONTNAME', (0, 0),
                                           (0, -1), 'Helvetica-Bold'),
                                          ('FONTSIZE', (0, 0), (-1, -1), 10),
                                          ('BOTTOMPADDING', (0, 0), (0, -1), 5),
                                          ('BACKGROUND', (1, 0), (-1, -1),
                                           colors.HexColor("#DDFFDD")),
                                          ('GRID', (0, 0), (-1, -1), 1, colors.black)])

    estilo_datos_estudiante2 = TableStyle([('BACKGROUND', (0, 0), (0, -1), colors.HexColor("#00A200")),
                                           ('BACKGROUND', (3, 0), (3, -1),
                                            colors.HexColor("#00A200")),
                                           ('TEXTCOLOR', (0, 0),
                                            (0, -1), colors.whitesmoke),
                                           ('TEXTCOLOR', (3, 0),
                                            (3, -1), colors.whitesmoke),
                                           ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                           ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                                           ('FONTNAME', (0, 0),
                                            (0, -1), 'Helvetica-Bold'),
                                           ('FONTNAME', (3, 0),
                                            (3, -1), 'Helvetica-Bold'),
                                           ('FONTSIZE', (0, 0), (-1, -1), 10),
                                           ('BOTTOMPADDING', (0, 0), (0, -1), 5),
                                           ('BOTTOMPADDING', (3, 0), (3, -1), 5),
                                           ('BACKGROUND', (1, 0), (1, -1),
                                            colors.HexColor("#DDFFDD")),
                                           ('BACKGROUND', (4, 0), (4, -1),
                                            colors.HexColor("#DDFFDD")),
                                           ('GRID', (0, 0), (1, -1),
                                            1, colors.black),
                                           ('GRID', (3, 0), (4, -1), 1, colors.black)])

    # Reestructurar fila de datos
    largo = len(filas1)
    print(largo)
    if largo % 2 == 0:
        primera_mitad = largo//2
    else:
        primera_mitad = largo//2+1

    filas_datos = []
    for i in range(primera_mitad):
        try:
            filas_datos.append(
                filas1[i]+["          "]+filas1[i+primera_mitad])
        except:
            filas_datos.append(filas1[i]+[" "]+[" ", " "])

    # Crear las tablas
    # tabla_datos_estudiante = Table(filas1)
    tabla_datos_estudiante = Table(filas_datos)
    # tabla_datos_estudiante.setStyle(estilo_datos_estudiante)
    tabla_datos_estudiante.setStyle(estilo_datos_estudiante2)

    tabla_respuestas_estudiante = Table(filas2, rowHeights=16)
    tabla_respuestas_estudiante.setStyle(estilo_respuestas_estudiante)
    # tabla_respuestas_estudiante

    # Obtener respuestas correctas e incorrectas
    respuestas_correctas = {'Correcta', 'Correcta (P)'}
    respuestas_incorrectas = {'Incorrecta', 'Incorrecta (P)'}

    # Iterar sobre las filas de respuestas
    for i, fila in enumerate(filas2[1:], start=1):
        if fila[3] in respuestas_correctas:
            # Respuesta correcta en verde
            color_fila = colors.HexColor("#DDFFDD")
        elif fila[3] in respuestas_incorrectas:
            # Respuesta incorrecta en rojo
            color_fila = colors.HexColor("#FFAAAA")
        else:
            color_fila = colors.white      # Otros casos en blanco

        # Aplicar color de fondo a la fila correspondiente
        estilo_fila = [('BACKGROUND', (0, i), (-1, i), color_fila)]
        tabla_respuestas_estudiante.setStyle(estilo_fila)

    # Crear el documento
    doc = SimpleDocTemplate(pdf_filename)

    # Añadir las tablas al contenido
    contenido = [Spacer(1, 20), tabla_datos_estudiante,
                 Spacer(1, 20), tabla_respuestas_estudiante]

    # Agregar título a la página

    titulo = str(nombre_archivo).split("/")[1]
    estilo_titulo = ParagraphStyle(
        name="Titulo", fontName="Helvetica-Bold", fontSize=18)
    contenido.insert(0, Paragraph(titulo, estilo_titulo))

    # Construir el PDF
    doc.build(contenido)

    print(f"Se ha guardado la tabla en el archivo PDF: {pdf_filename}")

    return pdf_filename

### SE OCUPA
def guardar_alumnos_PIE(contenido, col_nombre, col_apellido):
    global alumnos_PIE

    # Agregar alumno a la lista alumnos_PIE
    for alumno in contenido:
        al = []
        al.append(alumno[col_apellido].strip('"'))
        al.append(alumno[col_nombre].strip('"'))
        alumnos_PIE.append(al)
    for i in range(len(alumnos_PIE)):
        print(f"{i+1}.- {alumnos_PIE[i][0]} {alumnos_PIE[i][1]}")

    # Pedir al usuario los números de los alumnos PIE
    num = input(
        "Indica el número de los alumnos PIE (separados por coma) -> ").split(",")

    # Archivo CSV donde se guardan los datos de los alumnos PIE
    filename = "alumnos_PIE.csv"

    # Verificar si el archivo existe
    file_exists = os.path.isfile(filename)

    # Leer el contenido actual del archivo si existe
    existing_students = set()
    if file_exists:
        with open(filename, "r", encoding="utf-8") as pie:
            reader = csv.reader(pie)
            next(reader, None)  # Saltar el encabezado
            for row in reader:
                existing_students.add((row[0], row[1]))

    # Abrir el archivo en modo de adjuntar ('a') y escribir los nuevos alumnos si no existen
    with open(filename, "a", encoding="utf-8", newline='') as pie:
        writer = csv.writer(pie)
        if not file_exists:
            # Escribir encabezado si el archivo no existía
            writer.writerow(["Nombre", "Apellido"])

        for i in num:
            # Convertir a índice (restar 1 porque los índices empiezan en 0)
            index = int(i.strip()) - 1
            if index < len(alumnos_PIE):
                alumno = alumnos_PIE[index]
                if tuple(alumno) not in existing_students:
                    writer.writerow(alumno)
                    # Añadir a la lista de existentes
                    existing_students.add(tuple(alumno))
                else:
                    print(
                        f"El alumno {alumno[0]} {alumno[1]} ya está agregado.")
            else:
                print(f"Índice {index + 1} fuera de rango para alumnos_PIE.")
    with open(filename, "r", encoding="utf-8") as pie:
        lista_pie_0 = pie.readlines()

        lista_pie = []
        for lis in lista_pie_0:

            apellido, nombre = lis.strip("\n").split(",")
            if apellido != "Apellido":
                lista_pie.append([apellido, nombre])
        return lista_pie

### SE OCUPA
def elegir_grupo(nombre_ensayo):
    nombre_quiz = nombre_ensayo
    encabezado = []
    contenido = []
    with open(f"quiz-{nombre_quiz}-full.csv", "r", encoding='utf-8') as archivo:
        lineas = archivo.readlines()
        lista_lineas = []
        for l in lineas:
            lista_lineas.append(l.strip("\n").split(","))
        encabezado = lista_lineas[0]
        contenido = lista_lineas[1:]
    grupos = []
    for c in contenido:
        if c[1].strip('"') not in grupos:
            grupos.append(c[1].strip('"'))
    print("Los cursos disponibles son los siguientes:")
    i = 1
    for g in grupos:
        print(f"{i} {g}\n")
        i += 1
    val = int(input("Elige un grupo mindicando el numero corespondiente -> "))
    print(f"Elegiste: {grupos[val-1]}")
    return grupos[val-1]

### SE OCUPA
def csv_notas(nombre_evaluacion, nombres_y_notas):
    nombre_archivo = nombre_evaluacion+".csv"
    with open(nombre_archivo, "w", encoding="utf-8") as doc_csv:
        for a in nombres_y_notas:
            contenido = a[0]+","+str(a[1])+"\n"
            doc_csv.write(contenido)


print("--------------------------------------------------------------")
print("--------------------------------------------------------------")
print("Bienvenido, elege uno de los siguientes archivos para generar los informes:\n")
listar_archivos_en_carpeta()
print("--------------------------------------------------------------")
print("--------------------------------------------------------------")
nombre_quiz = input("\nIngresa el nombre del quiz: ")
# # verificar_existencia_de_archivos_csv(nombre_quiz)



#ruta,archivo,nombre_archivo=navegar_directorios.main()



print("\nPerfecto, comenzando a generar informes...\n")

curso_elegido = elegir_grupo(nombre_quiz)
iniciales = tablas_iniciales(nombre_quiz, curso_elegido)
print(type(iniciales))
nombre_ev = ""
for a in iniciales:
    # print(a)
    # print("---------------------------------------------------------------------\n")
    if not os.path.exists(f"{a[2][0][1]}_{curso_elegido}"):
        os.makedirs(f"{a[2][0][1]}_{curso_elegido}")
    crear_2tabla(a[2], a[3], f"{a[2][0][1]}_{curso_elegido}/{a[0]}_{a[1]}")
    nombre_ev = f"{a[2][0][1]}_{curso_elegido}"
csv_notas(nombre_ev, nombres_y_notas)