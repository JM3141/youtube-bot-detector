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





    



