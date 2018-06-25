# Open files to read from
CompChanges = open(
    "C:\\Users\\Leonieke.vandenB_nsp\\Programming\\Data_vertragingen\\Data_RAS\\RollingStockCompositionChanges.txt","r")

# Make files to write to
CompChangesNew = open(
    "C:\\Users\\Leonieke.vandenB_nsp\\Programming\\Data_vertragingen\\Data_RAS\\RollingStockCompositionChangesSameTrain.txt","w")
ConnectionsNew = open(
    "C:\\Users\\Leonieke.vandenB_nsp\\Programming\\Data_vertragingen\\Data_RAS\\RollingStockConnectionsAll.txt","w")

previous_day = 0
CompChanges.readline()
for line in CompChanges.readlines():
    line = line.rstrip("\r\n")
    columns = line.split("\t")
    current_day = columns[1]
    if(not(current_day == previous_day)):
        Connections = open(
            'C:\\Users\\Leonieke.vandenB_nsp\\Programming\\Data_vertragingen\\Data_RAS\\RollingStockConnections.txt', "r")
        Connections.readline()
        for line2 in Connections.readlines():
            line2 = line2.rstrip("\r\n")
            columns2 = line2.split("\t")
            if(columns2[0] == current_day):
                ConnectionsNew.write(line2 + "\t" + "N" + "\n")

        Connections.close()
    if(columns[2] == columns[3]):
        CompChangesNew.write(columns[0] + "\t" + columns[1] + "\t" + columns[2] + "\n")
    else:
        ConnectionsNew.write(columns[1] + "\t" + columns[2] + "\t" + columns[0] + "\t" + columns[3] + "\t" + "Y" + "\n" )
    previous_day = current_day

# Close files
CompChanges.close()
CompChangesNew.close()
ConnectionsNew.close()