import math
from sklearn.metrics import precision_score, recall_score, fbeta_score, mean_squared_error

# Script to compare predictions from model and two baselines to the ground truth

# Set which parameters you want to test
trainseries = '3000' # Choose a train series that have been made predictions for
dataset_type = 'Hard' # Choose between 'Simple' (Basic model), 'Medium' (Composition/Driver model) or 'Hard' (Interacting Trains model)
model = "NeuralNetwork" # Choose between 'XGBoost' or 'NeuralNetwork'

# Set if one-hot encoding was true
if(model == "XGBoost"):
    onehot = False
else:
    onehot = True

# Set file paths
prediction_file_Jump = "C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Predictions\\" + model + "\\TestDataset" + trainseries + "_Category-Jump_Normalization-False_OneHotEncoding-" + str(onehot) + "_Model-" + dataset_type + ".txt"
prediction_file_Change = "C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Predictions\\" + model + "\\TestDataset" + trainseries + "_Category-Change_Normalization-False_OneHotEncoding-" + str(onehot) + "_Model-" + dataset_type + ".txt"
prediction_file_Regression = "C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Predictions\\" + model + "\\TestDataset" + trainseries + "_Category-Regression_Normalization-False_OneHotEncoding-" + str(onehot) + "_Model-" + dataset_type + ".txt"
test_file = "C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Testsets\\TestDataset" + trainseries + "_Category-Jump_Normalization-False_OneHotEncoding-False_Model-Simple.txt"
groundtruth_file = "C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Evaluation\\ANSWER_FORM.txt"
baseline_file = "C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\JohnBrouwer\\Performance_JohnCode_complete.txt"

# Create list for every possible train number 1-99 to append answers to
predictions = []
answers = [[{"Prediction":[],"GroundTruth":[],"Trimean":[],"StaysTheSame":[]}] for j in range(100)]

# Fill predictions list with lists of a combination of the Jump, Change and Regression answer
prediction_data = open(prediction_file_Jump, "r")
for line in prediction_data:
    line = line.replace('\n', '')
    predictions.append([int(line)])

prediction_data = open(prediction_file_Change, "r")
for n,line in enumerate(prediction_data):
    line = line.replace('\n', '')
    predictions[n].append(int(line))

prediction_data = open(prediction_file_Regression, "r")
for n,line in enumerate(prediction_data):
    line = line.replace('\n', '')
    predictions[n].append(float(line))

# Filter answers from answer form that are relevant for the current train series
groundtruth_data = open(groundtruth_file, "r")
for line in groundtruth_data:
    columns = line.split(",")
    trainnumber = columns[1]
    if(trainnumber[:-2] == trainseries[:-2]):
        # Transform Jump answer
        if(columns[5] == "NO"):
            jump_answer = 0
        else:
            jump_answer = 1

        # Transform Change answer
        if(columns[6] == "decrease"):
            change_answer = 0
        elif(columns[6] == "equal"):
            change_answer = 1
        else:
            change_answer = 2

        # Set Regression answer
        regression_answer = int(columns[7])
        answers[int(trainnumber) % 100][0]["GroundTruth"].append([jump_answer,change_answer,regression_answer])

# Filter answers from baseline form that are relevant for the current train series
baseline_data = open(baseline_file, "r")
header = baseline_data.readline()
for line in baseline_data:
    columns = line.split(",")
    trainnumber = columns[0]
    baseline_series = trainnumber[:-2] + "00"
    if ((trainseries == baseline_series) or
            (len(baseline_series) == 6 and int(baseline_series) < 400000 and
             (5 - len(trainseries)) * "0" + trainseries == baseline_series[1:6])):
        # Set Regression Answers
        regression_answer_trimean = int(columns[6])
        regression_answer_staysthesame = int(columns[8])

        # Determine Change answers from the Regression Answers
        if (regression_answer_trimean - regression_answer_staysthesame > 1):
            change_answer_trimean = 2
        elif (regression_answer_staysthesame - regression_answer_trimean > 1):
            change_answer_trimean = 0
        else:
            change_answer_trimean = 1

        change_answer_staysthesame = 1

        # Determine Jump answer from Regression Answer
        if (abs(regression_answer_trimean - regression_answer_staysthesame) > 4):
            jump_answer_trimean = 1
        else:
            jump_answer_trimean = 0

        jump_answer_staysthesame = 0

        answers[int(trainnumber) % 100][0]["Trimean"].append([jump_answer_trimean, change_answer_trimean, regression_answer_trimean])
        answers[int(trainnumber) % 100][0]["StaysTheSame"].append([jump_answer_staysthesame, change_answer_staysthesame, regression_answer_staysthesame])

# Put predictions is answer list based on the test file order
i = 0
previous_hour = 0
previous_minutes = 0
previous_location = 0
test_data = open(test_file, "r")
header = test_data.readline()
for n,line in enumerate(test_data):
    columns = line.split(",")
    hour = columns[1]
    minutes = columns[2]
    location = columns[4]

    # Switch to next train number if the hour, minutes and location switch
    if(not(previous_hour == hour and previous_minutes == minutes and previous_location == location)):
        i = i+1

    # Skip numbers that are not used in this train series
    while(i < 100 and answers[i][0]["GroundTruth"] == [] ):
        i = i+1

    # Break if i reached the end
    if(i == 100):
        break

    # Collect predictions for this specific number
    jump_answer_prediction = predictions[n][0]
    change_answer_prediction = predictions[n][1]
    regression_answer_prediction = predictions[n][2]
    answers[i][0]["Prediction"].append([jump_answer_prediction,change_answer_prediction,regression_answer_prediction])

    # Set previous for next iteration
    previous_hour = hour
    previous_minutes = minutes
    previous_location = location

