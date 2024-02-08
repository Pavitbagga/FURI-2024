import serial
import time
import struct
import threading
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

timestamps = []
labels = []
values = [[] for _ in range(6)]

window_range = 5 # seconds
samples_range = window_range * 100 # Assuming 100 Hz sample rate

def read_serial():
    ser = serial.Serial('COM11', 921600)
    time.sleep(2)

    while True:
        if ser.in_waiting > 0:
            raw_data = ser.read(32)
            unpacked_data = struct.unpack('ffffffff', raw_data)

            timestamps.append(unpacked_data[0])
            for i in range(6):
                        values[i].append(unpacked_data[2+i])

thread = threading.Thread(target=read_serial)
thread.daemon = True 
thread.start()

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
    if timestamps:
        for i, line in enumerate(lines):
            if len(values[i]) > 0:
                line.set_data(timestamps[max(0, len(timestamps)-samples_range):-1], values[i][max(0, len(timestamps)-samples_range):-1])
                axs[i].relim()
                axs[i].autoscale_view()
    return lines

ani = FuncAnimation(fig, update, frames=range(1000), init_func=init, blit=False, interval=5)

plt.show()
