import spacy
from typing import List, Tuple, Any


custom_scibert = spacy.load(R"./model-ner")

def extract_medical_terms(text : str) -> List[str]:
    """
    Extracts medical terms from document
    """
    
    doc = scibert(text)
    return list(set([doc.ents[i].text for i in range(len(doc.ents))]))
