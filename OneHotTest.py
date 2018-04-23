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

a = ["hallo","hoi","doei","bye","cheers","deballen"]
print(one_hot_encoding(a,"deballen",False))




