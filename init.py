######### RSOC Initialization ##############
# pxi6534 = nidaqmx.system.device.Device('Dev36')
# pxi6534.reset_device()
data_gen_initial = pxi6534_gen.pxi6534_gen(sampling_clock)
input_arr_init = data_gen_initial.write_FPGA_initial(["20220831_tx8_rx_all_on_div_off.tsv"])
data_gen_initial.PXI6534_run(input_arr_init, 2+len(input_arr_init))
print('RSOC initilized! ('+datetime.now().strftime("%H:%M:%S")+")")
# time.sleep(1)

################# Initialize Matlab Engine  ########
eng = matlab.engine.start_matlab()
eng.cd(r'C:\LP_Lab\RSOC2\Matlab\RSOC_Data_Processing_M3100A')
print('Matlab engine initilized! ('+datetime.now().strftime("%H:%M:%S")+")")

######### Chirp Sequence Init ###################
# pxi6534.reset_device()
data_gen_run = pxi6534_gen.pxi6534_gen(sampling_clock)
file_to_write = ['tx_8.tsv',"tx_0.tsv","tx_1.tsv","tx_2.tsv","tx_3.tsv","tx_4.tsv","tx_5.tsv","tx_6.tsv","tx_7.tsv","tx_8.tsv"]
input_arr_run = data_gen_run.write_doppler(file_to_write,130e-6,num_of_doppler*num_of_int_avg)
# data_gen_run.sw_logic_analyzer(input_arr_run)
print('Chirp sequence initilized! ('+datetime.now().strftime("%H:%M:%S")+")")

################# Initialize M3100A ########
pxi_scope = M3100A.M3100A(capture_points, num_cycles, capture_delay, list_chn, prescaler)
print('M3100A DAQ initilized! ('+datetime.now().strftime("%H:%M:%S")+")")