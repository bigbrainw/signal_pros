# Alpha, Beta, and Theta Wave Data Logger

## Overview
This script reads alpha, beta, and theta wave data from an Arduino, processes it, and logs the results into a CSV file.

## Requirements
- matplotlib==3.8.2
- numpy==2.0.0
- pyserial==3.5
- scipy==1.14.0

## Setup

### 1. Install required libraries
- Open a terminal or command prompt.
- Run the following command to install the necessary Python libraries:
    ```bash
    pip install pyserial numpy
    ```

### 2. Connect Arduino
- Ensure your Arduino is properly connected to your computer.
- Identify the correct serial port your Arduino is connected to (e.g., `/dev/cu.usbserial-10` on macOS or `COM3` on Windows).
- Update the serial port in the script to match your system's port:
    ```python
    ser = serial.Serial('/dev/cu.usbserial-10', 9600)
    ```

### 3. Update CSV File Path
- Ensure the `csv_file_path` variable is set to the desired file name and location where data will be logged:
    ```python
    csv_file_path = 'fp1mastoid_workin630.csv'
    ```

## Usage

### Run the script
- Open a terminal or command prompt.
- Navigate to the directory containing the script.
- Execute the script with the following command:
    ```bash
    python script_name.py
    ```

## Notes
- Data is logged to `fp1mastoid_workin630.csv`.
- Interrupt the script with `Ctrl+C` to stop it gracefully, ensuring the CSV file and serial connection are properly closed.
