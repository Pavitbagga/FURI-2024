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

# Plotting
fig, axs = plt.subplots(6, 1, sharex=True, figsize=(10, 10))

axs[0].set_ylabel('acc_x')
axs[1].set_ylabel('acc_y')
axs[2].set_ylabel('acc_z')
axs[3].set_ylabel('gyro_x')
axs[4].set_ylabel('gyro_y')
axs[5].set_ylabel('gyro_z')

# Plot each data column
for i in range(1, 7):
    axs[i-1].plot(data['timestamp'], data[f'data{i}'], label=f'data{i}')
    axs[i-1].legend(loc="upper right")

    # Highlight the x-axis at timestamps
    if i == 2 or i == 6:
        for ts in start_timestamps:
            axs[i-1].axvline(x=ts, color='g', linestyle='--')

    if i == 2 or i == 3:
        for ts in end_timestamps:
            axs[i-1].axvline(x=ts, color='r', linestyle='--')

axs[-1].set_xlabel('Timestamp')

plt.tight_layout()
plt.show()
