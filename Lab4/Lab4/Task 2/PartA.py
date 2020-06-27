import numpy as np
from sklearn.model_selection import train_test_split


Data = np.loadtxt(open('Lab4PokerData.txt', 'rb'),
                  delimiter=';')

print(Data)
