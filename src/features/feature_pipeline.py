from .features import extract_text_features, extract_timing_features, extract_behavioural_features, extract_video_features 



#takes youtube comment rows and transforms them into a 1 complete
#dicitonary per comment
def build_feature_pipeline(rows):

   #group comments by author
   author_features = extract_behavioural_features(rows)

   #group comments by video
   video_features = extract_video_features(rows)

   final_dataset = []

   for row in rows:
       
       text_feats = extract_text_features(row)

       timing_feats = extract_timing_features(row)

       author_feats = author_features[row["authorname"]]

       video_feats = video_features[row["youtubevideo_id"]]


       # ** means the items in a dictionary(key value pairs)
       # are loaded as items in another dictionary

       merged = {
           **text_feats,
           **timing_feats,
           **author_feats,
           **video_feats
       }

       final_dataset.append(merged)

   return final_dataset    










   




