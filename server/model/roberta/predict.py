from argparse import ArgumentParser

from .config import TOP_K, THRESHHOLD, DEVICE, LABELS, INPUT_PATH, SVC_MODEL, \
    BERT_MODEL, BERT_TOKENIZER, OUTPUT_PATH
from .utils import preprocess_input_test, load_preprocess_vectors_test
import numpy as np
import pandas as pd


def predict(input_df: pd.DataFrame, threshold: int = 0) -> pd.DataFrame:
    """
        1.Input a csv file and preprocess it
        2.Computes embeddings and reduce dimentionality
        3.Loads model and returns prediction 
    """
    title_content, abstract_content, inclusion_content = preprocess_input_test(input_df)

    low_dims = load_preprocess_vectors_test(
        title_content,
        abstract_content,
        inclusion_content,
        model=BERT_MODEL,
        tokenizer=BERT_TOKENIZER,
        device=DEVICE
    )

    predictions = SVC_MODEL.predict_proba(low_dims)
    results = []
    for prediction in predictions:
        reordered = np.zeros(224)
        reordered[SVC_MODEL.classes_] = prediction
        i_predictions_ids = np.argsort(reordered)[::-1][:TOP_K]
        i_scores = np.sort(reordered)[::-1][:TOP_K]
        i_predictions_labels = list(map(lambda id: LABELS[id], i_predictions_ids))
        i_prediction = [
            {
                f"block_name_{i}": prediction_label,
                f"score_{i}": score,
            }
            for i, prediction_label, score in zip(
                range(len(reordered)),
                i_predictions_labels,
                i_scores
            )
        ] + [{
            "top_k": TOP_K
        }]

        results.append({key: value for element in i_prediction for key, value in element.items()})

    results = pd.DataFrame(results)
    return results


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('--input', default=INPUT_PATH,
                        help='csv file to use as input')
    parser.add_argument('--output', default=OUTPUT_PATH,
                        help='csv file to use as output')

    args = parser.parse_args()
    df = pd.read_csv(args.input)
    res = predict(df, threshold=THRESHHOLD)
    res.to_csv(OUTPUT_PATH, index=False)
    print(res)
