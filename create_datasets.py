from dataset_generator import generate_dataset

trainseries = [500]

for series in trainseries:
    generate_dataset(
        "C:\\Users\Leonieke.vandenB_nsp\\OneDrive - NS\\Data_vertragingen\\Data_RAS\\RealisationData\\RealisationDataWithoutValidation.txt",
        series,False)

for series in trainseries:
    generate_dataset(
        "C:\\Users\Leonieke.vandenB_nsp\\OneDrive - NS\\Data_vertragingen\\Data_RAS\\RealisationData\\Validationdata.txt",
        series, True)