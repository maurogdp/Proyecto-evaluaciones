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

from difflib import get_close_matches


correos_1B=["consuelo.zavalla@manquemavida.cl","karimme.tobar@manquemavida.cl","nicolas.rojas@manquemavida.cl","javiera.reyes@manquemavida.cl","lucas.nunez@manquemavida.cl","florencia.moraga@manquemavida.cl","sofia.munoz@manquemavida.cl","antonia.miranda@manquemavida.cl","rafael.martinez@manquemavida.cl","alejandra.galvez@manquemavida.cl","fernanda.herrera@manquemavida.cl","catalina.farias@manquemavida.cl","renato.duran@manquemavida.cl","beverly.cuevas@manquemavida.cl","monserrat.caceres@manquemavida.cl","raul.aliaga@manquemavida.cl","gaspar.valdes@manquemavida.cl","giuliana.ulloa@manquemavida.cl","guillermo.toledo@manquemavida.cl","facundo.salazar@manquemavida.cl","agustina.moscoso@manquemavida.cl","benjamin.ramos@manquemavida.cl","romina.moreno@manquemavida.cl","rayen.maldonado@manquemavida.cl","renato.gonzalez@manquemavida.cl","leonor.hidalgo@manquemavida.cl","isidora.lopez@manquemavida.cl","florencia.jorquera@manquemavida.cl","martin.herrera@manquemavida.cl","maite.echeverria@manquemavida.cl","sofia.cruz@manquemavida.cl","gabriela.cuevas@manquemavida.cl","agustin.cespedes@manquemavida.cl","emilia.bazaes@manquemavida.cl","renato.cruz@manquemavida.cl","joaquin.alvarado@manquemavida.cl"]
c="vicente.vidal@manquemavida.cl,luz.vega@manquemavida.cl,jose.verdugo@manquemavida.cl,antonia.vergara@manquemavida.cl,javiera.valdivia@manquemavida.cl,catalina.sierra@manquemavida.cl,martina.ojeda@manquemavida.cl,nicolas.munoz@manquemavida.cl,clemente.morales@manquemavida.cl,julieta.morales@manquemavida.cl,agustina.jeria@manquemavida.cl,claudio.herrera@manquemavida.cl,valentina.espinoza@manquemavida.cl,pia.cabrera@manquemavida.cl,renato.arellano@manquemavida.cl,lyssett.abarca@manquemavida.cl,florencia.beltran@manquemavida.cl,david.aguilera@manquemavida.cl,aaron.bravo@manquemavida.cl,amanda.martinez@manquemavida.cl,josefa.bustamante@manquemavida.cl,vicente.vilca@manquemavida.cl,camila.zamora@manquemavida.cl,antonella.suarez@manquemavida.cl,matilda.silva@manquemavida.cl,maximiliano.reyes@manquemavida.cl,maximo.soto@manquemavida.cl,lucas.reyes@manquemavida.cl,isidora.espindola@manquemavida.cl,damian.calderon@manquemavida.cl,benjamin.diaz@manquemavida.cl,benjamin.ibanez@manquemavida.cl,isidora.contreras@manquemavida.cl,carla.cabello@manquemavida.cl,rocio.arenas@manquemavida.cl,anahy.bustos@manquemavida.cl,maite.arcos@manquemavida.cl,kevin.alarcon@manquemavida.cl"
correos_8B=['rafaella.zepeda@manquemavida.cl', 'francisca.valdes@manquemavida.cl', 'agustin.sandoval@manquemavida.cl', 'joaquin.valenzuela@manquemavida.cl', 'alberto.urbina@manquemavida.cl', 'vicente.pina@manquemavida.cl', 'pia.perez@manquemavida.cl', 'javiera.onate@manquemavida.cl', 'damian.morales@manquemavida.cl', 'valentina.palomino@manquemavida.cl', 'fernanda.lopez@manquemavida.cl', 'isidora.herrera@manquemavida.cl', 'rafaela.munoz@manquemavida.cl', 'mateo.henriquez@manquemavida.cl', 'amanda.caballero@manquemavida.cl', 'bastian.cantero@manquemavida.cl', 'sofia.carrasco@manquemavida.cl', 'matias.cornejo@manquemavida.cl', 'matias.arriagada@manquemavida.cl', 'emilia.duarte@manquemavida.cl', 'josefa.cid@manquemavida.cl', 'camila.araneda@manquemavida.cl', 'florencia.vidal@manquemavida.cl', 'liceloth.vilches@manquemavida.cl', 'isidora.vergara@manquemavida.cl', 'nicolas.vergara@manquemavida.cl', 'maximiliano.sanchez@manquemavida.cl', 'amanda.sotelo@manquemavida.cl', 'dania.salas@manquemavida.cl', 'martin.saavedra@manquemavida.cl', 'josefa.pizarro@manquemavida.cl', 'antonieta.marin@manquemavida.cl', 'florencia.orellana@manquemavida.cl', 'mateo.fabres@manquemavida.cl', 'trinidad.bravo@manquemavida.cl', 'marcelo.albornoz@manquemavida.cl']
correos_1C=c.split(",")
def obtener_nombre_correo(lista_correos):
    lista_nombreApellido_correo=[]
    for a in lista_correos:
        nombre,apellido=a.split("@")[0].split(".")
        lista_nombreApellido_correo.append(f"{nombre} {apellido},{a}")
    return lista_nombreApellido_correo

def tablas_iniciales(nombre_ensayo,curso):
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

    nombres=[]
    for cont in contenido:
        nom=cont[2].strip('"')
        ape=cont[3].strip('"')
        nombres.append(f"{nom} {ape}")
    return nombres
    print(nombres)
    for a in nombres:
        print(a)


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
tablas_iniciales(nombre_quiz,curso_elegido)



print(obtener_nombre_correo(correos_8B))
#print(obtener_nombre(correos_1B))

l1=tablas_iniciales(nombre_quiz,curso_elegido)
l2=obtener_nombre_correo(correos_8B)

# Crear un diccionario para los correos de l2
dict_nombre_correo = {}
for entry in l2:
    name, email = entry.split(',')
    dict_nombre_correo[name.strip().lower()] = email.strip()

# Función para encontrar coincidencias aproximadas
def encontrar_coincidencia(nombre, nombres_l2):
    nombre = nombre.lower()
    coincidencias = get_close_matches(nombre, nombres_l2, n=1, cutoff=0.3)
    return coincidencias[0] if coincidencias else None

# Crear la nueva lista con nombres de l1 y correos de l2
nueva_lista = []
for nombre in l1:
    nombre_buscado = " ".join(nombre.split()[:2]).lower()  # Usar primer y segundo nombre
    coincidencia = encontrar_coincidencia(nombre_buscado, dict_nombre_correo.keys())
    if coincidencia:
        nueva_lista.append((nombre, dict_nombre_correo[coincidencia]))

# Imprimir la nueva lista
i=1
for nombre, correo in nueva_lista:
    print(f'{i}.- {nombre}: {correo}')
    i+=1
with open("correos_8B.csv", "a",encoding="utf-8") as correos:
    correos.write("Nombre,e-mail\n")
    for nombre, correo in nueva_lista:
        correos.write(f"{nombre},{correo}\n")