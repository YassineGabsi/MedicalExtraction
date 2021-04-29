import json
import os 

THRESHHOLD = 0 
TOP_K = 3

BASE_PATH = os.path.join(os.path.dirname(__file__))
INPUT_PATH = BASE_PATH + "/input.csv"
OUTPUT_PATH = BASE_PATH + "/output.csv"

PCA_PATH = "./pca_tfidf.sav" 
MODEL_PATH = "./clf_tfidf.sav"
PCA_PATH_TITLE = "./pca_title.sav"
PCA_PATH_ABSTRACT = "./pca_abstract.sav"
PCA_PATH_INCLUSION = "./pca_inclusion.sav"

TFIDF_PATH_TITLE = "./tfidf_title.sav"
TFIDF_PATH_ABSTRACT = "./tfidf_abstract.sav"
TFIDF_PATH_INCLUSION = "./tfidf_inclusion.sav"

LABELS = json.loads(open(BASE_PATH + "/../common/data/labels.json", "r").read())
