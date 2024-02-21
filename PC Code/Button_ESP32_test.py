import serial
import time

# Scan for available Bluetooth devices and find the ESP32
# The COM port will vary depending on your system and how the ESP32 is connected
# You may need to check your system's device manager to find the correct COM port
button_port = 'COM7'  # Replace COM_PORT with your ESP32's Bluetooth COM port
baud_rate = 115200

def connect_bluetooth():
    try:
        bt_serial = serial.Serial(button_port, baudrate=baud_rate, timeout=1)
        return bt_serial
    except Exception as e:
        print(f"Failed to connect: {e}")
        return None

def listen_for_button(bt_serial):
    while True:
        if bt_serial.in_waiting:
            msg = bt_serial.readline().decode('utf-8').strip()
            if msg == "Pressed":
                print("Button was pressed on ESP32")

if __name__ == "__main__":
    bt_serial = connect_bluetooth()
    if bt_serial:
        listen_for_button(bt_serial)
    else:
        print("Could not establish a connection. Please check your setup and try again.")
