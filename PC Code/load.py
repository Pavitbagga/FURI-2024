import pickle
import os

directory = os.getcwd() + r'\Data\Downsampled\03-26_1_10Hz_2.pkl'

with open(directory, 'rb') as file:
    data = pickle.load(file)

print(len(data.timestamps))
data.plot()