import csv

# Script to create file that states for each train series the locations it crosses

# Open files to read from
input_trainnumbers_csv = open(
    "C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Data_vertragingen\\TrainseriesForInput.csv","r") # Set file containg all train series that are relevant, made using "trainseries_to_list.py"
reader1 = csv.reader(input_trainnumbers_csv)
input_trainnumbers = sum(list(reader1),[])
input_trainnumbers_csv.close()

realisatie_data = open(
    "C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Data_vertragingen\\Data_RAS\\RealisationData\\RealisationDataWithoutValidation.txt","r")

# Read from realisation data and collect locations to each trainseries
all_locations = [[] * 1 for i in range(len(input_trainnumbers))]
for line in realisatie_data:
    line = line.replace('"','')
    columns = line.split(",")
    series = columns[1]
    location = columns[4]
    if(series in input_trainnumbers):
        if(location not in all_locations[input_trainnumbers.index(series)]):
            all_locations[input_trainnumbers.index(series)].append(location)

realisatie_data.close()

# Make file to write to and write series and associated locations
trainseries_locations_combinations_file = open(
    "C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Data_vertragingen\\TrainseriesLocations.txt","w")

for ser,locs in zip(input_trainnumbers,all_locations):
    trainseries_locations_combinations_file.write(ser + ":")
    for loc in locs:
        trainseries_locations_combinations_file.write(loc)
        if(not(locs.index(loc) == (len(locs) - 1))):
            trainseries_locations_combinations_file.write(",")
        else:
            trainseries_locations_combinations_file.write("\n")

trainseries_locations_combinations_file.close()
