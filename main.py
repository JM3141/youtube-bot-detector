import os
import pandas as pd

#from src.db.insert import insert_channel
#from src.db.insert import insert_video
#from src.api_client import searchForVideos
#from src.db.insert import get_comments
#from src.db.insert import get_author
#from src.db.extract_data import load_raw_comments
#from src.features.feature_pipeline import build_feature_pipeline
#from src.modeling.build_dataframe import construct_dataframe, save_features_csv
#from src.labeling.label_data import label_comments_menu

from data.split_data import splitting_dataset
from src.modeling.model_pipeline import feature_scaler
from src.modeling.model_pipeline import train_logistic_regression_model
#from src.modeling.model_pipeline import evaluating_model
from src.modeling.model_pipeline import load_unlabelled_data
from src.modeling.model_pipeline import predict_unlabelled
from src.results import  create_results_dataframe
from src.results import sort_by_probability
from src.results import filter_suspicious_comments




#from dotenv import load_dotenv
#load_dotenv()

#from googleapiclient.discovery import build

def main():

    list_of_keywords = ["crypto", "crypto news",
                    "crypto trading", "robux",
                    "robux free", "robux gift card codes",
                    "robux giveaway", "roblox", "roblox gameplay",
                    "roblox adopt me", "roblox trading"]
    

    #accessing value and storing it in variable
    #API_KEY = os.getenv("GOOGLE_API_KEY")

    #creating youtube resource object
    #build function contains API name, API version and API key
    #youtube = build('youtube','v3', developerKey=API_KEY)
    
    
    #videos = searchForVideos(youtube, list_of_keywords) 
    
    #insert_channel(youtube, videos)
    #insert_video(youtube, videos)
    #get_author(youtube, videos)
    #get_comments(youtube, videos)


    #load extracted YouTube rows

    #rows = load_raw_comments()

    #passing youtube rows into feature pipeline

    #final_dataset = build_feature_pipeline(rows)

    #print(final_dataset[0])


    #testing save features to csv function

    #dataframe = construct_dataframe()

    #save_features_csv(dataframe)

    #testing function to manually label csv isBot column 

    #df = pd.read_csv("datasets/labeled.csv")
    #df = label_comments_menu(df)

    # Splitting Dataset Using train_test_split()

    X_train, X_test, y_train, y_test = splitting_dataset()

    # .shape attribute tells you the size of the data
    #(number of rows, number of columns)


    #print(X_train.shape)
    #print(X_test.shape)
    #print(y_train.shape)
    #print(y_test.shape)

    #(160, 10)
    #(40, 10)
    #(160,)
    #(40,)

    X_train_scaled, X_test_scaled, scaler = feature_scaler(X_train, X_test)

    model = train_logistic_regression_model(X_train_scaled, y_train)
    
    #Evaluating training model performance
    #accuracy = evaluating_model(X_test_scaled, y_test, model)
    #print(accuracy)

    dataframe, X_unlabelled, X_unlabelled_scaled = load_unlabelled_data(scaler)

    y_predict, y_probability = predict_unlabelled(model, X_unlabelled_scaled)

    #print("Predicted labels: ", y_predict.tolist())

    #print("\nProbablilities", y_probability.round(3).tolist())

    result = create_results_dataframe(dataframe, y_predict, y_probability)

    #print(result.loc[5])

    sorted_df = sort_by_probability(result)

    #.iloc[0] retrieves the first row by position, not by index label.
    #print(sorted_df.iloc[0])

    #testing function to filter comments that have a bot probability greater than or equal to 0.8
    suspicious_comments = filter_suspicious_comments(sorted_df)

    print(suspicious_comments.head())




if __name__ == "__main__":
    main()
