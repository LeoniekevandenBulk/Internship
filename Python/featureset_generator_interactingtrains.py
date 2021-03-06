from datetime import timedelta
import numpy as np
from collections import defaultdict
from sklearn import preprocessing
from datetime import datetime
import copy

# Functions to create the Interacting Trains feature set used by "create_featuresets.py"

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

# Calculate weekday for timetable format
def calculate_weekday_timetable(date_in):
    daynr = int(date_in[0])
    month = date_in[2]
    year = int(date_in[6:8])
    yearnr = (year + int(year/4)) % 7
    centurynr = 6 #only the case for 2000s

    if(month == "1"):
        monthnr = 0
    elif(month == "2"):
        monthnr = 3
    elif(month == "3"):
        monthnr = 3
    elif(month == "4"):
        monthnr = 6
    elif(month == "5"):
        monthnr = 1
    elif(month == "6"):
        monthnr = 4
    elif(month == "7"):
        monthnr = 6
    elif(month == "8"):
        monthnr = 2
    elif(month == "9"):
        monthnr = 5
    elif(month == "10"):
        monthnr = 0
    elif(month == "11"):
        monthnr = 3
    else:
        monthnr = 5

    if ((year % 4) == 0 and (month == "1" or month == "2")):
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


# Generate feature set to train on or validate on from realisation data
def generate_featureset(realisation_path, connections_path, trainseries_locations_path, composition_change_path,
                            driver_change_path, route_path, timetable_path, trainseries, category, validation=False,
                            normalization=True, one_hot_encoding=False):
    # Open file to read from
    realisation_data = open(realisation_path, "r")

    # Create list for every possible train number 1-99 to append entries to
    train_nr_entries = [ [] for j in range(100)]

    # Initialize vector to save all current delays (needed if normalization is on)
    current_delay_array = []
    previous_delay_array = []
    previous_delay2_array = []

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

    # Add connection train number to each dictionary entry if it is the right trainseries and the day is correct
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

    # For each train with same_train is -1 that was not found in the connection file, add zero as connection and zero
    # as initial location and delay, previous delay and second previous delay. -1 can also be added for driver switch
    # and composition change
    for nr in train_nr_entries:
        if(nr):
            for entry in nr:
                if(not(len(entry) == 12)):
                    entry.append(0)
                    entry.append("Unknown")
                    entry.append(0)
                    entry.append(0)
                    entry.append(0)
                    current_delay_array.append(0)
                    previous_delay_array.append(0)
                    previous_delay2_array.append(0)
                    entry.append(-1)
                    entry.append(-1)

    print("Realisation data second iteration")

    # Open realisation data again to look for the delay 20 minutes in the past
    realisation_data = open(realisation_path, "r")
    previous_delay = {"delay": 0, "nr": 0, "loc":""}
    previous_delay2 = {"delay": 0, "nr": 0, "loc":""}
    previous_delay3 = {"delay": 0, "nr": 0, "loc":""}
    for line in realisation_data:
        line = line.replace('"', '')
        columns = line.split(",")
        current_date = columns[0]
        current_series = columns[1]
        current_train_nr = int(columns[3])
        current_location = columns[4]
        current_delay = float(columns[8])

        # If the current trainseries is the same as trainseries we are looking for
        if((str(trainseries) == current_series[0:-1]) or
                (len(current_series) == 7 and int(current_series[0:-1]) < 400000 and
                 (5-len(str(trainseries)))*"0"+str(trainseries) == current_series[1:6])):
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
                    future_location = entry[8]

                    # If we crossed the time we are looking for by one entry
                    if(((future_time - timedelta(minutes=20)) < current_time) and (len(entry) == 12)):
                        # Add current location
                        entry.append(previous_delay["loc"])
                        # Add delay from 20 minutes back
                        delay = previous_delay["delay"]
                        entry.append(delay)
                        current_delay_array.append(delay)
                        # Add the delay before that if it is within this train number
                        if(previous_delay2["nr"] == current_train_nr):
                            entry.append(previous_delay2["delay"])
                            previous_delay_array.append(previous_delay2["delay"])
                        else:
                            entry.append(0)
                            previous_delay_array.append(0)
                        # Also add the second previous delay if it is within this train number
                        if(previous_delay3["nr"] == current_train_nr):
                            entry.append(previous_delay3["delay"])
                            previous_delay2_array.append(previous_delay3["delay"])
                        else:
                            entry.append(0)
                            previous_delay2_array.append(0)

                    # If this is exactly 20 minutes back
                    elif(((future_time - timedelta(minutes=20)) == current_time) and (len(entry) == 12)):
                        # Add current location
                        entry.append(current_location)
                        # Add delay from 20 minutes back
                        delay = current_delay
                        entry.append(delay)
                        current_delay_array.append(delay)
                        # Add the delay before that if it is within this train number
                        if(previous_delay["nr"] == current_train_nr):
                            entry.append(previous_delay["delay"])
                            previous_delay_array.append(previous_delay["delay"])
                        else:
                            entry.append(0)
                            previous_delay_array.append(0)
                        # Also add the second previous delay if it is within this train number
                        if(previous_delay2["nr"] == current_train_nr):
                            entry.append(previous_delay2["delay"])
                            previous_delay2_array.append(previous_delay2["delay"])
                        else:
                            entry.append(0)
                            previous_delay2_array.append(0)

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
                    future_location = entry[8]
                    future_nr = entry[0]

                    # If we crossed the time we are looking for by one entry
                    if (((future_time - timedelta(minutes=20)) < current_time) and (len(entry) == 12)):
                        # Add current location
                        entry.append(previous_delay["loc"])
                        # Add delay from 20 minutes back
                        delay = previous_delay["delay"]
                        entry.append(delay)
                        current_delay_array.append(delay)
                        # Add the delay before that if it is within this train number
                        if (previous_delay2["nr"] == current_train_nr):
                            entry.append(previous_delay2["delay"])
                            previous_delay_array.append(previous_delay2["delay"])
                        else:
                            entry.append(0)
                            previous_delay_array.append(0)
                        # Also add the second previous delay if it is within this train number
                        if (previous_delay3["nr"] == current_train_nr):
                            entry.append(previous_delay3["delay"])
                            previous_delay2_array.append(previous_delay3["delay"])
                        else:
                            entry.append(0)
                            previous_delay2_array.append(0)

                    # If this is exactly 20 minutes back
                    elif (((future_time - timedelta(minutes=20)) == current_time) and (len(entry) == 12)):
                        # Add current location
                        entry.append(current_location)
                        # Add delay from 20 minutes back
                        delay = current_delay
                        entry.append(delay)
                        current_delay_array.append(delay)
                        # Add the delay before that if it is within this train number
                        if (previous_delay["nr"] == current_train_nr):
                            entry.append(previous_delay["delay"])
                            previous_delay_array.append(previous_delay["delay"])
                        else:
                            entry.append(0)
                            previous_delay_array.append(0)
                        # Also add the second previous delay if it is within this train number
                        if (previous_delay2["nr"] == current_train_nr):
                            entry.append(previous_delay2["delay"])
                            previous_delay2_array.append(previous_delay2["delay"])
                        else:
                            entry.append(0)
                            previous_delay2_array.append(0)

        # If the previous number was the connection of the trainnumber but the last data was more than 20 minutes back
        elif(previous_nr in train_cons.keys() and not(previous_nr == current_train_nr)):
            for entry in train_nr_entries[train_cons[previous_nr] % 100]:
                if (current_date == entry[1] and entry[10] == -1 and entry[11] == previous_nr and len(entry) == 12):
                    future_location = entry[8]
                    future_nr = entry[0]
                    # Add current location
                    entry.append(previous_delay["loc"])
                    # Add delay from 20 minutes back
                    delay = previous_delay["delay"]
                    entry.append(delay)
                    current_delay_array.append(delay)
                    # Add the delay before that if it is within this train number
                    if (previous_delay2["nr"] == previous_nr):
                        entry.append(previous_delay2["delay"])
                        previous_delay_array.append(previous_delay2["delay"])
                    else:
                        entry.append(0)
                        previous_delay_array.append(0)
                    # Also add the second previous delay if it is within this train number
                    if (previous_delay3["nr"] == previous_nr):
                        entry.append(previous_delay3["delay"])
                        previous_delay2_array.append(previous_delay3["delay"])
                    else:
                        entry.append(0)
                        previous_delay2_array.append(0)

        # Remember the previous delay and number
        previous_delay3 = previous_delay2
        previous_delay2 = previous_delay
        previous_delay = {"delay":current_delay, "nr":current_train_nr, "loc":current_location}
        previous_nr = current_train_nr

    realisation_data.close()
    del(train_cons)

    print("Fill the features driver_switch and composition_change")

    # Determine if driver_switch is true for every entry
    driver_data = open(driver_change_path, "r")
    for driver_line in driver_data:
        driver_columns = driver_line.replace("\n","").split(" ")
        if (not (driver_columns[3] == "-")):
            switch_nr = driver_columns[3]
            switch_series = switch_nr[:-2] + "00"
            if ((str(trainseries) == switch_series) or
                    (len(switch_series) == 6 and int(switch_series) < 400000 and
                     (5 - len(str(trainseries))) * "0" + str(trainseries) == switch_series[1:6])):
                switch_location = driver_columns[4]
                switch_day = int(driver_columns[5])
                for entry in train_nr_entries[int(switch_nr) % 100]:
                    if(switch_day == entry[2] and len(entry) == 16):
                        if (entry[7] == 1):
                            route = route_E
                        else:
                            route = route_O
                        if(entry[10] == 1):
                            if ((entry[12] in route) and (entry[8] in route)):
                                if (switch_location in route[route.index(entry[12]):route.index(entry[8])]):
                                    entry.append(1)
                        if(entry[10] == -1):
                            if (entry[8] in route):
                                if (switch_location in route[:route.index(entry[8])]):
                                    entry.append(1)

    # For all entries check if the driver switch feature has been added, else add -1.
    for nr in train_nr_entries:
        if (nr):
            for entry in nr:
                if (len(entry) == 16):
                    entry.append(-1)

    # Determine if composition_change is true for every entry
    composition_data = open(composition_change_path, "r")
    for comp_line in composition_data:
        comp_columns = comp_line.replace("\n","").split("\t")
        change_nr = comp_columns[2]
        change_series = change_nr[:-2] + "00"
        if ((str(trainseries) == change_series) or
                (len(change_series) == 6 and int(change_series) < 400000 and
                 (5 - len(str(trainseries))) * "0" + str(trainseries) == change_series[1:6])):
            change_location = comp_columns[0]
            change_day = int(comp_columns[1])
            for entry in train_nr_entries[int(change_nr) % 100]:
                if (change_day == entry[2] and len(entry) == 17):
                    if (entry[7] == 1):
                        route = route_E
                    else:
                        route = route_O
                    if (entry[10] == 1):
                        if ((entry[12] in route) and (entry[8] in route)):
                            if (change_location in route[route.index(entry[12]):route.index(entry[8])]):
                                entry.append(1)
                    elif (entry[10] == -1):
                        if (entry[8] in route):
                            if (change_location in route[:route.index(entry[8])]):
                                entry.append(1)

    # For all entries check if there is a initial delay, else add 0 for initial location and delay, previous and
    # second previous delay. -1 can also be added for composition change
    for nr in train_nr_entries:
        if (nr):
            for entry in nr:
                if (len(entry) == 12):
                    entry.append("Unknown")
                    entry.append(0)
                    entry.append(0)
                    entry.append(0)
                    current_delay_array.append(0)
                    previous_delay_array.append(0)
                    previous_delay2_array.append(0)
                    entry.append(-1)
                    entry.append(-1)
                elif (len(entry) == 17):
                    entry.append(-1)

    print("Fill relevant delays of other trains that cross the route of the current trainseries")

    # Find trainseries that have one or more overlapping locations in the route (intersection of route_O and route_E)
    crossing_series = []
    crossing_series_list = []
    main_locations = list(set(route_O).intersection(set(route_E)))
    route_data = open(route_path, "r")
    for route_line in route_data:
        route_columns = route_line.replace("\n","").split(":")
        route_locations = route_columns[1].split(",")
        if(not(route_columns[0] == (str(trainseries) + "O")) and not(route_columns[0] == (str(trainseries) + "E"))):
            if(len(set(main_locations).intersection(set(route_locations))) > 0):
                crossing_series.append({"series":route_columns[0],"locations":route_locations,"array":[]})
                crossing_series_list.append(route_columns[0])
    route_data.close()

    # For each entry, find best location for each overlapping trainseries to save delay from
    for nr in train_nr_entries:
        if (nr):
            for entry in nr:
                if(entry[10] == 1):
                    for series in crossing_series:
                        found = False
                        current_location = entry[12]
                        if(current_location in series["locations"]):
                            entry.append({"series": series["series"], "loc": current_location, "time": "", "nr": ("",False), "delay": ("",False)})
                            found = True
                        else:
                            if (entry[7] == 1):
                                route = route_E
                            else:
                                route = route_O
                            future_location = entry[8]
                            if(route.__contains__(current_location)):
                                index_begin = route.index(current_location)
                            else:
                                index_begin = 0
                            if (route.__contains__(future_location)):
                                index_end = route.index(future_location)
                            else:
                                index_end = len(route)-1

                            for i in range(index_begin+1,index_end+1):
                                if((route[i] in series["locations"]) and not found):
                                    entry.append({"series": series["series"], "loc": route[i], "time": "", "nr": ("",False), "delay": ("",False)})
                                    found = True
                else:
                    for series in crossing_series:
                        found = False
                        if (entry[7] == 1):
                            route = route_E
                        else:
                            route = route_O
                        future_location = entry[8]
                        if (route.__contains__(future_location)):
                            index_end = route.index(future_location)
                        else:
                            index_end = len(route) - 1
                        for i in range(0,index_end+1):
                            if((route[i] in series["locations"]) and not found):
                                entry.append({"series": series["series"], "loc": route[i], "time": "", "nr": ("",False), "delay": ("",False)})
                                found = True

    # Loop through planning and find time each entry crosses a location in which it is crossed
    timetable_data = open(timetable_path, "r")
    for timetable_line in timetable_data:
        timetable_line = timetable_line.replace('"', '')
        timetable_columns = timetable_line.split(",")
        timetable_nr = timetable_columns[1]
        timetable_series = timetable_nr[:-2] + "00"
        if ((str(trainseries) == timetable_series) or
                (len(timetable_series) == 6 and int(timetable_series) < 400000 and
                 (5 - len(str(trainseries))) * "0" + str(trainseries) == timetable_series[1:6])):
            timetable_location = timetable_columns[3]
            timetable_date = timetable_columns[0]
            timetable_day = calculate_weekday_timetable(timetable_date)
            timetable_direction = timetable_columns[2]
            for entry in train_nr_entries[int(timetable_nr) % 100]:
                current_day = entry[2]
                current_direction = entry[7]
                if (current_direction == 1):
                    current_direction = "E"
                else:
                    current_direction = "O"
                if(timetable_day == current_day and current_direction == timetable_direction):
                    for i in range(18,len(entry)):
                        crossing = entry[i]
                        if(crossing["loc"] == timetable_location):
                            if(not(timetable_columns[7] == '')):
                                timetable_hours = int(timetable_columns[7][9:11])
                                timetable_minutes = int(timetable_columns[7][12:14])
                                if(timetable_hours >= 0 and timetable_hours < 4):
                                    crossing["time"] = timedelta(days=1, hours=timetable_hours, minutes=timetable_minutes)
                                else:
                                    crossing["time"] = timedelta(days=0,hours=timetable_hours,minutes=timetable_minutes)
    timetable_data.close()

    # Fill all entries where there are crossing trains with relevant=1, but no time, this means it was not found in the timetable
    for nr in train_nr_entries:
        if (nr):
            for entry in nr:
                if(len(entry) > 18):
                    remove_list = []
                    for i in range(18, len(entry)):
                        crossing = entry[i]
                        if (crossing["time"] == ""):
                            remove_list.append(i)
                    remove_list.reverse()
                    for remove in remove_list:
                        entry.__delitem__(remove)

    # Reshape the entry list to be able to search on date and crossing to speed up computation
    date_dict = {}
    for nr in train_nr_entries:
        if (nr):
            for entry in nr:
                entry_date = entry[1]
                if(not(entry_date in date_dict)):
                    date_dict[entry_date] = ""

    crossing_dict = {}
    for series in crossing_series:
        location_dict = {}
        for location in series["locations"]:
            location_dict[location] = []
        for date in date_dict:
            date_dict[date] = copy.deepcopy(location_dict)
        crossing_dict[series["series"]] = copy.deepcopy(date_dict)

    train_entries_dict = {1:copy.deepcopy(crossing_dict), 2:copy.deepcopy(crossing_dict), 3:copy.deepcopy(crossing_dict), 4:copy.deepcopy(crossing_dict), 5:copy.deepcopy(crossing_dict)}
    entries_with_no_crossings = []
    tracking_number = 0 # number to know which dictionary entries belong to the same original entry
    for nr in train_nr_entries:
        if (nr):
            for entry in nr:
                if(len(entry) > 18):
                    entry_date = entry[1]
                    entry_day = calculate_weekday(entry_date)
                    for i in range(18, len(entry)):
                        new_entry = entry[0:18]
                        crossing = entry[i]
                        series = crossing["series"]
                        crossing_loc = crossing["loc"]
                        new_entry.append(crossing)
                        new_entry.append(tracking_number)
                        train_entries_dict[entry_day][series][entry_date][crossing_loc].append(new_entry)
                else:
                    new_entry = entry[0:18]
                    new_entry.append(tracking_number)
                    entries_with_no_crossings.append(new_entry)
                tracking_number = tracking_number + 1

    del(train_nr_entries)

    # Loop through planning to find the most suitable trainnumber per crossing series with the found times
    timetable_data = open(timetable_path, "r")
    for timetable_line in timetable_data:
        timetable_line = timetable_line.replace('"', '')
        timetable_columns = timetable_line.split(",")
        if (not (timetable_columns[7] == '')):
            timetable_date = timetable_columns[0]
            timetable_nr = timetable_columns[1]
            timetable_direction = timetable_columns[2]
            timetable_location = timetable_columns[3]
            timetable_day = calculate_weekday_timetable(timetable_date)
            timetable_series = timetable_nr[:-2] + "00" + timetable_direction
            if(timetable_series in crossing_series_list):
                normal_series = timetable_series
                relevant_entries_dict = train_entries_dict[timetable_day][normal_series]
            elif(len(timetable_series) == 7 and int(timetable_series[0:-1]) < 400000):
                normal_series = 0
                if(timetable_series[0:3] == "100" or timetable_series[0:3] == "200" or timetable_series[0:3] == "300"):
                    normal_series = timetable_series[3:]
                elif(timetable_series[0:2] == "10" or timetable_series[0:2] == "20" or timetable_series[0:2] == "30"):
                    normal_series = timetable_series[2:]
                elif(timetable_series[0:1] == "1" or timetable_series[0:1] == "2" or timetable_series[0:1] == "3"):
                    normal_series = timetable_series[1:]
                if(not(normal_series == 0) and normal_series in crossing_series_list):
                    relevant_entries_dict = train_entries_dict[timetable_day][normal_series]
                else:
                    continue
            else:
                continue

            if(timetable_location in crossing_series[crossing_series_list.index(normal_series)]["locations"]):
                timetable_hours = int(timetable_columns[7][9:11])
                timetable_minutes = int(timetable_columns[7][12:14])
                if (timetable_hours >= 0 and timetable_hours < 4):
                    timetable_time = timedelta(days=1, hours=timetable_hours, minutes=timetable_minutes)
                else:
                    timetable_time = timedelta(days=0, hours=timetable_hours, minutes=timetable_minutes)

                for date in relevant_entries_dict:
                    relevant_entries = relevant_entries_dict[date][timetable_location]
                    for entry in relevant_entries:
                        crossing = entry[18]
                        if (crossing["nr"][1] == False):
                            if (timetable_time <= crossing["time"]):
                                crossing["nr"] = (timetable_nr, False)
                            elif (timetable_time > crossing["time"]):
                                crossing["nr"] = (crossing["nr"][0], True)
            else:
                continue

    timetable_data.close()

    # Reshape the entry dictionary to be able to add the previously found number to speed up computation
    train_entries_dict_with_nr = copy.deepcopy(train_entries_dict)
    for weekday in train_entries_dict:
        for series in train_entries_dict[weekday]:
            for date in train_entries_dict[weekday][series]:
                train_entries_dict_with_nr[weekday][series][date] = {}
                for index in range(100):
                    train_entries_dict_with_nr[weekday][series][date][index] = {}
                for loc in train_entries_dict[weekday][series][date]:
                    for entry in train_entries_dict[weekday][series][date][loc]:
                        nr = entry[18]["nr"][0]
                        if(nr == ""): #Save entries with no crossing in number 0 as this a train number will never be 0
                            if(loc in train_entries_dict_with_nr[weekday][series][date][0]):
                                train_entries_dict_with_nr[weekday][series][date][0][loc].append(entry)
                            else:
                                train_entries_dict_with_nr[weekday][series][date][0][loc] = []
                                train_entries_dict_with_nr[weekday][series][date][0][loc].append(entry)
                        else:
                            if(loc in train_entries_dict_with_nr[weekday][series][date][int(nr)%100]):
                                train_entries_dict_with_nr[weekday][series][date][int(nr)%100][loc].append(entry)
                            else:
                                train_entries_dict_with_nr[weekday][series][date][int(nr)%100][loc] = []
                                train_entries_dict_with_nr[weekday][series][date][int(nr)%100][loc].append(entry)

    del(train_entries_dict)

    # Loop through the realisation data to find the delays of the found trainnumbers per crossing series
    realisation_data = open(realisation_path, "r")
    for line in realisation_data:
        line = line.replace('"', '')
        columns = line.split(",")
        date = columns[0]
        series = columns[1]
        train_nr = int(columns[3])%100
        weekday = calculate_weekday(date)
        if (series in crossing_series_list):
            normal_series = series
            if(train_nr in train_entries_dict_with_nr[weekday][normal_series][date]):
                relevant_entries_dict = train_entries_dict_with_nr[weekday][normal_series][date][train_nr]
            else:
                continue
        elif (len(series) == 7 and int(series[0:-1]) < 400000):
            normal_series = 0
            if (series[0:3] == "100" or series[0:3] == "200" or series[0:3] == "300"):
                normal_series = series[3:]
            elif (series[0:2] == "10" or series[0:2] == "20" or series[0:2] == "30"):
                normal_series = series[2:]
            elif (series[0:1] == "1" or series[0:1] == "2" or series[0:1] == "3"):
                normal_series = series[1:]
            if (not (normal_series == 0) and normal_series in crossing_series_list):
                if (train_nr in train_entries_dict_with_nr[weekday][normal_series][date]):
                    relevant_entries_dict = train_entries_dict_with_nr[weekday][normal_series][date][train_nr]
                else:
                    continue
            else:
                continue
        else:
            continue

        hours = int(columns[7][11:13])
        minutes = int(columns[7][14:16])
        if (hours >= 0 and hours < 4):
            time = timedelta(days=1, hours=hours, minutes=minutes)
        else:
            time = timedelta(days=0, hours=hours, minutes=minutes)

        for location in relevant_entries_dict:
            relevant_entries = relevant_entries_dict[location]
            for entry in relevant_entries:
                entry_hours = entry[4]
                entry_minutes = entry[5]
                if (entry_hours >= 0 and entry_hours < 4):
                    entry_time = timedelta(days=1, hours=entry_hours, minutes=entry_minutes)
                else:
                    entry_time = timedelta(days=0, hours=entry_hours, minutes=entry_minutes)
                crossing = entry[18]
                if (crossing["delay"][1] == False):
                    if (time < entry_time):
                        crossing_delay = int(columns[8])
                        if (crossing_delay < 0):
                            crossing_delay = 0
                        crossing["delay"] = (crossing_delay, False)
                    elif (time >= entry_time):
                        crossing["delay"] = (crossing["delay"][0], True)
    realisation_data.close()

    # Transform all crossing entries back to their original entry form and fill all delays that have not been filled with 0
    transformed_entries_dict = {}
    for day in train_entries_dict_with_nr:
        for series in train_entries_dict_with_nr[day]:
            for date in train_entries_dict_with_nr[day][series]:
                for nr in train_entries_dict_with_nr[day][series][date]:
                    for location in train_entries_dict_with_nr[day][series][date][nr]:
                        for entry in train_entries_dict_with_nr[day][series][date][nr][location]:
                            crossing = entry[18]
                            if(crossing["delay"][0] == ""):
                                crossing["delay"] = (0,False)
                                crossing_series[crossing_series_list.index(series)]["array"].append(0)
                            else:
                                crossing_series[crossing_series_list.index(series)]["array"].append(crossing["delay"][0])
                            if(entry[19] in transformed_entries_dict):
                                crossing = entry[18]
                                transformed_entries_dict[entry[19]].append(crossing)
                            else:
                                transformed_entries_dict[entry[19]] = entry[0:-1]

    del(train_entries_dict_with_nr)

    # Transform all entries with no crossing series back to the original entry form
    for entry in entries_with_no_crossings:
        transformed_entries_dict[entry[18]] = entry[0:-1]

    del(entries_with_no_crossings)

    # Fill all remaining gaps in the "array" key in crossing_series_list with zero for correct normalization
    for series in crossing_series:
        remaining = len(transformed_entries_dict) - len(series["array"])
        for i in range(remaining):
            series["array"].append(0)

    print("Write dataset to file")

    # Make file to write to
    if(not validation):
        file_name = "C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Datasets\\TrainDataset" + str(trainseries) + \
                    "_Category-" + category + "_Normalization-" + str(normalization) + "_OneHotEncoding-" + str(one_hot_encoding) + "_Model-Hard.txt"
        dataset = open(file_name, "w")

    else:
        file_name = "C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Datasets\\ValidationDataset" + str(trainseries) + \
                    "_Category-" + category + "_Normalization-" + str(normalization) + "_OneHotEncoding-" + str(one_hot_encoding) + "_Model-Hard.txt"
        dataset = open(file_name, "w")

    # Calculate parameters for the optional normalization and write them to file (also needed for validation/testing)
    if(not validation):
        normalization_columns = []
        mean = np.mean(current_delay_array)
        normalization_columns.append(mean)
        std = np.std(current_delay_array)
        normalization_columns.append(std)
        previous_mean = np.mean(previous_delay_array)
        normalization_columns.append(previous_mean)
        previous_std = np.std(previous_delay_array)
        normalization_columns.append(previous_std)
        previous_mean2 = np.mean(previous_delay2_array)
        normalization_columns.append(previous_mean2)
        previous_std2 = np.std(previous_delay2_array)
        normalization_columns.append(previous_std2)
        parameters = "Normalization parameters:" + str(mean) + "," + str(std) + "," + str(previous_mean) + "," + \
                      str(previous_std) + "," + str(previous_mean2) + "," + str(previous_std2) + ","
        for index,cross_series in enumerate(crossing_series):
            cross_mean = np.mean(cross_series["array"])
            normalization_columns.append(cross_mean)
            cross_std = np.std(cross_series["array"])
            normalization_columns.append(cross_std)
            parameters = parameters + str(cross_mean) + "," + str(cross_std)
            if(not(index == len(crossing_series)-1)):
                parameters = parameters + ","
        parameters = parameters + "\n"
        dataset.write(parameters)
    elif(normalization and validation):
        train_dataset = open(dataset.name.replace("Validation","Train"),"r")
        normalization_line = train_dataset.readline()
        normalization_columns = normalization_line.split(":")[1].split(",")
        train_dataset.close()

    title = "Day,Hour,Minutes,Direction,Location,Same_train,Driver_switch,Composition_change,"
    for cross_series in crossing_series:
        title = title + cross_series["series"] + ","
    title = title + "Previous_delay2,Previous_delay,Delay,Future_Delay\n"
    dataset.write(title)

    # Write all entries to the dataset file
    for num in transformed_entries_dict:
        entry = transformed_entries_dict[num]
        train_nr = entry[0]
        day = entry[3]
        hour = entry[4]
        minutes = entry[5]
        direction = entry[7]
        location = entry[8]
        future_delay = float(entry[9])
        same_train = entry[10]
        delay = float(entry[13])
        previous_delay = float(entry[14])
        previous_delay2 = float(entry[15])
        driver_switch = entry[16]
        composition_change = entry[17]

        # Ceil every delay under zero (so a train that is too early) to zero
        if(delay < 0):
            delay = 0.0
        if(future_delay < 0):
            future_delay = 0.0
        if(previous_delay < 0):
            previous_delay = 0.0
        if(previous_delay2 < 0):
            previous_delay2 = 0.0

        # # Normalize current delay with standardization
        if(normalization):
            hour = hour/23
            minutes = minutes/59
            delay = (delay - float(normalization_columns[0]))/float(normalization_columns[1])
            previous_delay = (previous_delay - float(normalization_columns[2]))/float(normalization_columns[3])
            previous_delay2 = (previous_delay2 - float(normalization_columns[4]))/float(normalization_columns[5])

        # Transform location as it is a categorical variable
        if (location in locations_list):
            if (one_hot_encoding):
                location = transform_to_one_hot_encoding(locations_list, location, False)
            else:
                location = location_encoder.transform(np.array([location]))[0]
        # If location in validatation/test set did not occur in train set, give either all zeros for one hot, or just -1
        else:
            if (one_hot_encoding):
                location = [0] * len(locations_list)
            else:
                location = -1

        # Change the future delay to match the problem (classification/regression)
        if(category == 'Regression'):
            if(one_hot_encoding):
                written_entry = str(day)[1:-1].replace(" ", "") + "," + str(hour) + "," + str(minutes) + "," + str(direction) \
                                + "," + str(location)[1:-1].replace(" ", "") + "," + str(same_train) + "," + str(driver_switch) \
                                + "," + str(composition_change) + ","
                found_series = {}
                if(len(entry)>18):
                    for i in range(18,len(entry)):
                        crossing = entry[i]
                        found_series[crossing["series"]] = crossing["delay"][0]

                for index,series in enumerate(crossing_series):
                    if(series["series"] in found_series):
                         crossing_delay = found_series[series["series"]]
                    else:
                        crossing_delay = 0
                    if(normalization):
                        if(not(float(normalization_columns[(2 * (index + 3)) + 1]) == 0)):
                            crossing_delay = (crossing_delay - float(normalization_columns[(2 * (index + 3))])) / float(
                                normalization_columns[(2 * (index + 3)) + 1])
                        else:
                            crossing_delay = -1
                    written_entry = written_entry + str(crossing_delay) + ","

                written_entry = written_entry + str(previous_delay2) + "," + str(previous_delay) + "," + \
                                str(delay) + "," + str(future_delay)
                dataset.write(written_entry)

            else:
                written_entry = str(day) + "," + str(hour) + "," + str(minutes) + "," + str(direction) + "," + \
                                str(location) + "," + str(same_train) + "," + str(driver_switch) + "," + \
                                str(composition_change) + ","
                found_series = {}
                if (len(entry) > 18):
                    for i in range(18, len(entry)):
                        crossing = entry[i]
                        found_series[crossing["series"]] = crossing["delay"][0]

                for index,series in enumerate(crossing_series):
                    if(series["series"] in found_series):
                         crossing_delay = found_series[series["series"]]
                    else:
                        crossing_delay = 0
                    if(normalization):
                        if(not(float(normalization_columns[(2 * (index + 3)) + 1]) == 0)):
                            crossing_delay = (crossing_delay - float(normalization_columns[(2 * (index + 3))])) / float(
                                normalization_columns[(2 * (index + 3)) + 1])
                        else:
                            crossing_delay = -1
                    written_entry = written_entry + str(crossing_delay) + ","

                written_entry = written_entry + str(previous_delay2) + "," + str(previous_delay) + "," + \
                                str(delay) + "," + str(future_delay)
                dataset.write(written_entry)

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
                written_entry = str(day)[1:-1].replace(" ", "") + "," + str(hour) + "," + str(minutes) + "," + str(direction) \
                    + "," + str(location)[1:-1].replace(" ", "") + "," + str(same_train) + "," + str(driver_switch) \
                    + "," + str(composition_change) + ","
                found_series = {}
                if (len(entry) > 18):
                    for i in range(18, len(entry)):
                        crossing = entry[i]
                        found_series[crossing["series"]] = crossing["delay"][0]

                for index,series in enumerate(crossing_series):
                    if(series["series"] in found_series):
                         crossing_delay = found_series[series["series"]]
                    else:
                        crossing_delay = 0
                    if(normalization):
                        if(not(float(normalization_columns[(2 * (index + 3)) + 1]) == 0)):
                            crossing_delay = (crossing_delay - float(normalization_columns[(2 * (index + 3))])) / float(
                                normalization_columns[(2 * (index + 3)) + 1])
                        else:
                            crossing_delay = -1
                    written_entry = written_entry + str(crossing_delay) + ","

                written_entry = written_entry + str(previous_delay2) + "," + str(previous_delay) + \
                    "," + str(delay) + "," + str(future_category)[1:-1].replace(" ", "")
                dataset.write(written_entry)

            else:
                output_encoder.fit(category_list)
                future_category = output_encoder.transform(np.array([future_category]))[0]
                written_entry = str(day) + "," + str(hour) + "," + str(minutes) + "," + str(direction) \
                    + "," + str(location) + "," + str(same_train)+ "," + str(driver_switch) \
                    + "," + str(composition_change) + ","
                found_series = {}
                if (len(entry) > 18):
                    for i in range(18, len(entry)):
                        crossing = entry[i]
                        found_series[crossing["series"]] = crossing["delay"][0]

                for index,series in enumerate(crossing_series):
                    if(series["series"] in found_series):
                         crossing_delay = found_series[series["series"]]
                    else:
                        crossing_delay = 0
                    if(normalization):
                        if(not(float(normalization_columns[(2 * (index + 3)) + 1]) == 0)):
                            crossing_delay = (crossing_delay - float(normalization_columns[(2 * (index + 3))])) / float(
                                normalization_columns[(2 * (index + 3)) + 1])
                        else:
                            crossing_delay = -1
                    written_entry = written_entry + str(crossing_delay) + ","

                written_entry = written_entry + str(previous_delay2) \
                    + "," + str(previous_delay) + "," + str(delay) + "," + str(future_category)
                dataset.write(written_entry)

        elif(category == 'Jump'):
            if(abs(future_delay - delay) > 4):
                future_category = 1
            else:
                future_category = 0

            if(one_hot_encoding):
                written_entry = str(day)[1:-1].replace(" ", "") + "," + str(hour) + "," + str(minutes)+ "," + str(direction) \
                    + "," + str(location)[1:-1].replace(" ", "") + "," + str(same_train) + "," + str(driver_switch) \
                    + "," + str(composition_change) + ","
                found_series = {}
                if (len(entry) > 18):
                    for i in range(18, len(entry)):
                        crossing = entry[i]
                        found_series[crossing["series"]] = crossing["delay"][0]

                for index,series in enumerate(crossing_series):
                    if(series["series"] in found_series):
                         crossing_delay = found_series[series["series"]]
                    else:
                        crossing_delay = 0
                    if(normalization):
                        if(not(float(normalization_columns[(2 * (index + 3)) + 1]) == 0)):
                            crossing_delay = (crossing_delay - float(normalization_columns[(2 * (index + 3))])) / float(
                                normalization_columns[(2 * (index + 3)) + 1])
                        else:
                            crossing_delay = -1
                    written_entry = written_entry + str(crossing_delay) + ","

                written_entry = written_entry + str(previous_delay2) + "," + str(previous_delay) + \
                    "," + str(delay) + "," + str(future_category)
                dataset.write(written_entry)

            else:
                written_entry = str(day) + "," + str(hour) + "," + str(minutes)+ "," + str(direction) \
                    + "," + str(location) + "," + str(same_train) + "," + str(driver_switch) \
                    + "," + str(composition_change) + ","
                found_series = {}
                if (len(entry) > 18):
                    for i in range(18, len(entry)):
                        crossing = entry[i]
                        found_series[crossing["series"]] = crossing["delay"][0]

                for index,series in enumerate(crossing_series):
                    if(series["series"] in found_series):
                         crossing_delay = found_series[series["series"]]
                    else:
                        crossing_delay = 0
                    if(normalization):
                        if(not(float(normalization_columns[(2 * (index + 3)) + 1]) == 0)):
                            crossing_delay = (crossing_delay - float(normalization_columns[(2 * (index + 3))])) / float(
                                normalization_columns[(2 * (index + 3)) + 1])
                        else:
                            crossing_delay = -1
                    written_entry = written_entry + str(crossing_delay) + ","

                written_entry = written_entry + str(previous_delay2) \
                    + "," + str(previous_delay) + "," + str(delay) + "," + str(future_category)
                dataset.write(written_entry)
        else:
            print("No choice was made in the parameters which form the output should have, please do so")
            exit()

        dataset.write("\n")

    # Close all files
    realisation_data.close()
    dataset.close()

