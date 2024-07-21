import numpy as np
import pandas as pd
from scipy.signal import welch

def read_eeg_data(file_path):
    data = pd.read_csv(file_path)
    time = data.iloc[:, 0].values
    voltage = data.iloc[:, 1].values
    return time, voltage

def extract_features(voltage):
    # Time-domain features
    mean = np.mean(voltage)
    variance = np.var(voltage)
    peak_to_peak = np.ptp(voltage)
    
    # Frequency-domain features using Welch's method
    freqs, psd = welch(voltage, fs=100, nperseg=256)
    total_power = np.sum(psd)
    
    # Band powers
    delta_power = np.sum(psd[(freqs >= 0.5) & (freqs < 4)])
    theta_power = np.sum(psd[(freqs >= 4) & (freqs < 8)])
    alpha_power = np.sum(psd[(freqs >= 8) & (freqs < 12)])
    beta_power = np.sum(psd[(freqs >= 12) & (freqs < 30)])
    
    features = {
        'mean': mean,
        'variance': variance,
        'peak_to_peak': peak_to_peak,
        'total_power': total_power,
        'delta_power': delta_power,
        'theta_power': theta_power,
        'alpha_power': alpha_power,
        'beta_power': beta_power,
    }
    
    return features

# File paths
file_path1 = 'driving/raw_dad_driving_6.csv'
file_path2 = 'dad_data/raw_dad.csv'

# Read EEG data
_, voltage1 = read_eeg_data(file_path1)
_, voltage2 = read_eeg_data(file_path2)

# Extract features from both EEG signals
features1 = extract_features(voltage1)
features2 = extract_features(voltage2)

print("Features from Signal 1:")
print(features1)

print("\nFeatures from Signal 2:")
print(features2)
