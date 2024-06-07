import serial
import numpy as np
from scipy.fft import fft
from scipy.signal import find_peaks

# Initialize serial communication
ser = serial.Serial('/dev/cu.usbserial-0001', 115200)  # Adjust the port as needed

try:
    while True:
        if ser.in_waiting > 0:
            try:
                # Read data from serial port
                data = ser.readline().decode('utf-8').strip()
                print("Received:", data)

                # Convert data to numpy array of floats
                values = np.array([float(x) for x in data.split(',')])

                # Apply FFT
                fft_values = fft(values)

                # Calculate frequencies
                sample_rate = 115200  # Adjust according to your actual sample rate
                n = len(values)
                frequencies = np.fft.fftfreq(n, 1 / sample_rate)

                # Find peaks in the FFT result within the desired range
                peaks, _ = find_peaks(np.abs(fft_values), height=1000, distance=10)

                # Filter peaks within 12-30 Hz
                freq_peaks = frequencies[peaks]
                freq_peaks_filtered = freq_peaks[(freq_peaks >= 12) & (freq_peaks <= 30)]

                # Print or process the relevant frequency information
                print("Frequency peaks between 12-30 Hz:", freq_peaks_filtered)

            except UnicodeDecodeError as e:
                print("Decode error:", e)
except KeyboardInterrupt:
    ser.close()
    print("Serial connection closed.")
