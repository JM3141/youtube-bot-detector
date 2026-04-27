import pandas as pd
#pandas is used for data analysis and manipulation

from ..db.extract_data import load_raw_comments
from ..features import build_feature_pipeline


rows = load_raw_comments()

data = build_feature_pipeline(rows)

df = pd.DataFrame(data)




