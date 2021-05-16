import os

import spacy
from typing import List, Tuple, Any
import re


def is_alpha_num(word: str) -> bool:
    return re.match(r'^[\w \t]+$', word, flags=re.IGNORECASE)


BASE_PATH = os.path.join(os.path.dirname(__file__))
custom_scibert = spacy.load(BASE_PATH + "/model-ner")

sp = spacy.load('en_core_web_sm')

all_stopwords = sp.Defaults.stop_words


def extract_medical_terms(text: str) -> List[str]:
    """
    Extracts medical terms from document
    """

    doc = custom_scibert(text)
    return list(set([doc.ents[i].text for i in range(len(doc.ents)) if
                     is_alpha_num(doc.ents[i].text) and not doc.ents[i].text in all_stopwords]))
