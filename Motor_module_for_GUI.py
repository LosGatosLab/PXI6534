import Arcus
import datetime
import pathlib
import sys
import time
from subprocess import Popen, PIPE, DEVNULL
import matplotlib.pyplot as plt

class motor_ctrl:
    def __init__(self):
        self.m = Arcus.Motor()
        self.m.cmd("CLR") # Clear flags
        self.m.cmd("HSPD=20000") # Set high speed
        ### Go to origin
        self.m.cmd("EO=3") # Enable motor 1 and 2
        self.m.wait()
        self.m.cmd("INC") # Set incremental mode, absolute mode isn't working, probably need to get polarity settings right
        self.m.wait()
        self.m.cmd("PX=0")
        self.m.wait()
        self.m.cmd("PY=0")
        self.m.wait()
        self.Results = []
        self.motor_x = 0
        self.motor_y = 0

    @staticmethod
    def mm_to_stepstr(mm):
        return str(int(mm * 100))

    def device_num(self):
        print(self.m.cmd_allow_timeout("DN")) # Should normally print device number string

    def scanning(self,x_num_point,y_num_point,x_step,y_step):
        Results = []
        self.motor_x = 0
        self.motor_y = 0
        self.m.cmd("INC")
        self.m.wait()
        # for i in x_range:
        #     self.m.cmd("X-"+motor_ctrl.mm_to_stepstr(i))
        #     self.m.wait()
        # for i in y_range:
        #     self.m.cmd("Y-"+motor_ctrl.mm_to_stepstr(i))
        #     self.m.wait()
        for i in range(y_num_point):
            ## read balah
            Results.append(D2D.D2D(self.motor_x,self.motor_y,0,0))
            for j in range(x_num_point):
                self.m.cmd("X-"+motor_ctrl.mm_to_stepstr(x_step))
                self.m.wait()
                self.motor_x += x_step
                ## read balah
                Results.append(D2D.D2D(self.motor_x,self.motor_y,0,0))
            ### x clean
            self.m.cmd("X"+motor_ctrl.mm_to_stepstr(len(range(x_num_point))*x_step))
            self.m.wait()
            self.motor_x -= len(range(x_num_point))*x_step
            ### y step +1
            self.m.cmd("Y-"+motor_ctrl.mm_to_stepstr(y_step))
            self.m.wait()
            self.motor_y += y_step
        ### y clean
        self.m.cmd("Y"+motor_ctrl.mm_to_stepstr(len(range(y_num_point))*y_step))
        self.m.wait()
        self.motor_y -= len(range(y_num_point))*y_step
        excel_handler.write_results('2D_Scan.xlsx','sweep',Results)
        print("scan finished successfully")


    def move_X_positive(self,step):
        self.m.cmd("INC")
        self.m.wait()
        self.m.cmd("X"+motor_ctrl.mm_to_stepstr(step))
        self.m.wait()
    def move_X_negative(self,step):
        self.m.cmd("INC")
        self.m.wait()
        self.m.cmd("X-"+motor_ctrl.mm_to_stepstr(step))
        self.m.wait()
    def move_Y_positive(self,step):
        self.m.cmd("INC")
        self.m.wait()
        self.m.cmd("Y"+motor_ctrl.mm_to_stepstr(step))
        self.m.wait()
    def move_Y_negative(self,step):
        self.m.cmd("INC")
        self.m.wait()
        self.m.cmd("Y-"+motor_ctrl.mm_to_stepstr(step))
        self.m.wait()

    def move_XY(self,step,move):
        if move[0] > 0:
            self.move_X_positive(step*move[0])
        elif move[0] < 0:
            self.move_X_negative(-step*move[0])
        if move[1] < 0:
            self.move_Y_positive(-step*move[1])
        elif move[1] > 0:
            self.move_Y_negative(step*move[1])

####################