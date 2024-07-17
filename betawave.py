import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft
from scipy.signal import butter, filtfilt

# Bandpass filter function
def butter_bandpass(lowcut, highcut, fs, order=5):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return b, a

def bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = filtfilt(b, a, data)
    return y

# Load the EEG data from CSV
#input_file = 'raw_relax_sean_2.csv'
input_file = 'raw_writing_sean_1.csv'
data = pd.read_csv(input_file)

# Convert EEG values to float
data['EEG Value'] = data['EEG Value'].astype(float)

# Parameters
fs = 250  # Sampling rate (adjust if necessary)
beta_lowcut = 13
beta_highcut = 30

# Apply bandpass filter for beta waves
beta_filtered_eeg = bandpass_filter(data['EEG Value'].values, beta_lowcut, beta_highcut, fs)

# Perform FFT
n = len(beta_filtered_eeg)
frequencies = np.fft.fftfreq(n, d=1/fs)
fft_values = fft(beta_filtered_eeg)

# Calculate amplitudes
amplitudes = np.abs(fft_values)[:n // 2]

# Filter frequencies for plotting
frequencies = frequencies[:n // 2]

# Calculate power in beta band
beta_power = np.mean(amplitudes[(frequencies >= beta_lowcut) & (frequencies < beta_highcut)])

print(f"Beta Power: {beta_power:.2f}")

# Plot the amplitude spectrum for beta waves
plt.figure(figsize=(12, 6))
plt.plot(frequencies, amplitudes, color='blue')
plt.title('EEG Beta Amplitude Spectrum')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.xlim(beta_lowcut, beta_highcut)  # Focus on beta frequencies
plt.grid()
plt.show()
