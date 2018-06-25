import Python.featureset_generator_basic as simple
import Python.featureset_generator_compositiondriverchanges as medium
import Python.featureset_generator_interactingtrains as hard
from datetime import datetime

def create_train_and_validation_set():
    startTime = datetime.now()

    trainseries = [3000, 3600, 4000, 8100]
    datasets = ['Simple', 'Medium', 'Hard']
    categories = ['Jump', 'Change', 'Regression']
    normalization = [False]
    one_hot_encoding = [False,True]
    parameters =  [(normalization[0],one_hot_encoding[0]),(normalization[0],one_hot_encoding[1])]
    realisation_path = "C:\\Users\Leonieke.vandenB_nsp\\OneDrive - NS\\Data_vertragingen\\Data_RAS\\RealisationData\\RealisationDataWithoutValidation.txt"
    validation_path = "C:\\Users\Leonieke.vandenB_nsp\\OneDrive - NS\\Data_vertragingen\\Data_RAS\\RealisationData\\Validationdata.txt"
    connections_path = "C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Data_vertragingen\\Data_RAS\\RollingStockConnectionsAll.txt"
    locations_path = "C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Data_vertragingen\\TrainseriesLocations.txt"
    composition_change_path = "C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Data_vertragingen\\Data_RAS\\RollingStockCompositionChangesSameTrain.txt"
    driver_change_path = "C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Data_vertragingen\\Data_RAS\\DriverSwitches.txt"
    route_path = "C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Data_vertragingen\\ModelTrainseriesRoutes.txt"
    timetable_path = "C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Data_vertragingen\\Data_RAS\\TimeTable\\TimeTable.txt"

    for series in trainseries:
        for param in parameters:
            for dataset in datasets:
                for category in categories:

                    if(dataset == 'Simple'):
                        print("Creating trainingset for trainseries " + str(series))
                        simple.generate_featureset(
                            realisation_path, connections_path, locations_path, route_path, series, category,
                            validation=False,normalization=param[0],one_hot_encoding=param[1])

                        print("Creating validationset for trainseries " + str(series))
                        simple.generate_featureset(
                            validation_path, connections_path, locations_path, route_path, series, category,
                            validation=True,normalization=param[0],one_hot_encoding=param[1])

                    elif(dataset == 'Medium'):
                        print("Creating trainingset for trainseries " + str(series))
                        medium.generate_featureset(
                            realisation_path, connections_path, locations_path, composition_change_path, driver_change_path, route_path,
                            series, category, validation=False, normalization=param[0], one_hot_encoding=param[1])

                        print("Creating validationset for trainseries " + str(series))
                        medium.generate_featureset(
                            validation_path, connections_path, locations_path, composition_change_path, driver_change_path, route_path,
                            series, category, validation=True, normalization=param[0], one_hot_encoding=param[1])

                    elif(dataset == 'Hard'):
                        print("Creating trainingset for trainseries " + str(series))
                        hard.generate_featureset(
                            realisation_path, connections_path, locations_path, composition_change_path, driver_change_path, route_path,
                            timetable_path, series, category, validation=False, normalization=param[0], one_hot_encoding=param[1])

                        print("Creating validationset for trainseries " + str(series))
                        hard.generate_featureset(
                            validation_path, connections_path, locations_path, composition_change_path, driver_change_path, route_path,
                            timetable_path, series, category, validation=True, normalization=param[0], one_hot_encoding=param[1])

    print(datetime.now() - startTime)


def create_test_set():
    startTime = datetime.now()

    trainseries = [3000, 3600, 4000, 8100]
    datasets = ['Simple', 'Medium', 'Hard']
    categories = ['Jump', 'Change', 'Regression']
    normalization = [False]
    one_hot_encoding = [False, True]
    parameters = [(normalization[0], one_hot_encoding[0]), (normalization[0], one_hot_encoding[1])]
    testset_path = "C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Data_vertragingen\\Data_RAS\\TestSet\\TestSet.txt"
    connections_path = "C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Data_vertragingen\\Data_RAS\\RollingStockConnectionsAll.txt"
    locations_path = "C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Data_vertragingen\\TrainseriesLocations.txt"
    composition_change_path = "C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Data_vertragingen\\Data_RAS\\RollingStockCompositionChangesSameTrain.txt"
    driver_change_path = "C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Data_vertragingen\\Data_RAS\\DriverSwitches.txt"
    route_path = "C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Data_vertragingen\\ModelTrainseriesRoutes.txt"
    timetable_path = "C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Data_vertragingen\\Data_RAS\\TimeTable\\TimeTable.txt"
    to_predict_path = "C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Evaluation\\ANSWER_FORM_LAYOUT.txt"

    for series in trainseries:
        for param in parameters:
            for dataset in datasets:
                for category in categories:

                    if (dataset == 'Simple'):
                        print("Creating testset for trainseries " + str(series))
                        simple.generate_testset(
                            testset_path, to_predict_path, connections_path, locations_path, route_path, series, category,
                            validation=True, normalization=param[0], one_hot_encoding=param[1])

                    elif (dataset == 'Medium'):
                        print("Creating trainingset for trainseries " + str(series))
                        medium.generate_testset(
                            testset_path, to_predict_path, connections_path, locations_path, composition_change_path,
                            driver_change_path, route_path,
                            series, category, validation=True, normalization=param[0], one_hot_encoding=param[1])

                    elif (dataset == 'Hard'):
                        print("Creating trainingset for trainseries " + str(series))
                        hard.generate_testset(
                            testset_path, to_predict_path, connections_path, locations_path, composition_change_path,
                            driver_change_path, route_path,
                            timetable_path, series, category, validation=True, normalization=param[0],
                            one_hot_encoding=param[1])

    print(datetime.now() - startTime)


if __name__ == "__main__":
    create_train_and_validation_set()
    #create_test_set()