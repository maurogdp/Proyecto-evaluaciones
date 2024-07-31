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

alumnos_PIE=[]

nombres_archivos_graficos=[]

nombres_y_notas=[]

def tablas_iniciales(nombre_ensayo,curso):
    global nombres_y_notas
    nombre_quiz=nombre_ensayo
    encabezado=[]
    contenido=[]
    with open(f"quiz-{nombre_quiz}-full.csv","r", encoding='utf-8') as archivo:
        lineas=archivo.readlines()
        lista_lineas=[]
        for l in lineas:
            lista_lineas.append(l.strip("\n").split(","))
        encabezado=lista_lineas[0]
        con=lista_lineas[1:]
        contenido = [c for c in con if c[1].strip('"') == curso]
    print(contenido)

    # print(encabezado)
    # print("--------------------------------------------------------------------------------")
    # for c in contenido:
    #     print(c)
    #     print("--------------------------------------------------------------------------------")
    # Extraer datos del estudiante

    col_evaluacion=encabezado.index("QuizName")
    col_clase=encabezado.index("QuizClass")
    col_nombre=encabezado.index("FirstName")
    col_apellido=encabezado.index("LastName")
    col_id=encabezado.index("StudentID")
    col_run=encabezado.index("CustomID")
    col_correctas=encabezado.index("Earned Points")
    col_totales=encabezado.index("Possible Points")
    col_porcentaje=encabezado.index("PercentCorrect")
    col_fecha_creacion=encabezado.index("QuizCreated")
    col_fecha_exportacion=encabezado.index("DataExported")
    col_key_version=encabezado.index("Key Version")
    encabezado_preguntas=["Pregunta","Tú respuesta","Clave","C/I","Número de correctas","% de correctas"]

    datos_y_respuestas_por_alumno=[]
    print("La evaluación tiene un total de",int(float(contenido[1][col_totales].strip('"'))),"preguntas válidas.")

    max={}

    for a in contenido:
        if a[col_clase].strip('"') not in max.keys():
            max[a[col_clase].strip('"')]=[]
    cursos=list(max.keys())
    for c in cursos:
        max[c].append(int(input(f"Puntaje maximo para {c} regular -> ")))
        max[c].append(int(input(f"Puntaje maximo para {c} PIE -> ")))
    #print(max)
    lista_pie=guardar_alumnos_PIE(contenido,col_nombre,col_apellido)
    exigencia=float(input("Ingresa el porcentaje de exigencia en una escala de 0 a 1 -> "))
    #print(lista_pie)
    for alumno in contenido:
        print(alumno)
        total=0
        porcentaje=0
        for a in lista_pie:
            if alumno[col_apellido].strip('"') == a[0] and alumno[col_nombre].strip('"') == a[1]:
                total=max[alumno[col_clase].strip('"')][1]
                break
            total=max[alumno[col_clase].strip('"')][0]
        porcentaje=str(round(int(float(alumno[col_correctas].strip('"')))*100/total,2))+"%"
        buenas=int(float(alumno[col_correctas].strip('"')))
        puntaje_aprobacion=total*exigencia
        nota=0
        if buenas>=puntaje_aprobacion:
            nota=round((3/(total-puntaje_aprobacion))*(buenas-puntaje_aprobacion)+4,1)
        else:
            nota=round((3/puntaje_aprobacion)*buenas+1,1)
        

        datos=[["Evaluación",alumno[col_evaluacion].strip('"')],
        ["Clase",alumno[col_clase].strip('"')],
        ["Nombre",alumno[col_nombre].strip('"')],
        ["Apellido",alumno[col_apellido].strip('"')],
        ["ID",alumno[col_id].strip('"')],
        ["RUN",alumno[col_run].strip('"')],
        ["Forma",alumno[col_key_version].strip('"')],
        ["Buenas",buenas],
        ["Total",total],
        ["Porcentaje",porcentaje],
        ["Nota",nota],
        ["Fecha de creación",alumno[col_fecha_creacion].strip('"')],
        ]
        #["Fecha de exportación",alumno[col_fecha_exportacion].strip('"')]
        #]
        #print(datos[1],datos[2],datos[3],datos[8])
        #print(datos)
        #print("----------------------------------------------------------------------------")


        # Guardar nombres y notas en la lista 
        nombres_y_notas.append([alumno[col_apellido].strip('"')+" "+alumno[col_nombre].strip('"'),nota])

        # Crear la lista para la tabla de respuestas
        respuestas=[encabezado_preguntas]
        numero_de_preguntas=len(contenido[0][col_key_version+1:])//4
        for i in range(numero_de_preguntas):
            r=[i+1,alumno[col_key_version+1+i*4].strip('"'),alumno[col_key_version+2+i*4].strip('"')]
            if alumno[col_key_version+4+i*4]=="C":
                r.append("Correcta")
            elif alumno[col_key_version+4+i*4]=="X":
                r.append("Incorrecta")
            elif alumno[col_key_version+4+i*4]=="" and alumno[col_key_version+1+i*4].strip('"')==alumno[col_key_version+2+i*4].strip('"'):
                r.append("Correcta (P)")
            elif alumno[col_key_version+4+i*4]=="" and alumno[col_key_version+1+i*4].strip('"')!=alumno[col_key_version+2+i*4].strip('"'):
                r.append("Incorrecta (P)")
            respuestas.append(r)    
        # print(respuestas)
        # print("-----------------------------------------------------------")

        #Identificar el porcentaje de correctas
        #for resp in respuestas:



        datos_y_respuestas_por_alumno.append([alumno[col_apellido].strip('"'),alumno[col_nombre].strip('"'),datos,respuestas])

    #Identificar el porcentaje de correctas
    contador_correctas=[]
    primero=True
    for detalle in datos_y_respuestas_por_alumno:
        for resp in detalle[3][1:]:
            if primero:
                if resp[1]==resp[2]:
                    contador_correctas.append(1)
                else:
                    contador_correctas.append(0)
                
            else:
                if resp[1]==resp[2]:
                    contador_correctas[detalle[3][1:].index(resp)]+=1
        primero=False
    numero_alumnos=len(datos_y_respuestas_por_alumno)
    porcentaje_correctas_por_pregunta=[]
    for c in range(len(contador_correctas)):
        porcentaje_correctas_por_pregunta.append(round(contador_correctas[c]*100/numero_alumnos,2))
    #print(porcentaje_correctas_por_pregunta)

    for detalle in datos_y_respuestas_por_alumno:
        
        for i in range(len(detalle[3][1:])):
            detalle[3][1:][i].append(contador_correctas[i])
            detalle[3][1:][i].append(porcentaje_correctas_por_pregunta[i])
            #print(detalle[3][1:][i])

    # for k in datos_y_respuestas_por_alumno:
    #     print(k)
    #     print("----------------------------------------")
    for a in datos_y_respuestas_por_alumno:
        for c in a:
            for b in c:
                pass
                #print(b)
    return datos_y_respuestas_por_alumno

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
    for nombre in lista_de_nombres:
        print(nombre.lower())

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

