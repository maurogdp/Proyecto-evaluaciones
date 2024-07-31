from difflib import get_close_matches

# Definir las listas l1 y l2
l1 = ['Lyssett Yanara Esperanza Abarca', 'David Ignacio Aguilera', 'Kevin Andrés Alarcón', 'Maite Jesús Arcos', 'Renato Andrés Del Carmen Arellano', 'Rocío Andrea Arenas', 'Florencia Isabel Beltrán', 'Aaron Nicolás Bravo', 'Josefa Antonia Bustamante', 'Anahy Belén Bustos', 'Carla Andrea Cabello', 'Pía Carolina Cabrera', 'Damián Ignacio Calderón', 'Isidora Sofía Contreras', 'Benjamín Alejandro Díaz', 'Valentina Fernanda Espinoza', 'Isidora Carolina Espíndola', 'Claudio Ignacio Herrera', 'Benjamín Alonso Ibáñez', 'Agustina Antonia Jeria', 'Amanda Martínez', 'Clemente Agustín Ignacio Morales', 'Julieta Valentina Morales', 'Nicolás Alonso Muñoz', 'Martina Constanza Ojeda', 'Francisca Leticia Paredes', 'Lucas Joaquín Reyes', 'Catalina Ignacia Sierra', 'Matilda Isidora Silva', 'Antonella Del Pilar Suárez', 'Javiera Emilia Valdivia', 'Luz Antonella Vega', 'José Pablo Verdugo', 'Antonia Florencia Vergara', 'Vicente Javier Vidal', 'Vicente Aníbal Vilca', 'Camila Fernanda Zamora']

l2 = ['vicente vidal,vicente.vidal@manquemavida.cl', 'luz vega,luz.vega@manquemavida.cl', 'jose verdugo,jose.verdugo@manquemavida.cl', 'antonia vergara,antonia.vergara@manquemavida.cl', 'javiera valdivia,javiera.valdivia@manquemavida.cl', 'catalina sierra,catalina.sierra@manquemavida.cl', 'martina ojeda,martina.ojeda@manquemavida.cl', 'nicolas munoz,nicolas.munoz@manquemavida.cl', 'clemente morales,clemente.morales@manquemavida.cl', 'julieta morales,julieta.morales@manquemavida.cl', 'agustina jeria,agustina.jeria@manquemavida.cl', 'claudio herrera,claudio.herrera@manquemavida.cl', 'valentina espinoza,valentina.espinoza@manquemavida.cl', 'pia cabrera,pia.cabrera@manquemavida.cl', 'renato arellano,renato.arellano@manquemavida.cl', 'lyssett abarca,lyssett.abarca@manquemavida.cl', 'florencia beltran,florencia.beltran@manquemavida.cl', 'david aguilera,david.aguilera@manquemavida.cl', 'aaron bravo,aaron.bravo@manquemavida.cl', 'amanda martinez,amanda.martinez@manquemavida.cl', 'josefa bustamante,josefa.bustamante@manquemavida.cl', 'vicente vilca,vicente.vilca@manquemavida.cl', 'camila zamora,camila.zamora@manquemavida.cl', 'antonella suarez,antonella.suarez@manquemavida.cl', 'matilda silva,matilda.silva@manquemavida.cl', 'maximiliano reyes,maximiliano.reyes@manquemavida.cl', 'maximo soto,maximo.soto@manquemavida.cl', 'lucas reyes,lucas.reyes@manquemavida.cl', 'isidora espindola,isidora.espindola@manquemavida.cl', 'damian calderon,damian.calderon@manquemavida.cl', 'benjamin diaz,benjamin.diaz@manquemavida.cl', 'benjamin ibanez,benjamin.ibanez@manquemavida.cl', 'isidora contreras,isidora.contreras@manquemavida.cl', 'carla cabello,carla.cabello@manquemavida.cl', 'rocio arenas,rocio.arenas@manquemavida.cl', 'anahy bustos,anahy.bustos@manquemavida.cl', 'maite arcos,maite.arcos@manquemavida.cl', 'kevin alarcon,kevin.alarcon@manquemavida.cl']

# Crear un diccionario para los correos de l2
dict_l2 = {}
for entry in l2:
    name, email = entry.split(',')
    dict_l2[name.strip().lower()] = email.strip()

# Función para encontrar coincidencias aproximadas
def encontrar_coincidencia(nombre, nombres_l2):
    nombre = nombre.lower()
    coincidencias = get_close_matches(nombre, nombres_l2, n=1, cutoff=0.3)
    return coincidencias[0] if coincidencias else None

# Crear la nueva lista con nombres de l1 y correos de l2
nueva_lista = []
for nombre in l1:
    nombre_buscado = " ".join(nombre.split()[:2]).lower()  # Usar primer y segundo nombre
    coincidencia = encontrar_coincidencia(nombre_buscado, dict_l2.keys())
    if coincidencia:
        nueva_lista.append((nombre, dict_l2[coincidencia]))

# Imprimir la nueva lista
i=1
for nombre, correo in nueva_lista:
    print(f'{i}.- {nombre}: {correo}')
    i+=1
