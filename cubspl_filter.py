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
from playsound import playsound
from scipy.interpolate import CubicSpline

# get the start time
st = time.time()

samplerate2, data_clean = wavfile.read('clean.wav')
samplerate1, data = wavfile.read('degraded.wav')

#playsound('degraded.wav')
#print('playing degraded sound using  playsound')


timer = np.linspace(0.0, len(data_clean), data_clean.shape[0])
plt.subplot(2,1,1)
plt.plot(timer, data_clean / 2)
plt.title('clean signal')
plt.subplots_adjust(hspace = 0.5)
plt.xlabel("Time[s]")
plt.ylabel("Amplitude")
#plt.show()

timeq = np.linspace(0.0, len(data), data.shape[0])
plt.subplot(2,1,2)
plt.plot(timeq, data)
plt.title('degraded signal')
plt.subplots_adjust(hspace = 0.5)
plt.xlabel("Time[s]")
plt.ylabel("Amplitude")
#plt.show()

def m_s_e(inp1, inp2):
    mse = ((np.sum(np.square(inp1 - inp2)) / len(inp1)))/1000
    return mse

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

def m_s_e(inp1, inp2):
    mse = np.sum(np.square(inp1 - inp2)) / (len(inp1) * len(inp2))
    return mse


index = np.where(detection == 1)

data2 = data
print(len(data2))
y_ind = np.arange(len(data2))
#print(y_ind)

Y_ind = np.delete(data2, index)
print(len(Y_ind))
#print(Y_ind[350:360])

X_ind = np.delete(y_ind, index)
#print(len(X_ind))


setdata = CubicSpline(X_ind, Y_ind, bc_type='not-a-knot', extrapolate=None)

for i in tqdm(range(100)):
    sleep(0.1)

for i in range(len(index)):
  data2[index[i]] = setdata(index)[i]

#write("restoredcs.wav", samplerate1, data2)

timep = np.linspace(0.0, len(data2), data2.shape[0])
data_clean2 = (data_clean / 2) 
plt.plot(timep, data2)
plt.title('restored signal')
plt.subplots_adjust(hspace = 0.5)
plt.xlabel("Time[s]")
plt.ylabel("Amplitude")
plt.show()

#playsound('restoredcs.wav')
# print('playing restored sound using  playsound')

mse2 = m_s_e(data_clean2, data2) 
print('Mean Squared Error between clean and restored audio:', mse2)

# get the end time
et = time.time()

elapsed_time = et - st
print('Execution time for Cubic Spline Interpolation:', elapsed_time, 'seconds')

print("DONE")