def graficar_horizontal(filas_tag,nombre_archivo,tag):
    # Datos para las barras agrupadas
    tags = []
    total = []
    correctas = []
    porcentaje = []
    for f in filas_tag:
        tags.append(f[0])
        total.append(int(f[2]))
        correctas.append(int(f[1]))
        porcentaje.append(f[3])
    

    # Altura de las barras
    bar_height = 0.35



    # Posiciones de las barras
    y = range(len(tags))
    

    # Crear la figura y los ejes
    fig_width = 8.5  # Ancho de la figura
    fig_height = 22  # Alto de la figura

    # Crear la figura y los ejes con el tamaño especificado
    fig, ax = plt.subplots(figsize=(fig_width, fig_height),)
    #plt.subplots_adjust(bottom=0.2)


    # Eliminar bordes del eje
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    
    # Eliminar tics del eje y
    ax.tick_params(axis='y', which='both', left=False)
    # Eliminar tics del eje x
    ax.tick_params(axis='x', which='both', bottom=False)

    # Graficar las barras agrupadas
    bars1 = ax.barh([i for i in y], total, bar_height, label='Total')
    bars2 = ax.barh([i + bar_height for i in y], correctas, bar_height, label='Correctas')


    # Agregar etiquetas de datos
    k=0
    for i, v in enumerate(total):
        ax.text(v + 3*max(total)/100, i, str(v), color='black', va='center',fontsize=12)
        #ax.text(v + 7*max(total)/100, i + bar_height/2, porcentaje[k], color='black', va='center',fontsize=12)
        k+=1
    for i, v in enumerate(correctas):
        ax.text(v + 3*max(total)/100, i + bar_height, str(v), color='black', va='center',fontsize=12)
        

    

    

    # Añadir etiquetas, título y leyenda
    #ax.set_ylabel('Categorías')
    #ax.set_xlabel('Valores')
    ax.set_title(f"{nombre_archivo}-{tag}")
    ax.set_yticks([i + bar_height / 2 for i in y])
    ax.set_yticklabels(tags,fontsize=12)
    ax.legend()

    # Añadir líneas guía verticales
    for i in range(0, max(total) + 1):
        ax.axvline(x=i, color='lightgray', linestyle='-', linewidth=1, zorder=0)  # Zorder controla la posición de las líneas guía


    # Nombre del archivo PDF
    pdf_filename = f"{nombre_archivo}-{tag}.pdf"

    # Guardar el gráfico en un archivo PDF
    with PdfPages(pdf_filename) as pdf:
        pdf.savefig(bbox_inches='tight', pad_inches=0.5, orientation='portrait')
        plt.close()

    print(f"Se ha guardado el gráfico en el archivo PDF: {pdf_filename}")


    return pdf_filename

