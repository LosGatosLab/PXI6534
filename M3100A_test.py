import M3100A_Digitizer as M3100A
import numpy as np 
import matplotlib.pyplot as plt



points_per_cycle = 6500
num_cycles = 256*27
delay_in = 3800
pxi_scope = M3100A.M3100A(points_per_cycle, num_cycles, delay_in)
data_read = pxi_scope.acqisition_wait(1)
# data_list = pxi_scope.acqisition_wait(1)
print(type(data_read))
# fig, ax = plt.subplots()
# ax.plot(data_read)
# plt.show()
data_list = list(data_read)
print(len(data_list))
results = []
for i in range(0, num_cycles, 27):
	_temp = []
	for j in range(points_per_cycle):
		_temp.append(data_read[i*points_per_cycle+j])
	results.append(_temp)

######### Averaging ##########
index1 = [i for i in range(points_per_cycle)]
Averaged = [0 for i in range(points_per_cycle)]
for i in range(points_per_cycle):
	for j in range(len(results)):
		Averaged[i]+=results[j][i]
	Averaged[i] = Averaged[i]/len(results)
fig, ax = plt.subplots()
ax.plot(index1, Averaged)
ax.plot(index1, results[0])
ax.plot(index1, results[1])
# ax.plot(index1, results[2])
# ax.plot(index1, results[3])
# ax.plot(index1, results[4])
# ax.plot(index1, results[5])

plt.show()

######### fft ############
arr_averaged = np.array(Averaged)
arr_windowed = arr_averaged*np.hanning(arr_averaged.size)
N = arr_windowed.size
pad_zero = 15*N
arr_windowed = np.pad(arr_windowed,(0,pad_zero),'constant',constant_values=(0,0))
fft_averaged = np.fft.fft(arr_averaged)
fft_windowed = np.fft.fft(arr_windowed)
psd_averaged = np.abs(fft_averaged)**2
psd_windowed = np.abs(fft_windowed)**2


fs = 100*1000000
time_step = float(1/fs)
freq = np.fft.fftfreq(arr_windowed.size,time_step)
print('fft drawing')
print(freq.size)
print(psd_averaged.size)
fig, ax = plt.subplots()
# ax.plot(freq[0:points_per_cycle//2], psd_averaged[0:points_per_cycle//2])
ax.plot(freq[0:points_per_cycle//2], psd_windowed[0:points_per_cycle//2])
plt.yscale("log")  
plt.xlim(200000,2000000)
plt.show()