from model.tfidf.utils import preprocess_input_test , tfidf_encode_content_test

from model.tfidf.config import TOP_K,INPUT_PATH, THRESHHOLD, LABELS , PCA_PATH \
    , PCA_PATH_ABSTRACT , PCA_PATH_INCLUSION, PCA_PATH_TITLE , TFIDF_PATH_ABSTRACT \
    , TFIDF_PATH_INCLUSION , TFIDF_PATH_TITLE , MODEL_PATH , OUTPUT_PATH

from argparse import ArgumentParser
import numpy as np
import pickle
import pandas as pd

def predict(input_df : pd.DataFrame ,top_k : int) -> pd.DataFrame:


    title_content , abstract_content, inclusion_content  = preprocess_input_test(input_df)

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
    predictions  = model.predict_proba(low_dims)
    top_k_preds = []
    for prediction in predictions:
        reordered = np.zeros(224)
        reordered[model.classes_]  = pred
        i_predictions_ids = np.argsort(reordered)[::-1][:top_k]
        i_scores = np.sort(reordered)[::-1][:top_k]
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
            "top_k": top_k
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
    parser.add_argument('--top-k', default=TOP_K, type=int,
                        help='number of predictions to return')

    args = parser.parse_args()
    df = pd.read_csv(args.input)
    res = predict(df, top_k=args.top_k)
    res.to_csv(OUTPUT_PATH, index=False)
    print(res)