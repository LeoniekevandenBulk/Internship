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

def generate_dataset(realisation_path,trainseries):



def generate_validationset(validation_path,trainseries):
    pass

def generate_testset(testdata_path, trainseries):
    pass

def get_databatch(dataset_path):
    pass

def get_testbatch(testset_path):
    pass