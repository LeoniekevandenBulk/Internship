from dataset_generator_simple import generate_dataset_simple
from dataset_generator_medium import generate_dataset_medium
from dataset_generator_hard_test import generate_dataset_hard
from datetime import datetime

startTime = datetime.now()

trainseries = [3000]
datasets = ['Hard']#['Simple','Medium','Hard']
categories = ['Change']#['Jump','Change','Regression']
normalization = [False]#[False,True]
one_hot_encoding = [False]#[False,True]
parameters = [(normalization[0],one_hot_encoding[0])]#[(normalization[0],one_hot_encoding[0]),(normalization[1],one_hot_encoding[1])]
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
                    generate_dataset_simple(
                        realisation_path, connections_path, locations_path, route_path, series, category,
                        validation=False,normalization=param[0],one_hot_encoding=param[1])

                    print("Creating validationset for trainseries " + str(series))
                    generate_dataset_simple(
                        validation_path, connections_path, locations_path, route_path, series, category,
                        validation=True,normalization=param[0],one_hot_encoding=param[1])

                elif(dataset == 'Medium'):
                    print("Creating trainingset for trainseries " + str(series))
                    generate_dataset_medium(
                        realisation_path, connections_path, locations_path, composition_change_path, driver_change_path, route_path,
                        series, category, validation=False, normalization=param[0], one_hot_encoding=param[1])

                    print("Creating validationset for trainseries " + str(series))
                    generate_dataset_medium(
                        validation_path, connections_path, locations_path, composition_change_path, driver_change_path, route_path,
                        series, category, validation=True, normalization=param[0], one_hot_encoding=param[1])

                elif(dataset == 'Hard'):
                    # print("Creating trainingset for trainseries " + str(series))
                    # generate_dataset_hard(
                    #     realisation_path, connections_path, locations_path, composition_change_path, driver_change_path, route_path,
                    #     timetable_path, series, category, validation=False, normalization=param[0], one_hot_encoding=param[1])

                    print("Creating validationset for trainseries " + str(series))
                    generate_dataset_hard(
                        validation_path, connections_path, locations_path, composition_change_path, driver_change_path, route_path,
                        timetable_path, series, category, validation=True, normalization=param[0], one_hot_encoding=param[1])

print(datetime.now() - startTime)