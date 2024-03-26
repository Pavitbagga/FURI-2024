import pickle
import os

directory = r'C:\Users\deves\Desktop\Desktop All\Class Material\Spring 2024\FURI\Data\Segments\Incomplete10.pkl'

with open(directory, 'rb') as file:
    data = pickle.load(file)

data.plot()