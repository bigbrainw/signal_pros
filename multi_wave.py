import serial
import time
import numpy as np
import csv
import os

soundCard = "A0"
chunk_size = 1024  # Number of samples per chunk
sampling_rate = 2000  # Sampling rate in Hz
beta_freq_range = (12, 30)  # Beta frequency range in Hz
alpha_freq_range = (8, 12)  # Alpha frequency range in Hz
theta_freq_range = (4, 8)  # Theta frequency range in Hz
csv_file_path = 'fp1mastoid_workin630.csv'

# Initialize serial communication
ser = serial.Serial('/dev/cu.usbserial-10', 9600)  # Change '/dev/cu.usbserial-110' to the appropriate port on your system

def setup():
    print("Setup completed.")
    # Open CSV file in append mode
    is_new_file = not os.path.isfile(csv_file_path)
    csv_file = open(csv_file_path, mode='a', newline='')
    csv_writer = csv.writer(csv_file)
    # Write the header row in the CSV file if it is a new file
    if is_new_file:
        csv_writer.writerow(['Timestamp', 'Average Beta Amplitude', 'Average Alpha Amplitude', 'Average Theta Amplitude'])
    return csv_file, csv_writer

def loop(csv_writer):
    print("Reading data...")
    # Read chunk of data from Arduino
    data_chunk = []
    for _ in range(chunk_size):
        ser.write(b"r" + soundCard.encode() + b"\n")
        alphaData = ser.readline().strip()
        if alphaData:
            print(f"Received data: {alphaData}")  # Print received data for debugging
            data_chunk.append(int(alphaData))
    #print(f"Data read: {len(data_chunk)} samples.")

    if len(data_chunk) == chunk_size:
        # Perform FFT
        print("Performing FFT...")
        fft_result = np.fft.fft(data_chunk)
        fft_freqs = np.fft.fftfreq(chunk_size, 1/sampling_rate)
        print("FFT completed.")
        
        # Calculate average amplitudes for beta, alpha, and theta ranges
        avg_beta_amplitude = calculate_average_amplitude(fft_result, fft_freqs, beta_freq_range)
        avg_alpha_amplitude = calculate_average_amplitude(fft_result, fft_freqs, alpha_freq_range)
        avg_theta_amplitude = calculate_average_amplitude(fft_result, fft_freqs, theta_freq_range)

        # Write the average amplitudes to the CSV file with timestamp
        timestamp = time.time()
        csv_writer.writerow([timestamp, avg_beta_amplitude, avg_alpha_amplitude, avg_theta_amplitude])
    else:
        print("Insufficient data samples read, skipping this chunk.")

    time.sleep(0.03)  

def calculate_average_amplitude(fft_result, fft_freqs, freq_range):
    # Find indices corresponding to the specified frequency range
    indices = np.where((fft_freqs >= freq_range[0]) & (fft_freqs <= freq_range[1]))[0]

    # Print FFT result for the specified range
    print(f"FFT result for {freq_range[0]}-{freq_range[1]} Hz range:")
    amplitudes = []
    for i in indices:
        amplitudes.append(np.abs(fft_result[i]))
        print("Frequency:", fft_freqs[i], "Hz, Amplitude:", np.abs(fft_result[i]))

    # Calculate average amplitude for the specified range
    avg_amplitude = np.mean(amplitudes)
    print(f"Average amplitude for {freq_range[0]}-{freq_range[1]} Hz range:", avg_amplitude)
    return avg_amplitude

if __name__ == "__main__":
    csv_file, csv_writer = setup()
    try:
        while True:
            loop(csv_writer)
            csv_file.flush()  # Ensure data is written to file
    except KeyboardInterrupt:
        # Close the CSV file when the program is interrupted
        csv_file.close()
        ser.close()
