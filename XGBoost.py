#Import libraries:
import csv
import math
from pathlib import Path
import pandas as pd
import numpy as np
import xgboost as xgb
from xgboost import XGBClassifier, XGBRegressor, plot_importance, plot_tree
from sklearn import metrics
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import OneHotEncoder
from scipy.sparse import csr_matrix
from matplotlib import pyplot
import pickle

# Function to train XGB on a categorical dataset with multiple sets of parameters, pick the best set and output performance of this set
def find_parameters_categorical_XGB(dataset_file, nr_of_classes, categorical_labels, one_hot_encoding=True, sparse=True):

    # Check if CSV already exists, else create csv from txt
    if(not(Path(dataset_file).is_file())):
        dataset_txt = dataset_file.replace("csv","txt")
        validation_txt = dataset_txt.replace("TrainDataset","ValidationDataset")
        dataset_reader = csv.reader(open(dataset_txt,"r"), delimiter = ",")
        dataset_csv = csv.writer(open(dataset_file,"w",newline=""))
        dataset_csv.writerows(dataset_reader)
        validation_reader = csv.reader(open(validation_txt,"r"), delimiter = ",")
        validation_csv = csv.writer(open(dataset_file.replace("TrainDataset","ValidationDataset"),"w", newline=""))
        validation_csv.writerows(validation_reader)

    # Load data and transform to Panda dataframe
    train = pd.read_csv(dataset_file)
    validation = pd.read_csv(dataset_file.replace("TrainDataset","ValidationDataset"))
    target = "Future_Delay"
    predictors = [x for x in train.columns if not (x == target)]

    # Split predictors and labels
    train_data = train[predictors]
    train_labels = train[target]
    validation_data = validation[predictors]
    validation_labels = validation[target]

    # If desired, transform categorical data in to one hot encoding and potentially sparse matrices
    if(one_hot_encoding):
        train_features = None
        validation_features = None

        for predictor in predictors:
            train_feature = train_data[predictor].values
            train_feature = train_feature.reshape(train_feature.shape[0], 1)
            validation_feature = validation_data[predictor].values
            validation_feature = validation_feature.reshape(validation_feature.shape[0], 1)

            if(predictor in categorical_labels):
                one_hot_encoder = OneHotEncoder(sparse=False)
                train_feature = one_hot_encoder.fit_transform(train_feature)
                validation_feature = one_hot_encoder.transform(validation_feature)

            if train_features is None:
                train_features = train_feature
                validation_features = validation_feature
            else:
                train_features = np.concatenate((train_features, train_feature), axis=1)
                validation_features = np.concatenate((validation_features, validation_feature), axis=1)

        if(sparse):
            train_features = csr_matrix(train_features)
            validation_features = csr_matrix(validation_features)

    else:
        train_features = train_data
        validation_features = validation_data

    # Set different values for the parameters to test to find the best model
    test_params = {
        'max_depth': [3,4,5],
        'min_child_weight': [3,5,7],
        'gamma': [0,0.2,0.4],
        'reg_alpha': [0.001, 0.01, 0.1],
        'learning_rate': [0.01, 0.1, 0.2],
        'scale_pos_weight': [1,3,5]
    }

    # Initialize the XGBoost classifier with a gridsearch to test all combinations of parameters
    xgb =  GridSearchCV(estimator = XGBClassifier(
        learning_rate=0.1,
        n_estimators=1000,
        max_depth=5,
        min_child_weight=1,
        gamma=0,
        subsample=0.8,
        colsample_bytree=0.8,
        reg_alpha=0,
        objective='multi:softmax',
        num_class = nr_of_classes,
        scale_pos_weight=1,
        seed=42),
        param_grid = test_params,
        scoring = 'f1_macro',
        cv = 5)

    # Determine an evaluation set during training
    eval_set = [(train_features,train_labels),(validation_features,validation_labels)]

    # Fit models and save the best parameters
    xgb.fit(train_features,train_labels,eval_set=eval_set,eval_metric="mlogloss",early_stopping_rounds=30)
    print(xgb.cv_results_)
    best_params = xgb.best_params_
    print(best_params)
    print(xgb.best_score_)

    # Make XGBoost classifier with the best found parameters
    best_xgb =  XGBClassifier(
        learning_rate=best_params["learning_rate"],
        n_estimators=1000,
        max_depth=best_params["max_depth"],
        min_child_weight=best_params["min_child_weight"],
        gamma=best_params["gamma"],
        subsample=0.8,
        colsample_bytree=0.8,
        reg_alpha=best_params["reg_alpha"],
        objective='multi:softmax',
        num_class = nr_of_classes,
        scale_pos_weight=1,
        seed=42)

    # Fit best model
    best_xgb.fit(train_features,train_labels,eval_set=eval_set,eval_metric=["merror","mlogloss"],early_stopping_rounds=30)

    # Pickle and save best model and training figures
    save_path_model = "C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Models\\XGBoost\\" + \
                dataset_file.replace("C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Datasets\\","").replace(".csv","") \
                + ".pkl"
    pickle.dump(best_xgb,open(save_path_model,"wb"))

    # Predict on validation set and print accuracy
    predictions = best_xgb.predict(validation_features)
    print("Accuracy: %.4g" % metrics.accuracy_score(validation_labels, predictions))


