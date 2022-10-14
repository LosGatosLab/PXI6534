import M3100A_Digitizer as M3100A

import time
from datetime import datetime
import os
import numpy as np 
import matplotlib.pyplot as plt
import matlab.engine
from scipy.io import savemat
import keyboard
import gc
import subprocess 
import paramiko

################# Define the capturing parameters  ########
num_of_doppler = 256
num_cycles = num_of_doppler*24

prescaler = 4;
capture_fs = 100e6/(prescaler+1)
capture_margin = 0/(prescaler+1)
capture_points = 6400/(prescaler+1)+2*capture_margin
capture_delay = 3600/(prescaler+1)-capture_margin
list_chn = range(1,9)

num_run = 1

################# Initialize Matlab Engine  ########
eng = matlab.engine.start_matlab()
eng.cd(r'C:\LP_Lab\RSOC2\Matlab\RSOC_Data_Processing_M3100A')
print('Matlab engine initilized! ('+datetime.now().strftime("%H:%M:%S")+")")

################# Setup SSH Connection to FPGA  ########
# host,port = "10.1.21.197",22
host,port = "10.1.21.173",22
username,password = "ubuntu","Porsche1"
client = paramiko.client.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(host, username=username, password=password)
print('FPGA connection established! ('+datetime.now().strftime("%H:%M:%S")+")")

################# Initialize M3100A ########
pxi_scope = M3100A.M3100A(capture_points, num_cycles, capture_delay, list_chn, prescaler)
print('M3100A DAQ initilized! ('+datetime.now().strftime("%H:%M:%S")+")")

################# Start Data Capture ########
print('Capture Start! ('+datetime.now().strftime("%H:%M:%S")+")")
BlockData = [ [0]*int(capture_points*num_cycles) for i in range(len(list_chn))]
for i in range(num_run):
	client.exec_command('./run_rsoc.sh')
	pxi_scope.daq_start()
	pxi_scope.daq_wait(list_chn[0])
	for idx_chn in list_chn:
		Data = pxi_scope.daq_acqisition(idx_chn)
		BlockData[idx_chn-1] = BlockData[idx_chn-1] + Data
	print('**** Capture Progress ('+datetime.now().strftime("%H:%M:%S")+'): RUN-'+str(i+1)+'/'+str(num_run)+' ****')
BlockData = np.array(BlockData)/num_run
print('Capture Finished! ('+datetime.now().strftime("%H:%M:%S")+")")

################# Create File Directory  ########
file_dir_data = r"C:\To_Share\Captured_Data\M3100A"+"\\"+datetime.now().strftime("%m%d")+"\\"+datetime.now().strftime("%H%M%S")
# Check whether the specified path exists or not
isExist = os.path.exists(file_dir_data)
if not isExist:
  os.makedirs(file_dir_data)
print("*** Save Path: "+file_dir_data+" ***")

# ################# Raw BlockData Saving (Single .mat file) ########
# print("Start BlockData Saving. ("+datetime.now().strftime("%H:%M:%S")+")")
# file_path = file_dir_data+"\\"+'BlockData.mat'
# BlockData = np.array(BlockData)
# T0 = capture_delay/capture_fs
# Fs = capture_fs
# # tstamp = np.arange(capture_delay/capture_fs,(capture_delay+capture_points)/capture_fs,1/capture_fs)
# mdic = {"BlockData": BlockData, "T0": T0, "Fs": Fs, "capture_points": capture_points}
# savemat(file_path, mdic)

################# Call Matlab ########
print("Start Matlab Processing. ("+datetime.now().strftime("%H:%M:%S")+")")
BlockData = matlab.double(BlockData)
Raw_sig = eng.M3100A_Resample_FPGA(BlockData,capture_points,num_of_doppler)
T0 = capture_delay/capture_fs
Fs = capture_fs*4/5
file_path = file_dir_data+"\\"+'Raw_sig.mat'
mdic = {"Raw_sig": Raw_sig, "T0": T0, "Fs": Fs}
savemat(file_path, mdic)

################# Release Memory ########
print("Finished and Realse Memory. ("+datetime.now().strftime("%H:%M:%S")+")")
del BlockData
del Raw_sig
del Data
gc.collect()

# ####### 
eng.quit()