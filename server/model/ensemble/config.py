import json
import os 

THRESHHOLD = 0 
TOP_K = 3

BASE_PATH = os.path.join(os.path.dirname(__file__))
INPUT_PATH = BASE_PATH + "/input.csv"
OUTPUT_PATH = BASE_PATH + "/output.csv"

LABELS = json.loads(open(BASE_PATH + "/../common/data/labels.json", "r").read())
