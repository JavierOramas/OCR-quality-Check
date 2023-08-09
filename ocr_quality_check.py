#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 10:01:27 2023

@author: rod
"""

import spacy
import re

def compute_non_alpha_ratio(text):
    # Encuentra todas las palabras con caracteres no alfabéticos en medio
    words_with_non_alpha = re.findall(r'\b\w*[^a-zA-Z0-9_]\w*\b', text)

    # Encuentra todas las palabras
    all_words = re.findall(r'\b\w+\b', text)

    if len(all_words) == 0: 
        return 0
    # Calcula y retorna el ratio
    return len(words_with_non_alpha) / len(all_words), len(all_words)

# Carga los modelo de lenguaje
try:
    import es_core_news_lg
    nlp_es = spacy.load('es_core_news_lg')
except OSError:
    import es_core_news_sm
    nlp_es = spacy.load('es_core_news_sm')
    
def compute_legible_ratio(text, nlp):
    # Procesamiento del texto
    doc = nlp(text)
    
    if len(doc) == 0:
        return 0

    # Contador de palabras legibles
    legible_count = 0

    # Revisión de cada palabra
    for token in doc:
        if token.pos_ != 'X':
            legible_count += 1

    # Cálculo del ratio de palabras legibles
    legible_ratio = legible_count / len(doc)

    return legible_ratio, len(doc)


# # Ejemplo de texto de entrada en español
# text = "Esto es un texto de ejemplo con algunas paabras mal escr\itas."

def compute_document(text):
    legible_ratio_es, detected_legible = compute_legible_ratio(text, nlp_es)
    
    # print(f"Ratio de palabras reconocidas: {legible_ratio_es}")
    
    # Cálculo del ratio de palabras con caracteres no alfabéticos
    non_alpha_ratio, detected_alpha = compute_non_alpha_ratio(text)

    # print(f"Ratio de palabas con carácteres no alfanúmericos: {non_alpha_ratio}")

    return legible_ratio_es, detected_legible, non_alpha_ratio, detected_alpha
