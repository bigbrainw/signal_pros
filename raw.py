import serial
import time
import numpy as np
import matplotlib.pyplot as plt

soundCard = "A0"
chunk_size = 512  # Number of samples per chunk
sampling_rate = 2000  # Sampling rate in Hz
beta_freq_range = (12, 30)  # Beta frequency range in Hz

# Initialize serial communication
ser = serial.Serial('/dev/cu.usbserial-10', 9600)  # Change '/dev/cu.usbmodem1401' to the appropriate port on your system

def setup():
    print("Setup completed.")

def loop():
    print("Reading data...")
    data_chunk = []
    for _ in range(chunk_size):
        ser.write(b"r" + soundCard.encode() + b"\n")
        raw_data = ser.readline().strip()
        print("Raw data received:", raw_data)  # Debugging print
        
        # Attempt to parse the data
        try:
            if raw_data.startswith(b'EEG Value:'):
                alphaData = int(raw_data.split(b':')[1].strip())
            else:
                alphaData = int(raw_data.strip())
                
            data_chunk.append(alphaData)
        
        except ValueError:
            print("Error: Could not convert data to integer:", raw_data)
            continue  # Skip appending this data point
        
        except Exception as e:
            print("Error:", str(e))
            continue  # Skip appending this data point

    print("Data read:", len(data_chunk), "samples.")

    if len(data_chunk) == 0:
        print("No valid data received. Skipping FFT and plot.")
        return

    print("Performing FFT...")
    fft_result = np.fft.fft(data_chunk)
    fft_freqs = np.fft.fftfreq(chunk_size, 1/sampling_rate)
    print("FFT completed.")

    beta_indices = np.where((fft_freqs >= beta_freq_range[0]) & (fft_freqs <= beta_freq_range[1]))[0]

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
