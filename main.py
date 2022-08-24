import nidaqmx

from nidaqmx.constants import LineGrouping
from nidaqmx.constants import Edge
from nidaqmx.constants import AcquisitionType
from nidaqmx.constants import DigitalDriveType

import sw_logic_analyzer as LA
import matplotlib as mpl
import matplotlib.pyplot as plt
import data_proc as dp

sampling_clock = 1000000 ## set for 10MHz now 
object1 = dp.data_proc(["init_div_off.tsv","tx_0.tsv","tx_1.tsv","tx_2.tsv","tx_3.tsv","tx_4.tsv","tx_5.tsv","tx_6.tsv","tx_7.tsv","tx_8.tsv"])
object1.PXI_seq_master(sampling_clock, 125e-6, 1)
signal_collection = ['Chirp_START', 'BUF3_ENB', 'BUF2_ENB', 'BUF1_ENB', 'SEL1', 'SEL0',
            'MUX_EN', 'RST','STRB', 'ADDR7', 'ADDR6', 'ADDR5', 'ADDR4', 'ADDR3', 'ADDR2',
            'ADDR1', 'ADDR0', 'REG7', 'REG6', 'REG5', 'REG4', 'REG3', 'REG2', 'REG1', 'REG0']
input_arr = object1.PXI_arr
logic_analyzer1 = LA.LogicAnalyzer(input_arr)
#logic_analyzer1.LogicPlot(signal_collection, sampling_clock)

with nidaqmx.Task() as task:

    
    do_channel = task.do_channels.add_do_chan(
        'Dev36/port0:3',
        line_grouping=LineGrouping.CHAN_FOR_ALL_LINES)

    do_channel.do_output_drive_type = DigitalDriveType.ACTIVE_DRIVE
    do_channel.do_invert_lines = 0

    task.timing.cfg_samp_clk_timing(sampling_clock,active_edge=Edge.RISING,
    	sample_mode=AcquisitionType.FINITE,samps_per_chan=len(input_arr))

    task.write(input_arr, auto_start=True)
    print('task finished successfully !')
