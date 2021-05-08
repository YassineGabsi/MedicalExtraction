import os

import spacy
from typing import List, Tuple, Any

BASE_PATH = os.path.join(os.path.dirname(__file__))
custom_scibert = spacy.load(BASE_PATH + "/model-ner")

def extract_medical_terms(text : str) -> List[str]:
    """
    Extracts medical terms from document
    """
    
    doc = custom_scibert(text)
    return list(set([doc.ents[i].text for i in range(len(doc.ents))]))
