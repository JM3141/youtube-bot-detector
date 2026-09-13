import pandas as pd

from data.split_data import splitting_dataset
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

#sklearn -> Scikit Learn, used for model building

#renamed file to model_pipeline,
#moved splitting data function to data folder


#Feature scaling 
# 1) makes all features comparable 
# 2) helps Logistic Regression train properly, 
# 3) scaler is fit only on training data and then applied to test data to avoid data leakage.
def feature_scaler(X_train, X_test):

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    return X_train_scaled, X_test_scaled, scaler


# max_iter is the number of chances the model gets to learn before it gives up.
# fit() method that teaches the model.

def train_logistic_regression_model(X_train, y_train):

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    return model
    

#evaluation of the trained model
# 1) X_test required
# 2) y_text required
# 3) model(trained)
def evaluating_model(X_test, y_test, model):
    accuracy = model.score(X_test, y_test)

    return accuracy

#function to load the remaining unlabelled data
def load_unlabelled_data(scaler):
    
    #updated method to keep the first row(header)
    #skip 201 rows to load the unlabelled data
    dataframe = pd.read_csv("datasets/labeled.csv", skiprows = range(1, 200))

    #From unlabelled rows, extract only the input features
    X_unlabelled = dataframe[['char_length', 'word_count',
                   'punctuation_ratio', 'uppercase_ratio',
                   'repeated_chars', 'has_link',
                   'token_count', 'stop_word_ratio',
                   'spacy_punctuation_ratio', 'repeated_phrases'
                   ]]
    
    #scaling the features
    #transform -> used for test data and unlabelled data
    #fit_transform -> used for training data
    X_unlabelled_scaled = scaler.transform(X_unlabelled)

    return dataframe, X_unlabelled, X_unlabelled_scaled


def predict_unlabelled(model, X_unlabelled_scaled):
    #returns a 1D NumPy array
    y_predict = model.predict(X_unlabelled_scaled)
    #returns a 2D NumPy array
    #obtaining the second column which represents the likelihood of comment being a bot
    y_probability = model.predict_proba(X_unlabelled_scaled)[:,1]

    return y_predict, y_probability






    



    



