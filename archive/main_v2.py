import pxi6534_gen
import time
import M3100A_Digitizer as M3100As
import numpy as np 
import matplotlib.pyplot as plt

###############
sampling_clock = 500000 ## set for 10MHz now 
num_of_doppler = 256
points_per_cycle = 6500
num_cycles = num_of_doppler*27
delay_in = 3800

######### Initialization ##############
data_gen_initial = pxi6534_gen.pxi6534_gen(sampling_clock)
input_arr_init = data_gen_initial.write_FPGA_initial(["init_div_on_RX15.tsv"])
# input_arr_init = data_gen_initial.write_FPGA_initial(["init_div_on.tsv"])
# data_gen_initial.PXI6534_run(input_arr_init, 2+len(input_arr_init))
time.sleep(2)

print('RSOC initilized!')

######### Data Init ###################
data_gen_run = pxi6534_gen.pxi6534_gen(sampling_clock)
file_to_write = ['do_nothing.tsv',"tx_0.tsv","tx_1.tsv","tx_2.tsv","tx_3.tsv","tx_4.tsv","tx_5.tsv","tx_6.tsv","tx_7.tsv","tx_8.tsv"]
# file_to_write = ['do_nothing.tsv',"tx_1.tsv","tx_1.tsv","tx_1.tsv","tx_1.tsv","tx_1.tsv","tx_1.tsv","tx_1.tsv","tx_1.tsv","tx_1.tsv"]
input_arr_run = data_gen_run.write_doppler(file_to_write, 130e-6,num_of_doppler)
# data_gen_run.sw_logic_analyzer(input_arr_run)
# data_gen_run.PXI6534_run(input_arr_run, 2+len(input_arr_run))
time.sleep(2)


######## OSC Initi ####################

# pxi_scope = M3100A.M3100A(points_per_cycle, num_cycles, delay_in)
# data_read = pxi_scope.acqisition_wait_1(ch = 1, run = data_gen_run, input_array = input_arr_run)
# print(type(data_read))
# print(data_read.size)



####### 



