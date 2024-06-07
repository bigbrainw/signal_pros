import serial
import time
import numpy as np
import matplotlib.pyplot as plt

soundCard = "A1"
chunk_size = 512  # Number of samples per chunk
sampling_rate = 2000  # Sampling rate in Hz
beta_freq_range = (12, 30)  # Beta frequency range in Hz

# Initialize serial communication
ser = serial.Serial('/dev/cu.usbmodem1401', 2000000)  # Change '/dev/cu.usbmodem1401' to the appropriate port on your system

def setup():
    print("Setup completed.")

def loop():
    print("Reading data...")
    # Read chunk of data from Arduino
    data_chunk = []
    for _ in range(chunk_size):
        ser.write(b"r" + soundCard.encode() + b"\n")
        alphaData = int(ser.readline().strip())
        data_chunk.append(alphaData)
    print("Data read.")

    # Perform FFT
    print("Performing FFT...")
    fft_result = np.fft.fft(data_chunk)
    fft_freqs = np.fft.fftfreq(chunk_size, 1/sampling_rate)
    print("FFT completed.")

    # Find indices corresponding to beta frequency range
    beta_indices = np.where((fft_freqs >= beta_freq_range[0]) & (fft_freqs <= beta_freq_range[1]))[0]

    # Plot FFT result for beta range
    print("Plotting FFT result...")
    plt.figure(figsize=(10, 6))
    plt.plot(fft_freqs[beta_indices], np.abs(fft_result[beta_indices]))
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    plt.title('FFT of EEG Signal (Beta Range)')
    plt.grid(True)
    plt.show()
    print("Plotting completed.")

    time.sleep(0.08)  # Wait for 80 milliseconds before the next read

if __name__ == "__main__":
    setup()
    while True:
        loop()
