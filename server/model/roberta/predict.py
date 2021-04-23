from argparse import ArgumentParser

from .config import MODEL, MODEL_PATH, TOP_K, PCA_PATH, THRESHHOLD, device, labels_to_keep, INPUT_PATH, ROBERTA_MODEL
from .utils import preprocess_input, load_preprocess_vectors_test, remove_labels
import pickle
import numpy as np
import torch
import pandas as pd

MODEL = pickle.load(open(MODEL_PATH, 'rb'))


def predict(input_df: pd.DataFrame, threshold: int = 0) -> pd.DataFrame:
    """
        1.Input a csv file and preprocess it
        2.Computes embeddings and reduce dimentionality
        3.Loads model and returns prediction 
    """
    title_content, abstract_content, inclusion_content = preprocess_input(input_df)

    low_dims = load_preprocess_vectors_test(title_content, abstract_content, inclusion_content, ROBERTA_MODEL, device)

    predictions = MODEL.predict_proba(low_dims)
    top_k_predictions = []
    for i, prediction in enumerate(predictions):
        reordered = np.zeros(224)
        reordered[MODEL.classes_] = prediction
        i_top_k_predictions = np.argsort(reordered)[::-1][:TOP_K]
        top_k_predictions.append(i_top_k_predictions)

    top_1, top_2, top_3 = [], [], []
    for i in range(len(input_df.index)):
        top_1.append(labels_to_keep[top_k_predictions[i][0]])
        top_2.append(labels_to_keep[top_k_predictions[i][1]])
        top_3.append(labels_to_keep[top_k_predictions[i][2]])
    results = pd.DataFrame({"1st prediction": top_1, "2nd prediction": top_2, "3rd prediction": top_3})
    return results


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('--input', default=INPUT_PATH,
                        help='csv file to use as input')
    args = parser.parse_args()
    df = pd.read_csv(args.input)
    res = predict(df, threshold=THRESHHOLD)
    print(res)