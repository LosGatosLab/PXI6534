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

sampling_clock = 1000000 ## set for 10MHz now 
# object1 = dp.data_proc(["init_div_off.tsv","tx_0.tsv","tx_1.tsv","tx_2.tsv","tx_3.tsv","tx_4.tsv","tx_5.tsv","tx_6.tsv","tx_7.tsv","tx_8.tsv"])
# object1 = dp.data_proc(["copy_RSOC_E2_Register_Everything_Off_out.tsv"])
# object1 = dp.data_proc(["copy_RSOC_E2_Register_V2_no002_out.tsv"])
object1 = dp.data_proc(["copy_RSOC_E2_Register_V2_no002_out_pad.tsv",'do_nothing.tsv'])

# object1 = dp.data_proc(["init_div_off.tsv","tx_0.tsv"])

object1.PXI_seq_master(sampling_clock, 125e-6, 1)
signal_collection = ['Chirp_START', 'BUF3_ENB', 'BUF2_ENB', 'BUF1_ENB', 'SEL1', 'SEL0',
            'MUX_EN', 'RST','STRB', 'ADDR7', 'ADDR6', 'ADDR5', 'ADDR4', 'ADDR3', 'ADDR2',
            'ADDR1', 'ADDR0', 'REG7', 'REG6', 'REG5', 'REG4', 'REG3', 'REG2', 'REG1', 'REG0']
input_arr = object1.PXI_arr
logic_analyzer1 = LA.LogicAnalyzer(input_arr)
logic_analyzer1.LogicPlot(signal_collection, sampling_clock)

input_arr = np.array(input_arr, dtype = 'uint32')

##################
test_arr = []
size = 100
for i in range(size):
    test_arr.append(4294967295)
    test_arr.append(0)

test_arr = np.array(test_arr, dtype = 'uint32')


with nidaqmx.Task() as task:
    do_channel = task.do_channels.add_do_chan(
        'Dev36/port0:3',
        line_grouping=LineGrouping.CHAN_FOR_ALL_LINES)

    do_channel.do_output_drive_type = DigitalDriveType.ACTIVE_DRIVE


    # task.timing.cfg_samp_clk_timing(sampling_clock,active_edge=Edge.RISING,
    #   sample_mode=AcquisitionType.CONTINUOUS)

    # task.out_stream.output_buf_size = size*2
    # task.out_stream.output_buf_size = 0
    task.timing.cfg_burst_handshaking_timing_export_clock(sampling_clock, sample_clk_outp_term = '/Dev36/PXI_Trig5', sample_mode=AcquisitionType.CONTINUOUS, 
        samps_per_chan=size*2, sample_clk_pulse_polarity=Polarity.ACTIVE_HIGH, pause_when=Level.HIGH, ready_event_active_level=Polarity.ACTIVE_HIGH)
    print('arr_size:' + str(input_arr.size))

    samples_written = task.write(input_arr, auto_start=True)

    time.sleep(10)
    # task.start()
    # print('output_buf_size: '+ str(task.out_stream.output_buf_size))
    # print('samples: ' + str(samples_written))
    # print('task finished successfully !')

# with nidaqmx.Task() as task:

#     do_channel = task.do_channels.add_do_chan(
#         'Dev36/port0:3',
#         line_grouping=LineGrouping.CHAN_FOR_ALL_LINES)

#     do_channel.do_output_drive_type = DigitalDriveType.ACTIVE_DRIVE

#     # task.timing.cfg_samp_clk_timing(sampling_clock,active_edge=Edge.RISING,
#     #   sample_mode=AcquisitionType.CONTINUOUS)


#     writer = DigitalSingleChannelWriter(task.out_stream,auto_start = True)
#     # task.out_stream.output_buf_size = 32768*2*2*2

#     writer.write_many_sample_port_uint32(test_arr)
#     time.sleep(5)

#     # task.start()

#     # print('space available in buffer: '+ str(task.out_stream.space_avail))

#     # task.start()
#     # task.out_stream.write(np.)
#     print('output_onbrd_buf_size: '+ str(task.out_stream.output_onbrd_buf_size))
#     print('output_buf_size: '+ str(task.out_stream.output_buf_size))
#     # print('samples: ' + str(samples_written))
#     print('task finished successfully !')