def graficar_ejes_horizontal(filas_tag,nombre_archivo,tag):
    # Datos para las barras agrupadas
    tags = []
    total = []
    correctas = []
    porcentaje = []
    for f in filas_tag:
        tags.append(f[0])
        total.append(int(f[2]))
        correctas.append(int(f[1]))
        porcentaje.append(f[3])
    

    # Altura de las barras
    bar_height = 0.35



    # Posiciones de las barras
    y = range(len(tags))
    #print(y)

    # Crear la figura y los ejes
    fig_width = 8.5  # Ancho de la figura
    fig_height = 7  # Alto de la figura

    # Crear la figura y los ejes con el tamaño especificado
    fig, ax = plt.subplots(figsize=(fig_width, fig_height),)
    #plt.subplots_adjust(bottom=0.2)


    # Eliminar bordes del eje
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    
    # Eliminar tics del eje y
    ax.tick_params(axis='y', which='both', left=False)
    # Eliminar tics del eje x
    ax.tick_params(axis='x', which='both', bottom=False)

    # Graficar las barras agrupadas
    bars1 = ax.barh([i for i in y], total, bar_height, label='Total')
    bars2 = ax.barh([i + bar_height for i in y], correctas, bar_height, label='Correctas')


    # Agregar etiquetas de datos
    k=0
    for i, v in enumerate(total):
        ax.text(v + 3*max(total)/100, i, str(v), color='black', va='center',fontsize=12)
        #ax.text(v + 7*max(total)/100, i + bar_height/2, porcentaje[k], color='black', va='center',fontsize=12)
        k+=1
    for i, v in enumerate(correctas):
        ax.text(v + 3*max(total)/100, i + bar_height, str(v), color='black', va='center',fontsize=12)
        

    

    

    # Añadir etiquetas, título y leyenda
    #ax.set_ylabel('Categorías')
    #ax.set_xlabel('Valores')
    ax.set_title(f"{nombre_archivo}-{tag}")
    ax.set_yticks([i + bar_height / 2 for i in y])
    ax.set_yticklabels(tags,fontsize=12)
    
    ax.set_xticks([i for i in range(max(total)+1)])
    ax.set_xticklabels([i for i in range(max(total)+1)],fontsize=10)
    ax.legend()

    # Añadir líneas guía verticales
    for i in range(0, max(total) + 1):
        ax.axvline(x=i, color='lightgray', linestyle='-', linewidth=1, zorder=0)  # Zorder controla la posición de las líneas guía


    # Nombre del archivo PDF
    pdf_filename = f"{nombre_archivo}-{tag}.pdf"

    # Guardar el gráfico en un archivo PDF
    with PdfPages(pdf_filename,) as pdf:
        pdf.savefig(bbox_inches='tight', pad_inches=0.5, orientation='portrait')
        plt.close()

    print(f"Se ha guardado el gráfico en el archivo PDF: {pdf_filename}")

    return pdf_filename

def crear_3tabla(filas1,filas2,filas3,nombre_archivo):
    # Crear el archivo PDF
    pdf_filename = f"{nombre_archivo}-Tablas.pdf"
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)

    # Crear la tabla
    table = Table(filas)

    
    # Definir estilos
    # style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    #                     ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    #                     ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    #                     ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    #                     ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    #                     ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    #                     ('GRID', (0, 0), (-1, -1), 1, colors.black)])
    
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#00A200")),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, -1), 10), 
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 5),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#DDFFDD")),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])

    # Crear las tablas
    tabla1 = Table(filas1)
    tabla1.setStyle(style)

    tabla2 = Table(filas2)
    tabla2.setStyle(style)

    tabla3 = Table(filas3)
    tabla3.setStyle(style)

    # Crear el documento
    doc = SimpleDocTemplate(pdf_filename)

    # Añadir las tablas al contenido
    contenido = [Spacer(1, 20),tabla1,Spacer(1, 20), tabla2,Spacer(1, 20), tabla3]

    # Agregar título a la página
    
    titulo = str(nombre_archivo).split("/")[1]
    estilo_titulo = ParagraphStyle(name="Titulo", fontName="Helvetica-Bold", fontSize=18)
    contenido.insert(0, Paragraph(titulo, estilo_titulo))

    # Construir el PDF
    doc.build(contenido)

    print(f"Se ha guardado la tabla en el archivo PDF: {pdf_filename}")

    return pdf_filename

