from datetime import timedelta
import random
import numpy as np

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
def list_trainseries_locations(trainseries):
    # Open file to read from
    location_data = open(
        "C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Data_vertragingen\\TrainseriesLocationsCombinations.txt", "r")

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

print(list_trainseries_locations(500))

# Generate dataset to train on from realisation data
def generate_dataset(realisation_path,trainseries,validation=False):
    # Open file to read from
    realisation_data = open(realisation_path, "r")

    # Make file to write to
    if(not validation):
        dataset = open(
            "C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Datasets\\TrainDataset" + str(trainseries) + "_simple.txt", "w")
    else:
        dataset = open(
            "C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Datasets\\ValidationDataset" + str(trainseries) + "_simple.txt", "w")

    # Read from realisation data and collect data from right trainseries
    previous_nr = 0
    for line in realisation_data:
        line = line.replace('"', '')
        columns = line.split(",")
        series = columns[1]
        train_nr = int(columns[3])
        if(str(trainseries) == series[0:len(str(trainseries))]):
            date = columns[0]
            weekday = calculate_weekday(date)
            day = one_hot_encoding([1,2,3,4,5],weekday,True)
            time = columns[6][11::]
            hour = int(time[0:2])
            minutes =  int(time[3:5])
            future_time = timedelta(hours=hour,minutes=minutes)
            if(train_nr is not previous_nr):
                begin_time = timedelta(hours=hour,minutes=minutes)
            direction = series[-1]
            if(direction == "E"):
                direction = 1
            else:
                direction = -1
            location = columns[4]
            location = one_hot_encoding(list_trainseries_locations(trainseries),location,True)
            future_delay = int(columns[8])

            # Open realisation data again to look 20 minutes in the past
            realisation_data2 = open(realisation_path, "r")

            previous_delay = 0
            # if begin time is not more than 20 minutes back and the delay should be picked from previous trainseries the train was driving on
            if (int((future_time - begin_time).__str__().split(":")[0]) == 0 and int(
                    (future_time - begin_time).__str__().split(":")[1]) < 20):
                same_train = -1
                # Open file to read connections
                connection_data = open(
                    "C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Data_vertragingen\\Data_RAS\\RollingStockConnectionsAll.txt",
                    "r")

                connection_nr = 0
                for con_line in connection_data:
                    con_columns = con_line.split("\t")
                    con_columns[4] = con_columns[4].replace("\n","")
                    con_weekday = con_columns[0]
                    con_train_nr = int(con_columns[3])
                    if (train_nr == con_train_nr and con_weekday == weekday):
                        connection_nr = con_train_nr
                        break
                connection_data.close()

                if (connection_nr == 0):
                    delay = 0
                    dataset.write(str(day)[1:-1].replace(" ", "") + "," + str(hour) + "," + str(minutes) + "," +
                                  str(direction) + "," + str(location)[1:-1].replace(" ", "") + "," + str(same_train)
                                  + "," + str(delay) + "," + str(future_delay) + "\n")
                else:
                    found = False
                    for line2 in realisation_data2:
                        line2 = line2.replace('"', '')
                        columns2 = line2.split(",")
                        current_train_nr = int(columns2[3])
                        current_delay = int(columns2[8])

                        if (connection_nr == current_train_nr):
                            time = columns2[6][11::]
                            current_hour = int(time[0:2])
                            current_minutes = int(time[3:5])
                            current_time = timedelta(hours=current_hour, minutes=current_minutes)

                            if ((future_time - timedelta(minutes=20)) > current_time):
                                delay = previous_delay
                                dataset.write(
                                    str(day)[1:-1].replace(" ", "") + "," + str(hour) + "," + str(minutes) + "," +
                                    str(direction) + "," + str(location)[1:-1].replace(" ", "") + "," + str(same_train)
                                    + "," + str(delay) + "," + str(future_delay) + "\n")
                                found = True
                                break
                            elif ((future_time - timedelta(minutes=20)) == current_time):
                                delay = current_delay
                                dataset.write(
                                    str(day)[1:-1].replace(" ", "") + "," + str(hour) + "," + str(minutes) + "," +
                                    str(direction) + "," + str(location)[1:-1].replace(" ", "") + "," + str(same_train)
                                    + "," + str(delay) + "," + str(future_delay) + "\n")
                                found = True
                                break

                        elif(connection_nr == previous_nr2 and not(previous_nr2 == current_train_nr)):
                            delay = previous_delay
                            dataset.write(
                                str(day)[1:-1].replace(" ", "") + "," + str(hour) + "," + str(minutes) + "," +
                                str(direction) + "," + str(location)[1:-1].replace(" ", "") + "," + str(same_train)
                                + "," + str(delay) + "," + str(future_delay) + "\n")
                            found = True
                            break
                        previous_delay = current_delay
                        previous_nr2 = current_train_nr

                    if(not found):
                        delay = 0
                        dataset.write(str(day)[1:-1].replace(" ", "") + "," + str(hour) + "," + str(minutes) + "," +
                                      str(direction) + "," + str(location)[1:-1].replace(" ", "") + "," + str(same_train)
                                      + "," + str(delay) + "," + str(future_delay) + "\n")

            # if begin time is more than 20 minutes back, look within the same trainnumber for the delay
            else:
                same_train = 1
                for line2 in realisation_data2:
                    line2 = line2.replace('"', '')
                    columns2 = line2.split(",")
                    current_train_nr = int(columns2[3])
                    current_delay = int(columns2[8])

                    if(train_nr == current_train_nr):
                        time = columns2[6][11::]
                        current_hour = int(time[0:2])
                        current_minutes = int(time[3:5])
                        current_time = timedelta(hours=current_hour, minutes=current_minutes)

                        if((future_time - timedelta(minutes=20)) > current_time):
                            delay = previous_delay
                            dataset.write(str(day)[1:-1].replace(" ", "") + "," + str(hour) + "," + str(minutes) + "," +
                                          str(direction) + "," + str(location)[1:-1].replace(" ", "") + "," + str(same_train)
                                          + "," + str(delay) + "," + str(future_delay) + "\n")
                            break
                        elif((future_time - timedelta(minutes=20)) == current_time):
                            delay = current_delay
                            dataset.write(str(day)[1:-1].replace(" ", "") + "," + str(hour) + "," + str(minutes) + "," +
                                          str(direction) + "," + str(location)[1:-1].replace(" ", "") + "," + str(same_train)
                                          + "," + str(delay) + "," + str(future_delay) + "\n")
                            break

                    previous_delay = current_delay
            realisation_data2.close()
        previous_nr = train_nr

    realisation_data.close()
    dataset.close()


def generate_testset(testdata_path, trainseries):
    pass


def get_databatch(dataset_path, batch_size=64, shuffle=True, augmentation=True, balance_batches=False):
    # Calculate size of dataset and entries
    data_file = open(dataset_path,"r")
    data = [line.split(',') for count,line in enumerate(data_file)]
    data_file.close()
    data_size = count+1
    line_size = len(line.split(","))

    while True:
        if(shuffle):
            random.shuffle(data)
        label_count = [0,0] #one element for delays of zero and one for the rest
        i = 0
        while i < data_size:
            entry_batch = np.zeros((batch_size, line_size-1), dtype=np.float32)
            label_batch = np.zeros((batch_size, 1), dtype=np.uint8)

            j = 0
            while j < batch_size:
                entry = data[i][0:-1]
                label = data[i][-1]
                i += 1
                if(label > 0):
                    label_category = 1
                else:
                    label_category = 0

                if balance_batches and label_count[label_category] >= batch_size / 2:
                    continue
                label_count[label_category] += 1

                # AUGMENTATION

                #ADD TO BATCH

                j += 1

            yield entry_batch, label_batch


def get_testbatch(testset_path, batch_size=64):
    pass