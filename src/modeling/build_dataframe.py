import pandas as pd
#pandas is used for data analysis and manipulation

from ..db.extract_data import load_raw_comments
from ..features.feature_pipeline import build_feature_pipeline


rows = load_raw_comments()

data = build_feature_pipeline(rows)

#data frame is a 2d table like structure
#data is arranged in rows and columns
df = pd.DataFrame(data)
df["isBot"] = None

def construct_dataframe():

    return df
    #acquiring first row of dataframe
    #print(df.iloc[0])

#function to convert dataframe to csv
#index = False, means does not include dataframe index
def save_features_csv(df, path= "datasets/features.csv"):
    df.to_csv(path, index=False)
    print(f"features have been saved to {path}")




