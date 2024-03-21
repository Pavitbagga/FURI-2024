import os
import pickle
import matplotlib.pyplot as plt

# Specify the directory you want to scan
directory = r'C:\Users\deves\Desktop\Desktop All\Class Material\Spring 2024\FURI\Data\03-20_1.pkl'

with open(directory, 'rb') as file:
    # Load the data from the file and assign it to a variable
    data = pickle.load(file)

data.plot()