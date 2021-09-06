from predict import predict
import pandas as pd
from config import INPUT_PATH , TOP_K

def test_predict(INPUT_PATH,TOP_K):

    """
        Tests all the predictions are provided, 
        Tests if TOP_K predictions are provided. 
    """

    data_to_predict = pd.read_csv(INPUT_PATH)
    results = predict(INPUT_PATH)


    assert len(results.columns) == TOP_K

    assert len(results) == len(data_to_predict)

