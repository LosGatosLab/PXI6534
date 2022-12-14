import nidaqmx
import time
from nidaqmx.constants import LineGrouping
from nidaqmx.constants import Edge
from nidaqmx.constants import AcquisitionType
from nidaqmx.constants import DigitalDriveType
from nidaqmx.constants import Polarity
from nidaqmx.constants import Level

import sw_logic_analyzer as LA
import matplotlib as mpl
import matplotlib.pyplot as plt
import data_proc as dp

import numpy as np

from nidaqmx.stream_writers import (
    DigitalSingleChannelWriter, DigitalMultiChannelWriter)


class pxi6534_gen(object):
    pxi6534_gen_arr = []
    def __init__(self, sampling_clock):
        self.sampling_clock = sampling_clock

    def write_FPGA_initial(self, file_to_write):
        object1 = dp.data_proc(file_to_write)
        # object1.PXI_seq_reset()
        object1.PXI_seq_initial(self.sampling_clock, 100e-6)
        return object1.PXI_arr

    def sw_logic_analyzer(self, input_arr):
        signal_collection = ['Chirp_START', 'BUF3_ENB', 'BUF2_ENB', 'BUF1_ENB', 'SEL1', 'SEL0',
            'MUX_EN', 'RST','STRB', 'ADDR7', 'ADDR6', 'ADDR5', 'ADDR4', 'ADDR3', 'ADDR2',
            'ADDR1', 'ADDR0', 'REG7', 'REG6', 'REG5', 'REG4', 'REG3', 'REG2', 'REG1', 'REG0']
        logic_analyzer1 = LA.LogicAnalyzer(input_arr)
        logic_analyzer1.LogicPlot(signal_collection, self.sampling_clock)
        logic_analyzer1.read_count(signal_collection)

    def write_doppler_w_initial(self,file_to_write, trig_period, num_of_doppler):
        result_arr = []
        result_arr += self.write_FPGA_initial(["20220831_tx8_rx_all_on_div_off.tsv"])
        # result_arr += self.write_FPGA_initial(["set_tx8_on.tsv"])
        result_arr += self.write_doppler(file_to_write, trig_period, num_of_doppler)
        return result_arr

    def write_doppler_w_pad(self,file_to_write,trig_period, num_of_doppler):
        result_arr = []
        result_arr += self.write_doppler(file_to_write, trig_period, num_of_doppler)
        result_arr += self.write_dummy_delay(file_to_write, BUF_ENB = 6, MUX = 0, MUX_EN = 1, time = 1000000e-6)
        return result_arr

    # def write_doppler_w_pad(self,file_to_write,trig_period, num_of_doppler):
    #     result_arr = []
    #     result_arr += self.write_doppler(file_to_write, trig_period, num_of_doppler)
    #     result_arr += self.write_dummy_delay(file_to_write, BUF_ENB = 0, MUX = 0, MUX_EN = 1, time = 1000000e-6)
    #     return result_arr

    def write_doppler(self, file_to_write, trig_period, num_of_doppler):
        object_write_doppler = dp.data_proc(file_to_write)
        object_write_doppler.PXI_seq_doppler(self.sampling_clock, trig_period, num_of_doppler)
        return object_write_doppler.PXI_arr

    def write_dummy_delay(self, file_to_write, BUF_ENB, MUX, MUX_EN, time):
        object1 = dp.data_proc(file_to_write)
        object1.PXI_seq_dummy_delay(BUF_ENB = BUF_ENB, MUX =MUX, MUX_EN = MUX_EN, fs =self.sampling_clock, time = time)
        # print(object1.PXI_arr)
        return object1.PXI_arr

    def write_chirp_only(self, file_to_write, num_of_chirp, trig_period, BUF_ENB, MUX, MUX_EN):
        object1 = dp.data_proc(file_to_write)
        object1.PXI_seq_chrip_only(fs = self.sampling_clock, trig_period = trig_period, num_of_chrips = num_of_chirp, BUF_ENB = BUF_ENB, MUX = MUX, MUX_EN = MUX_EN)
        return object1.PXI_arr

    def PXI6534_run(self, input_arr, size):
        # input_arr = np.array(input_arr, dtype = 'uint32')
        # size =  size
        with nidaqmx.Task() as task:
            do_channel = task.do_channels.add_do_chan('Dev36/port0:3',
                line_grouping=LineGrouping.CHAN_FOR_ALL_LINES)
            do_channel.do_output_drive_type = DigitalDriveType.ACTIVE_DRIVE
            # do_channel.do_use_only_on_brd_mem = False

            # task.timing.cfg_samp_clk_timing(self.sampling_clock,active_edge=Edge.RISING,
            #             sample_mode=AcquisitionType.FINITE,samps_per_chan=size)

            task.timing.cfg_burst_handshaking_timing_export_clock(self.sampling_clock, sample_clk_outp_term = '/Dev36/PXI_Trig5', sample_mode=AcquisitionType.FINITE, 
                samps_per_chan=size, sample_clk_pulse_polarity=Polarity.ACTIVE_HIGH, pause_when=Level.HIGH, ready_event_active_level=Polarity.ACTIVE_HIGH)

            # print('arr_size:' + str(input_arr.size))

            samples_written = task.write(input_arr, auto_start=True)
            time.sleep(4)
            # task.start()
            task.stop()
            # print('pxi6534 write done !')

    def PXI6534_run_initial(self, size):
        # input_arr = np.array(input_arr, dtype = 'uint32')
        # size =  size
        with nidaqmx.Task() as task:
            do_channel = task.do_channels.add_do_chan('Dev36/port0:3',
                line_grouping=LineGrouping.CHAN_FOR_ALL_LINES)
            do_channel.do_output_drive_type = DigitalDriveType.ACTIVE_DRIVE

            # task.timing.cfg_samp_clk_timing(self.sampling_clock,active_edge=Edge.RISING,
            #             sample_mode=AcquisitionType.FINITE,samps_per_chan=size)

            task.timing.cfg_burst_handshaking_timing_export_clock(self.sampling_clock, sample_clk_outp_term = '/Dev36/PXI_Trig5', sample_mode=AcquisitionType.FINITE, 
                samps_per_chan=size, sample_clk_pulse_polarity=Polarity.ACTIVE_HIGH, pause_when=Level.HIGH, ready_event_active_level=Polarity.ACTIVE_HIGH)

            # print('arr_size:' + str(input_arr.size))
            return task
            # task.start()
            # print('pxi6534 write done !')


