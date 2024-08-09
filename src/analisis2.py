import pandas as pd
import numpy as np
from scipy.stats import pointbiserialr
from sklearn.preprocessing import StandardScaler
from fpdf import FPDF

# Cargar los datos de respuestas
#data = pd.read_csv('/mnt/data/resultados.csv')
data = pd.read_csv('resultados.csv')

# Renombrar las columnas para que las preguntas estén numeradas del 1 al 30
data.columns = [f'Pregunta {i+1}' for i in range(data.shape[1] - 1)] + ['Puntaje']

# Calcular la dificultad de cada pregunta
dificultad = data.drop(columns=['Puntaje']).mean()

# Calcular la discriminación de cada pregunta
discriminacion = []
for col in data.drop(columns=['Puntaje']):
    r, _ = pointbiserialr(data[col], data['Puntaje'])
    discriminacion.append(r)
discriminacion = pd.Series(discriminacion, index=dificultad.index)

# Crear una tabla con los resultados
resultados = pd.DataFrame({
    'Dificultad': dificultad,
    'Discriminación': discriminacion
})

# Clasificación de la dificultad de los ítems
clasificacion_dificultad = pd.cut(
    resultados['Dificultad'],
    bins=[0, 0.39, 0.50, 0.80, 0.90, 1],
    labels=['Difícil', 'Relativamente difícil', 'Dificultad adecuada (Media)', 'Relativamente fácil', 'Fácil']
)

# Clasificación de la discriminación de los ítems
clasificacion_discriminacion = pd.cut(
    resultados['Discriminación'],
    bins=[-np.inf, 0, 0.19, 0.29, 0.39, 1],
    labels=['Pésimo', 'Pobre', 'Regular', 'Buena', 'Excelente']
)

resultados['Clasificación Dificultad'] = clasificacion_dificultad
resultados['Clasificación Discriminación'] = clasificacion_discriminacion

# Calcular el coeficiente de correlación biserial puntual
correlacion_biserial = []
for col in data.drop(columns=['Puntaje']):
    r, _ = pointbiserialr(data[col], data['Puntaje'])
    correlacion_biserial.append(r)
correlacion_biserial = pd.Series(correlacion_biserial, index=dificultad.index)
resultados['Correlación Biserial'] = correlacion_biserial

# Calcular la confiabilidad del instrumento (alfa de Cronbach)
def cronbach_alpha(df):
    item_scores = df.T
    item_variances = item_scores.var(axis=1, ddof=1)
    total_score_variance = item_scores.sum().var(ddof=1)
    n_items = len(df.columns)
    alpha = (n_items / (n_items - 1)) * (1 - (item_variances.sum() / total_score_variance))
    return alpha

confiabilidad = cronbach_alpha(data.drop(columns=['Puntaje']))

# Guardar los resultados en un archivo CSV
resultados.to_csv('analisis_evaluacion.csv', index_label='Pregunta')

# Imprimir los resultados
print("Análisis de la evaluación:")
print(resultados)

# Interpretación de los resultados
interpretacion = f"""
Interpretación de los resultados:

1. Dificultad:
   - Fácil: 0.91 - 1
   - Relativamente fácil: 0.81 - 0.90
   - Dificultad adecuada (Media): 0.51 - 0.80
   - Relativamente difícil: 0.40 - 0.50
   - Difícil: 0 - 0.39

2. Discriminación:
   - Excelente: 0.40 - 1 (Conservar)
   - Buena: 0.30 - 0.39 (Posibilidad de mejorar)
   - Regular: 0.20 - 0.29 (Necesidad de revisar)
   - Pobre: 0 - 0.19 (Descartar o revisar a profundidad)
   - Pésimo: < 0.01 (Descartar definitivamente)

Coeficiente de correlación biserial puntual:
{correlacion_biserial}

Confiabilidad del instrumento (Alfa de Cronbach):
{confiabilidad:.2f}

Preguntas más difíciles y con mejor discriminación:
"""

preguntas_dificiles = resultados[resultados['Clasificación Dificultad'] == 'Difícil']
preguntas_buenas = resultados[resultados['Clasificación Discriminación'] == 'Excelente']

interpretacion += "\nPreguntas más difíciles:\n"
interpretacion += preguntas_dificiles.to_string() + "\n"

interpretacion += "\nPreguntas con mejor discriminación:\n"
interpretacion += preguntas_buenas.to_string() + "\n"

print(interpretacion)

# Exportar el análisis a un archivo PDF
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Análisis de Evaluación', 0, 1, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(5)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()

    def add_table(self, df):
        self.set_font('Arial', 'B', 10)
        col_width = (self.w - 2 * self.l_margin) / len(df.columns)  # distribute content evenly
        for col in df.columns:
            self.cell(col_width, 10, col, 1)
        self.ln()

        self.set_font('Arial', '', 10)
        for index, row in df.iterrows():
            for col in df.columns:
                self.cell(col_width, 10, str(row[col]), 1)
            self.ln()

pdf = PDF()
pdf.add_page()
pdf.chapter_title('Interpretación de los Resultados')
pdf.chapter_body(interpretacion)
pdf.chapter_title('Resultados Detallados')
pdf.add_table(resultados)

#pdf.output('/mnt/data/analisis_evaluacion.pdf')
pdf.output('analisis_evaluacion.pdf')
