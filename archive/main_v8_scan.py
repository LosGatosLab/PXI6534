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
from nidaqmx.stream_writers import (
    DigitalSingleChannelWriter, DigitalMultiChannelWriter)
import Motor_module_for_GUI as motor


############# initiallize motor ################
m = motor.motor_ctrl()

################# Define the capturing parameters  ########
sampling_clock = 500000 ## set for 10MHz now 
num_of_doppler = 1030
points_per_cycle = 6500
num_cycles = num_of_doppler*27

prescaler = 4;
capture_fs = 100e6/(prescaler+1)
capture_margin = 0/(prescaler+1)
capture_points = 6400/(prescaler+1)+2*capture_margin
capture_delay = 3600/(prescaler+1)-capture_margin
list_chn = range(1,9)

num_run = 160

######### RSOC Initialization ##############
data_gen_initial = pxi6534_gen.pxi6534_gen(sampling_clock)
input_arr_init = data_gen_initial.write_FPGA_initial(["20220831_tx8_rx_all_on_div_off.tsv"])
data_gen_initial.PXI6534_run(input_arr_init, 2+len(input_arr_init))
print('RSOC initilized!')
time.sleep(1)

################# Initialize Matlab Engine  ########
eng = matlab.engine.start_matlab()
eng.cd(r'C:\LP_Lab\RSOC2\Matlab\RSOC_Data_Processing_M3100A')

######### Chirp Sequence Init ###################
data_gen_run = pxi6534_gen.pxi6534_gen(sampling_clock)
file_to_write = ['tx_8.tsv',"tx_0.tsv","tx_1.tsv","tx_2.tsv","tx_3.tsv","tx_4.tsv","tx_5.tsv","tx_6.tsv","tx_7.tsv","tx_8.tsv"]
input_arr_run = data_gen_run.write_doppler(file_to_write,130e-6,num_of_doppler)
# input_arr_run = np.array(input_arr_run)
# data_gen_run.sw_logic_analyzer(input_arr_run)

################# Initialize M3100A ########
pxi_scope = M3100A.M3100A(capture_points, num_cycles, capture_delay, list_chn, prescaler)

################# Create File Directory  ########
file_dir_data = r"C:\To_Share\Captured_Data\M3100A"+"\\"+datetime.now().strftime("%m%d")+"\\"+datetime.now().strftime("%H%M%S")
# Check whether the specified path exists or not
isExist = os.path.exists(file_dir_data)
if not isExist:
  os.makedirs(file_dir_data)
print("*** Save Path: "+file_dir_data+" ***")


##### Test ####
task = nidaqmx.Task()
do_channel = task.do_channels.add_do_chan('Dev36/port0:3',line_grouping=LineGrouping.CHAN_FOR_ALL_LINES)
task.timing.cfg_burst_handshaking_timing_export_clock(data_gen_run.sampling_clock, sample_clk_outp_term = '/Dev36/PXI_Trig5', sample_mode=AcquisitionType.CONTINUOUS, samps_per_chan = len(input_arr_run), sample_clk_pulse_polarity=Polarity.ACTIVE_HIGH, pause_when=Level.HIGH, ready_event_active_level=Polarity.ACTIVE_HIGH)
task.out_stream.regen_mode = RegenerationMode.ALLOW_REGENERATION
# task.out_stream.output_buf_size = len(input_arr_run)
DSW = DigitalSingleChannelWriter(task.out_stream)
DSW.auto_start = False
do_channel.do_use_only_on_brd_mem = True
DSW.write_many_sample_port_uint32(np.array(input_arr_run,dtype=np.uint32))
time.sleep(5)
print('input arr length :' +str(len(input_arr_run)))


# DSW.auto_start = True
# task.start()
# samples_written = task.write(input_arr_run, auto_start=False)
######### Scan ##########################
step = 80
counter = 0
total_run = 30

for _scan in range(total_run):
	################# Start Data Capture ########
	BlockData = [ [0]*int(capture_points*num_cycles) for i in range(len(list_chn))]
	for i in range(num_run):
		pxi_scope.daq_start()
		# print('**** time1: ('+datetime.now().strftime("%H:%M:%S")+'): RUN-'+str(i+1)+'/'+str(num_run)+' ****')
		# DSW.write_many_sample_port_uint32(np.array(input_arr_run,dtype=np.uint32))
		task.start()
		# print('**** time2: ('+datetime.now().strftime("%H:%M:%S")+'): RUN-'+str(i+1)+'/'+str(num_run)+' ****')
		time.sleep(4)
		task.stop()
		pxi_scope.daq_wait(list_chn[0])
		for idx_chn in list_chn:
			Data = pxi_scope.daq_acqisition(idx_chn)
			BlockData[idx_chn-1] = BlockData[idx_chn-1] + Data
		print('**** Capture Progress ('+datetime.now().strftime("%H:%M:%S")+'): RUN-'+str(i+1)+'/'+str(num_run)+' ****')
	BlockData = np.array(BlockData)/num_run

	# task.stop()
	# ################# Raw BlockData Saving (Single .mat file) ########
	# print("Start BlockData Saving. ("+datetime.now().strftime("%H:%M:%S")+")")
	# file_path = file_dir_data+"\\"+'BlockData.mat'
	# BlockData = np.array(BlockData)
	# T0 = capture_delay/capture_fs
	# Fs = capture_fs
	# # tstamp = np.arange(capture_delay/capture_fs,(capture_delay+capture_points)/capture_fs,1/capture_fs)
	# mdic = {"BlockData": BlockData, "T0": T0, "Fs": Fs, "capture_points": capture_points}
	# savemat(file_path, mdic)
	######## scanner move ####
	if (_scan < 15):
		m.move_X_positive(step)
	else:
		m.move_Y_negative(step)



	################# Call Matlab ########
	print("Start Matlab Processing. ("+datetime.now().strftime("%H:%M:%S")+")")
	BlockData = matlab.double(BlockData)
	Raw_sig_9 = eng.M3100A_Resample_9(BlockData,capture_points,1024)
	Raw_sig = eng.data_reform(Raw_sig_9,1)
	T0 = capture_delay/capture_fs
	Fs = capture_fs*4/5
	file_path = file_dir_data+"\\"+str(_scan)+'_Raw_sig_9.mat'
	mdic = {"Raw_sig_9": Raw_sig_9, "T0": T0, "Fs": Fs}
	savemat(file_path, mdic)
	file_path = file_dir_data+"\\"+str(_scan)+'_Raw_sig.mat'
	mdic = {"Raw_sig": Raw_sig, "T0": T0, "Fs": Fs}
	savemat(file_path, mdic)

	################# Release Memory ########
	print("Finished and Realse Memory. ("+datetime.now().strftime("%H:%M:%S")+")")
	del BlockData
	del Raw_sig_9
	del Raw_sig
	del Data
	gc.collect()


for i in range(total_run//2):
	m.move_Y_positive(step)
for i in range(total_run//2):
	m.move_X_negative(step)

# ####### 
eng.quit()