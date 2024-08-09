lista_nueva=[]
archivo="correos_8B.csv"
with open(archivo,"r",encoding="utf-8") as correos:
    
    lineas=correos.readlines()
    for lin in lineas:
        nombre,correo,verif=lin.strip("\n").split(",")
        if nombre!="Nombre":
            resp=input(f"Nombre: {nombre}\nE-mail:{correo}\nCorrecto? (s/n) -> ")
            if resp.lower()=="s":
                lista_nueva.append(f"{nombre},{correo},Correcto\n")
            else:
                lista_nueva.append(f"{nombre},{correo},Incorrecto\n")
        else:
            lista_nueva.append(f"{nombre},{correo},Verificación\n")

with open(archivo,"w",encoding="utf-8") as correos:
    for lis in lista_nueva:
        correos.write(lis)