# Function to test the XGB on a categorical dataset with the best parameters
def train_categorical_XGB(dataset_file, nr_of_classes, categorical_labels, params, one_hot_encoding=True, sparse=True, save_figures=True):

    # Check if CSV already exists, else create csv from txt
    if(not(Path(dataset_file).is_file())):
        dataset_txt = dataset_file.replace("csv","txt")
        validation_txt = dataset_txt.replace("TrainDataset","ValidationDataset")
        dataset_reader = csv.reader(open(dataset_txt,"r"), delimiter = ",")
        dataset_csv = csv.writer(open(dataset_file,"w",newline=""))
        dataset_csv.writerows(dataset_reader)
        validation_reader = csv.reader(open(validation_txt,"r"), delimiter = ",")
        validation_csv = csv.writer(open(dataset_file.replace("TrainDataset","ValidationDataset"),"w", newline=""))
        validation_csv.writerows(validation_reader)

    # Load data and transform to Panda dataframe
    train = pd.read_csv(dataset_file)
    validation = pd.read_csv(dataset_file.replace("TrainDataset","ValidationDataset"))
    target = "Future_Delay"
    predictors = [x for x in train.columns if not (x == target)]

    # Split predictors and labels
    train_data = train[predictors]
    train_labels = train[target]
    validation_data = validation[predictors]
    validation_labels = validation[target]

    # If desired, transform categorical data in to one hot encoding and potentially sparse matrices
    if(one_hot_encoding):
        train_features = None
        validation_features = None

        for predictor in predictors:
            train_feature = train_data[predictor].values
            train_feature = train_feature.reshape(train_feature.shape[0], 1)
            validation_feature = validation_data[predictor].values
            validation_feature = validation_feature.reshape(validation_feature.shape[0], 1)

            if(predictor in categorical_labels):
                one_hot_encoder = OneHotEncoder(sparse=False)
                train_feature = one_hot_encoder.fit_transform(train_feature)
                validation_feature = one_hot_encoder.transform(validation_feature)

            if train_features is None:
                train_features = train_feature
                validation_features = validation_feature
            else:
                train_features = np.concatenate((train_features, train_feature), axis=1)
                validation_features = np.concatenate((validation_features, validation_feature), axis=1)

        if(sparse):
            train_features = csr_matrix(train_features)
            validation_features = csr_matrix(validation_features)

    else:
        train_features = train_data
        validation_features = validation_data

    # Determine an evaluation set during training
    eval_set = [(train_features,train_labels),(validation_features,validation_labels)]

    # Make XGBoost classifier with the best found parameters
    best_xgb =  XGBClassifier(
        learning_rate=params["learning_rate"],
        n_estimators=1000,
        max_depth=params["max_depth"],
        min_child_weight=params["min_child_weight"],
        gamma=params["gamma"],
        subsample=0.8,
        colsample_bytree=0.8,
        reg_alpha=params["reg_alpha"],
        objective='multi:softmax',
        num_class = nr_of_classes,
        scale_pos_weight=1,
        seed=42)

    # Fit best model
    best_xgb.fit(train_features,train_labels,eval_set=eval_set,eval_metric=["merror","mlogloss"],early_stopping_rounds=30)

    # Pickle and save best model and training figures
    save_path_model = "C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Models\\XGBoost\\" + \
                dataset_file.replace("C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Datasets\\","").replace(".csv","") \
                + ".pkl"
    pickle.dump(best_xgb,open(save_path_model,"wb"))

    # Predict on validation set and print accuracy
    predictions = best_xgb.predict(validation_features)
    print("Accuracy: %.4g" % metrics.accuracy_score(validation_labels, predictions))

    if(save_figures):
        # Determine path to save figures
        save_path_figure = "C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Models\\XGBoost_Figures\\" + \
                    dataset_file.replace("C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Datasets\\","").replace(".csv","")

        # Plot feature importance
        plot_importance(best_xgb)
        pyplot.savefig(save_path_figure + "-ImporantFeatures.png")

        # Plot final decision tree
        for i in range (0,10):
            plot_tree(best_xgb, num_trees=i)
            fig = pyplot.gcf()
            fig.set_size_inches(150, 100)
            fig.savefig(save_path_figure + "-DecisionTree" + str(i+1) + ".png")

        # Plot learning curves
        results = best_xgb.evals_result()
        epochs = len(results['validation_0']['merror'])
        x_axis = range(0, epochs)
        # Log loss
        fig, ax = pyplot.subplots()
        ax.plot(x_axis, results['validation_0']['mlogloss'], label='Train')
        ax.plot(x_axis, results['validation_1']['mlogloss'], label='Validation')
        ax.legend()
        pyplot.ylabel('Log Loss')
        pyplot.title('XGBoost Log Loss')
        pyplot.savefig(save_path_figure + "-LogLoss.png")
        # Classification error
        fig, ax = pyplot.subplots()
        ax.plot(x_axis, results['validation_0']['merror'], label='Train')
        ax.plot(x_axis, results['validation_1']['merror'], label='Validation')
        ax.legend()
        pyplot.ylabel('Classification Error')
        pyplot.title('XGBoost Classification Error')
        pyplot.savefig(save_path_figure + "-ClassificationError.png")


