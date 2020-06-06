import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from LookUpTables import actions, hands, cardRanks


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
        # If player 2 was the last player to make an action.
        if len(action[6:]) % 4 == 0:
            p2_final_actions.append(action[-2])
            # The part of the entry to keep.
            actions_list[index] = action[:-2]

        # If player 1 was the last player to make an action.
        else:
            p2_final_actions.append(action[-4])
            # The part of the entry to keep.
            actions_list[index] = action[:-4]

    return p2_final_actions


# Determines the final action of player 2.
def extractPlayer2FinalActionsTest(actions_list):
    # Determines the average bet and the betting amount from player 2.
    def AverageBetRemainingMoney(entry):
        # The money player 2 had at the beginning of the round.
        initial_money = entry[5]
        betting_amount = 0
        temp_list = []
        # Start from the first bet of player 2, iterate over each bet of player 2.
        for bet in entry[9::4]:
            temp_list.append(bet)
            betting_amount += bet

        money_left = initial_money - betting_amount
        average_bet = betting_amount / len(temp_list)
        entry.extend([money_left, average_bet])

        return entry

    p2_final_actions = []
    for index, action in enumerate(actions_list):
        # If player 2 was the last player to make an action.
        if len(action[6:]) % 4 == 0:
            p2_final_actions.append(action[-2])

            # The part of the entry to keep.
            actions_list[index] = AverageBetRemainingMoney(action[:14])

        # If player 1 was the last player to make an action.
        else:
            p2_final_actions.append(action[-4])
            # The part of the entry to keep.
            actions_list[index] = AverageBetRemainingMoney(action[:14])

    return p2_final_actions


# Converts from string to numerical values.
def ConvertToNumerical(the_list):
    new_list = []

    for entry in the_list:
        temp_list = []

        handNumerical_p1 = hands[entry[1].split()[0]]
        cardNumerical_p1 = cardRanks[entry[1].split()[1]]
        moneyNumerical_p1 = int(entry[1].split()[2])

        handNumerical_p2 = hands[entry[2].split()[0]]
        cardNumerical_p2 = cardRanks[entry[2].split()[1]]
        moneyNumerical_p2 = int(entry[2].split()[2])

        temp_list.append(handNumerical_p1)
        temp_list.append(cardNumerical_p1)
        temp_list.append(moneyNumerical_p1)
        temp_list.append(handNumerical_p2)
        temp_list.append(cardNumerical_p2)
        temp_list.append(moneyNumerical_p2)

        # Focusing on the actions of each player
        for action in entry[3:]:

            action_numerical_p1 = actions[action.split()[0]]
            money_numerical_p1 = int(action.split()[1])

            temp_list.append(action_numerical_p1)
            temp_list.append(money_numerical_p1)

            if len(action.split()) > 2:
                action_numerical_p2 = actions[action.split()[2]]
                money_numerical_p2 = int(action.split()[3])

                temp_list.append(action_numerical_p2)
                temp_list.append(money_numerical_p2)

        new_list.append(temp_list)

    return new_list


def kNNClassifier(train_set, p2_final_actions_train, test_set, p2_final_actions_test):
    knn = KNeighborsClassifier()
    knn.fit(train_set, p2_final_actions_train)
    accuracy = knn.score(test_set,
                         p2_final_actions_test)
    print(f'Accuracy: {accuracy*100}%')


if __name__ == '__main__':
    data = np.loadtxt(open('Lab4PokerData.txt', 'rb'),
                      delimiter='\n ', dtype='str')

    actions_list = removeCommas(data)
    removeEmptyString(actions_list)
    actions_list = ConvertToNumerical(actions_list)

    # Split data.
    train_set, test_set = train_test_split(actions_list, test_size=0.2)

    # Extract final actions of p2 (target values).
    p2_final_actions_train = extractPlayer2FinalActionsTest(train_set)
    p2_final_actions_test = extractPlayer2FinalActionsTest(test_set)

    kNNClassifier(train_set, p2_final_actions_train,
                  test_set, p2_final_actions_test)
