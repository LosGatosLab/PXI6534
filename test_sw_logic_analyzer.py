import sw_logic_analyzer as LA
import matplotlib as mpl
import matplotlib.pyplot as plt
import data_proc as dp

object1 = dp.data_proc(["init_div_off.tsv","tx_0.tsv","tx_1.tsv","tx_2.tsv","tx_3.tsv","tx_4.tsv","tx_5.tsv","tx_6.tsv","tx_7.tsv","tx_8.tsv"])
object1.PXI_seq_master(10000000, 125e-6, 1)
signal_collection = ['Chirp_START', 'BUF3_ENB', 'BUF2_ENB', 'BUF1_ENB', 'SEL1', 'SEL0',
            'MUX_EN', 'RST','STRB', 'ADDR7', 'ADDR6', 'ADDR5', 'ADDR4', 'ADDR3', 'ADDR2',
            'ADDR1', 'ADDR0', 'REG7', 'REG6', 'REG5', 'REG4', 'REG3', 'REG2', 'REG1', 'REG0']
input_arr = object1.PXI_arr
logic_analyzer1 = LA.LogicAnalyzer(input_arr)
logic_analyzer1.LogicPlot(signal_collection, 10000000)
