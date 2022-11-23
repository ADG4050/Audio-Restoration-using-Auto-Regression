import numpy as np
import matplotlib.pyplot as plt
import scipy
from scipy.io import wavfile
import scipy.io
from scipy.io.wavfile import write
import median_filter as mf
from time import sleep
from tqdm import tqdm
import time

# get the start time
st = time.time()

samplerate2, data_clean = wavfile.read('clean.wav')
samplerate1, data = wavfile.read('degraded.wav')


timeq = np.linspace(0.0, len(data), data.shape[0])
plt.figure(figsize=(15, 5))
plt.plot(timeq, data, label='degraded signal')
plt.xlabel("Time[s]")
plt.ylabel("Amplitude")
plt.show()

mat = scipy.io.loadmat('detection.mat')
mat_list = list(mat.items())
detection = np.asarray(mat_list)[3][1][0]

wind_length = 3

import numpy as np
import scipy

# function for medial filtering


def median_filter(inp_sig, wind_length):
    # zero padding added as per window length
    pad = int((wind_length - 1)/2)
    inp_sig2 = np.pad(inp_sig, (pad, pad), 'constant',
                      constant_values=(0, 0))
    # selecting, sorting and taking out the median value
    l = len(inp_sig2)
    arr1 = []
    for i in range(0, l-(wind_length - 1)):
        arr = inp_sig2[i:wind_length+i]
        srt_arr = sorted(arr)
        middleIndex = int((len(srt_arr) - 1)/2)
        srt_arr = srt_arr[middleIndex]
        arr1.append(srt_arr)

    return (arr1)



def main(data, detection, wind_length):
    if (wind_length % 2 == 0):
        print('window length should always be odd, select again')
    else:
        index = np.where(detection == 1)
        for i in index[0]:
            cons = int((wind_length - 1) / 2)
            dataset = data[(i-(cons)): (i+(cons))]
            output = median_filter(dataset, wind_length)
            data[(i-(cons)): (i+(cons))] = output

        restored = data
    return restored

#if __name__ == "__main__":
for i in tqdm(range(100)):
    restored = main(data, detection, wind_length)
    #write("restored.wav", samplerate1, restored)
    sleep(0.1)

timep = np.linspace(0.0, len(restored), restored.shape[0])
plt.figure(figsize=(15, 5))
plt.plot(timep, restored, label='restored signal')
plt.xlabel("Time[s]")
plt.ylabel("Amplitude")
plt.show()

# get the end time
et = time.time()

elapsed_time = et - st
print('Execution time for Median Filter:', elapsed_time, 'seconds')

print("DONE")