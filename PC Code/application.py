import serial
import time
import struct
import threading
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pickle
import os
import datetime
from data import Data

timestamps = [0] # Initialize with 0
raw_values = [[0] for _ in range(6)] # Initialize with 0
processed_values = [[0] for _ in range(6)] # Initialize with 0

# Exponential Moving Average Data
N = 10 # Num Windows to average
alpha = 2/(N+1)

# Derivative 
N_d = 40 # Num Windows to average
alpha_d = 2/(N_d+1)
derivative = [0]

# Curl Settings
curl_timeout = 3.5
start_times = []
timeouts = []

# Value Ranges
value_range = [[-1.5, 1.5], [-1.5, 1.5], [-1.5, 1.5], [-100, 100], [-100, 100], [-100, 100]]

# Filesave  
savepath = os.getcwd() + r"\Data" 
current_datetime = datetime.datetime.now()
datetime_string = current_datetime.strftime('%m-%d_')
labels = [1,1,1,1,1,1,3,3,3,3,4,4,4,5,5,5] # 6 correct, 4 very fast, 3 incomplete, 3 no wrist rot
entries = os.listdir(savepath)
file_count = sum([1 for entry in entries if os.path.isfile(os.path.join(savepath, entry)) and entry.endswith('.pkl')])
name = datetime_string + str(file_count) + '.pkl'
filename = os.path.join(savepath, name)
print(filename)

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
    curl_start = False
    timeout_enable = False
    while True:
        if ser.in_waiting > 0:
            raw_data = ser.read(28)
            unpacked_data = struct.unpack('fffffff', raw_data)

            timestamps.append(unpacked_data[0])
            for i in range(6):
                if i < 3:
                    processed_values[i].append(cap(alpha*unpacked_data[1+i] + (1-alpha)*processed_values[i][-1], value_range[i])) # Exponential Moving Average
                else:
                    processed_values[i].append(cap_and_scale(alpha*unpacked_data[1+i] + (1-alpha)*processed_values[i][-1], value_range[i]))

                raw_values[i].append(unpacked_data[1+i])

            dy = processed_values[1][-1] - processed_values[1][-2]
            dt = timestamps[-1] - timestamps[-2]
            derivative.append(alpha_d*(dy/dt) + (1-alpha_d)*derivative[-1])
            derivative2 = (derivative[-1] - derivative[-2])/dt 

            if derivative[-1] > 0.3 and timestamps[-1] > 0.15 and derivative2 > 0:
                if not curl_start:
                    start_times.append(timestamps[-1])
                    curl_start = True
                    timeout_enable = True
                    print("Start")

            if derivative[-1] < 0:
                curl_start = False
                
            if len(start_times) != 0:
                if timestamps[-1] > start_times[-1] + curl_timeout and timeout_enable:
                    timeouts.append(timestamps[-1])
                    timeout_enable = False
                    print("Timeout")

serial_thread = threading.Thread(target=read_serial)
serial_thread.daemon = True 
serial_thread.start()

# Initialize plot
fig, axs = plt.subplots(6, 1, sharex=True)
colors = ['r', 'g', 'b', 'c', 'm', 'y']
lines = [axs[i].plot([], [], color=colors[i])[0] for i in range(6)]
samples_range = 5 * 100 # 5 seconds * assumed 100 Hz sample rate for visualizing only some seconds of data
data_to_plot = processed_values

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
    if timestamps:
        for i, line in enumerate(lines):
            if len(data_to_plot[i]) > 0:
                line.set_data(timestamps[max(0, len(timestamps)-samples_range):-1], data_to_plot[i][max(0, len(timestamps)-samples_range):-1])
                axs[i].relim()
                axs[i].autoscale_view()
    return lines

ani = FuncAnimation(fig, update, frames=range(1000), init_func=init, blit=False, interval=5)

plt.show()

data = Data()
data.timestamps = timestamps
data.raw_values = raw_values
data.processed_values = processed_values
data.start_times = start_times
data.timeouts =  timeouts
data.labels = labels

with open(filename, 'wb') as file:
    pickle.dump(data, file)