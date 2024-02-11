import matplotlib.pyplot as plt
import pandas as pd

# Load the main data file
data = pd.read_csv('data.csv', sep=';', names=['timestamp', 'data1', 'data2', 'data3', 'data4', 'data5', 'data6'])
data['label'] = 0

# Load the timestamps file
with open('timestamps.csv', 'r') as f:
    timestamps = f.read().split(';')
    # Remove the last element if it's empty due to trailing semicolon
    if not timestamps[-1]:
        timestamps.pop()

# Convert timestamps to float for comparison
timestamps = [float(ts) for ts in timestamps]

# Parameters
transient_window = 0.5 # seconds # aka start/end of rep window
states = ["intermediate", "inactivity", "correct", "fast", "incomplete", "swinging"]
label_order = [1, 2, 0, 2, 0, 2, 0, 2, 1, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 1]

# Extras
boundaries = []
boundary_iter = 0
label_iter = 0

for t in timestamps:
    boundaries.append(t-transient_window)
    boundaries.append(t+transient_window)

for index in range(len(data)):
    if boundary_iter < len(boundaries):
        if(data.at[index, "timestamp"] < boundaries[boundary_iter]):
            data.at[index, 'label'] = label_order[label_iter]

        elif (data.at[index, "timestamp"] > boundaries[boundary_iter]):
            label_iter += 1
            boundary_iter += 1
            data.at[index, 'label'] =label_order[label_iter]
    else:
        data.at[index, 'label'] =label_order[-1]

data.to_csv('processed_data.csv', index=False)