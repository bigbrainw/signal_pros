#recorder
import serial
import csv
import time

# Serial port configuration
SERIAL_PORT = '/dev/cu.usbserial-10'
BAUD_RATE = 9600

# Initialize serial communication
ser = serial.Serial(SERIAL_PORT, BAUD_RATE)

# File to save raw data
output_file = 'raw_chien_5.csv'

# Open the CSV file for writing
with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Timestamp', 'EEG Value'])  # Write header

    print("Recording EEG data for 1 minutes.")

    start_time = time.time()
    duration = 1 * 60  # x minutes in seconds

    try:
        while True:
            current_time = time.time()
            elapsed_time = current_time - start_time
            if elapsed_time > duration:
                break


            data = ser.readline().decode('utf-8').strip()
            timestamp = time.time()
            writer.writerow([timestamp, data])
            print(f"{timestamp}, {data}")  # Print data to console

    except KeyboardInterrupt:
        print("Stopped recording due to manual interruption.")

print("Finished recording EEG data.")
