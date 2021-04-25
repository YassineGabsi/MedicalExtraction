import os

import pandas as pd

CATEGORIES_DF = pd.read_csv(
    os.path.join(os.path.dirname(__file__) + "/data/categories.csv",),
    index_col="block_name"
)
