#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 10:01:27 2023

@author: rod
"""

import spacy
from collections import defaultdict
import re

from flair.data import Sentence
from flair.models import SequenceTagger
import flair, torch

# Forzar a Flair a usar la CPU
flair.device = torch.device('cpu')

# Carga los modelo de lenguaje
while True:
    try:
        nlp_es = spacy.load('es_core_news_lg')
        nlp_en = spacy.load('en_core_web_lg')
        # load tagger
        tagger = SequenceTagger.load("flair/ner-multi")
        break
    except OSError:
        import subprocess

        cmd = f"python -m spacy download es_core_news_lg"
        subprocess.check_call(cmd, shell=True)
        cmd = f"python -m spacy download en_core_web_lg"
        subprocess.check_call(cmd, shell=True)

        
    


nlp_es.max_length = 30000000  # por ejemplo, para establecer el límite en 30,000,000 caracteres
nlp_en.max_length = 30000000  # por ejemplo, para establecer el límite en 30,000,000 caracteres

def sliding_window(text, window_size, overlap):
    """
    Divide el texto en chunks utilizando una ventana deslizable.
    
    Args:
    - text (str): El texto a dividir.
    - window_size (int): Tamaño del chunk.
    - overlap (int): Cantidad de caracteres de solapamiento entre chunks consecutivos.

    Returns:
    - List[str]: Lista de chunks.
    """
    chunks = []
    start_idx = 0
    while start_idx < len(text):
        end_idx = start_idx + window_size
        chunks.append(text[start_idx:end_idx])
        start_idx = end_idx - overlap
    return chunks

def compute_non_alpha_ratio(doc):
    # Encuentra todas las palabras con caracteres no alfabéticos en medio
    words_with_non_alpha = [token.text for token in doc if re.search(r'\b\w*[^a-zA-Z0-9_áéíóúÁÉÍÓÚñÑ]\w*\b', token.text)]
    # print(words_with_non_alpha)
    
    if len(doc) == 0: 
        return 0
    # Calcula y retorna el ratio
    return len(words_with_non_alpha) / len(doc)


    
def compute_legible_ratio(doc):
    # Procesamiento del texto
       
    if len(doc) == 0:
        return 0

    # Contador de palabras legibles
    legible_count = 0

    # Revisión de cada palabra
    for token in doc:
        if token.pos_ != 'X':
            # print(token.text, token.pos_)
            legible_count += 1

    # Cálculo del ratio de palabras legibles
    legible_ratio = legible_count / len(doc)

    return float(legible_ratio)

def clean_text(text):
    text = re.sub(r'\s*\n\s*', ' ', text)  # Eliminar saltos de línea y espacios adicionales
    text = re.sub(r'\s{2,}', ' ', text)    # Eliminar espacios dobles
    return text.strip()


def detect_entities(text,engine="spacy"):
    if text == "":
        return ""
    
    entities = {}
    
    if engine == "spacy":
        doc = nlp_es(clean_text(text))
        # print("spacy")
        for ent in doc.ents:
            if ent.text in entities:
                if ent.label_ in entities[ent.text]:
                    entities[ent.text][ent.label_] += 1
                else:
                    entities[ent.text][ent.label_] = 1
            else:
                entities[ent.text] = {
                    ent.label_: 1
                }
    if engine == "flair":
        # print("flair")
        # make example sentence in any of the four languages
        
        chunks = sliding_window(text, window_size=1000, overlap=200)
        
        for chunk in chunks:
            sentence = Sentence(chunk)
            tagger.predict(sentence)
        
        # iterate over entities and print
        for ent in sentence.get_spans('ner'):
            if ent.text in entities:
                if ent.tag in entities[ent.text]:
                    entities[ent.text][ent.tag] += 1
                else:
                    entities[ent.text][ent.tag] = 1
            else:
                entities[ent.text] = {
                    ent.tag: 1
                }

    doc = nlp_en(text)
    
    for ent in doc.ents:
        if ent.label_ in ["DATE", "TIME"]:
            if ent.text in entities:
                if ent.label_ in entities[ent.text]:
                    entities[ent.text][ent.label_] += 1
                else:
                    entities[ent.text][ent.label_] = 1
            else:
                entities[ent.text] = {
                    ent.label_: 1
                }
            
    return entities

# # Ejemplo de texto de entrada en español
# text = "Esto es un texto de ejemplo con algunas paabras mal escr\itas."

def compute_document(text):
    
    doc = nlp_es(text)
    
    
    legible_ratio_es = compute_legible_ratio(doc)
    
    # print(f"Ratio de palabras reconocidas: {legible_ratio_es}")
    
    # Cálculo del ratio de palabras con caracteres no alfabéticos
    non_alpha_ratio = compute_non_alpha_ratio(doc)
    
    detected_entities = detect_entities(text)

    # print(f"Ratio de palabas con carácteres no alfanúmericos: {non_alpha_ratio}")

    return legible_ratio_es, non_alpha_ratio, len(doc), detected_entities


if __name__ == "__main__":
    
    from pdf_handler import get_ocr
            
    text = get_ocr('notas IBERO/IBNP2009021301.pdf')
    legible_ratio_es, non_alpha_ratio, num_tokens, detected_entities = compute_document(text)
    doc = nlp_es(text)
    tokens = [token.text for token in doc]
    print(detected_entities)
    