import csv

all_trainnumers = open(
    "C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Data_vertragingen\\AllTrainnumbersAndDirections.csv","r")
reader1 = csv.reader(all_trainnumers)
all_trainnumers_list = sum(list(reader1),[])

regular_trainnumers = open(
    "C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Data_vertragingen\\TreinnummersInRealisatie.csv","r")
reader1 = csv.reader(regular_trainnumers)
regular_trainnumers_list = list(set(sum(list(reader1),[])))

special_trainnumers = open(
    "C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Data_vertragingen\\VariatieTreinnummers.csv","r")
reader2 = csv.reader(special_trainnumers)
special_trainnumers_list = list(set(sum(list(reader2),[])))

input_list = []
for number in regular_trainnumers_list:
    if(number+"O" in all_trainnumers_list):
        input_list.append(number+"O")
    if(number + "E" in all_trainnumers_list):
        input_list.append(number + "E")

with open("C:\\Users\\Leonieke.vandenB_nsp\\OneDrive - NS\\Data_vertragingen\\TreinnummersVoorInput.csv", "w") as myfile:
    for number in input_list:
        myfile.write(number)
        myfile.write(",")

