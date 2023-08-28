import tqdm
from typer import Typer, Argument, Option
import os
from pdf_handler import get_ocr
from ocr_quality_check import compute_document
import concurrent
from report_generator import generate_excel_summary

from functools import wraps
import time


app = Typer()

def process_single_pdf(pdf_path:str):
    ocr_result = get_ocr(pdf_path)
    legible_ratio_es, detected_legible, non_alpha_ratio, detected_alpha, detected_entities = compute_document(ocr_result)
    return legible_ratio_es, detected_legible, non_alpha_ratio, detected_alpha, detected_entities
def process_pdf_files(path):
    data = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for folder, _, files in os.walk(path):
            with tqdm.tqdm(total=len(files), desc="Processing PDFs", unit="files") as pbar:
                for file in files:
                    if file.endswith(".pdf"):
                        pdf_path = os.path.join(folder, file)
                        future = executor.submit(process_single_pdf, pdf_path)
                        futures.append((pdf_path, future))

                for pdf_path, future in futures:
                    try:
                        legible_ratio_es, detected_legible, non_alpha_ratio, detected_alpha, detected_entities = future.result()
                        data[pdf_path] = {"legible_ratio_es": legible_ratio_es, 
                                          "non_alpha_ratio": non_alpha_ratio, 
                                          "detected_words_legible": detected_legible, 
                                          "detected_words_alpha": detected_alpha,
                                          "detected_entities": detected_entities}
                        pbar.update(1)
                    except Exception as e:
                        print(f"Error processing {pdf_path}: {e}")

    return data

@app.command(name="folder", help="procesa todos los documentos ded un directorio")
def process_folder(path=Argument(default=".", help="Ruta de la carpeta")):
    
    data = process_pdf_files(path)
    print("Procesado terminado, generando reporte")
    generate_excel_summary(data, excel_file_path=os.path.join(path, "summary.xlsx"))

    
            
if __name__ == "__main__":
    app()