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

# Load and preprocess the EEG data
def load_and_preprocess(file_path, fs=250, lowcut=0.5, highcut=50):
    data = pd.read_csv(file_path)
    data['EEG Value'] = data['EEG Value'].astype(float)
    filtered_data = bandpass_filter(data['EEG Value'].values, lowcut, highcut, fs)
    return filtered_data

# Calculate power in frequency bands
def calculate_band_powers(eeg_values, fs):
    n = len(eeg_values)
    frequencies = np.fft.fftfreq(n, d=1/fs)
    fft_values = fft(eeg_values)
    amplitudes = np.abs(fft_values)[:n // 2]
    frequencies = frequencies[:n // 2]

    band_powers = {
        'delta': np.mean(amplitudes[(frequencies >= 0.5) & (frequencies < 4)]),
        'theta': np.mean(amplitudes[(frequencies >= 4) & (frequencies < 8)]),
        'alpha': np.mean(amplitudes[(frequencies >= 8) & (frequencies < 13)]),
        'beta': np.mean(amplitudes[(frequencies >= 13) & (frequencies < 30)]),
        'gamma': np.mean(amplitudes[(frequencies >= 30) & (frequencies < 50)])
    }

    return band_powers

# Compare features between relaxation and problem-solving
def compare_features(relaxation_powers, problem_solving_powers):
    comparison = {}
    for band in relaxation_powers:
        comparison[band] = {
            'relaxation': relaxation_powers[band],
            'problem_solving': problem_solving_powers[band],
            'difference': problem_solving_powers[band] - relaxation_powers[band]
        }
    return comparison

# Main script
fs = 250  # Sampling rate

# Load and preprocess the data
relaxation_file = 'sean_data/raw_relax_sean_2.csv'
problem_solving_file = 'sean_data/raw_writing_sean_3.csv'

relaxation_data = load_and_preprocess(relaxation_file, fs)
problem_solving_data = load_and_preprocess(problem_solving_file, fs)

# Calculate band powers
relaxation_powers = calculate_band_powers(relaxation_data, fs)
problem_solving_powers = calculate_band_powers(problem_solving_data, fs)

# Compare features
comparison = compare_features(relaxation_powers, problem_solving_powers)

# Print comparison
for band, values in comparison.items():
    print(f"{band.capitalize()} Band:")
    print(f"  Relaxation: {values['relaxation']:.2f}")
    print(f"  Problem Solving: {values['problem_solving']:.2f}")
    print(f"  Difference: {values['difference']:.2f}")

# Optionally plot the amplitude spectrum for visual comparison
def plot_spectrum(eeg_values, title):
    n = len(eeg_values)
    frequencies = np.fft.fftfreq(n, d=1/fs)
    fft_values = fft(eeg_values)
    amplitudes = np.abs(fft_values)[:n // 2]
    frequencies = frequencies[:n // 2]

    plt.figure(figsize=(12, 6))
    plt.plot(frequencies, amplitudes, color='blue')
    plt.title(title)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    plt.xlim(0, 50)
    plt.grid()
    plt.show()

plot_spectrum(relaxation_data, 'EEG Amplitude Spectrum (Relaxation)')
plot_spectrum(problem_solving_data, 'EEG Amplitude Spectrum (Problem Solving)')
