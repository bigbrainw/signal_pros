import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

def read_eeg_data(file_path):
    data = pd.read_csv(file_path)
    time = data.iloc[:, 0].values
    voltage = data.iloc[:, 1].values
    return time, voltage

def normalize_voltage(voltage):
    return (voltage - np.mean(voltage)) / np.std(voltage)

def resample_eeg_data(time, voltage, new_time):
    interpolator = interp1d(time, voltage, kind='linear', bounds_error=False, fill_value='extrapolate')
    new_voltage = interpolator(new_time)
    return new_voltage

def plot_resampled_eeg(new_time, new_voltage1, new_voltage2):
    plt.figure(figsize=(10, 6))
    plt.plot(new_time, new_voltage1, label='EEG Signal 1')
    plt.plot(new_time, new_voltage2, label='EEG Signal 2')
    plt.xlabel('Time (s)')
    plt.ylabel('Normalized Voltage')
    plt.title('Resampled EEG Time Graphs')
    plt.legend()
    plt.grid(True)
    plt.show()

# File paths
file_path1 = 'driving/raw_dad_driving_6.csv'
file_path2 = 'dad_data/raw_dad.csv'

# Read EEG data
time1, voltage1 = read_eeg_data(file_path1)
time2, voltage2 = read_eeg_data(file_path2)

# Normalize voltages
normalized_voltage1 = normalize_voltage(voltage1)
normalized_voltage2 = normalize_voltage(voltage2)

# Define a common time frame (1 minute, 600 samples)
new_time = np.linspace(time1[0], time1[-1], 600)

# Resample the EEG data
new_voltage1 = resample_eeg_data(time1, normalized_voltage1, new_time)
new_voltage2 = resample_eeg_data(time2, normalized_voltage2, new_time)

# Plot the resampled EEG data
plot_resampled_eeg(new_time, new_voltage1, new_voltage2)
