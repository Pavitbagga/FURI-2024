import pickle
import os

directory = os.getcwd() + r'\Data\Segments\Correct\Correct0.pkl'

with open(directory, 'rb') as file:
    data = pickle.load(file)

print(len(data.timestamps))
data.to_image()