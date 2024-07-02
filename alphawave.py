import serial
import time
import numpy as np
import csv
import os

soundCard = "A0"
chunk_size = 512  # Number of samples per chunk
sampling_rate = 2000  # Sampling rate in Hz
alpha_freq_range = (8, 12)  # Alpha frequency range in Hz
csv_file_path = 'alphawave701.csv'

# Initialize serial communication
ser = serial.Serial('/dev/cu.usbserial-10', 9600)  # Change '/dev/cu.usbmodem1401' to the appropriate port on your system

def setup():
    print("Setup completed.")
    # Open CSV file in append mode
    is_new_file = not os.path.isfile(csv_file_path)
    csv_file = open(csv_file_path, mode='a', newline='')
    csv_writer = csv.writer(csv_file)
    # Write the header row in the CSV file if it is a new file
    if is_new_file:
        csv_writer.writerow(['Timestamp', 'Average Alpha Amplitude', 'Processing Time (s)'])
    return csv_file, csv_writer

def loop(csv_writer):
    start_time = time.time()
    
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
        
        # Find indices corresponding to alpha frequency range
        alpha_indices = np.where((fft_freqs >= alpha_freq_range[0]) & (fft_freqs <= alpha_freq_range[1]))[0]

        # Print FFT result for alpha range
        print("FFT result for alpha range:")
        alpha_amplitudes = []
        for i in alpha_indices:
            alpha_amplitudes.append(np.abs(fft_result[i]))
            print("Frequency:", fft_freqs[i], "Hz, Amplitude:", np.abs(fft_result[i]))

        # Calculate average amplitude for alpha range
        avg_alpha_amplitude = np.mean(alpha_amplitudes)
        print("Average amplitude for alpha range:", avg_alpha_amplitude)

        # Get current timestamp and formatted time string
        timestamp = time.time()
        formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))
        print(f"Time: {formatted_time}, Average Alpha Amplitude: {avg_alpha_amplitude}")

        # Calculate processing time
        processing_time = time.time() - start_time
        print(f"Processing Time: {processing_time} seconds")

        # Write the average alpha amplitude and processing time to the CSV file with timestamp
        csv_writer.writerow([timestamp, avg_alpha_amplitude, processing_time])
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
