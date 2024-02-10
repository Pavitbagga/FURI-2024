import matplotlib.pyplot as plt
import pandas as pd

# Load the main data file
data = pd.read_csv('data.csv', sep=';', names=['timestamp', 'data1', 'data2', 'data3', 'data4', 'data5', 'data6'])

# Load the timestamps file
with open('timestamps.csv', 'r') as f:
    button_timestamps = f.read().split(';')
    # Remove the last element if it's empty due to trailing semicolon
    if not button_timestamps[-1]:
        button_timestamps.pop()

# Convert button_timestamps to float for comparison
button_timestamps = [float(ts) for ts in button_timestamps]

# Parameters
transient_window = 0.5 # seconds # aka start/end of rep window
states = ["intermediate", "inactivity", "correct", "fast", "incomplete", "swinging"]
state_labels = [1, 2, 3, 4, 5, 6]

