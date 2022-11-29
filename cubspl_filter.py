#Author : ADG4050
# This code was developed for purely academic purposes by (ADG4050) as part of the module of Computational Methods (5c22) in Trinity College Dublin
# This file is for Cubic Splines Interpolation, For main.py containaining Median Filter, refer main.py


# Step 1 import all neccessary modules
import numpy as np
import matplotlib.pyplot as plt
import scipy
from scipy.io import wavfile  # reading wavfile
import scipy.io
from scipy.io.wavfile import write  # writing wavfile
from time import sleep  # Progress bar imports
from tqdm import tqdm  # Execution TIme imports
import time  # Execution TIme imports
import unittest  # Unittest imports
from playsound import playsound  # Playsound imports
from scipy.interpolate import CubicSpline  # In-built cubic spline function

# Start time for computing the execution time
st = time.time()

# Step 2 : Import clean and degraded audios
samplerate2, data_clean = wavfile.read('clean.wav')
samplerate1, data = wavfile.read('degraded.wav')

# Playing the degraded audio
playsound('degraded.wav')
print('playing degraded sound using  playsound')

# Step 3 : Preparing the graphs from clean and degraded audio's but holding it for final subplot
timer = np.linspace(0.0, len(data_clean), data_clean.shape[0])
plt.subplot(2, 1, 1)
plt.plot(timer, data_clean / 2)
plt.title('clean signal')
plt.subplots_adjust(hspace=0.5)
plt.xlabel("Time[s]")
plt.ylabel("Amplitude")
# plt.show()

timeq = np.linspace(0.0, len(data), data.shape[0])
plt.subplot(2, 1, 2)
plt.plot(timeq, data)
plt.title('degraded signal')
plt.subplots_adjust(hspace=0.5)
plt.xlabel("Time[s]")
plt.ylabel("Amplitude")
plt.show()


# Mean squared error calculation between two signal datasets function
def m_s_e(inp1, inp2):
    mse = np.sum(np.square(inp1 - inp2)) / (len(inp1) * len(inp2))
    return mse


# Step 4 : Initialising the window length parameter
wind_length = 3

# Step 5 : Importing the Detection file (Array of clicks [0,1]) from MATALB
mat = scipy.io.loadmat('detection.mat')
mat_list = list(mat.items())
detection = np.asarray(mat_list)[3][1][0]

# Step 6 : Cubic Spline Function Initialisation
"""Creating X indices and Y indices for Cubic Spline Function
X indices = Array of indices of the length of degraded data without clicks location
Y indices = Array of Signal Data of the length degraded data without the click data"""
index = np.where(detection == 1)
data2 = data
arx = np.arange(len(data2))
Y_ind = np.delete(data2, index)
X_ind = np.delete(arx, index)


# Step 7 : Applying Cubic Spline Function through a progress bar design
for i in tqdm(range(100)):
    setdata = CubicSpline(X_ind, Y_ind, bc_type='not-a-knot', extrapolate=None)
    sleep(0.1)


# Step 8 : Replacing the clicks data with the spline data prediction
for i in range(len(index)):
    data2[index[i]] = setdata(index)[i]

# Step 9 : writing out the restored audio (uncomment)
#write("restoredcs.wav", samplerate1, data2)

# Step 10 : Plotting the restored audio together with clean and degraded audio
timep = np.linspace(0.0, len(data2), data2.shape[0])
data_clean2 = (data_clean / 2)
plt.plot(timep, data2)
plt.title('restored signal')
plt.subplots_adjust(hspace=0.5)
plt.xlabel("Time[s]")
plt.ylabel("Amplitude")
plt.show()

# Step 11 : Playing the restorted audio
playsound('restoredcs.wav')
print('playing restored sound using  playsound')

# Step 12 : Calculation of MSE
mse2 = m_s_e(data_clean2, data2)
print('Mean Squared Error between clean and restored audio:', mse2)

# Step 13 : Displaying of Execution Time
et = time.time()
elapsed_time = et - st
print('Execution time for Cubic Spline Interpolation:', elapsed_time, 'seconds')

print("DONE")
