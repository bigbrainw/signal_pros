import serial
import csv
import time
import numpy as np
from scipy.signal import butter, filtfilt, welch

# Function to create a bandpass filter
def butter_bandpass(lowcut, highcut, fs, order=4):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return b, a

def bandpass_filter(data, lowcut, highcut, fs, order=4):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = filtfilt(b, a, data)
    return y

# Serial port initialization
port = serial.Serial('/dev/cu.usbmodem1401', 2000000)  # Replace with your port name

# Define sampling frequency and buffer size
fs = 2000
buffer_size = 500

# Initialize data buffer for beta band
data_buffer = np.zeros(buffer_size)

# Threshold for focus detection
threshold_beta = 1.11  # Adjust based on your observations

# Open CSV file for writing beta wave data
with open('alpha2.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Timestamp', 'Beta'])  # Write header for beta wave data

    start_time = time.time()

    # Main loop
    while True:
        # Read data from serial port
        data = port.readline().strip().decode('utf-8')
        try:
            timestamp = time.time() - start_time
            val = int(data)
            # Shift data buffer and add new value
            data_buffer = np.roll(data_buffer, -1)
            data_buffer[-1] = val

            # Apply bandpass filter for beta band
            filtered_data = bandpass_filter(data_buffer, 13, 30, fs)
            # Calculate beta power
            beta_power = np.trapz(np.abs(filtered_data), dx=1/fs)
            print(beta_power)
            # Determine if beta power is above or below the threshold
            focus_state = 1 if beta_power > threshold_beta else 0
            print(focus_state)

            # Write beta power to CSV
            writer.writerow([round(timestamp, 2), beta_power])

        except ValueError:
            print("Invalid data received from serial port:", data)

# Close serial port
port.close()
