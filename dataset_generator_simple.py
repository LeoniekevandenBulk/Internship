from datetime import timedelta
import numpy as np
from collections import defaultdict
from sklearn import preprocessing

# Create function for one hot encoding of categorical variables
def transform_to_one_hot_encoding(category_list, category, drop_column=False):
    if(drop_column):
        one_hot = [0] * (len(category_list) - 1)
        if(not(category_list.index(category) == 0)):
            one_hot[category_list.index(category) - 1] = 1

    else:
        one_hot = [0] * len(category_list)
        one_hot[category_list.index(category)] = 1

    return one_hot

# Calculated according to https://blog.artofmemory.com/how-to-calculate-the-day-of-the-week-4203.html
# 0 = sunday, 1 = monday, ... , 6 = saturday
def calculate_weekday(date_in):
    date = date_in[0:10]
    year = int(date[2:4])
    month = date[5:7]
    daynr = int(date[8:10])
    yearnr = (year + int(year/4)) % 7
    centurynr = 6 #only the case for 2000s

    if(month == "01"):
        monthnr = 0
    elif(month == "02"):
        monthnr = 3
    elif(month == "03"):
        monthnr = 3
    elif(month == "04"):
        monthnr = 6
    elif(month == "05"):
        monthnr = 1
    elif(month == "06"):
        monthnr = 4
    elif(month == "07"):
        monthnr = 6
    elif(month == "08"):
        monthnr = 2
    elif(month == "09"):
        monthnr = 5
    elif(month == "10"):
        monthnr = 0
    elif(month == "11"):
        monthnr = 3
    else:
        monthnr = 5

    if ((year % 4) == 0 and (month == "01" or month == "02")):
        leapnr = 1
    else:
        leapnr = 0

    weekday = (yearnr + monthnr + centurynr + daynr - leapnr) % 7
    return weekday

# Return list of locations that a trainseries passes in his route
def list_trainseries_locations(trainseries, trainseries_locations_path):
    # Open file to read from
    location_data = open(trainseries_locations_path,"r")

    locations = []
    # Search for locations of trainnumber
    for line in location_data:
        columns = line.split(":")
        series = columns[0]
        if((str(trainseries) == series[0:-1]) or
                (len(series) == 7 and int(series[0:-1]) < 400000 and (5-len(str(trainseries)))*"0"+str(trainseries) == series[1:6])):
            for loc in columns[1].split(","):
                loc = loc.replace("\n","")
                locations.append(loc)
    location_data.close()

    return locations


