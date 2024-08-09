from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def crear_pdf(nombre_archivo, contenido):
    pdf_filename = f"{nombre_archivo}-Tablas_datos_y_respuestas.pdf"

    # Definir los márgenes (en puntos, donde 1 pulgada = 72 puntos)
    left_margin = 10
    right_margin = 10
    top_margin = 10
    bottom_margin = 10

    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        leftMargin=left_margin,
        rightMargin=right_margin,
        topMargin=top_margin,
        bottomMargin=bottom_margin
    )

    styles = getSampleStyleSheet()
    flowables = []

    for item in contenido:
        paragraph = Paragraph(item, styles['Normal'])
        flowables.append(paragraph)
        flowables.append(Spacer(1, 12))  # Añadir espacio entre párrafos

    doc.build(flowables)

# Ejemplo de uso
nombre_archivo = "Ejemplo"
contenido = ["Este es un ejemplo de contenido para el PDF.", "Otra línea de contenido."]
crear_pdf(nombre_archivo, contenido)