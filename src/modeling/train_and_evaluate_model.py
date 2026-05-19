import pandas as pd

from sklearn.model_selection import train_test_split


def splitting_dataset():

    #first 200 rows of csv file containing youtube comment info labelled
    dataframe = pd.read_csv("datasets/labeled.csv", nrows= 200)

    #X is the inputs the model uses to make predictions(features)

    X = dataframe[['char_length','word_count',
               'punctuation_ratio','uppercase_ratio',
               'repeated_chars', 'has_link', 
               'token_count', 'stop_word_ratio',
               'spacy_punctuation_ratio', 'repeated_phrases'
               ]]

    #y is the answer the model tries to learn
    y = dataframe['isBot']

    return train_test_split(
    X, y, test_size=0.2, random_state=42
    )


   