# Generate dataset to train on from realisation data
def generate_dataset_simple(realisation_path, connections_path, trainseries_locations_path, route_path, trainseries, category,
                            validation=False, normalization=True, one_hot_encoding=False):
    # Open file to read from
    realisation_data = open(realisation_path, "r")

    # Create list for every possible train number 1-99 to append entries to
    train_nr_entries = [ [] for j in range(100)]

    # Initialize vector to save all current delays (needed if normalization is on)
    current_delay_array = []

    # Initialize label encoders in case one_hot_encoding is not used
    output_encoder = preprocessing.LabelEncoder()
    location_encoder = preprocessing.LabelEncoder()

    # Initialize list of locations the trainseries passes
    locations_list = list_trainseries_locations(trainseries, trainseries_locations_path)
    location_encoder.fit(locations_list)

    # Read route for this series
    route_O = []
    route_E = []
    route_data = open(route_path, "r")
    for route_line in route_data:
        route_columns = route_line.split(":")
        if(route_columns[0] == (str(trainseries) + "O")):
            route_O = route_columns[1].strip("\n").split(",")
        elif(route_columns[0] == (str(trainseries) + "E")):
            route_E = route_columns[1].strip("\n").split(",")
    route_data.close()

    print("Realisation data first iteration")

    # Read from realisation data and collect data from right trainseries
    previous_nr = 0
    for line in realisation_data:
        line = line.replace('"', '')
        columns = line.split(",")
        series = columns[1]
        train_nr = int(columns[3])

        # Check if the read line belongs to the right trainseries or a variation of that trainseries (when under construction)
        if((str(trainseries) == series[0:-1]) or
                (len(series) == 7 and int(series[0:-1]) < 400000 and (5-len(str(trainseries)))*"0"+str(trainseries) == series[1:6])):
            date = columns[0]
            weekday = calculate_weekday(date)
            # Transform day as it is a categorical variable
            if(one_hot_encoding):
                day = transform_to_one_hot_encoding([1,2,3,4,5],weekday,False)
            else:
                day = weekday
            time = columns[6][11::]
            hour = int(time[0:2])
            minutes =  int(time[3:5])
            if (hour >= 0 and hour < 4):
                future_time = timedelta(days=1, hours=hour, minutes=minutes)
            else:
                future_time = timedelta(days=0, hours=hour, minutes=minutes)
            # Save the begin time of a train number to be able to say if 20 minutes back is the same train
            if(not(train_nr == previous_nr)):
                if (hour >= 0 and hour < 4):
                    begin_time = timedelta(days=1, hours=hour, minutes=minutes)
                else:
                    begin_time = timedelta(days=0, hours=hour, minutes=minutes)
            direction = series[-1]
            if(direction == "E"):
                direction = 1
            else:
                direction = -1
            location = columns[4]
            # Transform location as it is a categorical variable
            if(location in locations_list):
                if (one_hot_encoding):
                    location = transform_to_one_hot_encoding(locations_list,location,False)
                else:
                    location = location_encoder.transform(np.array([location]))[0]
            # If location in validatation/test set did not occur in train set, give either all zeros for one hot, or just -1
            else:
                if (one_hot_encoding):
                    location = [0] * len(locations_list)
                else:
                    location = -1

            future_delay = float(columns[8])

            # Check time difference to decide if the delay 20 minutes ago should come from the same train number
            time_difference = (future_time - begin_time).__str__()
            # Check if the two times are in different days (can happen with trains around 00:00)
            if(len(time_difference.split(",")) == 1):
                # if begin time of this train number is not more than 20 minutes back, the delay should be picked from previous trainseries the train was driving on
                if (int(time_difference.split(":")[0]) == 0 and int(time_difference.split(":")[1]) < 20):
                    same_train = -1
                    train_nr_entries[train_nr%100].append([train_nr, date, weekday, day, hour, minutes, future_time, direction, location, future_delay, same_train])
                # else add this train number as the number to look for in the second iteration over the datafile
                else:
                    same_train = 1
                    train_nr_entries[train_nr%100].append([train_nr, date, weekday, day, hour, minutes, future_time, direction, location, future_delay, same_train, train_nr])
            else:
                # if begin time of this train number is not more than 20 minutes back, the delay should be picked from previous trainseries the train was driving on
                if (int(time_difference.split(",")[1].split(":")[0]) == 0 and int(time_difference.split(",")[1].split(":")[1]) < 20):
                    same_train = -1
                    train_nr_entries[train_nr%100].append([train_nr, date, weekday, day, hour, minutes, future_time, direction, location, future_delay, same_train])
                # else add this train number as the number to look for in the second iteration over the datafile
                else:
                    same_train = 1
                    train_nr_entries[train_nr%100].append([train_nr, date, weekday, day, hour, minutes, future_time, direction, location, future_delay, same_train, train_nr])

        # Save previous number to know when the number switches
        previous_nr = train_nr

    # Close data
    realisation_data.close()

    # Open file to read connections for trains that had a begin time of less than 20 minutes
    connection_data = open(connections_path,"r")

    # Create dictionary of train numbers that have a connection
    train_cons = defaultdict(list)

    print("Connection data")

    # Add connection train number to each dictionary entry if it is the right trainseries, same_train is -1 and the day is correct
    for con_line in connection_data:
        con_columns = con_line.split("\t")
        con_columns[4] = con_columns[4].replace("\n","")
        con_weekday = int(con_columns[0])
        con_location = con_columns[2]
        con_train_nr = con_columns[3]
        con_series = con_train_nr[:-2] + "00"
        if ((str(trainseries) == con_series) or
                (len(con_series) == 6 and int(con_series) < 400000 and
                 (5 - len(str(trainseries))) * "0" + str(trainseries) == con_series[1:6])):
            for entry in train_nr_entries[int(con_train_nr)%100]:
                direction = entry[7]
                if(direction == 1):
                    route = route_E
                else:
                    route = route_O
                # Check if same_train is -1 and the weekday is correct
                if(len(entry) == 11 and route[0] == con_location and entry[10] == -1 and con_weekday == entry[2]):
                    # Append with connection train number
                    entry.append(int(con_columns[1]))
                    train_cons[int(con_columns[1])] = int(con_train_nr)

    # Close connection file
    connection_data.close()

    print("Fill delays that were not found in connections")

    # For each train with same_train is -1 that was not found in the connection file, add zero as connection and zero as initial delay
    for nr in train_nr_entries:
        if(nr):
            for entry in nr:
                if(len(entry) == 11):
                    entry.append(0)
                    entry.append(0)
                    current_delay_array.append(0)

    print("Realisation data second iteration")

    # Open realisation data again to look for the delay 20 minutes in the past
    realisation_data = open(realisation_path, "r")
    previous_delay = 0
    for line in realisation_data:
        line = line.replace('"', '')
        columns = line.split(",")
        current_date = columns[0]
        current_series = columns[1]
        current_train_nr = int(columns[3])
        current_delay = float(columns[8])

        # If the current trainseries is the same as trainseries we are looking for
        if((str(trainseries) == current_series[0:-1]) or
                (len(current_series) == 7 and int(current_series[0:-1]) < 400000 and (5-len(str(trainseries)))*"0"+str(trainseries) == current_series[1:6])):
            for entry in train_nr_entries[current_train_nr % 100]:
                # If the entry should find the past delay within the same number at the same date
                if(current_date == entry[1] and entry[10] == 1):
                    time = columns[6][11::]
                    current_hour = int(time[0:2])
                    current_minutes = int(time[3:5])
                    if (current_hour >= 0 and current_hour < 4):
                        current_time = timedelta(days=1, hours=current_hour, minutes=current_minutes)
                    else:
                        current_time = timedelta(days=0, hours=current_hour, minutes=current_minutes)
                    future_time = entry[6]

                    # If we crossed the time we are looking for by one entry
                    if(((future_time - timedelta(minutes=20)) < current_time) and (len(entry) == 12)):
                        delay = previous_delay
                        entry.append(delay)
                        current_delay_array.append(delay)

                    # If this is exactly 20 minutes back
                    elif(((future_time - timedelta(minutes=20)) == current_time) and (len(entry) == 12)):
                        delay = current_delay
                        entry.append(delay)
                        current_delay_array.append(delay)

        # If the current trainseries is the a connection of the trainnumber we are looking for
        elif(current_train_nr in train_cons.keys()):
            for entry in train_nr_entries[train_cons[current_train_nr] % 100]:

                # If the entry should find the past delay within this different number at the same date
                if(current_date == entry[1] and entry[10] == -1 and entry[11] == current_train_nr):
                    time = columns[6][11::]
                    current_hour = int(time[0:2])
                    current_minutes = int(time[3:5])
                    if (current_hour >= 0 and current_hour < 4):
                        current_time = timedelta(days=1, hours=current_hour, minutes=current_minutes)
                    else:
                        current_time = timedelta(days=0, hours=current_hour, minutes=current_minutes)
                    future_time = entry[6]

                    # If we crossed the time we are looking for by one entry
                    if (((future_time - timedelta(minutes=20)) < current_time) and (len(entry) == 12)):
                        delay = previous_delay
                        entry.append(delay)
                        current_delay_array.append(delay)

                    # If this is exactly 20 minutes back
                    elif (((future_time - timedelta(minutes=20)) == current_time) and (len(entry) == 12)):
                        delay = current_delay
                        entry.append(delay)
                        current_delay_array.append(delay)

        # If the previous number was the connection of the trainnumber but the last data was more than 20 minutes back
        elif(previous_nr in train_cons.keys() and not(previous_nr == current_train_nr)):
            for entry in train_nr_entries[train_cons[previous_nr] % 100]:
                if (current_date == entry[1] and entry[10] == -1 and entry[11] == previous_nr and len(entry) == 12):
                    delay = previous_delay
                    entry.append(delay)
                    current_delay_array.append(delay)

        # Remember the previous delay and number
        previous_delay = current_delay
        previous_nr = current_train_nr

    # For all entries check if there is a intial delay, else add 0
    for nr in train_nr_entries:
        if(nr):
            for entry in nr:
                if(len(entry) == 12):
                    entry.append(0)
                    current_delay_array.append(0)

    # Make file to write to
    if(not validation):
        file_name = "C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Datasets\\TrainDataset" + str(trainseries) + \
                    "_Category-" + category + "_Normalization-" + str(normalization) + "_OneHotEncoding-" + str(one_hot_encoding) + "_Model-Simple.txt"
        dataset = open(file_name, "w")

    else:
        file_name = "C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Datasets\\ValidationDataset" + str(trainseries) + \
                    "_Category-" + category + "_Normalization-" + str(normalization) + "_OneHotEncoding-" + str(one_hot_encoding) + "_Model-Simple.txt"
        dataset = open(file_name, "w")

    # Calculate parameters for the optional normalization and write them to file (also needed for validation/testing)
    if(normalization and not validation):
        mean = np.mean(current_delay_array)
        std = np.std(current_delay_array)
        dataset.write("Normalization parameters:" + str(mean) + "," + str(std) + "\n")
    elif(normalization and validation):
        train_dataset = open(dataset.name.replace("Validation","Train"),"r")
        line = train_dataset.readline()
        columns = line.split(":")[1].split(",")
        mean = float(columns[0])
        std = float(columns[1])
        train_dataset.close()

    dataset.write("Day,Hour,Minutes,Direction,Location,Same_train,Delay,Future_Delay\n")

    # Write all entries to the dataset file
    for i,nr in enumerate(train_nr_entries):
        if(nr):
            for j,entry in enumerate(nr):
                train_nr = entry[0]
                day = entry[3]
                hour = entry[4]
                minutes = entry[5]
                direction = entry[7]
                location = entry[8]
                future_delay = float(entry[9])
                same_train = entry[10]
                delay = float(entry[12])

                # Ceil every delay under zero (so a train that is too early) to zero
                if(delay < 0):
                    delay = 0.0
                if(future_delay < 0):
                    future_delay = 0.0

                #Normalize current delay with standardization
                if(normalization):
                    hour = hour/23
                    minutes = minutes/59
                    delay = (delay - mean)/std

                # Change the future delay to match the problem (classification/regression)
                if(category == 'Regression'):
                    if(one_hot_encoding):
                        dataset.write(
                            str(day)[1:-1].replace(" ", "") + "," + str(hour) + "," + str(minutes) + "," + str(direction)
                            + "," + str(location)[1:-1].replace(" ", "") + "," + str(same_train)
                            + "," + str(delay) + "," + str(future_delay))
                    else:
                        dataset.write(
                            str(day) + "," + str(hour) + "," + str(minutes) + "," + str(direction)
                            + "," + str(location) + "," + str(same_train)
                            + "," + str(delay) + "," + str(future_delay))
                elif(category == 'Change'):
                    category_list = ["increase","equal","decrease"]
                    if(future_delay - delay > 1):
                        future_category = "increase"
                    elif(delay - future_delay > 1):
                        future_category = "decrease"
                    else:
                        future_category = "equal"

                    if(one_hot_encoding):
                        future_category = transform_to_one_hot_encoding(category_list,future_category,False)
                        dataset.write(
                            str(day)[1:-1].replace(" ", "") + "," + str(hour) + "," + str(minutes) + "," + str(direction)
                            + "," + str(location)[1:-1].replace(" ", "") + "," + str(same_train)
                            + "," + str(delay) + "," + str(future_category)[1:-1].replace(" ", ""))
                    else:
                        output_encoder.fit(category_list)
                        future_category = output_encoder.transform(np.array([future_category]))[0]
                        dataset.write(
                            str(day) + "," + str(hour) + "," + str(minutes) + "," + str(direction)
                            + "," + str(location) + "," + str(same_train)
                            + "," + str(delay) + "," + str(future_category))
                elif(category == 'Jump'):
                    if(abs(future_delay - delay) > 4):
                        future_category = 1
                    else:
                        future_category = 0

                    if(one_hot_encoding):
                        dataset.write(
                            str(day)[1:-1].replace(" ", "") + "," + str(hour) + "," + str(minutes)+ "," + str(direction)
                            + "," + str(location)[1:-1].replace(" ", "") + "," + str(same_train)
                            + "," + str(delay) + "," + str(future_category))
                    else:
                        dataset.write(
                            str(day) + "," + str(hour) + "," + str(minutes)+ "," + str(direction)
                            + "," + str(location) + "," + str(same_train)
                            + "," + str(delay) + "," + str(future_category))
                else:
                    print("No choice was made in the parameters which form the output should have, please do so")
                    exit()

                dataset.write("\n")

    # Close all files
    realisation_data.close()
    dataset.close()


def generate_testset(testdata_path, trainseries):
    pass
