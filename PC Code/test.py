import matplotlib.pyplot as plt
import pandas as pd

# Load the main data file
data = pd.read_csv('data.csv', sep=';', names=['timestamp', 'data1', 'data2', 'data3', 'data4', 'data5', 'data6'])

# Load the timestamps files
with open('start_timestamps.csv', 'r') as f:
    start_timestamps = f.read().split(';')
    # Remove the last element if it's empty due to trailing semicolon
    if not start_timestamps[-1]:
        start_timestamps.pop()

with open('end_timestamps.csv', 'r') as f:
    end_timestamps = f.read().split(';')
    # Remove the last element if it's empty due to trailing semicolon
    if not end_timestamps[-1]:
        end_timestamps.pop()

# Convert start_timestamps to float for comparison
start_timestamps = [float(ts) for ts in start_timestamps]
end_timestamps = [float(ts) for ts in end_timestamps]

def segmenter(data, time, start, end):
    start_idx = time.index(start)
    end_idx = time.index(end)
    segment = data[start_idx:end_idx+1]
    return len(segment)

print(segmenter(data['data1'], data['timestamp'], start_timestamps[0], end_timestamps[0]))