import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import mne
from scipy.signal import butter, filtfilt

# Serial port configuration
SERIAL_PORT = '/dev/cu.usbserial-10'
BAUD_RATE = 9600
fs = 250  # Sampling rate
lowcut = 0.5  # Low cutoff frequency
highcut = 30.0  # High cutoff frequency

# Initialize serial communication
ser = serial.Serial(SERIAL_PORT, BAUD_RATE)

# Function to read data from the serial port
def read_serial_data():
    try:
        data = ser.readline().decode('utf-8').strip()
        return float(data)
    except:
        return 0.0

# Define bandpass filter function
def bandpass_filter(data, lowcut, highcut, fs):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(1, [low, high], btype='band')
    return filtfilt(b, a, data)

# Set up the plot
fig, ax = plt.subplots()
x_data, y_data = [], []
line, = ax.plot([], [], lw=2)

# Set plot limits
ax.set_xlim(0, 100)
ax.set_ylim(-100, 100)
ax.grid()

# Initialize the plot data
def init():
    line.set_data([], [])
    return line,

# Update the plot data
def update(frame):
    y = read_serial_data()
    x_data.append(len(x_data) / fs)
    y_data.append(y)

    # Limit the x_data to the last 250 points
    x_data_plot = x_data[-250:]
    y_data_plot = y_data[-250:]

    # Apply bandpass filter
    y_data_filtered = bandpass_filter(y_data_plot, lowcut, highcut, fs)

    # Create MNE Raw object
    data_array = np.array(y_data_filtered).reshape(1, -1)
    info = mne.create_info(ch_names=['EEG'], sfreq=fs, ch_types=['eeg'])
    raw = mne.io.RawArray(data_array, info)

    # Compute Power Spectral Density (PSD)
    f, Pxx = mne.time_frequency.psd_array_welch(raw.get_data()[0], sfreq=fs, n_fft=fs)

    # Calculate amplitude
    amplitudes = np.sqrt(Pxx)
    delta_amplitude = np.mean(amplitudes[(f >= 0.5) & (f < 4)])
    theta_amplitude = np.mean(amplitudes[(f >= 4) & (f < 8)])
    alpha_amplitude = np.mean(amplitudes[(f >= 8) & (f < 13)])
    beta_amplitude = np.mean(amplitudes[(f >= 13) & (f < 30)])
    
    print(f"Delta: {delta_amplitude:.2f}, Theta: {theta_amplitude:.2f}, Alpha: {alpha_amplitude:.2f}, Beta: {beta_amplitude:.2f}")

    line.set_data(x_data_plot, y_data_filtered)
    ax.set_xlim(x_data_plot[0], x_data_plot[-1] if x_data_plot else 1)

    return line,

# Create the animation
ani = animation.FuncAnimation(fig, update, init_func=init, blit=True, interval=50)

plt.show()
