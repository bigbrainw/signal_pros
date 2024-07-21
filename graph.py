import matplotlib.pyplot as plt
import numpy as np

def read_eeg_data(file_path):
    data = np.loadtxt(file_path, delimiter=',', skiprows=1)
    time = data[:, 0]
    voltage = data[:, 1]
    return time, voltage

def plot_multiple_eeg_subplots(time1, voltage1, time2, voltage2):
    fig, axs = plt.subplots(2, 1, figsize=(10, 10))

    axs[0].plot(time1, voltage1, label='EEG Signal 1')
    axs[0].set_xlabel('Time (s)')
    axs[0].set_ylabel('Voltage (µV)')
    axs[0].set_title('EEG Signal 1')
    axs[0].grid(True)
    
    axs[1].plot(time2, voltage2, label='EEG Signal 2')
    axs[1].set_xlabel('Time (s)')
    axs[1].set_ylabel('Voltage (µV)')
    axs[1].set_title('EEG Signal 2')
    axs[1].grid(True)
    
    plt.tight_layout()
    plt.show()

# Example usage
file_path1 = 'driving/raw_dad_driving_6.csv'
file_path2 = 'dad_data/raw_dad_2.csv'
time1, voltage1 = read_eeg_data(file_path1)
time2, voltage2 = read_eeg_data(file_path2)
plot_multiple_eeg_subplots(time1, voltage1, time2, voltage2)
