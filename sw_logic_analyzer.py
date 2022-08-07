

class LogicAnalyzer(object):
    results = {}
    name = ['Chirp_START', 'BUF3_ENB', 'BUF2_ENB', 'BUF1_ENB', 'SEL1', 'SEL0',
            'MUX_EN', 'P2.7', 'P2.6', 'P2.5', 'P2.4', 'P2.3', 'P2.2', 'RST',
            'STRB', 'ADDR7', 'ADDR6', 'ADDR5', 'ADDR4', 'ADDR3', 'ADDR2',
            'ADDR1', 'ADDR0', 'REG7', 'REG6', 'REG5', 'REG4', 'REG3', 'REG2', 'REG1', 'REG0']

    def __init__(self, input_array):
        self.name.reverse()
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

