import matplotlib as mpl
import matplotlib.pyplot as plt

class LogicAnalyzer(object):
    results = {}
    # name_1 = ['Chirp_START', 'BUF3_ENB', 'BUF2_ENB', 'BUF1_ENB', 'SEL1', 'SEL0',
    #         'MUX_EN', 'P2.7', 'P2.6', 'P2.5', 'P2.4', 'P2.3', 'P2.2', 'RST',
    #         'STRB', 'ADDR7', 'ADDR6', 'ADDR5', 'ADDR4', 'ADDR3', 'ADDR2',
    #         'ADDR1', 'ADDR0', 'REG7', 'REG6', 'REG5', 'REG4', 'REG3', 'REG2', 'REG1', 'REG0']

    # name = ['REG0', 'REG1', 'REG2', 'REG3', 'REG4', 'REG5', 'REG6', 'REG7',
    #           'ADDR0', 'ADDR1', 'ADDR2', 'ADDR3', 'ADDR4', 'ADDR5', 'ADDR6', 'ADDR7', 'STRB',
    #           'RST', 'P2.2', 'P2.3', 'P2.4', 'P2.5', 'P2.6', 'P2.7', 'MUX_EN', 'SEL0', 'SEL1',
    #           'BUF1_ENB', 'BUF2_ENB', 'BUF3_ENB', 'Chirp_START']

    name_1 = ['Chirp_START', 'BUF3_ENB', 'BUF2_ENB', 'BUF1_ENB', 'SEL1', 'SEL0',
            'MUX_EN', 'ADDR7', 'ADDR6', 'ADDR5', 'ADDR4', 'ADDR3', 'ADDR2',
            'ADDR1', 'ADDR0', 'P1.7', 'P1.6', 'P1.5', 'P1.4', 'P1.3', 'RST', 'P1.1',
            'STRB', 'REG7', 'REG6', 'REG5', 'REG4', 'REG3', 'REG2', 'REG1', 'REG0']

    name = ['REG0', 'REG1', 'REG2', 'REG3', 'REG4', 'REG5', 'REG6', 'REG7',
               'STRB','P1.1', 'RST', 'P1.3', 'P1.4', 'P1.5', 'P1.6', 'P1.7', 
               'ADDR0', 'ADDR1', 'ADDR2', 'ADDR3', 'ADDR4', 'ADDR5', 'ADDR6', 'ADDR7',
               'MUX_EN', 'SEL0', 'SEL1',
              'BUF1_ENB', 'BUF2_ENB', 'BUF3_ENB', 'Chirp_START']

    def __init__(self, input_array):
        for i in input_array:
           self.integer2bit(30, i)

    def integer2bit(self, bit, input):
        if (bit < 0):
            return
        if (self.name[bit] not in list(self.results.keys())):
            self.results[self.name[bit]] = [input // pow(2, bit)]
        else:
            self.results[self.name[bit]].append(input // pow(2, bit))
        return self.integer2bit(bit - 1, input % pow(2, bit))

    def LogicPlot(self, input, fs):
        plt.rcParams.update({'font.size': 6})
        fs_in_MHz = (float) (fs / 1000000)
        time_step = (float) (1 / fs_in_MHz)
        xaxis = [i*time_step for i in range(len(self.results[input[0]]))]
        fig, axs = plt.subplots(len(input), 1, sharex=True)
        for j in input:
            axs[input.index(j)].step(xaxis, self.results[j])
            axs[input.index(j)].set_ylabel(j,rotation = 0,fontsize=4)
            if (input.index(j) == len(input)-1):
                axs[input.index(j)].set_xlabel('time(us)')

        plt.show()

