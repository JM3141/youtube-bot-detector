from data.split_data import splitting_dataset
from sklearn.preprocessing import StandardScaler

#renamed file to model_pipeline,
#moved splitting data function to data folder


#Feature scaling 
# 1) makes all features comparable 
# 2) helps Logistic Regression train properly, 
# 3) scaler is fit only on training data and then applied to test data to avoid data leakage.
def feature_scaler(X_train, X_test):

    scaler = StandardScaler
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    return X_train_scaled, X_test_scaled, scaler




    



