from datetime import timedelta
import random
import numpy as np
from collections import defaultdict

# Create function for one hot encoding of categorical variables
def one_hot_encoding(category_list, category, drop_column=False):
    if(drop_column):
        one_hot = [0] * (len(category_list) - 1)
        if(not(category_list.index(category) == 0)):
            one_hot[category_list.index(category) - 1] = 1

    else:
        one_hot = [0] * len(category_list)
        if(not(category_list.index(category) == 0)):
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
def list_trainseries_locations(trainseries,trainseries_locations_path):
    # Open file to read from
    location_data = open(trainseries_locations_path,"r")

    locations = []
    # Search for locations of trainnumber
    for line in location_data:
        columns = line.split(":")
        series = columns[0]
        if(str(trainseries) == series[0:len(str(trainseries))]):
            for loc in columns[1].split(","):
                loc = loc.replace("\n","")
                locations.append(loc)
    location_data.close()

    return locations


# Generate dataset to train on from realisation data
def generate_dataset(realisation_path,connections_path,trainseries_locations_path,
                     trainseries,jump=False,change=False,regression=False,validation=False,
                     normalization=True,drop_column_one_hot_encoding=False):
    # Open file to read from
    realisation_data = open(realisation_path, "r")

    # Create list for every possible train number 1-99 to append entries to
    train_nr_entries = [ [] for j in range(100)]

    # Initialize vector to save all current delays (needed if normalization is on)
    current_delay_array = []

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
            day = one_hot_encoding([1,2,3,4,5],weekday,drop_column_one_hot_encoding)
            time = columns[6][11::]
            hour = int(time[0:2])
            minutes =  int(time[3:5])
            future_time = timedelta(hours=hour,minutes=minutes)
            if(not(train_nr == previous_nr)):
                begin_time = timedelta(hours=hour,minutes=minutes)
            direction = series[-1]
            if(direction == "E"):
                direction = 1
            else:
                direction = -1
            location = columns[4]
            location = one_hot_encoding(list_trainseries_locations(trainseries,trainseries_locations_path),location,drop_column_one_hot_encoding)
            future_delay = int(columns[8])

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
        con_weekday = con_columns[0]
        con_train_nr = int(con_columns[3])
        if((int(con_train_nr/100) == int(trainseries/100)) or
                (len(str(con_train_nr)) == 6 and con_train_nr < 400000 and
                 int(str(int(con_train_nr/100))[-1*len(str(int(trainseries/100))):]) == int(trainseries/100))):
            for entry in train_nr_entries[con_train_nr%100]:

                # Check if same_train is -1 and the weekday is correct
                if(entry[10] == -1 and con_weekday == entry[2]):

                    # Append with connection train number
                    entry.append(int(con_columns[1]))
                    train_cons[int(con_columns[1])] = con_train_nr

    # Close connection file
    connection_data.close()

    print("Fill delays that were not found in connections")

    # For each train with same_train is -1 that was not found in the connection file, add zero as connection and zero as initial delay
    for nr in train_nr_entries:
        if(nr):
            for entry in nr:
                if(not(len(entry) == 12)):
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
        current_delay = int(columns[8])

        # If the current trainseries is the same as trainseries we are looking for
        if ((str(trainseries) == current_series[0:len(str(trainseries))]) or (
                (5 - len(str(trainseries))) * "0" + str(trainseries) == current_series[1:6])):
            for entry in train_nr_entries[current_train_nr % 100]:
                # If the entry should find the past delay within the same number at the same date
                if(current_date == entry[1] and entry[10] == 1):
                    time = columns[6][11::]
                    current_hour = int(time[0:2])
                    current_minutes = int(time[3:5])
                    current_time = timedelta(hours=current_hour, minutes=current_minutes)
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
                    current_time = timedelta(hours=current_hour, minutes=current_minutes)
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

    # Make file to write to
    if(not validation):
        if(regression):
            dataset = open(
                "C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Datasets\\TrainDataset" + str(trainseries) +
                "_regression_" + str(normalization) + "_" + str(drop_column_one_hot_encoding) + "_simple.txt", "w")
        elif(change):
            dataset = open(
                "C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Datasets\\TrainDataset" + str(trainseries) +
                "_change_" + str(normalization) + "_" + str(drop_column_one_hot_encoding) + "_simple.txt", "w")
        elif(jump):
            dataset = open(
                "C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Datasets\\TrainDataset" + str(trainseries) +
                "_jump_" + str(normalization) + "_" + str(drop_column_one_hot_encoding) + "_simple.txt", "w")
    else:
        if(regression):
            dataset = open(
                "C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Datasets\\ValidationDataset" + str(trainseries) +
                "_regression_" + str(normalization) + "_" + str(drop_column_one_hot_encoding) + "_simple.txt", "w")
        elif (change):
            dataset = open(
                "C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Datasets\\ValidationDataset" + str(trainseries) +
                "_change_" + str(normalization) + "_" + str(drop_column_one_hot_encoding) + "_simple.txt", "w")
        elif (jump):
            dataset = open(
                "C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Datasets\\ValidationDataset" + str(trainseries) +
                "_jump_" + str(normalization) + "_" + str(drop_column_one_hot_encoding) + "_simple.txt", "w")

    # For all entries check if there is a intial delay, else add 0
    for nr in train_nr_entries:
        if(nr):
            for entry in nr:
                if(len(entry) == 12):
                    entry.append(0)
                    current_delay_array.append(0)

    # Calculate parameters for the optional normalization and write them to file (needed for testing)
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

    # Write all entries to the dataset file
    for nr in train_nr_entries:
        if(nr):
            for entry in nr:
                train_nr = entry[0]
                day = entry[3]
                hour = entry[4]
                minutes = entry[5]
                direction = entry[7]
                location = entry[8]
                future_delay = entry[9]
                same_train = entry[10]
                delay = entry[12]

                # Ceil every delay under zero (so a train that is too early) to zero
                if(delay < 0):
                    delay = 0
                if(future_delay < 0):
                    future_delay = 0

                # Normalize current delay with standardization
                if(normalization):
                    hour = hour/23
                    minutes = minutes/59
                    delay = (delay - mean)/std

                # Change the future delay to match the problem (classification/regression)
                if(regression):
                    dataset.write(
                        str(day)[1:-1].replace(" ", "") + "," + str(hour) + "," + str(minutes) + "," + str(direction)
                        + "," + str(location)[1:-1].replace(" ", "") + "," + str(same_train)
                        + "," + str(delay) + "," + str(future_delay) + "\n")
                elif(change):
                    category_list = ["increase","equal","decrease"]
                    if(future_delay - delay > 1):
                        future_category = "increase"
                    elif(delay - future_delay > 1):
                        future_category = "decrease"
                    else:
                        future_category = "equal"
                    future_category = one_hot_encoding(category_list,future_category,drop_column_one_hot_encoding)
                    dataset.write(
                        str(day)[1:-1].replace(" ", "") + "," + str(hour) + "," + str(minutes) + "," + str(direction)
                        + "," + str(location)[1:-1].replace(" ", "") + "," + str(same_train)
                        + "," + str(delay) + "," + str(future_category)[1:-1].replace(" ", "") + "\n")
                elif(jump):
                    category_list = ["YES", "NO"]
                    if (abs(future_delay - delay) > 4):
                        future_category = 1
                    else:
                        future_category = -1
                    dataset.write(
                        str(day)[1:-1].replace(" ", "") + "," + str(hour) + "," + str(minutes)+ "," + str(direction)
                        + "," + str(location)[1:-1].replace(" ", "") + "," + str(same_train)
                        + "," + str(delay) + "," + str(future_category) + "\n")
                else:
                    print("No choice was made in the parameters which form the output should have, please do so")
                    exit()

    # Close all files
    realisation_data.close()
    dataset.close()


