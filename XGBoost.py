#Import libraries:
import csv
from pathlib import Path
import pandas as pd
import numpy as np
import xgboost as xgb
from xgboost.sklearn import XGBClassifier
from sklearn import cross_validation, metrics   #Additional scklearn functions
from sklearn.model_selection import GridSearchCV   #Perforing grid search
import matplotlib.pylab as plt


def test_XGB(XGB_params, dtrain, dval, predictors, target, early_stopping_rounds=30):

    # Fit the algorithm on the data
    XGB_params.fit(dtrain[predictors], dtrain[target], eval_metric='auc', early_stopping_rounds=early_stopping_rounds)

    #Predict training set:
    dtrain_predictions = XGB_params.predict(dtrain[predictors])
    dtrain_predprob = XGB_params.predict_proba(dtrain[predictors])[:,1]

    # Predict testing set:
    dval_predictions = XGB_params.predict(dval[predictors])
    dval_predprob = XGB_params.predict_proba(dval[predictors])[:, 1]

    # Print model report:
    print
    "\nModel Report"
    print
    "Accuracy (Train) : %.4g" % metrics.accuracy_score(dtrain[target].values, dtrain_predictions)
    print
    "AUC Score (Train): %f" % metrics.roc_auc_score(dtrain[target], dtrain_predprob)
    print
    "Accuracy (Test) : %.4g" % metrics.accuracy_score(dval[target].values, dval_predictions)
    print
    "AUC Score (Test): %f" % metrics.roc_auc_score(dval[target], dval_predprob)

    feat_imp = pd.Series(XGB_params.booster().get_fscore()).sort_values(ascending=False)
    feat_imp.plot(kind='bar', title='Feature Importances')
    plt.ylabel('Feature Importance Score')

    # ADD GRAPH OF TRAINING AND TESTING -> via XGB_params.evals_result() + eval_set (accuracy can go?) https://machinelearningmastery.com/avoid-overfitting-by-early-stopping-with-xgboost-in-python/


def train_XGB():
    # Define file to train on here
    dataset_file = "C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Datasets\\TrainDataset3000_Category-Change_Normalization-False_OneHotEncoding-False_Model-Simple.csv"
    nr_of_classes = 3
    #ADD MORE PARAMETERS

    # Check if CSV already exists, else create csv from txt
    if(Path(dataset_file).is_file()):
        dataset_txt = "C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Datasets\\TrainDataset3000_Category-Change_Normalization-False_OneHotEncoding-False_Model-Simple.txt"
        dataset_reader = csv.reader(open(dataset_txt,"r"), delimeter = ",")
        dataset_csv = csv.writer(open(dataset_file,"w"))
        dataset_csv.writerows(dataset_reader)

    #################################
    # Make sparse matrix of dataset #
    #################################

    # Transform CSV to Panda dataframe
    train = pd.read_csv(dataset_file)
    validation = pd.read_csv(dataset_file.replace("TrainDataset","ValidationDataset"))
    target = "Future_Delay"
    predictors = [x for x in train.columns if not (x == target)]

    # ADAPT VALUES
    test_params = {
        'max_depth': [3,4,5],
        'min_child_weight': [3,4,5],
        'gamma': [0,0.2,0.4],
        'reg_alpha': [0.001, 0.01, 0.1],
        'learning_rate': [0.01, 0.1, 0.2],
        'n_estimators=': [500, 1000, 2000]
    }

    # ADAPT VALUES
    xgb =  GridSearchCV(estimator = XGBClassifier(
        learning_rate=0.1,
        n_estimators=1000,
        max_depth=5,
        min_child_weight=1,
        gamma=0,
        subsample=0.8,
        colsample_bytree=0.8,
        objective='multi:softmax',
        num_class = nr_of_classes,
        scale_pos_weight=1,
        seed=42),
        param_grid = test_params,
        scoring = 'f1_macro',
        cv = 5)

    eval_set = [(train[predictors],train[target]),((validation[predictors],validation[target]))]

    xgb.fit(train[predictors],train[target],eval_set=eval_set,eval_metric="error",early_stopping_rounds=30)



if __name__== "__main__":
  train_XGB()
  # ALSO