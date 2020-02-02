import numpy as np
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt


class kNN:
    def __init__(self, k):
        Data = np.loadtxt(open('Lab4Data.csv', 'rb'),
                          delimiter=';', skiprows=1)

        Train_set, Test_set = train_test_split(Data, test_size=0.2)

        self.Input_train = Train_set[:, :9]
        self.Target_train = Train_set[:, 7]

        self.Input_test = Test_set[:, :9]
        self.Target_test = Test_set[:, 7]

        # Delete Fuel Consumption column.
        self.Input_train = np.delete(self.Input_train, 7, 1)
        self.Input_test = np.delete(self.Input_test, 7, 1)

        self.predictedConsumption = []
        self.error = []
        self.averageError = 0
        self.k = k

    def euclideanDistance(self):
        # For each test node.
        for testIndex, testNode in enumerate(self.Input_test):
            self.distanceNearestNeighbors = []
            self.consumptionOfNearestNeighbors = [None]*self.k
            # For each training node.
            for trainIndex, trainNode in enumerate(self.Input_train):
                # Determine euclidean distance between current test node and training node.
                eucDist = np.linalg.norm(
                    self.Input_test[testIndex] - self.Input_train[trainIndex], ord=None)

                if len(self.distanceNearestNeighbors) < self.k:
                    self.distanceNearestNeighbors.append(eucDist)
                    self.distanceNearestNeighbors.sort()
                    # Insert fuel consumption of neighbor in corresponding index.
                    self.consumptionOfNearestNeighbors[self.distanceNearestNeighbors.index(
                        eucDist)] = self.Target_train[trainIndex]

                elif eucDist < max(self.distanceNearestNeighbors) and len(self.distanceNearestNeighbors) == self.k:
                    self.distanceNearestNeighbors.pop()
                    # self.consumptionOfNearestNeighbors.pop()
                    self.distanceNearestNeighbors.append(eucDist)
                    self.distanceNearestNeighbors.sort()
                    # Insert fuel consumption of neighbor in corresponding index.
                    self.consumptionOfNearestNeighbors[self.distanceNearestNeighbors.index(
                        eucDist)] = self.Target_train[trainIndex]

            self.predictedConsumption.append(self.determineFuelConsumption())
        self.calculateError()

    def determineFuelConsumption(self):
        notNone = 0
        total = 0
        for consumption in self.consumptionOfNearestNeighbors:
            if consumption is not None:
                notNone += 1
                total += consumption
        return total/notNone

    def calculateError(self):
        for index, element in enumerate(self.predictedConsumption):
            self.error.append(abs(self.Target_test[index]-element))
        self.averageError = np.mean(self.error)


if __name__ == "__main__":
    kValues = np.arange(1, 6, 1)
    kNNregression = []
    averageErrors = []
    for value in kValues:
        kNNregression.append(kNN(value))
    for kNN in kNNregression:
        print(f'Currently calculating for {kNN.k} number of neighbors.')
        kNN.euclideanDistance()
        averageErrors.append(kNN.averageError)

    for kNN in kNNregression:
        print(
            f'With {kNN.k} neighbors, the average error was {kNN.averageError}')

    fig, ax = plt.subplots()

    ax.scatter(kValues, averageErrors)

    plt.xlabel('Number of neighbors')
    plt.ylabel('Average error')
    plt.show()
