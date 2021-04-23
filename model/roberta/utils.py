import joblib
from config import MODEL , device , VECTORS_PATH, PCA_COMPONENTS , PCA_PATH
import gc
from sklearn.decomposition import PCA
from transformers import AutoModel, AutoTokenizer
from tqdm import tqdm
import pandas as pd
import pickle
import numpy as np
import torch
from datetime import date

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

def preprocess_input_train(INPUT_PATH,threshhold=0):
    df = pd.read_csv(INPUT_PATH)
    df,labels_to_keep = remove_labels(df,threshhold)
    content = df[["Title","Research Summary","Inclusion Criteria"]].values.T.astype(str)
    title_content, abstract_content, inclusion_content = content[0], content[1], content[2]  
    
    title_content = [str(x) for x in title_content]
    abstract_content = [str(x) for x in abstract_content]
    inclusion_content = [str(x) for x in inclusion_content]

    return title_content, abstract_content,inclusion_content , labels_to_keep , df


def preprocess_input_test(INPUT_PATH,threshhold=0):
    df = pd.read_csv(INPUT_PATH)
    content = df[["Title","Research Summary","Inclusion Criteria"]].values.T.astype(str)
    title_content, abstract_content, inclusion_content = content[0], content[1], content[2]  
    
    title_content = [str(x) for x in title_content]
    abstract_content = [str(x) for x in abstract_content]
    inclusion_content = [str(x) for x in inclusion_content]

    return title_content, abstract_content,inclusion_content

def vectorize(device,documents,model_name="distilbert-base-multilingual-cased", verbose=None,gpu=False):
    """ Tokenize with BERT-like model. Use mean of embeddings for now. 
        * general: microsoft/Multilingual-MiniLM-L12-H384
    """
    if verbose:
        print("Creating document embeddings")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model     = AutoModel.from_pretrained(model_name)
    # tokenize the document, return it as PyTorch tensors (vectors),
    # and pass it onto the model
    vectorized = []

    if gpu :
        model = model.to(device)
        for doc in tqdm(documents):
            d = 768 # dimensions of the embedding
            l = len(doc)
            chunks = list(range(0, l, 512*7))+[l]
            vector = torch.cat([model(**tokenizer(doc[chunks[i-1] : chunks[i]],
                                    return_tensors='pt',
                                    max_length=512,
                                    truncation=True).to(device))[0].detach().squeeze()         
                                for i in range(1, len(chunks))], dim=0).cpu().numpy()
            vectorized.append(vector)
    else :
        for doc in tqdm(documents):
            d = 768 # dimensions of the embedding
            l = len(doc)
            chunks = list(range(0, l, 512*7))+[l]
            vector = torch.cat([model(**tokenizer(doc[chunks[i-1] : chunks[i]],
                                    return_tensors='pt',
                                    max_length=512,
                                    truncation=True))[0].detach().squeeze()             
                                for i in range(1, len(chunks))], dim=0).cpu().numpy()
            vectorized.append(vector)
    return vectorized


def vectorize_all(title_content,abstract_content,inclusion_content,MODEL,device,save=False):
    """
        Use to vectorize multiple columns, i.e titles, abstracts,inclusions
    """
    vectors = []
    vectors.append(vectorize(device,title_content,MODEL))
    vectors.append(vectorize(device,abstract_content,MODEL))
    vectors.append(vectorize(device,inclusion_content,MODEL))

    if save == True :
        joblib.dump(vectors,VECTORS_PATH) 
    return vectors

def load_preprocess_vectors_train(INPUT_PATH="",title_content="",abstract_content="",inclusion_content="",MODEL="",device="",default_embeddings=False,save=False):
    """
        Loads and preprocesses the vectors for training
    """
    df = pd.read_csv(INPUT_PATH)
    true_labels = df["ICD Block Names"] 
    labels_to_keep = list(set(true_labels.values))
    if default_embeddings :
        title_vectors, abstract_vectors, inclusion_vectors = joblib.load(VECTORS_PATH)
    else :
        title_vectors, abstract_vectors, inclusion_vectors = vectorize_all(title_content,abstract_content,inclusion_content,MODEL,device,save)
    title_fix , abstract_fix , inclusion_fix = [] , [] , []
    for title in title_vectors :
        title_fix.append(title[0])
    for abstract in abstract_vectors :
        abstract_fix.append(abstract[0])
    for inclusion in inclusion_vectors :
        inclusion_fix.append(inclusion[0])        
    
    del title_vectors , abstract_vectors , inclusion_vectors
    gc.collect()

    # reduce number of dimensions
    pca    = PCA(n_components=PCA_COMPONENTS)
    final_rep = np.concatenate([titles_fix,abstract_fix,inclusions_fix], axis=-1) 
    low_dims  = pca.fit_transform(final_rep)
    pickle.dump(PCA, open(PCA_PATH+" {}".format(date.today()), 'wb'))
    return low_dims , df , labels_to_keep

def load_preprocess_vectors_test(title_content="",abstract_content="",inclusion_content="",MODEL="",device="",save=False):
    """
        Loads and preprocesses the vectors for testing
    """

    title_vectors, abstract_vectors, inclusion_vectors = vectorize_all(title_content,abstract_content,inclusion_content,MODEL,device,save)
    title_fix , abstract_fix , inclusion_fix = [] , [] , []
    for title in title_vectors :
        title_fix.append(title[0])
    for abstract in abstract_vectors :
        abstract_fix.append(abstract[0])
    for inclusion in inclusion_vectors :
        inclusion_fix.append(inclusion[0])        
    
    del title_vectors , abstract_vectors , inclusion_vectors
    gc.collect()


    # reduce number of dimensions
    pca    = pickle.load(open(PCA_PATH,'rb'))
    final_rep = np.concatenate([title_fix,abstract_fix,inclusion_fix], axis=-1) 
    low_dims  = pca.transform(final_rep)
    return low_dims