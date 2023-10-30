import tqdm
from typer import Typer, Argument, Option
import os
from pdf_handler import get_ocr
from ocr_quality_check import compute_document
import concurrent.futures
from report_generator import generate_excel_summary
import json

from functools import wraps
import time


app = Typer()

def process_single_pdf(pdf_path:str):
    ocr_result = get_ocr(pdf_path)
    return compute_document(ocr_result)

def process_pdf_files(path):
    data = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        futures = []
        for folder, _, files in os.walk(path):
            with tqdm.tqdm(total=len(files), desc="Processing Files", unit="files") as pbar:
                for file in files:
                    pdf_path = os.path.join(folder, file)
                    future = executor.submit(process_single_pdf, pdf_path)
                    futures.append((pdf_path, future))

                for pdf_path, future in futures:
                    try:
                        legible_ratio_es, non_alpha_ratio, num_tokens, detected_entities = future.result()
                        data[pdf_path] = {"legible_ratio_es": legible_ratio_es, 
                                          "non_alpha_ratio": non_alpha_ratio, 
                                          "num_tokens": num_tokens, 
                                          "detected_entities": detected_entities
                                         }
                        pbar.update(1)
                    except Exception as e:
                        print(f"Error processing {pdf_path}: {e}")

    return data

@app.command(name="folder", help="procesa todos los documentos ded un directorio")
def process_folder(path=Argument(default=".", help="Ruta de la carpeta")):
    data = process_pdf_files(path)
    with open(os.path.join(path,'datos.json'), 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    print("Procesado terminado, generando reporte")
    generate_excel_summary(data, excel_file_path=os.path.join(path, "summary.xlsx"))

    
            
if __name__ == "__main__":
    app()