# Function to train XGB on a regression dataset with multiple sets of parameters, pick the best set and output performance of this set
def find_parameters_regression_XGB(dataset_file, categorical_labels, one_hot_encoding=True, sparse=True):

    # Check if CSV already exists, else create csv from txt
    if(not(Path(dataset_file).is_file())):
        dataset_txt = dataset_file.replace("csv","txt")
        validation_txt = dataset_txt.replace("TrainDataset","ValidationDataset")
        dataset_reader = csv.reader(open(dataset_txt,"r"), delimiter = ",")
        dataset_csv = csv.writer(open(dataset_file,"w",newline=""))
        dataset_csv.writerows(dataset_reader)
        validation_reader = csv.reader(open(validation_txt,"r"), delimiter = ",")
        validation_csv = csv.writer(open(dataset_file.replace("TrainDataset","ValidationDataset"),"w", newline=""))
        validation_csv.writerows(validation_reader)

    # Load data and transform to Panda dataframe
    train = pd.read_csv(dataset_file)
    validation = pd.read_csv(dataset_file.replace("TrainDataset","ValidationDataset"))
    target = "Future_Delay"
    predictors = [x for x in train.columns if not (x == target)]

    # Split predictors and labels
    train_data = train[predictors]
    train_labels = train[target]
    validation_data = validation[predictors]
    validation_labels = validation[target]

    # If desired, transform categorical data in to one hot encoding and potentially sparse matrices
    if(one_hot_encoding):
        train_features = None
        validation_features = None

        for predictor in predictors:
            train_feature = train_data[predictor].values
            train_feature = train_feature.reshape(train_feature.shape[0], 1)
            validation_feature = validation_data[predictor].values
            validation_feature = validation_feature.reshape(validation_feature.shape[0], 1)

            if(predictor in categorical_labels):
                one_hot_encoder = OneHotEncoder(sparse=False)
                train_feature = one_hot_encoder.fit_transform(train_feature)
                validation_feature = one_hot_encoder.transform(validation_feature)

            if train_features is None:
                train_features = train_feature
                validation_features = validation_feature
            else:
                train_features = np.concatenate((train_features, train_feature), axis=1)
                validation_features = np.concatenate((validation_features, validation_feature), axis=1)

        if(sparse):
            train_features = csr_matrix(train_features)
            validation_features = csr_matrix(validation_features)

    else:
        train_features = train_data
        validation_features = validation_data

    # Set different values for the parameters to test to find the best model
    test_params = {
        'max_depth': [3,4,5],
        'min_child_weight': [3,5,7],
        'gamma': [0,0.2,0.4],
        'reg_alpha': [0.001, 0.01, 0.1],
        'learning_rate': [0.01, 0.1, 0.2],
        'scale_pos_weight': [1,3,5]
    }

    # Initialize the XGBoost classifier with a gridsearch to test all combinations of parameters
    xgb =  GridSearchCV(estimator = XGBRegressor(
        learning_rate=0.1,
        n_estimators=1000,
        max_depth=5,
        min_child_weight=1,
        gamma=0,
        subsample=0.8,
        colsample_bytree=0.8,
        reg_alpha=0,
        objective='reg:linear',
        scale_pos_weight=1,
        seed=42),
        param_grid = test_params,
        scoring = 'neg_mean_squared_error',
        cv = 5)

    # Determine an evaluation set during training
    eval_set = [(train_features,train_labels),(validation_features,validation_labels)]

    # Fit models and save the best parameters
    xgb.fit(train_features,train_labels,eval_set=eval_set,eval_metric="rmse",early_stopping_rounds=30)
    print(xgb.cv_results_)
    best_params = xgb.best_params_
    print(best_params)
    print(xgb.best_score_)

    # Make XGBoost classifier with the best found parameters
    best_xgb =  XGBRegressor(
        learning_rate=best_params["learning_rate"],
        n_estimators=1000,
        max_depth=best_params["max_depth"],
        min_child_weight=best_params["min_child_weight"],
        gamma=best_params["gamma"],
        subsample=0.8,
        colsample_bytree=0.8,
        reg_alpha=best_params["reg_alpha"],
        objective='reg:linear',
        seed=42)

    # Fit best model
    best_xgb.fit(train_features,train_labels,eval_set=eval_set,eval_metric="rmse",early_stopping_rounds=30)

    # Pickle and save best model and training figures
    save_path_model = "C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Models\\XGBoost\\" + \
                dataset_file.replace("C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Datasets\\","").replace(".csv","") \
                + ".pkl"
    pickle.dump(best_xgb,open(save_path_model,"wb"))

    # Predict on validation set and print accuracy
    predictions = best_xgb.predict(validation_features)
    print("Root Mean squared error: %.4g" % math.sqrt(metrics.mean_squared_error(validation_labels.values, predictions)))