def agregar_puntaje(datos,prueba):
    num_buenas=0
    for d in datos:
        if d[0]=="Buenas":
            num_buenas=d[1]
    puntaje_paes=0
    archivo_de_puntajes=f"puntajes_{prueba}.csv"
    with open(archivo_de_puntajes, "r") as puntajes:
        todos_los_puntajes=puntajes.readlines()
        listas_puntajes=[]
        for t in todos_los_puntajes:
            listas_puntajes.append(t.strip("\n").split(","))
        for p in listas_puntajes:
            if int(p[0])==num_buenas:
                puntaje_paes=int(p[1])
    return puntaje_paes

def crear_2tabla(filas1,filas2,nombre_archivo):
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

    #doc = SimpleDocTemplate(pdf_filename, pagesize=letter)

    # prueba=""
    # if "m2" in nombre_archivo.lower():
    #     prueba="m2"
    # elif "m1" in nombre_archivo.lower():
    #     prueba="m1"
    # puntaje_paes=agregar_puntaje(filas1,prueba)
    # filas1.append(["Puntaje PAES",str(puntaje_paes)])



    # Definir estilos
    
    estilo_respuestas_estudiante = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#00A200")),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, -1), 10), 
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 5),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#DDFFDD")),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])
    
    estilo_datos_estudiante = TableStyle([('BACKGROUND', (0, 0), (0, -1), colors.HexColor("#00A200")),
                        ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, -1), 10), 
                        ('BOTTOMPADDING', (0, 0), (0, -1), 5),
                        ('BACKGROUND', (1, 0), (-1, -1), colors.HexColor("#DDFFDD")),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])
    
    estilo_datos_estudiante2 = TableStyle([('BACKGROUND', (0, 0), (0, -1), colors.HexColor("#00A200")),
                        ('BACKGROUND', (3, 0), (3, -1), colors.HexColor("#00A200")),
                        ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
                        ('TEXTCOLOR', (3, 0), (3, -1), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                        ('FONTNAME', (3, 0), (3, -1), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, -1), 10), 
                        ('BOTTOMPADDING', (0, 0), (0, -1), 5),
                        ('BOTTOMPADDING', (3, 0), (3, -1), 5),
                        ('BACKGROUND', (1, 0), (1, -1), colors.HexColor("#DDFFDD")),
                        ('BACKGROUND', (4, 0), (4, -1), colors.HexColor("#DDFFDD")),
                        ('GRID', (0, 0), (1, -1), 1, colors.black),
                        ('GRID', (3, 0), (4, -1), 1, colors.black)])

    # Reestructurar fila de datos
    largo=len(filas1)
    print(largo)
    if largo%2==0:
        primera_mitad=largo//2
    else:
        primera_mitad=largo//2+1

    filas_datos=[]
    for i in range(primera_mitad):
        try:
            filas_datos.append(filas1[i]+["          "]+filas1[i+primera_mitad])
        except:
            filas_datos.append(filas1[i]+[" "]+[" "," "])


    # Crear las tablas
    #tabla_datos_estudiante = Table(filas1)
    tabla_datos_estudiante = Table(filas_datos)
    #tabla_datos_estudiante.setStyle(estilo_datos_estudiante)
    tabla_datos_estudiante.setStyle(estilo_datos_estudiante2)
    

    tabla_respuestas_estudiante = Table(filas2,rowHeights=16)
    tabla_respuestas_estudiante.setStyle(estilo_respuestas_estudiante)
    #tabla_respuestas_estudiante

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
    contenido = [Spacer(1, 20),tabla_datos_estudiante,Spacer(1, 20), tabla_respuestas_estudiante]

    # Agregar título a la página
    
    titulo = str(nombre_archivo).split("/")[1]
    estilo_titulo = ParagraphStyle(name="Titulo", fontName="Helvetica-Bold", fontSize=18)
    contenido.insert(0, Paragraph(titulo, estilo_titulo))

    # Construir el PDF
    doc.build(contenido)

    print(f"Se ha guardado la tabla en el archivo PDF: {pdf_filename}")

    return pdf_filename

