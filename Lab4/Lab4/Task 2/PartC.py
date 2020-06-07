from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score, train_test_split
import matplotlib.pyplot as plt
import numpy as np
import PartB


neighbors = [1, 3, 5, 10, 15]
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


data = np.loadtxt(open('Lab4PokerData.txt', 'rb'),
                  delimiter='\n ', dtype='str')

actions_list = PartB.removeCommas(data)
PartB.removeEmptyString(actions_list)
actions_list = PartB.ConvertToNumerical(actions_list)

# Split data.
train_set, test_set = train_test_split(actions_list, test_size=0.2)

# Extract final actions of p2 (target values).
p2_final_actions_train = PartB.extractPlayer2FinalActionsTest(train_set)
p2_final_actions_test = PartB.extractPlayer2FinalActionsTest(test_set)


for kNN in kNNClassifiers:
    cross_validation_score = cross_val_score(
        kNN, test_set, p2_final_actions_test, cv=3)
    mean_acc = np.mean(cross_validation_score)
    ax.scatter(kNN.n_neighbors, mean_acc,
               label=f'{kNN.n_neighbors} neighbors with {list(distanceMethods.keys())[list(distanceMethods.values()).index(list(kNN.get_params().values())[6])]} distance')
plt.ylabel("Average accuracy")
plt.xlabel("Number of neighbors")
plt.legend()
plt.show()
