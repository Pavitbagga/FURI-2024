import serial
import time
import struct
import threading
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

timestamps = []
values = [[] for _ in range(6)]
file = open("data.csv", "w")
file2 = open("timestamps.csv", "w")

window_range = 5 # seconds
samples_range = window_range * 100 # Assuming 100 Hz sample rate

button_timestamps = []

button_port = 'COM7'  
baud_rate = 115200

# def button():
#     while True:
#         if bt_serial.in_waiting:
#             msg = bt_serial.readline().decode('utf-8').strip()
#             if msg == "Pressed":
#                 button_timestamps.append(timestamps[-1])
#                 file2.write(str(timestamps[-1]) + ";")
#                 print(timestamps[-1])
                
def read_serial():
    ser = serial.Serial('COM11', 921600)
    time.sleep(2)
    while True:
        if ser.in_waiting > 0:
            raw_data = ser.read(28)
            unpacked_data = struct.unpack('fffffff', raw_data)

            timestamps.append(unpacked_data[0])
            for i in range(6):
                        values[i].append(unpacked_data[1+i])
            file.write("{:.5f};{:.5f};{:.5f};{:.5f};{:.5f};{:.5f};{:.5f}".format(*unpacked_data) + '\n')

# try:
#     bt_serial = serial.Serial(button_port, baudrate=baud_rate, timeout=1)
# except Exception as e:
#     print(f"Failed to connect: {e}")

# button_thread = threading.Thread(target=button)
# button_thread.daemon = True
# button_thread.start()

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
    if timestamps:
        for i, line in enumerate(lines):
            if len(values[i]) > 0:
                line.set_data(timestamps[max(0, len(timestamps)-samples_range):-1], values[i][max(0, len(timestamps)-samples_range):-1])
                axs[i].relim()
                axs[i].autoscale_view()
    return lines

ani = FuncAnimation(fig, update, frames=range(1000), init_func=init, blit=False, interval=5)

plt.show()

file.close()
file2.close()