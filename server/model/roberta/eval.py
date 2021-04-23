from config import MODEL , MODEL_PATH , TOP_K, PCA_PATH , THRESHHOLD , device , labels_to_keep , INPUT_PATH , SAMPLE_SIZE ,FULL_DATA_PATH
from utils import preprocess_input, load_preprocess_vectors_test
import pickle
import numpy as np
import torch
import pandas as pd

def eval(MODEL_PATH,THRESHHOLD=0):
    """
        Function to evaluate new models on data : 

        1. samples data from the original full data
        2.Computes embeddings and reduce dimentionality
        3.Loads model and returns evaluation 
    """

    data = pd.read_csv(FULL_DATA_PATH)
    partial_data = data.sample(SAMPLE_SIZE)
    true_labels = partial_data["ICD Block Names"] 

    content = partial_data[["Title", "Research Summary", "Inclusion Criteria"]].values.T.astype(str)
    title_content, abstract_content, inclusion_content = content[0], content[1], content[2]
    
    unique_labels = list(set(true_labels.values))
    print("Number of unique classes:", len(unique_labels))
    
    useful_labels = [labels_to_keep.index(label) for label in true_labels]
    
    title_content = [str(x) for x in title_content]
    abstract_content = [str(x) for x in abstract_content]
    inclusion_content = [str(x) for x in inclusion_content]

    low_dims = load_preprocess_vectors_test(title_content,abstract_content,inclusion_content,MODEL,device) 

    model = pickle.load(open(MODEL_PATH, 'rb'))

    preds  = model.predict_proba(low_dims)

    embd_val_labels = np.array(useful_labels)
    # for validation data
    pred_probs_val  = model.predict_proba(low_dims)
    in_or_out_val   = []
    top_k_preds_val = []
    for i,pred in enumerate(pred_probs_val):
        reordered = np.zeros(224) 
        reordered[model.classes_]  = pred
        this_top_k = np.argsort(reordered)[::-1][:TOP_K] 
        top_k_preds_val.append(this_top_k)
        in_or_out_val.append( embd_val_labels[i] in this_top_k )

    # print results

    print("A more realistic estimate on validation data can be:", np.mean(model.predict(low_dims) == embd_val_labels), "in top 1")
    print("A more realistic estimate on validation data can be:", np.mean(in_or_out_val), "in top", TOP_K)

    return np.mean(model.predict(low_dims) == embd_val_labels) , np.mean(in_or_out_val)
if __name__ == "__main__":
    top1_performance, top3_performance = eval(MODEL_PATH=MODEL_PATH,THRESHHOLD=THRESHHOLD)