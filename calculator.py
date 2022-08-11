a = range(31)
name = ['Chirp_START','BUF3_ENB','BUF2_ENB', 'BUF1_ENB', 'SEL1', 'SEL0',
            'MUX_EN','P2.7','P2.6', 'P2.5', 'P2.4', 'P2.3', 'P2.2', 'RST',
            'STRB','ADDR7','ADDR6','ADDR5','ADDR4','ADDR3','ADDR2',
            'ADDR1','ADDR0','REG7','REG6','REG5','REG4','REG3','REG2','REG1','REG0']
name.reverse()
print(name)
fs = 10000000
fs_in_MHz = (float)(fs / 1000000)
time_step = (float)(1 / fs_in_MHz)

print(time_step)

import matplotlib.pyplot as plt
import numpy as np


# Fixing random state for reproducibility
