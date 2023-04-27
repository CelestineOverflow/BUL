import numpy as np
import matplotlib.pyplot as plt
import serial
import pandas as pd

port = 'COM3'
baud = 9600
ser = serial.Serial(port, baud, timeout=1)
data


plt.axis([0, 10, 0, 1])

for i in range(10):
    y = np.random.random()
    plt.scatter(i, y)
    plt.pause(0.05)

plt.show()


