import pxi6534_gen
import M3100A_Digitizer as M3100A
from create_dir import create_dir

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

################# Define the capturing parameters  ########
sampling_clock = 500000 ## set for 10MHz now 
num_of_doppler = 256
num_of_int_avg = 4
num_cycles = num_of_int_avg*num_of_doppler*27
num_run = 160

prescaler = 4;
capture_fs = 100e6/(prescaler+1)
capture_margin = 0/(prescaler+1)
capture_points = 6400/(prescaler+1)+2*capture_margin
capture_delay = 3600/(prescaler+1)-capture_margin
list_chn = range(1,9)