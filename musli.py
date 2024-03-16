import serial
from datetime import datetime
import time
import numpy as np
import sys

# Define the serial port and baud rate
serial_port = '/dev/ttyACM0'  # Change this to your Arduino's serial port
baud_rate = 9600  # Change this to match your Arduino's baud rate

ser = serial.Serial(serial_port, baud_rate)

current_datetime = datetime.now().strftime("%d_%H_%M_%S")
experiment_type = sys.argv[1].upper().strip()
##str(input("(R) Russin eller (M) Musli, (B) Batch or (S) single: ")).upper().strip()

# Open serial port
print("Serial port opened successfully.")

# Open a file for writing
if experiment_type[0] == "R" and experiment_type[1] == "S":
    file_path = f"data/sensor_data_russin_single{current_datetime}.txt"
elif experiment_type[0] == "R" and experiment_type[1] == "B":
    file_path = f"data/sensor_data_russin_batch{current_datetime}.txt"
elif experiment_type[0] == "M" and experiment_type[1] == "S":
    file_path = f"data/sensor_data_musli_single{current_datetime}.txt"
elif experiment_type[0] == "M" and experiment_type[1] == "B":
    file_path = f"data/sensor_data_musli_batch{current_datetime}.txt"
else:
    raise Exception("Experiment type must be either M or R")

buff = ""
calibration_data = []

try:
    print("Initializing...")
    # Discard data from the first 500 ms
    start_time = time.time()
    while time.time() - start_time < 0.5:
        ser.readline()

    print("Calibrating...")
    # Collect data for calibration phase (next 3 seconds)
    start_time = time.time()
    while time.time() - start_time < 3:
        line = ser.readline().decode().strip()
        if line:  # Skip empty lines
            try:
                calibration_data.append(int(line))
            except ValueError:
                pass  # Skip unreadable rows

    # Calculate median of calibration data
    calibration_median = np.median(calibration_data)
    print("Calibration median:", calibration_median)
    print("Ready")
    # Read data from serial port, subtract calibration median, and write to file
    standingByForFirstPour = True
    while True:
        line = int(ser.readline().decode().strip()) - calibration_median
        if line < -3 or 5 < line:
            standingByForFirstPour = False
        if standingByForFirstPour:
            continue
        if line:  # Skip empty lines
            try:
                sensor_value = line
                buff += str(sensor_value) + "\n"
                print(sensor_value)  # Print to console (optional)
            except ValueError:
                pass  # Skip unreadable rows

except KeyboardInterrupt:
    print("Keyboard Interrupt detected. Closing files and serial port.")
    ser.close()
    print("File opened successfully.")
    with open(file_path, 'w') as file:
        file.write(buff)
        file.close()
