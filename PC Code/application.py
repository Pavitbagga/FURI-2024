import serial
import time
import struct
import threading
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

timestamps = [0] # Initialize with 0
values = [[0] for _ in range(6)] # Initialize with 0
file = open("data.csv", "w")

samples_range = 5 * 100 # 5 seconds * assumed 100 Hz sample rate for visualizing only some seconds of data

window_size = 10
smoothed_values = [[0] for _ in range(6)] # Initialize with 0
N = 10 # Num Wndows to average
alpha = 2/(N+1)

value_range = [[-1.5, 1.5], [-1.5, 1.5], [-1.5, 1.5], [-250, 250], [-250, 250], [-250, 250]]

def cap_and_scale(value, value_range):
    if value > value_range[1]:
        return 1
    elif value < value_range[0]:
        return -1
    else:
        return value/value_range[1] 
    
def cap(value, value_range):
    if value > value_range[1]:
        return value_range[1]
    elif value < value_range[0]:
        return value_range[0]
    else:
        return value
                
def read_serial():
    ser = serial.Serial('COM11', 921600)
    time.sleep(2)
    while True:
        if ser.in_waiting > 0:
            raw_data = ser.read(28)
            unpacked_data = struct.unpack('fffffff', raw_data)

            timestamps.append(unpacked_data[0])
            for i in range(6):
                if i < 3:
                    smoothed_values[i].append(cap(alpha*unpacked_data[1+i] + (1-alpha)*smoothed_values[i][-1], value_range[i]))
                else:
                    smoothed_values[i].append(cap_and_scale(alpha*unpacked_data[1+i] + (1-alpha)*smoothed_values[i][-1], value_range[i]))
                values[i].append(unpacked_data[1+i])
            file.write("{:.5f};{:.5f};{:.5f};{:.5f};{:.5f};{:.5f};{:.5f}".format(*unpacked_data) + '\n')

serial_thread = threading.Thread(target=read_serial)
serial_thread.daemon = True 
serial_thread.start()

# Initialize plot
fig, axs = plt.subplots(6, 1, sharex=True)
colors = ['r', 'g', 'b', 'c', 'm', 'y']
lines = [axs[i].plot([], [], color=colors[i])[0] for i in range(6)]

def init():
    axs[0].set_ylabel('acc_x')
    axs[1].set_ylabel('acc_y')
    axs[2].set_ylabel('acc_z')
    axs[3].set_ylabel('gyro_x')
    axs[4].set_ylabel('gyro_y')
    axs[5].set_ylabel('gyro_z')
    axs[-1].set_xlabel('Timestamp')
    return lines

def update(frame):
    data_to_plot = smoothed_values
    if timestamps:
        for i, line in enumerate(lines):
            if len(values[i]) > 0:
                line.set_data(timestamps[max(0, len(timestamps)-samples_range):-1], data_to_plot[i][max(0, len(timestamps)-samples_range):-1])
                axs[i].relim()
                axs[i].autoscale_view()
    return lines

ani = FuncAnimation(fig, update, frames=range(1000), init_func=init, blit=False, interval=5)

plt.show()

file.close()