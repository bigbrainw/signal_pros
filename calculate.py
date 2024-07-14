#calculate result
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft

# Load the EEG data from CSV
input_file = 'raw_uncle_5.csv'
data = pd.read_csv(input_file)

# Convert EEG values to float
data['EEG Value'] = data['EEG Value'].astype(float)

# Perform FFT
eeg_values = data['EEG Value'].values
n = len(eeg_values)
fs = 250  # Sampling rate (adjust if necessary)

# Calculate FFT
frequencies = np.fft.fftfreq(n, d=1/fs)
fft_values = fft(eeg_values)

# Calculate amplitudes
amplitudes = np.abs(fft_values)[:n // 2]

# Filter frequencies
frequencies = frequencies[:n // 2]

# Calculate power in different bands
delta_power = np.mean(amplitudes[(frequencies >= 0.5) & (frequencies < 4)])
theta_power = np.mean(amplitudes[(frequencies >= 4) & (frequencies < 8)])
alpha_power = np.mean(amplitudes[(frequencies >= 8) & (frequencies < 13)])
beta_power = np.mean(amplitudes[(frequencies >= 13) & (frequencies < 30)])

print(f"Delta Power: {delta_power:.2f}")
print(f"Theta Power: {theta_power:.2f}")
print(f"Alpha Power: {alpha_power:.2f}")
print(f"Beta Power: {beta_power:.2f}")

# Plot the amplitude spectrum
plt.figure(figsize=(12, 6))
plt.plot(frequencies, amplitudes, color='blue')
plt.title('EEG Amplitude Spectrum')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.xlim(0, 30)  # Focus on relevant frequencies
plt.grid()
plt.show()
