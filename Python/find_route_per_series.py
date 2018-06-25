import numpy as np

# Open files to read from
input_trainseries_file = open(
    "C:\\Users\Leonieke.vandenB_nsp\\OneDrive - NS\\Data_vertragingen\\TrainseriesFromAnswerForm.txt","r")
input_trainnumbers = input_trainseries_file.readline().split(",")

trainseries = []
for series in input_trainnumbers:
    trainseries.append(series + "O")
    trainseries.append(series + "E")

realisatie_data = open(
    "C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Data_vertragingen\\Data_RAS\\RealisationData\\RealisationDataWithoutValidation.txt","r")

# Read from realisation data and collect locations to each trainseries
all_locations = [[] * 1 for i in range(len(trainseries))]
route_frequency = [[] * 1 for i in range(len(trainseries))]
locations = []
previous_number = 0
for line in realisatie_data:
    line = line.replace('"','')
    columns = line.split(",")
    series = columns[1]
    number = columns[3]
    location = columns[4]

    if(series in trainseries):

        if(not(number == previous_number) and not(locations == [])):
            if(locations in all_locations[trainseries.index(series)]):
                route_frequency[trainseries.index(series)][all_locations[trainseries.index(series)].index(locations)] = \
                    route_frequency[trainseries.index(series)][all_locations[trainseries.index(series)].index(locations)] + 1
            else:
                all_locations[trainseries.index(series)].append(locations)
                route_frequency[trainseries.index(series)].append(1)

            locations = []
            locations.append(location)

        else:
            locations.append(location)

    previous_number = number

realisatie_data.close()

most_frequent_locations = []
for i,frequencies in enumerate(route_frequency):
    index = np.argmax(frequencies)
    route = all_locations[i][index]
    previous_loc = ''
    remove_indices= []
    for j,loc in enumerate(route):
        if(previous_loc == loc):
            remove_indices.append(j)
        previous_loc = loc

    route = [i for j, i in enumerate(route) if j not in remove_indices]
    most_frequent_locations.append(route)

# Make file to write to and write series and associated locations
trainseries_locations_combinations_file = open(
    "C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Data_vertragingen\\ModelTrainseriesRoutes.txt","w")

for ser,locs in zip(trainseries, most_frequent_locations):
    print(ser)
    print(locs)
    trainseries_locations_combinations_file.write(ser + ":")
    for loc in locs:
        trainseries_locations_combinations_file.write(loc)
        if(not(locs.index(loc) == (len(locs) - 1))):
            trainseries_locations_combinations_file.write(",")
        else:
            trainseries_locations_combinations_file.write("\n")

trainseries_locations_combinations_file.close()