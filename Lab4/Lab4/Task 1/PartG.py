import numpy as np
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import cross_val_score

Data = np.loadtxt(open('Lab4Data.csv', 'rb'),
                  delimiter=';', skiprows=1)

Train_set, Test_set = train_test_split(Data, test_size=0.2)

Input_train = Train_set[:, :8]
Target_train = Train_set[:, 9]

Input_test = Test_set[:, :8]
Target_test = Test_set[:, 9]

neighbors = [1, 3, 5, 10, 15, 20, 30, 40, 50]
legends = [f'{neighbor} neighbors' for neighbor in neighbors]
rounds = np.arange(1, 50, 1)

fig, ax = plt.subplots()
ax.set_xlabel("Number of neighbors")
ax.set_ylabel("Mean accuracy")

kNNRegressors = []

for numberOfNeighbors in neighbors:
    kNNRegressors.append(KNeighborsRegressor(n_neighbors=numberOfNeighbors))

for kNN in kNNRegressors:
    accuracies = []
    for currentRound in rounds:
        kNN.fit(Input_train, Target_train)
        accuracy = kNN.score(Input_test, Target_test)
        accuracies.append(accuracy)

    # Scatter plot of mean accuracy for each number of neighbors.
    ax.scatter(kNN.n_neighbors, sum(accuracies)/len(accuracies),
               label=f'{kNN.n_neighbors} number of neighbors.')

for kNN in kNNRegressors:
    print(
        f'Cross validation scores: {cross_val_score(kNN, Input_test, Target_test, cv=100)}')

plt.ylabel("Average accuracy")
plt.xlabel("Number of neighbors")
plt.legend()
plt.show()
