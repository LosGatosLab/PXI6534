import pxi6534_gen
import time


sampling_clock = 500000 ## set for 10MHz now 

flag = 2

data_gen = pxi6534_gen.pxi6534_gen(sampling_clock)
# time.sleep(10)
if flag == 0:
	# input_arr1 = data_gen.write_FPGA_initial(["copy_RSOC_E2_Register_+V2_no002_out.tsv"])
	# input_arr1 = data_gen.write_FPGA_initial(["init_div_off.tsv"])
	# input_arr1 = data_gen.write_FPGA_initial(["20220831_tx8_rx_all_on_div_off.tsv"])
	# input_arr1 = data_gen.write_FPGA_initial(["tx_1.tsv"])

	input_arr1 = data_gen.write_FPGA_initial(["copy_RSOC_E2_Register_Everything_Off_out.tsv"])
	# data_gen.sw_logic_analyzer(input_arr1)

	# print(input_arr1)
	# for i in range(0,len(input_arr1)-1,2):
	# 	data_gen.PXI6534_run([838796543, 838796799,input_arr1[i],input_arr1[i+1]])
	# 	time.sleep(0.01)
	print('input_arr1_size: '+str(len(input_arr1)))
	data_gen.PXI6534_run(input_arr1, 2+len(input_arr1))
	# data_gen.PXI6534_run(input_arr1, 256)
	time.sleep(2)
	print('everything finished !')
if flag == 1:
	# input_arr1 = data_gen.write_FPGA_initial(["20220729_tx1_rx_all_on.tsv"])
	# input_arr1 = data_gen.write_FPGA_initial(["copy_RSOC_E2_Register_V2_no002_out.tsv"])

	# input_arr1 = data_gen.write_FPGA_initial(["copy_RSOC_E2_Register_Everything_Off_out.tsv"])
	# data_gen.sw_logic_analyzer(input_arr1)
	data_gen.PXI6534_run(input_arr1)
	time.sleep(2)

if flag == 2:
	file_to_write = ['tx_8.tsv',"tx_0.tsv","tx_1.tsv","tx_2.tsv","tx_3.tsv","tx_4.tsv","tx_5.tsv","tx_6.tsv","tx_7.tsv","tx_8.tsv"]
	# file_to_write = ['do_nothing.tsv',"tx_1.tsv","tx_1.tsv","tx_1.tsv","tx_1.tsv","tx_1.tsv","tx_1.tsv","tx_1.tsv","tx_1.tsv","tx_1.tsv"]
	# file_to_write = ['tx_0.tsv',"tx_0.tsv","tx_0.tsv","tx_0.tsv","tx_0.tsv","tx_0.tsv","tx_0.tsv","tx_0.tsv","tx_0.tsv","tx_0.tsv"]
	# file_to_write = ['tx8_on.tsv',"tx8_on.tsv","tx8_on.tsv","tx8_on.tsv","tx8_on.tsv","tx8_on.tsv","tx8_on.tsv","tx8_on.tsv","tx8_on.tsv","tx8_on.tsv"]
	# file_to_write = ['tx_1_off.tsv',"tx_1.tsv","tx_1_off.tsv","tx_1.tsv","tx_1_off.tsv","tx_1.tsv","tx_1_off.tsv","tx_1.tsv","tx_1_off.tsv","tx_1_off.tsv"]
	# file_to_write = ['tx_2.tsv',"tx_2.tsv","tx_2.tsv","tx_2.tsv","tx_2.tsv","tx_2.tsv","tx_2.tsv","tx_2.tsv","tx_2.tsv","tx_2.tsv"]
	# file_to_write = ['do_nothing.tsv',"do_nothing.tsv","do_nothing.tsv","do_nothing.tsv","do_nothing.tsv","do_nothing.tsv","do_nothing.tsv","do_nothing.tsv","do_nothing.tsv","do_nothing.tsv"]

	input_arr1 = data_gen.write_doppler(file_to_write, 130e-6,1030)
	# data_gen.sw_logic_analyzer(input_arr1)
	data_gen.PXI6534_run(input_arr1, 2+len(input_arr1))
	time.sleep(2)

if flag == 3:
##	    def write_chirp_only(file_to_write, num_of_chirp, trig_period, BUF_ENB, MUX, MUX_EN):
	input_arr1 = data_gen.write_chirp_only(file_to_write = ["do_nothing.tsv","do_nothing.tsv"], num_of_chirp = 1000, trig_period = 130e-6, BUF_ENB = 6, MUX = 0, MUX_EN = 1)
	# data_gen.sw_logic_analyzer(input_arr1)
	data_gen.PXI6534_run(input_arr1,2+len(input_arr1))
	time.sleep(2)