# Generate test feature set
def generate_testset(testset_path, to_predict_path, connections_path, trainseries_locations_path, composition_change_path,
                            driver_change_path, route_path, timetable_path, trainseries, category, validation=False,
                            normalization=True, one_hot_encoding=False):
    # Open file to read from
    testset_data = open(testset_path, "r")

    # Create list for every possible train number 1-99 to append entries to
    train_nr_entries = [ [] for j in range(100)]

    # Initialize vector to save all current delays (needed if normalization is on)
    current_delay_array = []
    previous_delay_array = []
    previous_delay2_array = []

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

    # Determine which entries have to be predicted from the testset (only the ones around 8:20, 12:20 and 16:20 in this case)
    to_predict = {}
    predict_data = open(to_predict_path, "r")
    for predict_line in predict_data:
        predict_columns = predict_line.split(",")
        predict_series = predict_columns[1][0:-2] + "00"
        if(predict_series == str(trainseries)):
            predict_nr = predict_columns[1]
            predict_loc = predict_columns[2]
            predict_time = predict_columns[4]
            if(predict_nr in to_predict):
                if(predict_time in to_predict[predict_nr]):
                    to_predict[predict_nr][predict_time].append(predict_loc)
                else:
                    to_predict[predict_nr][predict_time] = [predict_loc]
            else:
                to_predict[predict_nr] = {}
                to_predict[predict_nr][predict_time] = [predict_loc]
    predict_data.close()

    print("Realisation data first iteration")

    # Read from realisation data and collect data from right trainseries
    previous_nr = 0
    for line in testset_data:
        line = line.replace('"', '')
        columns = line.split(",")
        series = columns[1]
        train_nr = int(columns[3])

        # Check if the read line belongs to the right trainseries or a variation of that trainseries (when under construction)
        if ((str(trainseries) == series[0:-1]) or
                (len(series) == 7 and int(series[0:-1]) < 400000 and (5 - len(str(trainseries))) * "0" + str(
                    trainseries) == series[1:6])):
            date = columns[0]
            weekday = calculate_weekday(date)
            # Transform day as it is a categorical variable
            if (one_hot_encoding):
                day = transform_to_one_hot_encoding([1, 2, 3, 4, 5], weekday, False)
            else:
                day = weekday
            time = columns[6][11::]
            hour = int(time[0:2])
            minutes = int(time[3:5])
            if (hour >= 0 and hour < 4):
                future_time = timedelta(days=1, hours=hour, minutes=minutes)
            else:
                future_time = timedelta(days=0, hours=hour, minutes=minutes)
            # Save the begin time of a train number to be able to say if 20 minutes back is the same train
            if (not (train_nr == previous_nr)):
                if (hour >= 0 and hour < 4):
                    begin_time = timedelta(days=1, hours=hour, minutes=minutes)
                else:
                    begin_time = timedelta(days=0, hours=hour, minutes=minutes)

            location = columns[4]

            if (str(train_nr) in to_predict and time in to_predict[str(train_nr)] and location in
                    to_predict[str(train_nr)][time]):
                direction = series[-1]
                if (direction == "E"):
                    direction = 1
                else:
                    direction = -1

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
    testset_data.close()

    # Open file to read connections for trains that had a begin time of less than 20 minutes
    connection_data = open(connections_path,"r")

    # Create dictionary of train numbers that have a connection
    train_cons = defaultdict(list)

    print("Connection data")

    # Add connection train number to each dictionary entry if it is the right trainseries and the day is correct
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

    # For each train with same_train is -1 that was not found in the connection file, add zero as connection and zero
    # as initial location and delay, previous delay and second previous delay. -1 can also be added for driver switch
    # and composition change
    for nr in train_nr_entries:
        if(nr):
            for entry in nr:
                if(not(len(entry) == 12)):
                    entry.append(0)
                    entry.append("Unknown")
                    entry.append(0)
                    entry.append(0)
                    entry.append(0)
                    current_delay_array.append(0)
                    previous_delay_array.append(0)
                    previous_delay2_array.append(0)
                    entry.append(-1)
                    entry.append(-1)

    print("Realisation data second iteration")

    # Open realisation data again to look for the delay 20 minutes in the past
    realisation_data = open(testset_path, "r")
    previous_delay = {"delay": 0, "nr": 0, "loc":""}
    previous_delay2 = {"delay": 0, "nr": 0, "loc":""}
    previous_delay3 = {"delay": 0, "nr": 0, "loc":""}
    for line in realisation_data:
        line = line.replace('"', '')
        columns = line.split(",")
        current_date = columns[0]
        current_series = columns[1]
        current_train_nr = int(columns[3])
        current_location = columns[4]
        current_delay = float(columns[8])

        # If the current trainseries is the same as trainseries we are looking for
        if((str(trainseries) == current_series[0:-1]) or
                (len(current_series) == 7 and int(current_series[0:-1]) < 400000 and
                 (5-len(str(trainseries)))*"0"+str(trainseries) == current_series[1:6])):
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
                    future_location = entry[8]

                    # If we crossed the time we are looking for by one entry
                    if(((future_time - timedelta(minutes=20)) < current_time) and (len(entry) == 12)):
                        # Add current location
                        entry.append(previous_delay["loc"])
                        # Add delay from 20 minutes back
                        delay = previous_delay["delay"]
                        entry.append(delay)
                        current_delay_array.append(delay)
                        # Add the delay before that if it is within this train number
                        if(previous_delay2["nr"] == current_train_nr):
                            entry.append(previous_delay2["delay"])
                            previous_delay_array.append(previous_delay2["delay"])
                        else:
                            entry.append(0)
                            previous_delay_array.append(0)
                        # Also add the second previous delay if it is within this train number
                        if(previous_delay3["nr"] == current_train_nr):
                            entry.append(previous_delay3["delay"])
                            previous_delay2_array.append(previous_delay3["delay"])
                        else:
                            entry.append(0)
                            previous_delay2_array.append(0)

                    # If this is exactly 20 minutes back
                    elif(((future_time - timedelta(minutes=20)) == current_time) and (len(entry) == 12)):
                        # Add current location
                        entry.append(current_location)
                        # Add delay from 20 minutes back
                        delay = current_delay
                        entry.append(delay)
                        current_delay_array.append(delay)
                        # Add the delay before that if it is within this train number
                        if(previous_delay["nr"] == current_train_nr):
                            entry.append(previous_delay["delay"])
                            previous_delay_array.append(previous_delay["delay"])
                        else:
                            entry.append(0)
                            previous_delay_array.append(0)
                        # Also add the second previous delay if it is within this train number
                        if(previous_delay2["nr"] == current_train_nr):
                            entry.append(previous_delay2["delay"])
                            previous_delay2_array.append(previous_delay2["delay"])
                        else:
                            entry.append(0)
                            previous_delay2_array.append(0)

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
                    future_location = entry[8]
                    future_nr = entry[0]

                    # If we crossed the time we are looking for by one entry
                    if (((future_time - timedelta(minutes=20)) < current_time) and (len(entry) == 12)):
                        # Add current location
                        entry.append(previous_delay["loc"])
                        # Add delay from 20 minutes back
                        delay = previous_delay["delay"]
                        entry.append(delay)
                        current_delay_array.append(delay)
                        # Add the delay before that if it is within this train number
                        if (previous_delay2["nr"] == current_train_nr):
                            entry.append(previous_delay2["delay"])
                            previous_delay_array.append(previous_delay2["delay"])
                        else:
                            entry.append(0)
                            previous_delay_array.append(0)
                        # Also add the second previous delay if it is within this train number
                        if (previous_delay3["nr"] == current_train_nr):
                            entry.append(previous_delay3["delay"])
                            previous_delay2_array.append(previous_delay3["delay"])
                        else:
                            entry.append(0)
                            previous_delay2_array.append(0)

                    # If this is exactly 20 minutes back
                    elif (((future_time - timedelta(minutes=20)) == current_time) and (len(entry) == 12)):
                        # Add current location
                        entry.append(current_location)
                        # Add delay from 20 minutes back
                        delay = current_delay
                        entry.append(delay)
                        current_delay_array.append(delay)
                        # Add the delay before that if it is within this train number
                        if (previous_delay["nr"] == current_train_nr):
                            entry.append(previous_delay["delay"])
                            previous_delay_array.append(previous_delay["delay"])
                        else:
                            entry.append(0)
                            previous_delay_array.append(0)
                        # Also add the second previous delay if it is within this train number
                        if (previous_delay2["nr"] == current_train_nr):
                            entry.append(previous_delay2["delay"])
                            previous_delay2_array.append(previous_delay2["delay"])
                        else:
                            entry.append(0)
                            previous_delay2_array.append(0)

        # If the previous number was the connection of the trainnumber but the last data was more than 20 minutes back
        elif(previous_nr in train_cons.keys() and not(previous_nr == current_train_nr)):
            for entry in train_nr_entries[train_cons[previous_nr] % 100]:
                if (current_date == entry[1] and entry[10] == -1 and entry[11] == previous_nr and len(entry) == 12):
                    future_location = entry[8]
                    future_nr = entry[0]
                    # Add current location
                    entry.append(previous_delay["loc"])
                    # Add delay from 20 minutes back
                    delay = previous_delay["delay"]
                    entry.append(delay)
                    current_delay_array.append(delay)
                    # Add the delay before that if it is within this train number
                    if (previous_delay2["nr"] == previous_nr):
                        entry.append(previous_delay2["delay"])
                        previous_delay_array.append(previous_delay2["delay"])
                    else:
                        entry.append(0)
                        previous_delay_array.append(0)
                    # Also add the second previous delay if it is within this train number
                    if (previous_delay3["nr"] == previous_nr):
                        entry.append(previous_delay3["delay"])
                        previous_delay2_array.append(previous_delay3["delay"])
                    else:
                        entry.append(0)
                        previous_delay2_array.append(0)

        # Remember the previous delay and number
        previous_delay3 = previous_delay2
        previous_delay2 = previous_delay
        previous_delay = {"delay":current_delay, "nr":current_train_nr, "loc":current_location}
        previous_nr = current_train_nr

    realisation_data.close()
    del(train_cons)

    print("Fill the features driver_switch and composition_change")

    # Determine if driver_switch is true for every entry
    driver_data = open(driver_change_path, "r")
    for driver_line in driver_data:
        driver_columns = driver_line.replace("\n","").split(" ")
        if (not (driver_columns[3] == "-")):
            switch_nr = driver_columns[3]
            switch_series = switch_nr[:-2] + "00"
            if ((str(trainseries) == switch_series) or
                    (len(switch_series) == 6 and int(switch_series) < 400000 and
                     (5 - len(str(trainseries))) * "0" + str(trainseries) == switch_series[1:6])):
                switch_location = driver_columns[4]
                switch_day = int(driver_columns[5])
                for entry in train_nr_entries[int(switch_nr) % 100]:
                    if(switch_day == entry[2] and len(entry) == 16):
                        if (entry[7] == 1):
                            route = route_E
                        else:
                            route = route_O
                        if(entry[10] == 1):
                            if ((entry[12] in route) and (entry[8] in route)):
                                if (switch_location in route[route.index(entry[12]):route.index(entry[8])]):
                                    entry.append(1)
                        if(entry[10] == -1):
                            if (entry[8] in route):
                                if (switch_location in route[:route.index(entry[8])]):
                                    entry.append(1)

    # For all entries check if the driver switch feature has been added, else add -1.
    for nr in train_nr_entries:
        if (nr):
            for entry in nr:
                if (len(entry) == 16):
                    entry.append(-1)

    # Determine if composition_change is true for every entry
    composition_data = open(composition_change_path, "r")
    for comp_line in composition_data:
        comp_columns = comp_line.replace("\n","").split("\t")
        change_nr = comp_columns[2]
        change_series = change_nr[:-2] + "00"
        if ((str(trainseries) == change_series) or
                (len(change_series) == 6 and int(change_series) < 400000 and
                 (5 - len(str(trainseries))) * "0" + str(trainseries) == change_series[1:6])):
            change_location = comp_columns[0]
            change_day = int(comp_columns[1])
            for entry in train_nr_entries[int(change_nr) % 100]:
                if (change_day == entry[2] and len(entry) == 17):
                    if (entry[7] == 1):
                        route = route_E
                    else:
                        route = route_O
                    if (entry[10] == 1):
                        if ((entry[12] in route) and (entry[8] in route)):
                            if (change_location in route[route.index(entry[12]):route.index(entry[8])]):
                                entry.append(1)
                    elif (entry[10] == -1):
                        if (entry[8] in route):
                            if (change_location in route[:route.index(entry[8])]):
                                entry.append(1)

    # For all entries check if there is a initial delay, else add 0 for initial location and delay, previous and
    # second previous delay. -1 can also be added for composition change
    for nr in train_nr_entries:
        if (nr):
            for entry in nr:
                if (len(entry) == 12):
                    entry.append("Unknown")
                    entry.append(0)
                    entry.append(0)
                    entry.append(0)
                    current_delay_array.append(0)
                    previous_delay_array.append(0)
                    previous_delay2_array.append(0)
                    entry.append(-1)
                    entry.append(-1)
                elif (len(entry) == 17):
                    entry.append(-1)

    print("Fill relevant delays of other trains that cross the route of the current trainseries")

    # Find trainseries that have one or more overlapping locations in the route (intersection of route_O and route_E)
    crossing_series = []
    crossing_series_list = []
    main_locations = list(set(route_O).intersection(set(route_E)))
    route_data = open(route_path, "r")
    for route_line in route_data:
        route_columns = route_line.replace("\n","").split(":")
        route_locations = route_columns[1].split(",")
        if(not(route_columns[0] == (str(trainseries) + "O")) and not(route_columns[0] == (str(trainseries) + "E"))):
            if(len(set(main_locations).intersection(set(route_locations))) > 0):
                crossing_series.append({"series":route_columns[0],"locations":route_locations,"array":[]})
                crossing_series_list.append(route_columns[0])
    route_data.close()

    # For each entry, find best location for each overlapping trainseries to save delay from
    for nr in train_nr_entries:
        if (nr):
            for entry in nr:
                if(entry[10] == 1):
                    for series in crossing_series:
                        found = False
                        current_location = entry[12]
                        if(current_location in series["locations"]):
                            entry.append({"series": series["series"], "loc": current_location, "time": "", "nr": ("",False), "delay": ("",False)})
                            found = True
                        else:
                            if (entry[7] == 1):
                                route = route_E
                            else:
                                route = route_O
                            future_location = entry[8]
                            if(route.__contains__(current_location)):
                                index_begin = route.index(current_location)
                            else:
                                index_begin = 0
                            if (route.__contains__(future_location)):
                                index_end = route.index(future_location)
                            else:
                                index_end = len(route)-1

                            for i in range(index_begin+1,index_end+1):
                                if((route[i] in series["locations"]) and not found):
                                    entry.append({"series": series["series"], "loc": route[i], "time": "", "nr": ("",False), "delay": ("",False)})
                                    found = True
                else:
                    for series in crossing_series:
                        found = False
                        if (entry[7] == 1):
                            route = route_E
                        else:
                            route = route_O
                        future_location = entry[8]
                        if (route.__contains__(future_location)):
                            index_end = route.index(future_location)
                        else:
                            index_end = len(route) - 1
                        for i in range(0,index_end+1):
                            if((route[i] in series["locations"]) and not found):
                                entry.append({"series": series["series"], "loc": route[i], "time": "", "nr": ("",False), "delay": ("",False)})
                                found = True

    # Loop through planning and find time each entry crosses a location in which it is crossed
    timetable_data = open(timetable_path, "r")
    for timetable_line in timetable_data:
        timetable_line = timetable_line.replace('"', '')
        timetable_columns = timetable_line.split(",")
        timetable_nr = timetable_columns[1]
        timetable_series = timetable_nr[:-2] + "00"
        if ((str(trainseries) == timetable_series) or
                (len(timetable_series) == 6 and int(timetable_series) < 400000 and
                 (5 - len(str(trainseries))) * "0" + str(trainseries) == timetable_series[1:6])):
            timetable_location = timetable_columns[3]
            timetable_date = timetable_columns[0]
            timetable_day = calculate_weekday_timetable(timetable_date)
            timetable_direction = timetable_columns[2]
            for entry in train_nr_entries[int(timetable_nr) % 100]:
                current_day = entry[2]
                current_direction = entry[7]
                if (current_direction == 1):
                    current_direction = "E"
                else:
                    current_direction = "O"
                if(timetable_day == current_day and current_direction == timetable_direction):
                    for i in range(18,len(entry)):
                        crossing = entry[i]
                        if(crossing["loc"] == timetable_location):
                            if(not(timetable_columns[7] == '')):
                                timetable_hours = int(timetable_columns[7][9:11])
                                timetable_minutes = int(timetable_columns[7][12:14])
                                if(timetable_hours >= 0 and timetable_hours < 4):
                                    crossing["time"] = timedelta(days=1, hours=timetable_hours, minutes=timetable_minutes)
                                else:
                                    crossing["time"] = timedelta(days=0,hours=timetable_hours,minutes=timetable_minutes)
    timetable_data.close()

    # Fill all entries where there are crossing trains with relevant=1, but no time, this means it was not found in the timetable
    for nr in train_nr_entries:
        if (nr):
            for entry in nr:
                if(len(entry) > 18):
                    remove_list = []
                    for i in range(18, len(entry)):
                        crossing = entry[i]
                        if (crossing["time"] == ""):
                            remove_list.append(i)
                    remove_list.reverse()
                    for remove in remove_list:
                        entry.__delitem__(remove)

    # Reshape the entry list to be able to search on date and crossing to speed up computation
    date_dict = {}
    for nr in train_nr_entries:
        if (nr):
            for entry in nr:
                entry_date = entry[1]
                if(not(entry_date in date_dict)):
                    date_dict[entry_date] = ""

    crossing_dict = {}
    for series in crossing_series:
        location_dict = {}
        for location in series["locations"]:
            location_dict[location] = []
        for date in date_dict:
            date_dict[date] = copy.deepcopy(location_dict)
        crossing_dict[series["series"]] = copy.deepcopy(date_dict)

    train_entries_dict = {1:copy.deepcopy(crossing_dict), 2:copy.deepcopy(crossing_dict), 3:copy.deepcopy(crossing_dict), 4:copy.deepcopy(crossing_dict), 5:copy.deepcopy(crossing_dict)}
    entries_with_no_crossings = []
    tracking_number = 0 # number to know which dictionary entries belong to the same original entry
    for nr in train_nr_entries:
        if (nr):
            for entry in nr:
                if(len(entry) > 18):
                    entry_date = entry[1]
                    entry_day = calculate_weekday(entry_date)
                    for i in range(18, len(entry)):
                        new_entry = entry[0:18]
                        crossing = entry[i]
                        series = crossing["series"]
                        crossing_loc = crossing["loc"]
                        new_entry.append(crossing)
                        new_entry.append(tracking_number)
                        train_entries_dict[entry_day][series][entry_date][crossing_loc].append(new_entry)
                else:
                    new_entry = entry[0:18]
                    new_entry.append(tracking_number)
                    entries_with_no_crossings.append(new_entry)
                tracking_number = tracking_number + 1

    del(train_nr_entries)

    # Loop through planning to find the most suitable trainnumber per crossing series with the found times
    timetable_data = open(timetable_path, "r")
    for timetable_line in timetable_data:
        timetable_line = timetable_line.replace('"', '')
        timetable_columns = timetable_line.split(",")
        if (not (timetable_columns[7] == '')):
            timetable_date = timetable_columns[0]
            timetable_nr = timetable_columns[1]
            timetable_direction = timetable_columns[2]
            timetable_location = timetable_columns[3]
            timetable_day = calculate_weekday_timetable(timetable_date)
            timetable_series = timetable_nr[:-2] + "00" + timetable_direction
            if(timetable_series in crossing_series_list):
                normal_series = timetable_series
                relevant_entries_dict = train_entries_dict[timetable_day][normal_series]
            elif(len(timetable_series) == 7 and int(timetable_series[0:-1]) < 400000):
                normal_series = 0
                if(timetable_series[0:3] == "100" or timetable_series[0:3] == "200" or timetable_series[0:3] == "300"):
                    normal_series = timetable_series[3:]
                elif(timetable_series[0:2] == "10" or timetable_series[0:2] == "20" or timetable_series[0:2] == "30"):
                    normal_series = timetable_series[2:]
                elif(timetable_series[0:1] == "1" or timetable_series[0:1] == "2" or timetable_series[0:1] == "3"):
                    normal_series = timetable_series[1:]
                if(not(normal_series == 0) and normal_series in crossing_series_list):
                    relevant_entries_dict = train_entries_dict[timetable_day][normal_series]
                else:
                    continue
            else:
                continue

            if(timetable_location in crossing_series[crossing_series_list.index(normal_series)]["locations"]):
                timetable_hours = int(timetable_columns[7][9:11])
                timetable_minutes = int(timetable_columns[7][12:14])
                if (timetable_hours >= 0 and timetable_hours < 4):
                    timetable_time = timedelta(days=1, hours=timetable_hours, minutes=timetable_minutes)
                else:
                    timetable_time = timedelta(days=0, hours=timetable_hours, minutes=timetable_minutes)

                for date in relevant_entries_dict:
                    relevant_entries = relevant_entries_dict[date][timetable_location]
                    for entry in relevant_entries:
                        crossing = entry[18]
                        if (crossing["nr"][1] == False):
                            if (timetable_time <= crossing["time"]):
                                crossing["nr"] = (timetable_nr, False)
                            elif (timetable_time > crossing["time"]):
                                crossing["nr"] = (crossing["nr"][0], True)
            else:
                continue

    timetable_data.close()

    # Reshape the entry dictionary to be able to add the previously found number to speed up computation
    train_entries_dict_with_nr = copy.deepcopy(train_entries_dict)
    for weekday in train_entries_dict:
        for series in train_entries_dict[weekday]:
            for date in train_entries_dict[weekday][series]:
                train_entries_dict_with_nr[weekday][series][date] = {}
                for index in range(100):
                    train_entries_dict_with_nr[weekday][series][date][index] = {}
                for loc in train_entries_dict[weekday][series][date]:
                    for entry in train_entries_dict[weekday][series][date][loc]:
                        nr = entry[18]["nr"][0]
                        if(nr == ""): #Save entries with no crossing in number 0 as this a train number will never be 0
                            if(loc in train_entries_dict_with_nr[weekday][series][date][0]):
                                train_entries_dict_with_nr[weekday][series][date][0][loc].append(entry)
                            else:
                                train_entries_dict_with_nr[weekday][series][date][0][loc] = []
                                train_entries_dict_with_nr[weekday][series][date][0][loc].append(entry)
                        else:
                            if(loc in train_entries_dict_with_nr[weekday][series][date][int(nr)%100]):
                                train_entries_dict_with_nr[weekday][series][date][int(nr)%100][loc].append(entry)
                            else:
                                train_entries_dict_with_nr[weekday][series][date][int(nr)%100][loc] = []
                                train_entries_dict_with_nr[weekday][series][date][int(nr)%100][loc].append(entry)

    del(train_entries_dict)

    # Loop through the realisation data to find the delays of the found trainnumbers per crossing series
    testset_data = open(testset_path, "r")
    for line in testset_data:
        line = line.replace('"', '')
        columns = line.split(",")
        date = columns[0]
        series = columns[1]
        train_nr = int(columns[3])%100
        weekday = calculate_weekday(date)
        if (series in crossing_series_list):
            normal_series = series
            if(train_nr in train_entries_dict_with_nr[weekday][normal_series][date]):
                relevant_entries_dict = train_entries_dict_with_nr[weekday][normal_series][date][train_nr]
            else:
                continue
        elif (len(series) == 7 and int(series[0:-1]) < 400000):
            normal_series = 0
            if (series[0:3] == "100" or series[0:3] == "200" or series[0:3] == "300"):
                normal_series = series[3:]
            elif (series[0:2] == "10" or series[0:2] == "20" or series[0:2] == "30"):
                normal_series = series[2:]
            elif (series[0:1] == "1" or series[0:1] == "2" or series[0:1] == "3"):
                normal_series = series[1:]
            if (not (normal_series == 0) and normal_series in crossing_series_list):
                if (train_nr in train_entries_dict_with_nr[weekday][normal_series][date]):
                    relevant_entries_dict = train_entries_dict_with_nr[weekday][normal_series][date][train_nr]
                else:
                    continue
            else:
                continue
        else:
            continue

        hours = int(columns[7][11:13])
        minutes = int(columns[7][14:16])
        if (hours >= 0 and hours < 4):
            time = timedelta(days=1, hours=hours, minutes=minutes)
        else:
            time = timedelta(days=0, hours=hours, minutes=minutes)

        for location in relevant_entries_dict:
            relevant_entries = relevant_entries_dict[location]
            for entry in relevant_entries:
                entry_hours = entry[4]
                entry_minutes = entry[5]
                if (entry_hours >= 0 and entry_hours < 4):
                    entry_time = timedelta(days=1, hours=entry_hours, minutes=entry_minutes)
                else:
                    entry_time = timedelta(days=0, hours=entry_hours, minutes=entry_minutes)
                crossing = entry[18]
                if (crossing["delay"][1] == False):
                    if (time < entry_time):
                        crossing_delay = int(columns[8])
                        if (crossing_delay < 0):
                            crossing_delay = 0
                        crossing["delay"] = (crossing_delay, False)
                    elif (time >= entry_time):
                        crossing["delay"] = (crossing["delay"][0], True)
    realisation_data.close()

    # Transform all crossing entries back to their original entry form and fill all delays that have not been filled with 0
    transformed_entries_dict = {}
    for day in train_entries_dict_with_nr:
        for series in train_entries_dict_with_nr[day]:
            for date in train_entries_dict_with_nr[day][series]:
                for nr in train_entries_dict_with_nr[day][series][date]:
                    for location in train_entries_dict_with_nr[day][series][date][nr]:
                        for entry in train_entries_dict_with_nr[day][series][date][nr][location]:
                            crossing = entry[18]
                            if(crossing["delay"][0] == ""):
                                crossing["delay"] = (0,False)
                                crossing_series[crossing_series_list.index(series)]["array"].append(0)
                            else:
                                crossing_series[crossing_series_list.index(series)]["array"].append(crossing["delay"][0])
                            if(entry[19] in transformed_entries_dict):
                                crossing = entry[18]
                                transformed_entries_dict[entry[19]].append(crossing)
                            else:
                                transformed_entries_dict[entry[19]] = entry[0:-1]

    del(train_entries_dict_with_nr)

    # Transform all entries with no crossing series back to the original entry form
    for entry in entries_with_no_crossings:
        transformed_entries_dict[entry[18]] = entry[0:-1]

    del(entries_with_no_crossings)

    # Fill all remaining gaps in the "array" key in crossing_series_list with zero for correct normalization
    for series in crossing_series:
        remaining = len(transformed_entries_dict) - len(series["array"])
        for i in range(remaining):
            series["array"].append(0)

    print("Write dataset to file")

    # Make file to write to
    file_name = "C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Testsets\\TestDataset" + str(trainseries) + \
                "_Category-" + category + "_Normalization-" + str(normalization) + "_OneHotEncoding-" + str(one_hot_encoding) + "_Model-Hard.txt"
    dataset = open(file_name, "w")


    # Read normalization parameters if necessary
    if(normalization):
        train_dataset = open(dataset.name.replace("Testsets\\TestDataset","Datasets\\TrainDataset"),"r")
        normalization_line = train_dataset.readline()
        normalization_columns = normalization_line.split(":")[1].split(",")
        train_dataset.close()

    title = "Day,Hour,Minutes,Direction,Location,Same_train,Driver_switch,Composition_change,"
    for cross_series in crossing_series:
        title = title + cross_series["series"] + ","
    title = title + "Previous_delay2,Previous_delay,Delay,Future_Delay\n"
    dataset.write(title)

    # Write all entries to the dataset file
    for num in transformed_entries_dict:
        entry = transformed_entries_dict[num]
        train_nr = entry[0]
        day = entry[3]
        hour = entry[4]
        minutes = entry[5]
        direction = entry[7]
        location = entry[8]
        future_delay = float(entry[9])
        same_train = entry[10]
        delay = float(entry[13])
        previous_delay = float(entry[14])
        previous_delay2 = float(entry[15])
        driver_switch = entry[16]
        composition_change = entry[17]

        # Ceil every delay under zero (so a train that is too early) to zero
        if(delay < 0):
            delay = 0.0
        if(future_delay < 0):
            future_delay = 0.0
        if(previous_delay < 0):
            previous_delay = 0.0
        if(previous_delay2 < 0):
            previous_delay2 = 0.0

        # # Normalize current delay with standardization
        if(normalization):
            hour = hour/23
            minutes = minutes/59
            delay = (delay - float(normalization_columns[0]))/float(normalization_columns[1])
            previous_delay = (previous_delay - float(normalization_columns[2]))/float(normalization_columns[3])
            previous_delay2 = (previous_delay2 - float(normalization_columns[4]))/float(normalization_columns[5])

        # Transform location as it is a categorical variable
        if (location in locations_list):
            if (one_hot_encoding):
                location = transform_to_one_hot_encoding(locations_list, location, False)
            else:
                location = location_encoder.transform(np.array([location]))[0]
        # If location in validatation/test set did not occur in train set, give either all zeros for one hot, or just -1
        else:
            if (one_hot_encoding):
                location = [0] * len(locations_list)
            else:
                location = -1

        # Change the future delay to match the problem (classification/regression)
        if(category == 'Regression'):
            if(one_hot_encoding):
                written_entry = str(day)[1:-1].replace(" ", "") + "," + str(hour) + "," + str(minutes) + "," + str(direction) \
                                + "," + str(location)[1:-1].replace(" ", "") + "," + str(same_train) + "," + str(driver_switch) \
                                + "," + str(composition_change) + ","
                found_series = {}
                if(len(entry)>18):
                    for i in range(18,len(entry)):
                        crossing = entry[i]
                        found_series[crossing["series"]] = crossing["delay"][0]

                for index,series in enumerate(crossing_series):
                    if(series["series"] in found_series):
                         crossing_delay = found_series[series["series"]]
                    else:
                        crossing_delay = 0
                    if(normalization):
                        if(not(float(normalization_columns[(2 * (index + 3)) + 1]) == 0)):
                            crossing_delay = (crossing_delay - float(normalization_columns[(2 * (index + 3))])) / float(
                                normalization_columns[(2 * (index + 3)) + 1])
                        else:
                            crossing_delay = -1
                    written_entry = written_entry + str(crossing_delay) + ","

                written_entry = written_entry + str(previous_delay2) + "," + str(previous_delay) + "," + \
                                str(delay) + "," + str(future_delay)
                dataset.write(written_entry)

            else:
                written_entry = str(day) + "," + str(hour) + "," + str(minutes) + "," + str(direction) + "," + \
                                str(location) + "," + str(same_train) + "," + str(driver_switch) + "," + \
                                str(composition_change) + ","
                found_series = {}
                if (len(entry) > 18):
                    for i in range(18, len(entry)):
                        crossing = entry[i]
                        found_series[crossing["series"]] = crossing["delay"][0]

                for index,series in enumerate(crossing_series):
                    if(series["series"] in found_series):
                         crossing_delay = found_series[series["series"]]
                    else:
                        crossing_delay = 0
                    if(normalization):
                        if(not(float(normalization_columns[(2 * (index + 3)) + 1]) == 0)):
                            crossing_delay = (crossing_delay - float(normalization_columns[(2 * (index + 3))])) / float(
                                normalization_columns[(2 * (index + 3)) + 1])
                        else:
                            crossing_delay = -1
                    written_entry = written_entry + str(crossing_delay) + ","

                written_entry = written_entry + str(previous_delay2) + "," + str(previous_delay) + "," + \
                                str(delay) + "," + str(future_delay)
                dataset.write(written_entry)

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
                written_entry = str(day)[1:-1].replace(" ", "") + "," + str(hour) + "," + str(minutes) + "," + str(direction) \
                    + "," + str(location)[1:-1].replace(" ", "") + "," + str(same_train) + "," + str(driver_switch) \
                    + "," + str(composition_change) + ","
                found_series = {}
                if (len(entry) > 18):
                    for i in range(18, len(entry)):
                        crossing = entry[i]
                        found_series[crossing["series"]] = crossing["delay"][0]

                for index,series in enumerate(crossing_series):
                    if(series["series"] in found_series):
                         crossing_delay = found_series[series["series"]]
                    else:
                        crossing_delay = 0
                    if(normalization):
                        if(not(float(normalization_columns[(2 * (index + 3)) + 1]) == 0)):
                            crossing_delay = (crossing_delay - float(normalization_columns[(2 * (index + 3))])) / float(
                                normalization_columns[(2 * (index + 3)) + 1])
                        else:
                            crossing_delay = -1
                    written_entry = written_entry + str(crossing_delay) + ","

                written_entry = written_entry + str(previous_delay2) + "," + str(previous_delay) + \
                    "," + str(delay) + "," + str(future_category)[1:-1].replace(" ", "")
                dataset.write(written_entry)

            else:
                output_encoder.fit(category_list)
                future_category = output_encoder.transform(np.array([future_category]))[0]
                written_entry = str(day) + "," + str(hour) + "," + str(minutes) + "," + str(direction) \
                    + "," + str(location) + "," + str(same_train)+ "," + str(driver_switch) \
                    + "," + str(composition_change) + ","
                found_series = {}
                if (len(entry) > 18):
                    for i in range(18, len(entry)):
                        crossing = entry[i]
                        found_series[crossing["series"]] = crossing["delay"][0]

                for index,series in enumerate(crossing_series):
                    if(series["series"] in found_series):
                         crossing_delay = found_series[series["series"]]
                    else:
                        crossing_delay = 0
                    if(normalization):
                        if(not(float(normalization_columns[(2 * (index + 3)) + 1]) == 0)):
                            crossing_delay = (crossing_delay - float(normalization_columns[(2 * (index + 3))])) / float(
                                normalization_columns[(2 * (index + 3)) + 1])
                        else:
                            crossing_delay = -1
                    written_entry = written_entry + str(crossing_delay) + ","

                written_entry = written_entry + str(previous_delay2) \
                    + "," + str(previous_delay) + "," + str(delay) + "," + str(future_category)
                dataset.write(written_entry)

        elif(category == 'Jump'):
            if(abs(future_delay - delay) > 4):
                future_category = 1
            else:
                future_category = 0

            if(one_hot_encoding):
                written_entry = str(day)[1:-1].replace(" ", "") + "," + str(hour) + "," + str(minutes)+ "," + str(direction) \
                    + "," + str(location)[1:-1].replace(" ", "") + "," + str(same_train) + "," + str(driver_switch) \
                    + "," + str(composition_change) + ","
                found_series = {}
                if (len(entry) > 18):
                    for i in range(18, len(entry)):
                        crossing = entry[i]
                        found_series[crossing["series"]] = crossing["delay"][0]

                for index,series in enumerate(crossing_series):
                    if(series["series"] in found_series):
                         crossing_delay = found_series[series["series"]]
                    else:
                        crossing_delay = 0
                    if(normalization):
                        if(not(float(normalization_columns[(2 * (index + 3)) + 1]) == 0)):
                            crossing_delay = (crossing_delay - float(normalization_columns[(2 * (index + 3))])) / float(
                                normalization_columns[(2 * (index + 3)) + 1])
                        else:
                            crossing_delay = -1
                    written_entry = written_entry + str(crossing_delay) + ","

                written_entry = written_entry + str(previous_delay2) + "," + str(previous_delay) + \
                    "," + str(delay) + "," + str(future_category)
                dataset.write(written_entry)

            else:
                written_entry = str(day) + "," + str(hour) + "," + str(minutes)+ "," + str(direction) \
                    + "," + str(location) + "," + str(same_train) + "," + str(driver_switch) \
                    + "," + str(composition_change) + ","
                found_series = {}
                if (len(entry) > 18):
                    for i in range(18, len(entry)):
                        crossing = entry[i]
                        found_series[crossing["series"]] = crossing["delay"][0]

                for index,series in enumerate(crossing_series):
                    if(series["series"] in found_series):
                         crossing_delay = found_series[series["series"]]
                    else:
                        crossing_delay = 0
                    if(normalization):
                        if(not(float(normalization_columns[(2 * (index + 3)) + 1]) == 0)):
                            crossing_delay = (crossing_delay - float(normalization_columns[(2 * (index + 3))])) / float(
                                normalization_columns[(2 * (index + 3)) + 1])
                        else:
                            crossing_delay = -1
                    written_entry = written_entry + str(crossing_delay) + ","

                written_entry = written_entry + str(previous_delay2) \
                    + "," + str(previous_delay) + "," + str(delay) + "," + str(future_category)
                dataset.write(written_entry)
        else:
            print("No choice was made in the parameters which form the output should have, please do so")
            exit()

        dataset.write("\n")

    # Close all files
    realisation_data.close()
    dataset.close()