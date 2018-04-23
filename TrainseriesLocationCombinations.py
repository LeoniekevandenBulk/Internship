import csv

# Open files to read from
input_trainnumbers_csv = open(
    "C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Data_vertragingen\\TrainnumbersForInput.csv","r")
reader1 = csv.reader(input_trainnumbers_csv)
input_trainnumbers = sum(list(reader1),[])
input_trainnumbers_csv.close()

realisatie_data = open(
    "C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Data_vertragingen\\Data_RAS\\RealisationData\\RealisationDataWithoutValidation.txt","r")

# Read from realisation data and collect locations to each trainseries
locations = [[] * 1 for i in range(len(input_trainnumbers))]
for line in realisatie_data:
    line = line.replace('"','')
    columns = line.split(",")
    series = columns[1]
    location = columns[4]
    if(series in input_trainnumbers):
        if(location not in locations[input_trainnumbers.index(series)]):
            locations[input_trainnumbers.index(series)].append(location)

realisatie_data.close()

# Make file to write to and write series and associated locations
trainseries_locations_combinations_file = open(
    "C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Data_vertragingen\\TrainseriesLocationsCombinations.txt","w")

for ser,locs in zip(input_trainnumbers,locations):
    trainseries_locations_combinations_file.write(ser + ":")
    for loc in locs:
        trainseries_locations_combinations_file.write(loc)
        if(not(locs.index(loc) == (len(locs) - 1))):
            trainseries_locations_combinations_file.write(",")
        else:
            trainseries_locations_combinations_file.write("\n")

trainseries_locations_combinations_file.close()
