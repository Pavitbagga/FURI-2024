import matplotlib.pyplot as plt
import pandas as pd

# Load the main data file
data = pd.read_csv('data2.csv', sep=';', names=['timestamp', 'data1', 'data2', 'data3', 'data4', 'data5', 'data6'])

# Load the timestamps file
with open('timestamps2.csv', 'r') as f:
    button_timestamps = f.read().split(';')
    # Remove the last element if it's empty due to trailing semicolon
    if not button_timestamps[-1]:
        button_timestamps.pop()

# Convert button_timestamps to float for comparison
button_timestamps = [float(ts) for ts in button_timestamps]

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

    # Highlight the x-axis at button press timestamps
    for ts in button_timestamps:
        axs[i-1].axvline(x=ts, color='r', linestyle='--')

axs[-1].set_xlabel('Timestamp')

plt.tight_layout()
plt.show()
