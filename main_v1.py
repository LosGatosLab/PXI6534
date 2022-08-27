import pxi6534_gen
import time


sampling_clock = 1000000 ## set for 10MHz now 

flag = 0


data_gen = pxi6534_gen.pxi6534_gen(sampling_clock)
# time.sleep(10)
if flag == 0:
	input_arr1 = data_gen.write_FPGA_initial(["copy_RSOC_E2_Register_V2_no002_out_pad.tsv"])
	# input_arr1 = data_gen.write_FPGA_initial(["copy_RSOC_E2_Register_Everything_Off_out.tsv"])
	# data_gen.sw_logic_analyzer(input_arr1)
	print(input_arr1)
	data_gen.PXI6534_run(input_arr1)
	time.sleep(2)
if flag == 1:
	# input_arr1 = data_gen.write_FPGA_initial(["20220729_tx1_rx_all_on.tsv"])
	# input_arr1 = data_gen.write_FPGA_initial(["copy_RSOC_E2_Register_V2_no002_out.tsv"])

	# input_arr1 = data_gen.write_FPGA_initial(["copy_RSOC_E2_Register_Everything_Off_out.tsv"])
	# data_gen.sw_logic_analyzer(input_arr1)
	data_gen.PXI6534_run(input_arr1)
	time.sleep(2)

if flag == 2:
	input_arr1 = data_gen.write_doppler(["do_nothing.tsv","do_nothing.tsv"], 125e-6,1)
	data_gen.sw_logic_analyzer(input_arr1)
	data_gen.PXI6534_run(input_arr1)
	time.sleep(2)

if flag == 3:
##	    def write_chirp_only(file_to_write, num_of_chirp, trig_period, BUF_ENB, MUX, MUX_EN):
	input_arr1 = data_gen.write_chirp_only(file_to_write = ["do_nothing.tsv","do_nothing.tsv"], num_of_chirp = 1000, trig_period = 125e-6, BUF_ENB = 6, MUX = 0, MUX_EN = 1)
	data_gen.sw_logic_analyzer(input_arr1)
	data_gen.PXI6534_run(input_arr1)
	time.sleep(2)