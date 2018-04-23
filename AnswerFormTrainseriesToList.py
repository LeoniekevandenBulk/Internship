# Open file to read from
AnswerForm = open(
    "C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Evaluation\\ANSWER_FORM_LAYOUT.txt","r")

# Make file to write to
TrainseriesFile = open(
    "C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Data_vertragingen\\TrainseriesFromAnswerForm.txt","w")

trainseries_list = []
for line in AnswerForm.readlines():
    columns = line.split(",")
    trainnumber = columns[1]
    trainseries = trainnumber[:-2] + "00"
    if(trainseries not in trainseries_list):
        trainseries_list.append(trainseries)
        TrainseriesFile.write(trainseries + "\n")

# Close file
TrainseriesFile.close()
