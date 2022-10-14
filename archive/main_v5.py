import pxi6534_gen
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
import nidaqmx
from nidaqmx.constants import LineGrouping
from nidaqmx.constants import Edge
from nidaqmx.constants import AcquisitionType
from nidaqmx.constants import DigitalDriveType
from nidaqmx.constants import Polarity
from nidaqmx.constants import Level
from nidaqmx.constants import RegenerationMode

################# Define the capturing parameters  ########
sampling_clock = 500000 ## set for 10MHz now 
num_of_doppler = 1031
points_per_cycle = 6500
num_cycles = num_of_doppler*27

prescaler = 4;
capture_fs = 100e6/(prescaler+1)
capture_margin = 0/(prescaler+1)
capture_points = 6400/(prescaler+1)+2*capture_margin
capture_delay = 3600/(prescaler+1)-capture_margin
list_chn = range(1,9)

num_run = 16

################ PXI-6534 Data Preparation ########
data_gen_initial = pxi6534_gen.pxi6534_gen(sampling_clock)
input_arr_init = data_gen_initial.write_FPGA_initial(["20220831_tx8_rx_all_on_div_off.tsv"])
data_gen_run = pxi6534_gen.pxi6534_gen(sampling_clock)
file_to_write = ['tx_8.tsv',"tx_0.tsv","tx_1.tsv","tx_2.tsv","tx_3.tsv","tx_4.tsv","tx_5.tsv","tx_6.tsv","tx_7.tsv","tx_8.tsv"]
input_arr_run = data_gen_run.write_doppler(file_to_write,130e-6,num_of_doppler)

################ PXI-6534 Reset ########
pxi6534 = nidaqmx.system.device.Device('Dev36')
pxi6534.reset_device()

task = nidaqmx.Task()
do_channel = task.do_channels.add_do_chan('Dev36/port0:3',line_grouping=LineGrouping.CHAN_FOR_ALL_LINES)
# task.timing.cfg_burst_handshaking_timing_export_clock(data_gen_run.sampling_clock, sample_clk_outp_term = '/Dev36/PXI_Trig5', sample_mode=AcquisitionType.FINITE, samps_per_chan=2+len(input_arr_run), sample_clk_pulse_polarity=Polarity.ACTIVE_HIGH, pause_when=Level.HIGH, ready_event_active_level=Polarity.ACTIVE_HIGH)

######### RSOC Initialization ##############
do_channel.do_use_only_on_brd_mem = False
task.timing.cfg_samp_clk_timing(sampling_clock, active_edge=Edge.RISING, sample_mode=AcquisitionType.FINITE,samps_per_chan=2+len(input_arr_init))
samples_written = task.write(input_arr_init, auto_start=True)
time.sleep(0.5)
task.stop()
print('RSOC initilized! ('+datetime.now().strftime("%H:%M:%S")+")")
# time.sleep(1)

################# Initialize Matlab Engine  ########
eng = matlab.engine.start_matlab()
eng.cd(r'C:\LP_Lab\RSOC2\Matlab\RSOC_Data_Processing_M3100A')
print('Matlab engine initilized! ('+datetime.now().strftime("%H:%M:%S")+")")

################# Initialize M3100A ########
pxi_scope = M3100A.M3100A(capture_points, num_cycles, capture_delay, list_chn, prescaler)
print('M3100A DAQ initilized! ('+datetime.now().strftime("%H:%M:%S")+")")

######### Chirp Sequence Init ###################
do_channel.do_use_only_on_brd_mem = True
task.timing.cfg_samp_clk_timing(sampling_clock, active_edge=Edge.RISING, sample_mode=AcquisitionType.FINITE, samps_per_chan=2+len(input_arr_run))
task.out_stream.regen_mode = RegenerationMode.ALLOW_REGENERATION
# time.sleep(0.5)
samples_written = task.write(input_arr_run, auto_start=False)
print(task.out_stream.regen_mode)
print(do_channel.do_use_only_on_brd_mem)
print('Chirp sequence initilized! ('+datetime.now().strftime("%H:%M:%S")+")")
time.sleep(5)

################# Start Data Capture ########
print('Capture Start! ('+datetime.now().strftime("%H:%M:%S")+")")
BlockData = [ [0]*int(capture_points*num_cycles) for i in range(len(list_chn))]
for i in range(num_run):
	pxi_scope.daq_start()
	# print(task.out_stream.curr_write_pos)
	task.start()
	time.sleep(4)
	# print(task.out_stream.curr_write_pos)
	task.stop()
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
Raw_sig_9 = eng.M3100A_Resample_9(BlockData,capture_points,1024)
Raw_sig = eng.data_reform(Raw_sig_9,1)
T0 = capture_delay/capture_fs
Fs = capture_fs*4/5
file_path = file_dir_data+"\\"+'Raw_sig_9.mat'
mdic = {"Raw_sig_9": Raw_sig_9, "T0": T0, "Fs": Fs}
savemat(file_path, mdic)
file_path = file_dir_data+"\\"+'Raw_sig.mat'
mdic = {"Raw_sig": Raw_sig, "T0": T0, "Fs": Fs}
savemat(file_path, mdic)

################# Release Memory ########
print("Finished and Realse Memory. ("+datetime.now().strftime("%H:%M:%S")+")")
del BlockData
del Raw_sig_9
del Raw_sig
del Data
gc.collect()

# ####### 
eng.quit()