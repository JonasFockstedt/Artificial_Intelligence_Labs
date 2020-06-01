import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder

# TODO:
# Make estimate of opponent hand strength.
# This will hopefully be a good estimate of whether opponent will call of fold.

knn = KNeighborsClassifier()


# To remove commas between each attribute.
def removeCommas(data):
    the_list = []
    for line in data:
        the_list.append(line.split(' , '))

    return the_list


# To sort out empty strings that might occur at end of each row.
def removeEmptyString(the_list):
    for index, action in enumerate(the_list):
        # Check if the row has empty string at the end. Then replace.
        if action[-1] == '':
            the_list[index] = action[:-1]


# Determines the final action of player 2.
def extractPlayer2FinalActions(actions_list):
    p2_final_actions = []
    for index, action in enumerate(actions_list):
        # Split the last action of both players.
        splitted_string = action[-1].split()
        # If the length of the separated string is greater than 2,
        # then the final action of p2 is at index 2.
        if len(splitted_string) > 2:
            # Append p2 final action to list.
            p2_final_actions.append(splitted_string[2])

            # Extract p2 final action from original list.
            temp_string = splitted_string[0] + ' ' + splitted_string[1]
            temp_list = action[:-1]
            temp_list.append(temp_string)
            actions_list[index] = temp_list

        # If the length of the separated string is lesser than or equal to 2,
        # then the last action of p2 is from the previous action round.
        elif len(splitted_string) <= 2:
            # Append p2 final action to list.
            p2_final_actions.append(action[-2].split()[2])

            # Extract what comes after p2 final action and replace in the original list.
            temp_string = action[-2].split()[0] + ' ' + action[-2].split()[1]
            temp_list = action[:-2]
            temp_list.append(temp_string)
            actions_list[index] = temp_list

    return p2_final_actions


if __name__ == '__main__':
    data = np.loadtxt(open('Lab4PokerData.txt', 'rb'),
                      delimiter='\n ', dtype='str')

    actions_list = removeCommas(data)
    removeEmptyString(actions_list)

    # Extract final actions of p2 (target values).
    p2_final_actions = extractPlayer2FinalActions(actions_list)
    print(p2_final_actions)
    print(actions_list)

    # Split data.
    train_set, test_set = train_test_split(actions_list, test_size=0.2)

    # Sort target and input portions of data.
    input_train, target_train = [], []
    for action in train_set:
        input_train.append(action[:-1])
        target_train.append(action[-1])
