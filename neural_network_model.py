from pathlib import Path
import csv
import math
import numpy as np
import pandas as pd
from keras import regularizers
from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout, BatchNormalization
from keras.optimizers import Adam, SGD
from keras.callbacks import CSVLogger, ModelCheckpoint, ReduceLROnPlateau
from sklearn.metrics import fbeta_score, mean_squared_error
from batch_generator import get_databatch, get_testbatch
from matplotlib import pyplot

def train_network(train_data, validation_data, category, dataset_type, batch_size, epochs, dataset_file, mean, std,
                  normalization=True, augmentation=True, balance_batches=True):
    # Create Batch generators
    train_generator = get_databatch(train_data, mean, std, batch_size=batch_size, category=category, shuffle=True, normalization=normalization,
                                    augmentation=augmentation, balance_batches=balance_batches)
    validation_generator = get_databatch(validation_data, mean, std, batch_size=batch_size, category=category, shuffle=True, normalization=normalization,
                                         augmentation=True, balance_batches=balance_batches)

    # Determine path to save logger files, models and figures
    csv_logger_path = "C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Models\\NeuralNetwork\\" + category + "\\epoch_results.csv"
    save_model_path = "C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Models\\NeuralNetwork\\" + category + "\\" + dataset_type + "_model.{epoch:02d}-{val_loss:.2f}.hdf5"
    save_figure_path = "C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Models\\NeuralNetwork_Figures\\" + category + \
                       "\\" + dataset_file.replace("C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Datasets\\", "").replace(".csv", "")

    # Depending on the category, set some of the model parameters differently
    if(category=='Regression'):
        output_dim = 1
        last_activation = 'linear'
        loss = 'mean_squared_error'
        metrics = ['mean_squared_error']
    elif(category=='Change'):
        output_dim = 3
        last_activation = 'softmax'
        loss = 'categorical_crossentropy'
        metrics = ['accuracy', 'categorical_crossentropy']
    elif(category == 'Jump'):
        output_dim = 1
        last_activation = 'sigmoid'
        loss = 'binary_crossentropy'
        metrics = ['accuracy', 'binary_crossentropy']
    input_dim = train_data.shape[1]-output_dim

    # Create network architecture
    if(category=='Change' or category=='Jump'):
        model = Sequential()
        model.add(Dense(400, input_dim=input_dim, kernel_initializer='he_normal', activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(200, kernel_initializer='he_normal', activation='relu'))
        model.add(Dense(output_dim, activation=last_activation))
        model.compile(loss=loss,optimizer=Adam(lr=0.01),metrics=metrics)
    else:
        model = Sequential()
        model.add(Dense(400, input_dim=input_dim, kernel_initializer='he_normal', activation='relu'))
        model.add(Dense(200, kernel_initializer='he_normal', activation='relu'))
        model.add(Dense(output_dim, activation=last_activation))
        model.compile(loss=loss, optimizer=Adam(lr=0.001), metrics=metrics)

    # Train network
    csv_logger = CSVLogger(csv_logger_path)
    lr_plateau = ReduceLROnPlateau(monitor='val_loss', patience=1, verbose=1, factor=0.5)
    checkpoint = ModelCheckpoint(
        filepath=save_model_path,
        verbose=1, save_best_only=True)

    history = model.fit_generator(train_generator, steps_per_epoch=len(train_data) / batch_size,
                        epochs=epochs, verbose=2,
                        callbacks=[csv_logger, lr_plateau, checkpoint],
                        validation_data=validation_generator, validation_steps=len(validation_data)/batch_size)

    if(not(category == 'Regression')):
        # Plot accuracy
        pyplot.plot(history.history['acc'])
        pyplot.plot(history.history['val_acc'])
        pyplot.title('Model accuracy')
        pyplot.ylabel('Accuracy')
        pyplot.xlabel('Epoch')
        pyplot.legend(['train', 'test'], loc='upper left')
        pyplot.savefig(save_figure_path + "-Accuracy.png")
        pyplot.clf()

    # Plot loss
    pyplot.plot(history.history['loss'])
    pyplot.plot(history.history['val_loss'])
    pyplot.title('model loss')
    pyplot.ylabel('loss')
    pyplot.xlabel('epoch')
    pyplot.legend(['train', 'test'], loc='upper left')
    pyplot.savefig(save_figure_path + "-Loss.png")

def validate_network(network_path, validation_data, category, batch_size, mean, std):
    # Load model
    model = load_model(network_path)

    # Generator for predictions
    prediction_generator = get_databatch(train_data, mean, std, batch_size=batch_size, category=category, shuffle=False, normalization=True,
                                         augmentation=False, balance_batches=False)

    # Predict labels for the validation data
    val_steps = int(np.ceil(float(len(validation_data)) / float(batch_size)))
    preds = model.predict_generator(prediction_generator, val_steps)
    preds = preds[:len(validation_data)]

    # Depending on the category, output either f1-score (categorical) or Root mean square error (regression)
    if(category=='Regression'):
        # Determine ground truth for the validation
        validation_labels = validation_data[:, -1]

        # Calculate RMSE and print
        rmse = math.sqrt(mean_squared_error(validation_labels, preds))
        print('RMSE score: ' + str(rmse))

    elif(category=='Change'):
        # Determine ground truth for the validation
        validation_labels = validation_data[:,-3:]

        # Determine ground truth per label
        decrease_label = (validation_labels[:,0]).astype(int)
        equal_label = (validation_labels[:,1]).astype(int)
        increase_label = (validation_labels[:,2]).astype(int)

        # Decide predictions with a minimum probability of 0.5
        decrease_pred = (preds[:,0] > 0.5).astype(int)
        equal_pred = (preds[:,1] > 0.5).astype(int)
        increase_pred = (preds[:,2] > 0.5).astype(int)

        # Print f1 scores
        print('F1 score decrease: ' + str(fbeta_score(decrease_label, decrease_pred, 1)))
        print('F1 score equal: ' + str(fbeta_score(equal_label, equal_pred, 1)))
        print('F1 score increase: ' + str(fbeta_score(increase_label, increase_pred, 1)))

    elif(category=='Jump'):
        # Determine ground truth for the validation
        validation_labels = (validation_data[:,-1]).astype(int)

        # Decide predictions (under 0.5 is no_jump, over 0.5 is jump)
        jump_pred = (preds[:,0] > 0.5).astype(int)

        # Print f1 scores
        print('F1 score no jump/jump: ' + str(fbeta_score(validation_labels, jump_pred, 1)))


if __name__ == "__main__":
    # Set important training parameters
    trainseries = '3000'
    category = 'Change'
    dataset_type = 'Medium'
    batch_size = 32
    epochs = 40
    dataset_file = "C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Datasets\\TrainDataset" + trainseries + "_Category-" + category + "_Normalization-True_OneHotEncoding-True_Model-" + dataset_type + ".csv"

    # Set parameters for the batch generator on basis of the category
    if(category=='Regression'):
        normalization = False
        augmentation = False
        balance_batches = False
    else:
        normalization = True
        augmentation = True
        balance_batches = True

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

    # Load data and transform to Panda dataframe (skip first two lines in train and first line in validation)
    train_data = pd.read_csv(dataset_file, header=None, skiprows=2)
    validation_data = pd.read_csv(dataset_file.replace("TrainDataset","ValidationDataset"), header=None, skiprows=1)

    # Load normalization parameters if necessary
    dataset = open(dataset_file)
    line = dataset.readline()
    columns = line.split(":")[1].split(",")
    mean = float(columns[0])
    std = float(columns[1])
    dataset.close()

    ####################

    # Train network with the data
    train_network(train_data, validation_data, category, dataset_type, batch_size, epochs, dataset_file, mean, std,
                  normalization=normalization, augmentation=augmentation, balance_batches=balance_batches)

    #########OR#########

    # # Validate network with data
    # network_path = ""
    # validate_network(network_path, validation_data, category, batch_size, mean, std)

    ###################
