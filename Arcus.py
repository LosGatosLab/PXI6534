import usb.core
import usb.util
import time

ARCUS_MST_ACCEL = 1 # motor in acceleration
ARCUS_MST_DECEL = 2 # motor in decelertaion
ARCUS_MST_CONSTANT = 4 # motor running at constant speed
ARCUS_MST_LIM_PLUS = 16 # plus limit switch status
ARCUS_MST_LIM_MINUS = 32 # minus limit switch status
ARCUS_MST_HOME = 64 # home input switch status
ARCUS_MST_LIM_PLUS_ERR = 128 # plus limit error
ARCUS_MST_LIM_MINUS_ERR = 256 # minus limit error
ARCUS_MST_Z_INDEX_CHANNEL = 512 # Z index channel status
ARCUS_MST_JOY_CONTROL = 1024 # joystick control on status
ARCUS_MST_TOC_TIMEOUT = 2048 # TOC timeout status

class Motor:
    def __init__(self):
        self.readTimeout = 10000
        self.writeTimeout = 10000
        self.dev = usb.core.find(idVendor=0x1589, idProduct=0xa101)
        if self.dev is None:
            raise ValueError('Motor not found')
        self.dev.set_configuration()
        self.dev.default_timeout = 10000
        self.cfg = self.dev.get_active_configuration()
        intf = self.cfg[(0,0)]
        self.out = usb.util.find_descriptor(
                intf,
                custom_match = lambda e: e.bEndpointAddress == 0x82)
        assert self.out is not None
        assert self.dev.ctrl_transfer(0x40, 0x02, 0x02, 0x00, []) == 0 # open command
        self.flush()

    def flush(self):
        """Flush communications."""
        assert self.dev.ctrl_transfer(0x40, 0x02, 0x01, 0x00, []) == 0 # flush command

    def cmd(self, command):
        """Send a command and return the resulting status"""
        self.flush() # Seems to need to be done every time, otherwise get timeouts
        time.sleep(.01)
        # result = self.dev.read(0x82, 4096, self.readTimeout) # clear outstanding reads
        assert self.dev.write(0x02, command.ljust(64, '\0'), self.writeTimeout) == 64 # always send 64 bytes idk why. actually i think i just need to null terminate the string since python strings are not
        r = self.dev.read(0x82, 64, self.readTimeout)
        #return r
        null_ind = 63
        try:
            null_ind = r.index(0)
        except ValueError:
            pass
        return ''.join([chr(x) for x in r[0:null_ind]])

    def wait(self):
        """Wait until motor is done moving"""
        status = 1
        while(status != 0):
            time.sleep(.01)
            status = int(self.cmd("MSTX"))
            status = status & (ARCUS_MST_ACCEL | ARCUS_MST_DECEL | ARCUS_MST_CONSTANT)
        status = 1
        while(status != 0):
            time.sleep(.01)
            status = int(self.cmd("MSTY"))
            status = status & (ARCUS_MST_ACCEL | ARCUS_MST_DECEL | ARCUS_MST_CONSTANT)

    def cmd_allow_timeout(self, command):
        """Do command but allow timeout"""
        try:
            return self.cmd(command)
        except usb.core.USBTimeoutError:
            return ""
