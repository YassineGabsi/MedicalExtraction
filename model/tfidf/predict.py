from utils import preprocess_input_test , tfidf_encode_content_test
from config import TOP_K,INPUT_PATH, THRESHHOLD, labels_to_keep , PCA_PATH , PCA_PATH_ABSTRACT , PCA_PATH_INCLUSION , PCA_PATH_TITLE , TFIDF_PATH_ABSTRACT , TFIDF_PATH_INCLUSION , TFIDF_PATH_TITLE , MODEL_PATH
import numpy as np
import pickle
import pandas as pd

def predict(INPUT_PATH,THRESHHOLD=0):


    title_content , abstract_content, inclusion_content , df = preprocess_input_test(INPUT_PATH,THRESHHOLD)

    title_tfidf = tfidf_encode_content_test(TFIDF_PATH_TITLE,
        PCA_PATH_TITLE,
        title_content
    )

    abstract_tfidf = tfidf_encode_content_test(TFIDF_PATH_ABSTRACT,
        PCA_PATH_ABSTRACT,
        abstract_content
    )

    inclusion_tfidf = tfidf_encode_content_test(TFIDF_PATH_INCLUSION,
        PCA_PATH_INCLUSION,
        inclusion_content
    )

    pca = pickle.load(open(PCA_PATH,'rb'))
    final_rep = np.concatenate([title_tfidf,inclusion_tfidf,abstract_tfidf], axis=-1)
    low_dims  = pca.transform(final_rep)

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
        top_1.append( labels_to_keep[top_k_preds[i][0]] )
        top_2.append( labels_to_keep[top_k_preds[i][1]] )
        top_3.append( labels_to_keep[top_k_preds[i][2]] )
    results = pd.DataFrame({"1st prediction":top_1,"2nd prediction":top_2,"3rd prediction":top_3})
    results.to_csv('results.csv',index=False)
    return results

if __name__ == "__main__": 
    predict(INPUT_PATH=INPUT_PATH,THRESHHOLD=THRESHHOLD)