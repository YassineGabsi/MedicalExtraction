import json
import os
import pickle

import torch
from datetime import date

from transformers import AutoTokenizer, AutoModel

from model.common import CATEGORIES_DF

DEVICE = torch.device("cuda:0")
MODEL = "allenai/biomed_roberta_base"
VECTORS_PATH = "{}_vectors_{}.vectors".format(MODEL, date.today())
THRESHHOLD = 0  # Minimum number of occurences to keep the class (0 for keeping all classes)

SAMPLE_SIZE = 50
BASE_PATH = os.path.join(os.path.dirname(__file__))
FULL_DATA_PATH = BASE_PATH + "/final_data.csv"
INPUT_PATH = BASE_PATH + "/input.csv"
OUTPUT_PATH = BASE_PATH + "/output.csv"
MODEL_PATH = BASE_PATH + "/model_svc.sav"
PCA_PATH = BASE_PATH + "/pca.sav"
NEW_MODEL_PATH = ""
PCA_COMPONENTS = 256

SVC_MODEL = pickle.load(open(MODEL_PATH, 'rb'))

BERT_TOKENIZER = AutoTokenizer.from_pretrained(MODEL)
BERT_MODEL = AutoModel.from_pretrained(MODEL)
LABELS = json.loads(open(BASE_PATH + "/../common/data/labels.json", "r").read())
TOP_K = len(LABELS)
