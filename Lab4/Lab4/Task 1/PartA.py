import numpy as np
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt


class kNN:
    def __init__(self):
        Data = np.loadtxt(open('Lab4Data.csv', 'rb'),
                          delimiter=';', skiprows=1)

        Train_set, Test_set = train_test_split(Data, test_size=0.2)
        self.Input_train = Train_set[:, :8]  # Input features.
        self.Target_train = Train_set[:, 9]  # Output labels.

        self.Input_test = Test_set[:, :8]    # Input features test set.
        self.Target_test = Test_set[:, 9]    # Output labels test set.

        self.nearestNeighbors = []
        self.actualOutput = []
        self.estimatedOutput = []
        self.correctEstimate = 0

    def euclideanDistance(self, k):
        self.correctEstimate = 0
        self.classOfNearestNeighbors = [None]*k
        self.estimatedOutput = []

        for testIndex, testData in enumerate(self.Input_test):
            # As moving on to new data point, clear the nearest neighbors.
            self.nearestNeighbors = []
            for trainingIndex, trainingData in enumerate(self.Input_train):
                # self.nearestNeighbors = lambda theList:
                # Calculate Euclidean distance between two data points.
                euc_dist = np.linalg.norm(
                    self.Input_test[testIndex] - self.Input_train[trainingIndex], ord=None)

                if len(self.nearestNeighbors) < k:
                    # Add new entry into list of nearest neighbors.
                    self.nearestNeighbors.append(euc_dist)
                    self.assignClassOfNeighbors(euc_dist, trainingIndex)
                    # Sort nearest neighbors in ascending order.
                    self.nearestNeighbors.sort()

                elif euc_dist < max(self.nearestNeighbors):
                    # Remove greatest distance in list of nearest neighbors.
                    self.nearestNeighbors.pop()
                    # Insert new neighbor in ascending order.
                    self.nearestNeighbors.append(euc_dist)
                    self.assignClassOfNeighbors(euc_dist, trainingIndex)
                    # Sort nearest neighbors in ascending order.
                    self.nearestNeighbors.sort()

                if euc_dist in self.nearestNeighbors:
                    #self.assignClassOfNeighbors(euc_dist, trainingIndex)
                    # REMOVE THIS LATER
                    if self.nearestNeighbors.index(
                            euc_dist) == None:
                        print('Halt')

            self.estimatedOutput.append(int(self.determineClass()))

    def assignClassOfNeighbors(self, euc_dist, trainingIndex):
        classToBeAdded = self.Target_train[trainingIndex]

        # Insert the actual output into seperate list.
        self.classOfNearestNeighbors[self.nearestNeighbors.index(
            euc_dist)] = classToBeAdded

    def determineClass(self):
        # All possible values of Driver Performance.
        neighborClasses = {1.0: 0, 2.0: 0, 3.0: 0}
        for element in self.classOfNearestNeighbors:
            # Increase number of occurences of given class.
            neighborClasses[element] += 1
        return max(neighborClasses, key=lambda index: neighborClasses[index])


if __name__ == "__main__":
    kNN = kNN()
    results = []

    for i in range(2, 31, 1):
        kNN.euclideanDistance(i)
        for element in kNN.estimatedOutput:
            if element == kNN.Target_test[kNN.estimatedOutput.index(element)]:
                kNN.correctEstimate += 1
        print(f'k = {i}')
        print(f'Number of correct estimates: {kNN.correctEstimate}')
        print(f'Accuracy: {kNN.correctEstimate/len(kNN.Target_test)*100}%')
        results.append(kNN.correctEstimate/len(kNN.Target_test)*100)

    data = [23, 45, 56, 78, 213]
    plt.bar([2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
             18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30], results)
    plt.ylabel('Accuracy (%)')
    plt.xlabel('k')
    plt.grid(color='#95a5a6', linestyle='-', linewidth=2, axis='y', alpha=0.7)
    plt.show()
    # print(f'Number of neighbors: {len(kNN.nearestNeighbors)}')
    # print(f'Number of estimates: {len(kNN.estimatedOutput)}')

    # print(f'Estimated outputs: {kNN.estimatedOutput}')
    # print(f'Actual output: {kNN.Target_test}')

    # print(f'Number of correct estimates: {kNN.correctEstimate}')
    # print(f'Accuracy: {kNN.correctEstimate/len(kNN.Target_test)*100}%')
