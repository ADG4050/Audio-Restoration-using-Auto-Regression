#Author : ADG4050
# This code was developed for purely academic purposes by (ADG4050) as part of the module of Computational Methods (5c22) in Trinity College Dublin
# main.py contains Median Filter, see separate file for Cubic Splines Interpolation

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
plt.subplot(3, 1, 1)
plt.plot(timer, data_clean / 2)
plt.title('clean signal')
plt.subplots_adjust(hspace=0.5)
plt.xlabel("Time[s]")
plt.ylabel("Amplitude")
# plt.show()

timeq = np.linspace(0.0, len(data), data.shape[0])
plt.subplot(3, 1, 2)
plt.plot(timeq, data)
plt.title('degraded signal')
plt.subplots_adjust(hspace=0.5)
plt.xlabel("Time[s]")
plt.ylabel("Amplitude")



# Step 4 : Importing the Detection file (Array of clicks [0,1]) from MATALB
mat = scipy.io.loadmat('detection.mat')
mat_list = list(mat.items())
detection = np.asarray(mat_list)[3][1][0]

# Step 5 : Initialising the window length parameter
wind_length = 3


# Step 6 : Median filter
""" Provides sorted median sequence for an array of length of window length """


def median_filter(inp_sig, wind_length):
    """Input Arguments = Input sequuence & Window length
    Returns = Modified sorted median sequence"""
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


# Step 7 : Main Function for audio restoration
"""Provides restored data for a degraded data, also calls in median filter function"""


def main(data, detection, wind_length):
    """Input Arguments : Degarded data from input audio source, Detection file data from MATLAB containing click location and window length. 
    Returns = Restored data without any clicks  """
    # Window length check - Has to be odd, error for even
    if (wind_length % 2 == 0):
        print('window length should always be odd, select again')
    else:
        index = np.where(detection == 1)
        data2 = data
        # passing window length through median filter and replacing the degraded data with restored data
        for i in index[0]:
            cons = int((wind_length - 1) / 2)
            dataset = data2[(i-(cons)): (i+(cons+1))]
            output = median_filter(dataset, wind_length)
            data2[(i-(cons)): (i+(cons+1))] = output

        restored = data2
    return restored


# Mean squared error calculation between two signal datasets function
def m_s_e(inp1, inp2):
    mse = np.sum(np.square(inp1 - inp2)) / (len(inp1) * len(inp2))
    return mse


# Step 8 : Calling Main Function through the progress bar calculator
for i in tqdm(range(100)):
    restored = main(data, detection, wind_length)
    sleep(0.1)



# Step 9 : writing out the restored audio (uncomment)
#write("restoredmf.wav", samplerate1, restored)


# Step 10 : Plotting the restored audio together with clean and degraded audio
timep = np.linspace(0.0, len(restored), restored.shape[0])
data_clean2 = (data_clean / 2)
plt.subplot(3, 1, 3)
plt.plot(timep, restored)
plt.title('restored signal')
plt.subplots_adjust(hspace=0.5)
plt.xlabel("Time[s]")
plt.ylabel("Amplitude")
plt.show()


# Step 11 : Playing the restorted audio
playsound('restoredmf.wav')
print('playing restored sound using  playsound')


# Step 12 : Calculation of MSE
mse2 = m_s_e(data_clean2, restored)
print('Mean Squared Error between clean and restored audio:', mse2)


# Step 13 : Displaying of Execution Time
et = time.time()
elapsed_time = et - st
print('Execution time for Median Filter:', elapsed_time, 'seconds')


# Step 14 : Unittest Checking
"""Two unit test performed (1) length checking (2) Inbuilt median function values = Designed median function values"""

class testcode(unittest.TestCase):
    """Length checking between resored signal length and degraded signal length"""
    def test_length(self):
        length1 = len(data)
        length2 = len(restored)
        self.assertEqual(length1, length2)

    def test_medfil(self):
        """Restored signal Value checked after passing through inbuilt function & compared with Designed function"""
        index = np.where(detection == 1)
        data3 = data
        for i in index[0]:
            cons = int((wind_length - 1) / 2)
            dataset2 = data3[(i-(cons)): (i+(cons+1))]
            output2 = scipy.signal.medfilt(dataset2, kernel_size=wind_length)
            data3[(i-(cons)): (i+(cons+1))] = output2
        ckc2 = np.array_equal(restored, data3)


if __name__ == "__main__":
    unittest.main(argv=['first-arg-is-ignored'], exit=False)

print("DONE")
