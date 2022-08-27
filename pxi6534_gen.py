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
    def __init__(self, sampling_clock):
        self.sampling_clock = sampling_clock

    def write_FPGA_initial(self, file_to_write):
        object1 = dp.data_proc(file_to_write)
        object1.PXI_seq_initial()
        print('data proc length:' + str(len(object1.PXI_arr)))

        return object1.PXI_arr

    def sw_logic_analyzer(self, input_arr):
        signal_collection = ['Chirp_START', 'BUF3_ENB', 'BUF2_ENB', 'BUF1_ENB', 'SEL1', 'SEL0',
            'MUX_EN', 'RST','STRB', 'ADDR7', 'ADDR6', 'ADDR5', 'ADDR4', 'ADDR3', 'ADDR2',
            'ADDR1', 'ADDR0', 'REG7', 'REG6', 'REG5', 'REG4', 'REG3', 'REG2', 'REG1', 'REG0']
        logic_analyzer1 = LA.LogicAnalyzer(input_arr)
        logic_analyzer1.LogicPlot(signal_collection, self.sampling_clock)

    def write_doppler(self, file_to_write, trig_period, num_of_doppler):
        object1 = dp.data_proc(file_to_write)
        object1.PXI_seq_doppler(self.sampling_clock, trig_period, num_of_doppler)
        return object1.PXI_arr

    def write_chirp_only(self, file_to_write, num_of_chirp, trig_period, BUF_ENB, MUX, MUX_EN):
        object1 = dp.data_proc(file_to_write)
        object1.PXI_seq_chrip_only(fs = self.sampling_clock, trig_period = trig_period, num_of_chrips = num_of_chirp, BUF_ENB = BUF_ENB, MUX = MUX, MUX_EN = MUX_EN)
        return object1.PXI_arr

    def PXI6534_run(self, input_arr):
        input_arr = np.array(input_arr, dtype = 'uint32')
        size =  input_arr.size
        with nidaqmx.Task() as task:
            do_channel = task.do_channels.add_do_chan('Dev36/port0:3',
                line_grouping=LineGrouping.CHAN_FOR_ALL_LINES)
            do_channel.do_output_drive_type = DigitalDriveType.ACTIVE_DRIVE

            task.timing.cfg_burst_handshaking_timing_export_clock(self.sampling_clock, sample_clk_outp_term = '/Dev36/PXI_Trig5', sample_mode=AcquisitionType.CONTINUOUS, 
                samps_per_chan=size, sample_clk_pulse_polarity=Polarity.ACTIVE_HIGH, pause_when=Level.HIGH, ready_event_active_level=Polarity.ACTIVE_HIGH)
            print('arr_size:' + str(input_arr.size))

            samples_written = task.write(input_arr, auto_start=True)
            time.sleep(2)
            print('pxi6534 write done !')



