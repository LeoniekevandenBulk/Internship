import numpy as np
import random

def get_databatch2(data, mean, std, batch_size=32, category='Regression', shuffle=True, normalization=True, augmentation=True, balance_batches=False):
    # Set label length for category
    if(category=='Change'):
        label_length = 3
    else:
        label_length = 1

    # A generator loop for the creation of batches
    while True:
        # Load data
        data_size = data.shape[0]
        line_size = data.shape[1]

        # Shuffle the data
        if(shuffle):
            data = np.random.permutation(data)

        i = 0
        while i < data_size:
            entry_batch = np.zeros((batch_size, line_size-label_length), dtype=np.float32)
            if(category=='Regression'):
                label_batch = np.zeros((batch_size, label_length), dtype=np.float32)
            else:
                label_batch = np.zeros((batch_size, label_length), dtype=np.uint8)

            if (category == 'Change'):
                label_count = [0, 0, 0] # One element for each of the change categories: decrease, equal, increase
            else:
                label_count = [0, 0]  # One element for delays of zero(regression) or no_jump (jump) and one for delays of bigger than zero(regression) or jump (jump)

            j = 0
            while j < batch_size:
                # Get the position modula data_size to prevent bacth size not lining up with the dataset size
                entry = data[i % data_size][0:-1*label_length]
                label = data[i % data_size][-1*label_length:]

                i += 1
                if(category=='Regression'):
                    if(label > 0):
                        label_category = 1
                    else:
                        label_category = 0
                elif(category=='Change'):
                    if(label[0] == 1):
                        label_category = 0
                    elif(label[1] == 1):
                        label_category = 1
                    else:
                        label_category = 2
                else:
                    if(label == 1):
                        label_category = 1
                    else:
                        label_category = 0

                if balance_batches and label_count[label_category] >= batch_size / len(label_count):
                    continue
                label_count[label_category] += 1

                # Augmentation by addding or subtracting one minute from the entries with a delay > 0
                if (category == 'Change'):
                    if(augmentation and (label_category == 0 or label_category == 2)):
                        plus_one = random.uniform(0,1)
                        minus_one = random.uniform(0,1)
                        if(plus_one <= 0.25):
                            entry[-1] += 1
                        if(minus_one <= 0.25 and not(entry[-1] == 1)):
                            entry[-1] -= 1
                else:
                    if(augmentation and label_category == 1):
                        plus_one = random.uniform(0,1)
                        minus_one = random.uniform(0,1)
                        if(plus_one <= 0.25):
                            entry[-1] += 1
                        if(minus_one <= 0.25 and not(entry[-1] == 1)):
                            entry[-1] -= 1

                # Add normalization on the fly as it otherwise interferes with the augmentation (assumes one-hot encoding)
                if(normalization):
                    entry[1] = entry[1]/23
                    entry[2] = entry[2]/59
                    for x in range(len(mean)):
                        entry[(x+1)*-1] = (entry[(x+1)*-1] -  mean[x]) / std[x]

                entry_batch[j] = entry
                label_batch[j] = label

                j += 1

            yield entry_batch, label_batch

def get_databatch(data, mean, std, batch_size=32, category='Regression', shuffle=True, normalization=True, augmentation=True, balance_batches=False):
    # Set label length for category
    if(category=='Change'):
        label_length = 3
    else:
        label_length = 1

    # A generator loop for the creation of batches
    while True:
        # Load data
        data_size = data.shape[0]
        line_size = data.shape[1]

        # Shuffle the data
        if(shuffle):
            data = np.random.permutation(data)

        i = 0
        while i < data_size:
            entry_batch = np.zeros((batch_size, line_size-label_length), dtype=np.float32)
            if(category=='Regression'):
                label_batch = np.zeros((batch_size, label_length), dtype=np.float32)
            else:
                label_batch = np.zeros((batch_size, label_length), dtype=np.uint8)

            if (category == 'Change'):
                label_count = [0, 0, 0] # One element for each of the change categories: decrease, equal, increase
            else:
                label_count = [0, 0]  # One element for delays of zero(regression) or no_jump (jump) and one for delays of bigger than zero(regression) or jump (jump)

            j = 0
            while j < batch_size:
                # Get the position modula data_size to prevent bacth size not lining up with the dataset size
                entry = data[i % data_size][0:-1*label_length]
                label = data[i % data_size][-1*label_length:]

                i += 1
                if(category=='Regression'):
                    if(label > 0):
                        label_category = 1
                    else:
                        label_category = 0
                elif(category=='Change'):
                    if(label[0] == 1):
                        label_category = 0
                    elif(label[1] == 1):
                        label_category = 1
                    else:
                        label_category = 2
                else:
                    if(label == 1):
                        label_category = 1
                    else:
                        label_category = 0

                if balance_batches and label_count[label_category] >= batch_size / len(label_count):
                    continue
                label_count[label_category] += 1

                # Augmentation by addding or subtracting one minute from the entries with a delay > 0
                if(augmentation):
                    plus_one = random.uniform(0,1)
                    minus_one = random.uniform(0,1)
                    if(plus_one <= 0.25):
                        entry[-1] += 1
                    if(minus_one <= 0.25 and not(entry[-1] == 1)):
                        entry[-1] -= 1

                # Add normalization on the fly as it otherwise interferes with the augmentation (assumes one-hot encoding)
                if(normalization):
                    entry[1] = entry[1]/23
                    entry[2] = entry[2]/59
                    for x in range(len(mean)):
                        entry[(x+1)*-1] = (entry[(x+1)*-1] -  mean[x]) / std[x]

                entry_batch[j] = entry
                label_batch[j] = label

                j += 1

            yield entry_batch, label_batch

def get_testbatch(data, mean, std, batch_size=32, category='Regression', normalization=True, augmentation=True):
    # A generator loop for the creation of batches
    while True:
        # Load data
        data_size = data.shape[0]
        line_size = data.shape[1]

        i = 0
        while i < data_size:
            entry_batch = np.zeros((batch_size, line_size), dtype=np.float32)
            j = 0
            for j in range(batch_size):
                # Get the position modula data_size to prevent bacth size not lining up with the dataset size
                entry = data[i % data_size]
                i += 1

                # Augmentation by addding or subtracting one minute from the entries with a delay > 0
                if(augmentation):
                    plus_one = random.uniform(0,1)
                    minus_one = random.uniform(0,1)
                    if(plus_one <= 0.25):
                        entry[-1] += 1
                    if(minus_one <= 0.25 and not(entry[-1] == 1)):
                        entry[-1] -= 1

                # Add normalization on the fly as it otherwise interferes with the augmentation (assumes one-hot encoding)
                if(normalization):
                    entry[1] = entry[1]/23
                    entry[2] = entry[2]/59
                    for x in range(len(mean)):
                        entry[(x+1)*-1] = (entry[(x+1)*-1] -  mean[x]) / std[x]

                entry_batch[j] = entry

            yield entry_batch