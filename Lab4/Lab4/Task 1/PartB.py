import numpy as np
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
# Support Vector Classifier
from sklearn.svm import SVC
# Decision Tree Classifier
from sklearn.tree import DecisionTreeClassifier
# Gaussian Naive Bayes
from sklearn.naive_bayes import GaussianNB


Data = np.loadtxt(open('Lab4Data.csv', 'rb'),
                  delimiter=';', skiprows=1)

Train_set, Test_set = train_test_split(Data, test_size=0.2)

Input_train = Train_set[:, :8]
Target_train = Train_set[:, 9]

Input_test = Test_set[:, :8]
Target_test = Test_set[:, 9]

classifiers = [DecisionTreeClassifier(), SVC(), GaussianNB()]
legends = ["Decision Tree", "Support Vector Classifier", "Gaussian Naive Bayes"]

numberOfRounds = np.arange(1, 101, 1)
for classifier in classifiers:
    accuracies = []
    for currentRound in numberOfRounds:
        classifier.fit(Input_train, Target_train)
        accuracy = classifier.score(Input_test, Target_test)
        accuracies.append(accuracy)
    plt.plot(numberOfRounds, accuracies)


plt.ylabel("Accuracy")
plt.xlabel("Round")
plt.legend(legends)

plt.show()
