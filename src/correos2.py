from difflib import get_close_matches

# Definir las listas l1 y l2
l1 = ['Marcelo Anthony Ignacio Albornoz', 'Camila Danae Araneda', 'Matías Alejandro Arriagada', 'Trinidad Agustina Bravo', 'Amanda Sofía Caballero', 'Bastián Andrés Cantero', 'Sofía Antonia Carrasco', 'Josefa Valentina Cid', 'Matías Benjamín Cornejo', 'Magdalena Cumsille', 'Emilia Jesús Duarte', 'Mateo Antonio Fabres', 'Mateo Alonso Henríquez', 'Isidora Fernanda Herrera', 'Fernanda Antonia López', 'Antonieta Consuelo Marín', 'Damián Esteban Morales', 'Rafaela Ignacia Muñoz', 'Florencia Renata Orellana', 'Javiera Valentina Oñate', 'Valentina Ignacia Palomino', 'Josefa Emilia Pizarro', 'Vicente Gaspar Piña', 'Pía Martina Pérez', 'Martín Jesús Saavedra', 'Dania Constanza Salas', 'Agustín Ignacio Sandoval', 'Amanda Ali Sol Sotelo', 'Maximiliano Agustín Sánchez', 'Alberto Alfonso Urbina', 'Francisca Ignacia Valdés', 'Joaquín Andrés Valenzuela', 'Isidora Agustina Vergara', 'Nicolás Patricio Vergara', 'Florencia Antonia Vidal', 'Liceloth Paula Vilches', 'Rafaella Agustina Zepeda']

l2 = ['rafaella.zepeda@manquemavida.cl', 'francisca.valdes@manquemavida.cl', 'agustin.sandoval@manquemavida.cl', 'joaquin.valenzuela@manquemavida.cl', 'alberto.urbina@manquemavida.cl', 'vicente.pina@manquemavida.cl', 'pia.perez@manquemavida.cl', 'javiera.onate@manquemavida.cl', 'damian.morales@manquemavida.cl', 'valentina.palomino@manquemavida.cl', 'fernanda.lopez@manquemavida.cl', 'isidora.herrera@manquemavida.cl', 'rafaela.munoz@manquemavida.cl', 'mateo.henriquez@manquemavida.cl', 'amanda.caballero@manquemavida.cl', 'bastian.cantero@manquemavida.cl', 'sofia.carrasco@manquemavida.cl', 'matias.cornejo@manquemavida.cl', 'matias.arriagada@manquemavida.cl', 'emilia.duarte@manquemavida.cl', 'josefa.cid@manquemavida.cl', 'camila.araneda@manquemavida.cl', 'florencia.vidal@manquemavida.cl', 'liceloth.vilches@manquemavida.cl', 'isidora.vergara@manquemavida.cl', 'nicolas.vergara@manquemavida.cl', 'maximiliano.sanchez@manquemavida.cl', 'amanda.sotelo@manquemavida.cl', 'dania.salas@manquemavida.cl', 'martin.saavedra@manquemavida.cl', 'josefa.pizarro@manquemavida.cl', 'antonieta.marin@manquemavida.cl', 'florencia.orellana@manquemavida.cl', 'mateo.fabres@manquemavida.cl', 'trinidad.bravo@manquemavida.cl', 'marcelo.albornoz@manquemavida.cl']

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
