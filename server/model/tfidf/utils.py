import pickle
import pandas as pd
import numpy as np 
import os , gc 

def remove_labels(df,threshhold=0):
    """
        Remove labels that have count under a certain threshhold
    """
    true_labels = df["ICD Block Names"] 
    labels_to_keep = []
    for i in true_labels.value_counts().index:
        if true_labels.value_counts()[i] >= threshhold : 
            labels_to_keep.append(i)
    labels_to_keep = list(set(labels_to_keep))
    df = df[df["ICD Block Names"].isin(labels_to_keep)]
    return df , labels_to_keep 

def tfidf_encode_content_test(TF_IDF_PATH,PCA_PATH,content):
    loaded_vectorizer = pickle.load(open(TF_IDF_PATH,'rb'))
    loaded_pca = pickle.load(open(PCA_PATH,'rb'))

    vectors = loaded_vectorizer.transform(content)
    feature_names = loaded_vectorizer.get_feature_names()
    dense = vectors.todense()
    denselist = dense.tolist()
    content = pd.DataFrame(denselist, columns=feature_names)


    content_low_dims  = loaded_pca.transform(content)
    del content
    gc.collect()

    return content_low_dims

def preprocess_input_train(INPUT_PATH,threshhold=0):
    df = pd.read_csv(INPUT_PATH)
    df,labels_to_keep = remove_labels(df,threshhold)
    content = df[["Title","Research Summary","Inclusion Criteria"]].values.T.astype(str)
    title_content, abstract_content, inclusion_content = content[0], content[1], content[2]  
    
    title_content = [str(x) for x in title_content]
    abstract_content = [str(x) for x in abstract_content]
    inclusion_content = [str(x) for x in inclusion_content]

    return title_content, abstract_content,inclusion_content , labels_to_keep , df

def preprocess_input_test(df: pd.DataFrame):
    content = df[["Title", "Research Summary", "Inclusion Criteria"]].values.T.astype(str)
    title_content, abstract_content, inclusion_content = content[0], content[1], content[2]

    title_content = [str(x) for x in title_content]
    abstract_content = [str(x) for x in abstract_content]
    inclusion_content = [str(x) for x in inclusion_content]

    return title_content, abstract_content, inclusion_content