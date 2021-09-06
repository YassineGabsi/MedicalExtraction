from config import MODEL , MODEL_PATH , TOP_K, PCA_PATH , THRESHHOLD , device , LABELS_TO_KEEP , INPUT_PATH
from utils import preprocess_input_test, load_preprocess_vectors_test
import pickle
import numpy as np
import torch
import pandas as pd

def predict(INPUT_PATH,THRESHHOLD=0):
    """
        1.Input a csv file and preprocess it
        2.Computes embeddings and reduce dimentionality
        3.Loads model and returns prediction 
    """
    title_content , abstract_content, inclusion_content, df = preprocess_input_test(INPUT_PATH,THRESHHOLD)


    low_dims = load_preprocess_vectors_test(title_content,abstract_content,inclusion_content,MODEL,device) 

    model = pickle.load(open(MODEL_PATH, 'rb'))
    preds  = model.predict_proba(low_dims)
    top_k_preds = []
    for i,pred in enumerate(preds):
        reordered = np.zeros(224)
        reordered[model.classes_]  = pred
        this_top_k = np.argsort(reordered)[::-1][:TOP_K] 
        top_k_preds.append(this_top_k)



    top_1, top_2, top_3 = [], [], []
    for i in range(len(df)):
        top_1.append( LABELS_TO_KEEP[top_k_preds[i][0]] )
        top_2.append( LABELS_TO_KEEP[top_k_preds[i][1]] )
        top_3.append( LABELS_TO_KEEP[top_k_preds[i][2]] )
    results = pd.DataFrame({"1st prediction":top_1,"2nd prediction":top_2,"3rd prediction":top_3})
    results.to_csv('results.csv',index=False)
    return results
if __name__ == "__main__":
    print(predict(INPUT_PATH=INPUT_PATH,THRESHHOLD=THRESHHOLD))