# Fill different arrays all in the same order so that metrics can be calculated between arrays
jump_preds = []
jump_baseline_trimean = []
jump_baseline_staysthesame = []
jump_labels = []

change_preds = []
change_baseline_trimean = []
change_baseline_staysthesame = []
change_labels = []

regression_preds = []
regression_baseline_trimean = []
regression_baseline_staysthesame = []
regression_labels = []

for dictionaries in answers:
    if(dictionaries[0]["Prediction"] == []):
        continue
    else:
        # Fill preds arrays
        preds = dictionaries[0]["Prediction"]
        for pred in preds:
            jump_preds.append(pred[0])
            change_preds.append(pred[1])
            regression_preds.append(pred[2])
        # Fill trimean baselines arrays
        trimeans = dictionaries[0]["Trimean"]
        for pred in trimeans:
            jump_baseline_trimean.append(pred[0])
            change_baseline_trimean.append(pred[1])
            regression_baseline_trimean.append(pred[2])
        # Fill staysthesame baselines arrays
        staysthesame = dictionaries[0]["StaysTheSame"]
        for pred in staysthesame:
            jump_baseline_staysthesame.append(pred[0])
            change_baseline_staysthesame.append(pred[1])
            regression_baseline_staysthesame.append(pred[2])
        # Fill label arrays
        labels = dictionaries[0]["GroundTruth"]
        for label in labels:
            jump_labels.append(label[0])
            change_labels.append(label[1])
            regression_labels.append(label[2])

# Determine F1 score of Jump and Change category and RMSE for Regression category for predictions and baselines
print("SCORE PREDICTIONS IN JUMP CATEGORY")
print('Precision:' + str(precision_score(jump_labels, jump_preds)))
print('Recall:' + str(recall_score(jump_labels, jump_preds)))
print('F1 score: ' + str(fbeta_score(jump_labels, jump_preds, 1)))
print("")
print("SCORE TRIMEAN BASELINE IN JUMP CATEGORY")
print('Precision:' + str(precision_score(jump_labels, jump_baseline_trimean)))
print('Recall:' + str(recall_score(jump_labels, jump_baseline_trimean)))
print('F1 score: ' + str(fbeta_score(jump_labels, jump_baseline_trimean, 1)))
print("")
print("SCORE STAYSTHESAME BASELINE IN JUMP CATEGORY")
print('Precision:' + str(precision_score(jump_labels, jump_baseline_staysthesame)))
print('Recall:' + str(recall_score(jump_labels, jump_baseline_staysthesame)))
print('F1 score ' + str(fbeta_score(jump_labels, jump_baseline_staysthesame, 1)))
print("")
print("----------------------------------------------")
print("")
print("SCORE PREDICTIONS IN CHANGE CATEGORY")
print('Precision:' + str(precision_score(change_labels, change_preds, labels=[0,1,2], average="macro")))
print('Recall:' + str(recall_score(change_labels, change_preds, labels=[0,1,2], average="macro")))
print('F1 score: ' + str(fbeta_score(change_labels, change_preds, 1, labels=[0,1,2], average="macro")))
print("")
print("SCORE TRIMEAN BASELINE IN CHANGE CATEGORY")
print('Precision:' + str(precision_score(change_labels, change_baseline_trimean, labels=[0,1,2], average="macro")))
print('Recall:' + str(recall_score(change_labels, change_baseline_trimean, labels=[0,1,2], average="macro")))
print('F1 score: ' + str(fbeta_score(change_labels, change_baseline_trimean, 1, labels=[0,1,2], average="macro")))
print("")
print("SCORE STAYSTHESAME BASELINE IN CHANGE CATEGORY")
print('Precision:' + str(precision_score(change_labels, change_baseline_staysthesame, labels=[0,1,2], average="macro")))
print('Recall:' + str(recall_score(change_labels, change_baseline_staysthesame, labels=[0,1,2], average="macro")))
print('F1 score ' + str(fbeta_score(change_labels, change_baseline_staysthesame, 1, labels=[0,1,2], average="macro")))
print("")
print("----------------------------------------------")
print("")
print("SCORE PREDICTIONS IN REGRESSION CATEGORY")
print('RMSE:' + str(math.sqrt(mean_squared_error(regression_labels, regression_preds))))
print("")
print("SCORE TRIMEAN BASELINE IN REGRESSION CATEGORY")
print('RMSE:' + str(math.sqrt(mean_squared_error(regression_labels, regression_baseline_trimean))))
print("")
print("SCORE STAYSTHESAME BASELINE IN REGRESSION CATEGORY")
print('RMSE:' + str(math.sqrt(mean_squared_error(regression_labels, regression_baseline_staysthesame))))