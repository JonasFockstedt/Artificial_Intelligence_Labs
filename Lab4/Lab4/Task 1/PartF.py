import numpy as np
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
# Decision Tree
from sklearn.tree import DecisionTreeRegressor
# MLP Regressor
from sklearn.neural_network import MLPRegressor
# Support Vector Regressor
from sklearn.svm import SVR

Data = np.loadtxt(open('Lab4Data.csv', 'rb'),
                  delimiter=';', skiprows=1)

Train_set, Test_set = train_test_split(Data, test_size=0.2)

Input_train = Train_set[:, :8]
Target_train = Train_set[:, 9]

Input_test = Test_set[:, :8]
Target_test = Test_set[:, 9]

regressors = [DecisionTreeRegressor(), MLPRegressor(), SVR()]
legends = ["Decision Tree", "MLP", "Support Vector Regressor"]

numberOfRounds = np.arange(1, 101, 1)
for regressor in regressors:
    accuracies = []
    for currentRound in numberOfRounds:
        regressor.fit(Input_train, Target_train)
        accuracy = regressor.score(Input_test, Target_test)
        accuracies.append(accuracy)

    plt.plot(numberOfRounds, accuracies)

plt.ylabel("Accuracy")
plt.xlabel("Round")
plt.legend(legends)
plt.show()
