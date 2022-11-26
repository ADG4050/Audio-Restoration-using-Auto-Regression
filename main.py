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
import unittest
from playsound import playsound

# get the start time
st = time.time()

samplerate2, data_clean = wavfile.read('clean.wav')
samplerate1, data = wavfile.read('degraded.wav')

#playsound('degraded.wav')
#print('playing degraded sound using  playsound')

# data = data - np.mean(data)


timer = np.linspace(0.0, len(data_clean), data_clean.shape[0])
plt.subplot(3,1,1)
plt.plot(timer, data_clean / 2)
plt.title('clean signal')
plt.subplots_adjust(hspace = 0.5)
plt.xlabel("Time[s]")
plt.ylabel("Amplitude")
#plt.show()


timeq = np.linspace(0.0, len(data), data.shape[0])
plt.subplot(3,1,2)
plt.plot(timeq, data)
plt.title('degraded signal')
plt.subplots_adjust(hspace = 0.5)
plt.xlabel("Time[s]")
plt.ylabel("Amplitude")
#plt.show()

mat = scipy.io.loadmat('detection.mat')
mat_list = list(mat.items())
detection = np.asarray(mat_list)[3][1][0]

wind_length = 3


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

def m_s_e(inp1, inp2):
    mse = np.sum(np.square(inp1 - inp2)) / (len(inp1) * len(inp2))
    return mse

def main(data, detection, wind_length):
    if (wind_length % 2 == 0):
        print('window length should always be odd, select again')
    else:
        index = np.where(detection == 1)
        data2 = data
        for i in index[0]:
            cons = int((wind_length - 1) / 2)
            dataset = data2[(i-(cons)): (i+(cons))]
            output = median_filter(dataset, wind_length)
            data2[(i-(cons)): (i+(cons))] = output

        restored = data2
    return restored






for i in tqdm(range(100)):
    restored = main(data, detection, wind_length)
    sleep(0.1)


#write("restoredmf.wav", samplerate1, restored)

timep = np.linspace(0.0, len(restored), restored.shape[0])
data_clean2 = (data_clean / 2) 
plt.subplot(3,1,3)
plt.plot(timep, restored)
plt.title('restored signal')
plt.subplots_adjust(hspace = 0.5)
plt.xlabel("Time[s]")
plt.ylabel("Amplitude")
plt.show()

#playsound('restoredmf.wav')
#print('playing restored sound using  playsound')

mse2 = m_s_e(data_clean2, restored) 
print('Mean Squared Error between clean and restored audio:', mse2)

# get the end time
et = time.time()

elapsed_time = et - st
print('Execution time for Median Filter:', elapsed_time, 'seconds')


class testcode(unittest.TestCase):
    def test_length(self):
        length1 = len(data)
        length2 = len(restored)
        self.assertEqual(length1, length2)


    def test_medfil(self):
        
        index = np.where(detection == 1)
        data3 = data
        for i in index[0]:
            cons = int((wind_length - 1) / 2)
            dataset2 = data3[(i-(cons)): (i+(cons))]
            output2 = scipy.signal.medfilt(dataset2, kernel_size=wind_length)
            data3[(i-(cons)): (i+(cons))] = output2     
        ckc2 = np.array_equal(restored, data3)

if __name__ == "__main__":
    unittest.main(argv=['first-arg-is-ignored'], exit=False)


print("DONE")