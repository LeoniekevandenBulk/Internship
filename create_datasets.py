from dataset_generator_simple import generate_dataset

trainseries = [3000]

for series in trainseries:
    print("Creating trainingset for trainseries " + str(series))
    generate_dataset(
        "C:\\Users\Leonieke.vandenB_nsp\\OneDrive - NS\\Data_vertragingen\\Data_RAS\\RealisationData\\RealisationDataWithoutValidation.txt",
        "C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Data_vertragingen\\Data_RAS\\RollingStockConnectionsAll.txt",
        "C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Data_vertragingen\\TrainseriesLocationsCombinations.txt",
        series,jump=False,change=True,regression=False,validation=False,normalization=True,one_hot_encoding=True)

    print("Creating validationset for trainseries " + str(series))
    generate_dataset(
        "C:\\Users\Leonieke.vandenB_nsp\\OneDrive - NS\\Data_vertragingen\\Data_RAS\\RealisationData\\Validationdata.txt",
        "C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Data_vertragingen\\Data_RAS\\RollingStockConnectionsAll.txt",
        "C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Data_vertragingen\\TrainseriesLocationsCombinations.txt",
        series,jump=False,change=True,regression=False,validation=True,normalization=True,one_hot_encoding=True)