def generate_testset(testdata_path, trainseries):
    pass


def get_databatch(dataset_path, batch_size=64, shuffle=True, augmentation=True, balance_batches=False):
    # Calculate size of dataset and entries
    data_file = open(dataset_path,"r")
    data = []
    count = 0
    for count, line in enumerate(data_file):
        data.append(line.split(','))
        count += 1
    data_file.close()
    data_size = count+1
    line_size = len(data[0])

    # A generator loop for the creation of batches
    while True:
        # Shuffle the data
        if(shuffle):
            random.shuffle(data)

        i = 0
        while i < data_size:
            entry_batch = np.zeros((batch_size, line_size-1), dtype=np.float32)
            label_batch = np.zeros((batch_size, 1), dtype=np.uint8)
            label_count = [0, 0]  # one element for delays of zero and one for the rest
            j = 0
            while j < batch_size:
                # Get the position modula data_size to prevent bacth size not lining up with the dataset size
                entry = data[i % data_size][0:-1]
                label = data[i % data_size][-1]
                i += 1
                if(label > 0):
                    label_category = 1
                else:
                    label_category = 0

                if balance_batches and label_count[label_category] >= batch_size / 2:
                    continue
                label_count[label_category] += 1

                # Augmentation by addding or subtracting one minute from the entries with a delay > 0
                if(augmentation and label_category == 1):
                    plus_one = random.uniform(0,1)
                    minus_one = random.uniform(0,1)
                    if(plus_one <= 0.25):
                        entry[-1] += 1
                    if(minus_one <= 0.25 and not(entry[-1] == 1)):
                        entry[-1] += 1

                entry_batch[j] = entry
                label_batch[j] = label

                j += 1

            yield entry_batch, label_batch


def get_testbatch(testset_path, batch_size=64):
    # Calculate size of dataset and entries
    data_file = open(testset_path, "r")
    data = []
    count = 0
    for count, line in enumerate(data_file):
        data.append(line.split(','))
        count += 1
    data_file.close()
    data_size = count + 1
    line_size = len(data[0])

    # A generator loop for the creation of batches
    while True:
        i = 0
        while i < data_size:
            entry_batch = np.zeros((batch_size, line_size - 1), dtype=np.float32)
            j = 0
            for j in range(batch_size):
                # Get the position modula data_size to prevent bacth size not lining up with the dataset size
                entry = data[i % data_size]
                entry_batch[j] = entry
                i += 1

            yield entry_batch