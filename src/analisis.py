import pandas as pd


nombre_mapeo="mapeos_potencias 8vo.csv"
with open(nombre_mapeo,"r",encoding="utf-8") as map:
    lista_lineas=[linea.strip("\n").split(",") for linea in map.readlines()]
    mapeos={"Forma A":[],"Forma B":[],"Forma C":[],"Forma D":[],"Forma E":[]}
    for linea in lista_lineas[1:]:
        mapeos["Forma A"].append(linea[0])
        mapeos["Forma B"].append(linea[1])
        mapeos["Forma C"].append(linea[2])
        mapeos["Forma D"].append(linea[3])
        mapeos["Forma E"].append(linea[4])
print(mapeos)

    

def reor_forma_A(lista_original,mapeo):
    #print(mapeo)
    reordenada=[0 for i in lista_original]
    for idx,resp in enumerate(lista_original):
        #print(type(idx))
        reordenada[int(mapeo[idx])-1]=resp
    return reordenada


nombre_archivo="quiz-Potencias 8vo-full.csv"
with open(nombre_archivo,"r",encoding="utf-8") as archivo:
    lineas=archivo.readlines()
    lineas_limpias=[l.strip("\n").split(",") for l in lineas]
respuestas_alumnos=[]
for a in lineas_limpias[1:]:
    alumno={}
    id=a[4]
    alumno["Id"]=id
    print(f"Id: {id}")
    nombre=a[2].strip('"')+" "+a[3].strip('"')
    alumno["Nombre"]=nombre
    #respuestas_alumnos[]=nombre
    print(f"Nombre: {nombre}")
    forma="Forma "+a[11]
    alumno["Forma"]=forma
    print(f"Forma: {forma}")
    clave={"C":1,"X":0}
    rev=[clave[e] for indice,e in enumerate(a[12:]) if indice%4==3]
    alumno["Respuestas forma original"]=rev
    respuestas_alumnos.append(alumno)
    rev_mapeadas=reor_forma_A(rev,mapeos[forma])
    alumno["Respuestas mapeadas a forma A"]=rev_mapeadas
    alumno["Datos para analizar"]=[alumno["Id"],alumno["Nombre"]]+alumno["Respuestas mapeadas a forma A"]
    print(rev_mapeadas)
    print(rev)
    print("-----------------")

matriz_respuestas=[]
matriz_respuestas_para_analisis=[["Id","Nombre"]+[f"p{i}" for i in range(1,31)]]

for a in respuestas_alumnos:
    #print(list(a.keys()))
    
    matriz_respuestas.append(a["Respuestas mapeadas a forma A"])
    matriz_respuestas_para_analisis.append(a["Datos para analizar"])
    #print(a["Respuestas mapeadas a forma A"])
with open("resultados.csv","a",encoding="utf-8") as rasult:
    for a in matriz_respuestas:
        rasult.write(str(a).strip("[").strip("]")+"\n")
with open("resultados_alumnos.csv","a",encoding="utf-8") as rasult:
    for a in matriz_respuestas_para_analisis:
        rasult.write(str(a).strip("[").strip("]")+"\n")

#print(matriz_respuestas)
#for a in matriz_respuestas:
#    print(a)

# df = pd.DataFrame(matriz_respuestas)
# print("-----------------------------------------------------")
# df['Total_Correctas'] = df.sum(axis=1)
# print(df[['Total_Correctas']])
# print("-----------------------------------------------------")
# df_pregunta = df.mean(axis=0)
# print(df_pregunta)
# print("-----------------------------------------------------")
# df['Porcentaje_Correctas'] = (df.sum(axis=1) / df.shape[1]) * 100
# print(df[['Porcentaje_Correctas']])
# print("-----------------------------------------------------")
# preguntas_dificiles = df_pregunta[df_pregunta < 0.5]
# print(preguntas_dificiles)
# print("-----------------------------------------------------")
# df_pregunta = df.mean(axis=0)
# print(df_pregunta)
# print("-----------------------------------------------------")
# import matplotlib.pyplot as plt

# plt.hist(df['Porcentaje_Correctas'], bins=10, edgecolor='k')
# plt.title('Distribución del Porcentaje de Respuestas Correctas')
# plt.xlabel('Porcentaje de Respuestas Correctas')
# plt.ylabel('Número de Estudiantes')
# plt.show()
# print("-----------------------------------------------------")
# df_pregunta.plot(kind='bar')
# plt.title('Promedio de Respuestas Correctas por Pregunta')
# plt.xlabel('Pregunta')
# plt.ylabel('Promedio de Respuestas Correctas')
# plt.show()
# print("-----------------------------------------------------")
# preguntas_dificiles = df_pregunta[df_pregunta < 0.5]
# print(preguntas_dificiles)
# print("-----------------------------------------------------")
# # Contar las respuestas correctas por pregunta
# cantidad_correctas_por_pregunta = df.sum(axis=0)


# print(cantidad_correctas_por_pregunta.round())

# print("-----------------------------------------------------")

# print("-----------------------------------------------------")

