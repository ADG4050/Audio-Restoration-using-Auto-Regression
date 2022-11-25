import numpy as np
import matplotlib.pyplot as plt
import scipy
from scipy.io import wavfile
import scipy.io
from scipy.io.wavfile import write
from time import sleep
from tqdm import tqdm
import time
import unittest

# get the start time
st = time.time()

samplerate2, data_clean = wavfile.read('clean.wav')
samplerate1, data = wavfile.read('degraded.wav')

mat = scipy.io.loadmat('detection.mat')
mat_list = list(mat.items())
detection = np.asarray(mat_list)[3][1][0]

wind_length = 3

timep = np.linspace(0.0, len(data), data.shape[0])
plt.figure(figsize=(15, 5))
plt.plot(timep, data, label='degraded signal')
plt.xlabel("Time[s]")
plt.ylabel("Amplitude")
plt.show()

index = np.where(detection == 1)

data2 = data
print(len(data2))
y_ind = np.arange(len(data2))
print(y_ind)

Y_ind = np.delete(data2, index)
print(len(Y_ind))
#print(Y_ind[350:360])

X_ind = np.delete(y_ind, index)
print(len(X_ind))

from scipy.interpolate import CubicSpline
setdata = CubicSpline(X_ind, Y_ind, bc_type='not-a-knot', extrapolate=None)

for i in tqdm(range(100)):
    sleep(0.1)

for i in range(len(index)):
  data2[index[i]] = setdata(index)[i]

#write("restored_cs.wav", samplerate1, data2)

timeq = np.linspace(0.0, len(data2), data.shape[0])
plt.figure(figsize=(15, 5))
plt.plot(timeq, data2, label='degraded signal')
plt.xlabel("Time[s]")
plt.ylabel("Amplitude")
plt.show()


mse = np.sum(np.square(data_clean - data2)) / len(data_clean)
print(mse)

# get the end time
et = time.time()

elapsed_time = et - st
print('Execution time for Cubic Spline Interpolation:', elapsed_time, 'seconds')

print("DONE")