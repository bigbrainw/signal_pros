import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# Replace 'COM3' with the appropriate serial port
ser = serial.Serial('/dev/cu.usbserial-110', 9600)

# Function to read data from the serial port
def read_serial_data():
    try:
        data = ser.readline().decode('utf-8').strip()
        return float(data)
    except:
        return 0.0

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
    x_data.append(len(x_data))
    y_data.append(y)
    
    # Limit the x_data to the last 100 points
    x_data_plot = x_data[-100:]
    y_data_plot = y_data[-100:]
    
    line.set_data(x_data_plot, y_data_plot)
    ax.set_xlim(x_data_plot[0], x_data_plot[-1])
    return line,

# Create the animation
ani = animation.FuncAnimation(fig, update, init_func=init, blit=True, interval=50)

plt.show()
