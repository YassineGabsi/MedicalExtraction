from model.roberta.predict import prediction_pipeline_roberta
from model.tfidf.predict import prediction_pipeline_tfidf 
import pandas as pd
from model.ensemble.config import INPUT_PATH , OUTPUT_PATH , TOP_K , LABELS

def predict(input_df : pd.DataFrame, top_k : int = TOP_K) -> pd.DataFrame:
    predictions_tfidf = prediction_pipeline_tfidf(input_df,top_k)
    predictions_roberta = prediction_pipeline_roberta(input_df,top_k)

    predictions = predictions_tfidf * 0.6 + 0.4 * predictions_roberta
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