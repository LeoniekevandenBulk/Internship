from dataset_generator_simple import generate_dataset_simple
from dataset_generator_medium import generate_dataset_medium
from dataset_generator_hard import generate_dataset_hard
from datetime import datetime

startTime = datetime.now()

trainseries = [3000]
dataset = 'Hard'
category = 'Change'
normalization = False
one_hot_encoding = False
realisation_path = "C:\\Users\Leonieke.vandenB_nsp\\OneDrive - NS\\Data_vertragingen\\Data_RAS\\RealisationData\\RealisationDataWithoutValidation.txt"
validation_path = "C:\\Users\Leonieke.vandenB_nsp\\OneDrive - NS\\Data_vertragingen\\Data_RAS\\RealisationData\\Validationdata.txt"
connections_path = "C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Data_vertragingen\\Data_RAS\\RollingStockConnectionsAll.txt"
locations_path = "C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Data_vertragingen\\TrainseriesLocations.txt"
composition_change_path = "C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Data_vertragingen\\Data_RAS\\RollingStockCompositionChangesSameTrain.txt"
driver_change_path = "C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Data_vertragingen\\Data_RAS\\DriverSwitches.txt"
route_path = "C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Data_vertragingen\\ModelTrainseriesRoutes.txt"
timetable_path = "C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Data_vertragingen\\Data_RAS\\TimeTable\\TimeTable.txt"

for series in trainseries:

    if(dataset == 'Simple'):
        print("Creating trainingset for trainseries " + str(series))
        generate_dataset_simple(
            realisation_path, connections_path, locations_path, route_path, series, category,
            validation=False,normalization=normalization,one_hot_encoding=one_hot_encoding)

        print("Creating validationset for trainseries " + str(series))
        generate_dataset_simple(
            validation_path, connections_path, locations_path, route_path, series, category,
            validation=True,normalization=normalization,one_hot_encoding=one_hot_encoding)

    elif(dataset == 'Medium'):
        print("Creating trainingset for trainseries " + str(series))
        generate_dataset_medium(
            realisation_path, connections_path, locations_path, composition_change_path, driver_change_path, route_path,
            series, category, validation=False, normalization=normalization, one_hot_encoding=one_hot_encoding)

        print("Creating validationset for trainseries " + str(series))
        generate_dataset_medium(
            validation_path, connections_path, locations_path, composition_change_path, driver_change_path, route_path,
            series, category, validation=True, normalization=normalization, one_hot_encoding=one_hot_encoding)

    elif(dataset == 'Hard'):
        print("Creating trainingset for trainseries " + str(series))
        generate_dataset_hard(
            realisation_path, connections_path, locations_path, composition_change_path, driver_change_path, route_path,
            timetable_path, series, category, validation=False, normalization=normalization, one_hot_encoding=one_hot_encoding)

        print("Creating validationset for trainseries " + str(series))
        generate_dataset_hard(
            validation_path, connections_path, locations_path, composition_change_path, driver_change_path, route_path,
            timetable_path, series, category, validation=True, normalization=normalization, one_hot_encoding=one_hot_encoding)

print(datetime.now() - startTime)