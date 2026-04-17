from .features import extract_text_features, extract_timing_features, extract_behavioural_features, extract_video_features 


#pipeline produces two  dictionaries: one with per‑authorand one with per‑video metrics
def build_feature_pipeline(rows):

   author_features = extract_behavioural_features(rows)
   video_features = extract_video_features(rows)

   