# Function to test the XGB on a regression dataset with the best parameters
def train_regression_XGB(dataset_file, categorical_labels, params, one_hot_encoding=True, sparse=True, save_figures = True):

    # Check if CSV already exists, else create csv from txt
    if(not(Path(dataset_file).is_file())):
        dataset_txt = dataset_file.replace("csv","txt")
        validation_txt = dataset_txt.replace("TrainDataset","ValidationDataset")
        dataset_reader = csv.reader(open(dataset_txt,"r"), delimiter = ",")
        dataset_csv = csv.writer(open(dataset_file,"w",newline=""))
        dataset_csv.writerows(dataset_reader)
        validation_reader = csv.reader(open(validation_txt,"r"), delimiter = ",")
        validation_csv = csv.writer(open(dataset_file.replace("TrainDataset","ValidationDataset"),"w", newline=""))
        validation_csv.writerows(validation_reader)

    # Load data and transform to Panda dataframe
    train = pd.read_csv(dataset_file)
    validation = pd.read_csv(dataset_file.replace("TrainDataset","ValidationDataset"))
    target = "Future_Delay"
    predictors = [x for x in train.columns if not (x == target)]

    # Split predictors and labels
    train_data = train[predictors]
    train_labels = train[target]
    validation_data = validation[predictors]
    validation_labels = validation[target]

    # If desired, transform categorical data in to one hot encoding and potentially sparse matrices
    if(one_hot_encoding):
        train_features = None
        validation_features = None

        for predictor in predictors:
            train_feature = train_data[predictor].values
            train_feature = train_feature.reshape(train_feature.shape[0], 1)
            validation_feature = validation_data[predictor].values
            validation_feature = validation_feature.reshape(validation_feature.shape[0], 1)

            if(predictor in categorical_labels):
                one_hot_encoder = OneHotEncoder(sparse=False)
                train_feature = one_hot_encoder.fit_transform(train_feature)
                validation_feature = one_hot_encoder.transform(validation_feature)

            if train_features is None:
                train_features = train_feature
                validation_features = validation_feature
            else:
                train_features = np.concatenate((train_features, train_feature), axis=1)
                validation_features = np.concatenate((validation_features, validation_feature), axis=1)

        if(sparse):
            train_features = csr_matrix(train_features)
            validation_features = csr_matrix(validation_features)

    else:
        train_features = train_data
        validation_features = validation_data

    # Determine an evaluation set during training
    eval_set = [(train_features,train_labels),(validation_features,validation_labels)]

    # Make XGBoost classifier with the best found parameters
    best_xgb =  XGBRegressor(
        objective='reg:linear',
        booster='gbtree',
        learning_rate=params["learning_rate"],
        n_estimators=1000,
        max_depth=params["max_depth"],
        min_child_weight=params["min_child_weight"],
        gamma=params["gamma"],
        subsample=0.8,
        colsample_bytree=0.8,
        reg_alpha=params["reg_alpha"],
        seed=42)

    # Fit best model
    best_xgb.fit(train_features,train_labels,eval_set=eval_set,eval_metric="rmse",early_stopping_rounds=30)

    # Pickle and save best model and training figures
    save_path_model = "C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Models\\XGBoost\\" + \
                dataset_file.replace("C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Datasets\\","").replace(".csv","") \
                + ".pkl"
    pickle.dump(best_xgb,open(save_path_model,"wb"))

    # Predict on validation set and print accuracy
    predictions = best_xgb.predict(validation_features)
    print("Root Mean squared error: %.4g" % math.sqrt(metrics.mean_squared_error(validation_labels.values, predictions)))

    if(save_figures):
        # Determine path to save figures
        save_path_figure = "C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Models\\XGBoost_Figures\\" + \
                    dataset_file.replace("C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Datasets\\","").replace(".csv","")

        # Plot feature importance
        plot_importance(best_xgb)
        pyplot.savefig(save_path_figure + "-ImporantFeatures.png")

        # Plot final decision tree
        for i in range (0,10):
            plot_tree(best_xgb, num_trees=i)
            fig = pyplot.gcf()
            fig.set_size_inches(150, 100)
            fig.savefig(save_path_figure + "-DecisionTree" + str(i+1) + ".png")

        # Plot learning curves
        results = best_xgb.evals_result()
        epochs = len(results['validation_0']['rmse'])
        x_axis = range(0, epochs)
        # Log loss
        fig, ax = pyplot.subplots()
        ax.plot(x_axis, results['validation_0']['rmse'], label='Train')
        ax.plot(x_axis, results['validation_1']['rmse'], label='Validation')
        ax.legend()
        pyplot.ylabel('RMSE')
        pyplot.title('XGBoost RMSE')
        pyplot.savefig(save_path_figure + "-RMSE.png")


