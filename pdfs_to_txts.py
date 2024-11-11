import os
from tika import parser

def extraer_texto_pdf(ruta_pdf):
    # Extrae el texto del PDF usando Tika
    texto_extraido = parser.from_file(ruta_pdf)
    return texto_extraido['content']

def guardar_texto_en_txt(texto, ruta_txt):
    # Guarda el texto en un archivo .txt
    with open(ruta_txt, 'w', encoding='utf-8') as archivo_txt:
        archivo_txt.write(texto)

def procesar_directorio(directorio):
    for archivo in os.listdir(directorio):
        if archivo.lower().endswith('.pdf'):
            ruta_pdf = os.path.join(directorio, archivo)
            texto = extraer_texto_pdf(ruta_pdf)
            if texto:
                nombre_archivo_txt = archivo[:-4] + '.txt'
                if not os.path.exists(directorio + "_txts"):
                    os.makedirs(directorio + "_txts")
                ruta_txt = os.path.join(directorio + "_txts", nombre_archivo_txt)
                guardar_texto_en_txt(texto, ruta_txt)
                print(f"Texto extraído y guardado: {nombre_archivo_txt}")
            else:
                print(f"No se pudo extraer texto de: {archivo}")

directorio_pdfs = 'notas IBERO'  # Cambia esto por la ruta de tu carpeta con PDFs
procesar_directorio(directorio_pdfs)