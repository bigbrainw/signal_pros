import serial
import time
import numpy as np
import csv
import os

soundCard = "A0"
chunk_size = 512  # Number of samples per chunk
sampling_rate = 2000  # Sampling rate in Hz
beta_freq_range = (12, 30)  # Beta frequency range in Hz
csv_file_path = 'fp1mastoid_working.csv'

# Initialize serial communication
ser = serial.Serial('/dev/cu.usbserial-10', 2000000)  # Change '/dev/cu.usbmodem1401' to the appropriate port on your system

def setup():
    print("Setup completed.")
    # Open CSV file in append mode
    is_new_file = not os.path.isfile(csv_file_path)
    csv_file = open(csv_file_path, mode='a', newline='')
    csv_writer = csv.writer(csv_file)
    # Write the header row in the CSV file if it is a new file
    if is_new_file:
        csv_writer.writerow(['Timestamp', 'Average Beta Amplitude'])
    return csv_file, csv_writer

def loop(csv_writer):
    print("Reading data...")
    # Read chunk of data from Arduino
    data_chunk = []
    for _ in range(chunk_size):
        ser.write(b"r" + soundCard.encode() + b"\n")
        alphaData = ser.readline().strip()
        if alphaData:
            data_chunk.append(int(alphaData))
    print(f"Data read: {len(data_chunk)} samples.")

    if len(data_chunk) == chunk_size:
        # Perform FFT
        print("Performing FFT...")
        fft_result = np.fft.fft(data_chunk)
        fft_freqs = np.fft.fftfreq(chunk_size, 1/sampling_rate)
        print("FFT completed.")
        
        # Find indices corresponding to beta frequency range
        beta_indices = np.where((fft_freqs >= beta_freq_range[0]) & (fft_freqs <= beta_freq_range[1]))[0]

        # Print FFT result for beta range
        print("FFT result for beta range:")
        beta_amplitudes = []
        for i in beta_indices:
            beta_amplitudes.append(np.abs(fft_result[i]))
            print("Frequency:", fft_freqs[i], "Hz, Amplitude:", np.abs(fft_result[i]))

        # Calculate average amplitude for beta range
        avg_beta_amplitude = np.mean(beta_amplitudes)
        print("Average amplitude for beta range:", avg_beta_amplitude)

        # Write the average beta amplitude to the CSV file with timestamp
        timestamp = time.time()
        csv_writer.writerow([timestamp, avg_beta_amplitude])
    else:
        print("Insufficient data samples read, skipping this chunk.")

    time.sleep(0.08)  # Wait for 80 milliseconds before the next read

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