if __name__== "__main__":
    ###############
    # Categorical #
    ###############
    # Define file to train on and amount of classes of the dataset here
    dataset_file = "C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Datasets\\TrainDataset3000_Category-Change_Normalization-False_OneHotEncoding-False_Model-Simple.csv"
    nr_of_classes = 3
    categorical_labels = ["Day", "Location"]

    # Train/test
    #find_parameters_categorical_XGB(dataset_file, nr_of_classes, categorical_labels, one_hot_encoding=False, sparse=False)
    params = {'gamma': 0, 'learning_rate': 0.1, 'max_depth': 4, 'min_child_weight': 3, 'reg_alpha': 0.01, 'scale_pos_weight': 1}
    train_categorical_XGB(dataset_file, nr_of_classes, categorical_labels, params, one_hot_encoding=False, sparse=False, save_figures=True)

    ##############
    # Regression #
    ##############
    # Define file to train on for regression
    dataset_file = "C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Datasets\\TrainDataset3000_Category-Regression_Normalization-False_OneHotEncoding-False_Model-Simple.csv"
    categorical_labels = ["Day", "Location"]

    # Train/test
    #find_parameters_regression_XGB(dataset_file, categorical_labels, one_hot_encoding=False, sparse=False)
    params = {'gamma': 0, 'learning_rate': 0.1, 'max_depth': 4, 'min_child_weight': 3, 'reg_alpha': 0.01}
    train_regression_XGB(dataset_file, categorical_labels, params, one_hot_encoding=False, sparse=False, save_figures=True)