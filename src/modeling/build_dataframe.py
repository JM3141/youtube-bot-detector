import pandas as pd
#pandas is used for data analysis and manipulation

from ..db.extract_data import load_raw_comments
from ..features import build_feature_pipeline


rows = load_raw_comments()

data = build_feature_pipeline(rows)

#data frame is a 2d table like structure
#data is arranged in rows and columns
df = pd.DataFrame(data)

def construct_dataframe():

    return df




