import numpy as np
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier

Data = np.loadtxt(open('Lab4Data.csv', 'rb'),
                  delimiter=';', skiprows=1)

Train_set, Test_set = train_test_split(Data, test_size=0.2)

Input_train = Train_set[:, :8]
Target_train = Train_set[:, 9]

Input_test = Test_set[:, :8]
Target_test = Test_set[:, 9]

neighbors = [1, 3, 5, 10, 15, 20, 30, 40, 50]
legends = [f'{neighbor} neighbors' for neighbor in neighbors]
kNNClassifiers = []
distanceMethods = {"manhattan": 1, "euclidean": 2}

fig, ax = plt.subplots()
ax.set_xlabel("Number of neighbors")
ax.set_ylabel("Mean accuracy")

for method in distanceMethods.values():
    for numberOfNeighBors in neighbors:
        kNNClassifiers.append(KNeighborsClassifier(
            n_neighbors=numberOfNeighBors, p=method))

rounds = np.arange(1, 50, 1)
for kNN in kNNClassifiers:
    accuracies = []
    for currentRound in rounds:
        kNN.fit(Input_train, Target_train)
        accuracy = kNN.score(Input_test, Target_test)
        accuracies.append(accuracy)
    # Scatter plot of mean accuracy for each number of neighbors
    ax.scatter(kNN.n_neighbors, sum(accuracies)/len(accuracies),
               label=f'{kNN.n_neighbors} neighbors with {list(distanceMethods.keys())[list(distanceMethods.values()).index(list(kNN.get_params().values())[6])]} distance')


plt.ylabel("Average accuracy")
plt.xlabel("Number of neighbors")
plt.legend()
plt.show()