def combinar_pdf(archivos_entrada, archivo_salida):
    # Crear un objeto PDFWriter para el archivo de salida
    pdf_writer = PyPDF2.PdfWriter()

    # Recorrer cada archivo de entrada y agregar sus páginas al archivo de salida
    for archivo_entrada in archivos_entrada:
        with open(archivo_entrada, 'rb') as archivo:
            pdf_reader = PyPDF2.PdfReader(archivo)
            for pagina in range(len(pdf_reader.pages)):
                pdf_writer.add_page(pdf_reader.pages[pagina])

    # Escribir el contenido combinado en un nuevo archivo PDF
    with open(archivo_salida, 'wb') as archivo:
        pdf_writer.write(archivo)

    print(f"Se han combinado los archivos PDF en: {archivo_salida}")

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
    num = input("Indica el número de los alumnos PIE (separados por coma) -> ").split(",")

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
            writer.writerow(["Nombre", "Apellido"])  # Escribir encabezado si el archivo no existía

        for i in num:
            index = int(i.strip()) - 1  # Convertir a índice (restar 1 porque los índices empiezan en 0)
            if index < len(alumnos_PIE):
                alumno = alumnos_PIE[index]
                if tuple(alumno) not in existing_students:
                    writer.writerow(alumno)
                    existing_students.add(tuple(alumno))  # Añadir a la lista de existentes
                else:
                    print(f"El alumno {alumno[0]} {alumno[1]} ya está agregado.")
            else:
                print(f"Índice {index + 1} fuera de rango para alumnos_PIE.")
    with open(filename,"r",encoding="utf-8") as pie:
        lista_pie_0=pie.readlines()
        
        lista_pie=[]
        for lis in lista_pie_0:
            
            apellido,nombre=lis.strip("\n").split(",")
            if apellido!="Apellido":
                lista_pie.append([apellido,nombre])
        return lista_pie

def elegir_grupo(nombre_ensayo):
    nombre_quiz=nombre_ensayo
    encabezado=[]
    contenido=[]
    with open(f"quiz-{nombre_quiz}-full.csv","r", encoding='utf-8') as archivo:
        lineas=archivo.readlines()
        lista_lineas=[]
        for l in lineas:
            lista_lineas.append(l.strip("\n").split(","))
        encabezado=lista_lineas[0]
        contenido=lista_lineas[1:]
    grupos=[]
    for c in contenido:
        if c[1].strip('"') not in grupos:
            grupos.append(c[1].strip('"'))
    print("Los cursos disponibles son los siguientes:")
    i=1
    for g in grupos:
        print(f"{i} {g}\n")
        i+=1
    val=int(input("Elige un grupo mindicando el numero corespondiente -> "))
    print(f"Elegiste: {grupos[val-1]}")
    return grupos[val-1]

def csv_notas(nombre_evaluacion,nombres_y_notas):
    nombre_archivo=nombre_evaluacion+".csv"
    with open(nombre_archivo,"w",encoding="utf-8") as doc_csv:
        for a in nombres_y_notas:
            contenido=a[0]+","+str(a[1])+"\n"
            doc_csv.write(contenido)
    

print("--------------------------------------------------------------")
print("--------------------------------------------------------------")
print("Bienvenido, elege uno de los siguientes archivos para generar los informes:\n")
listar_archivos_en_carpeta()
print("--------------------------------------------------------------")
print("--------------------------------------------------------------")
nombre_quiz=input("\nIngresa el nombre del quiz: ")
#verificar_existencia_de_archivos_csv(nombre_quiz)

print("\nPerfecto, comenzando a generar informes...\n")

curso_elegido=elegir_grupo(nombre_quiz)
iniciales=tablas_iniciales(nombre_quiz,curso_elegido)
nombre_ev=""
for a in iniciales:
    #print(a)
    #print("---------------------------------------------------------------------\n")
    if not os.path.exists(f"{a[2][0][1]}_{curso_elegido}"):
        os.makedirs(f"{a[2][0][1]}_{curso_elegido}")
    crear_2tabla(a[2],a[3],f"{a[2][0][1]}_{curso_elegido}/{a[0]}_{a[1]}")
    nombre_ev=f"{a[2][0][1]}_{curso_elegido}"
csv_notas(nombre_ev,nombres_y_notas)
