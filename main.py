import nidaqmx

from nidaqmx.constants import (
    LineGrouping)

data_to_write = [85,85,85]

with nidaqmx.Task() as task:

    task.do_channels.add_do_chan(
        'Dev1/port0:3',
        line_grouping=LineGrouping.CHAN_FOR_ALL_LINES)

    task.cfg_samp_clk_timing(20000000,active_edge=Edge.RISING,
    	sample_mode=AcquisitionType.FINITE,samps_per_chan=10000)

    task.write(data_to_write, auto_start=true)
