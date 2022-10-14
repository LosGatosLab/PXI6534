import Motor_module_for_GUI as motor

import os
from datetime import datetime
import time
import numpy as np 

############# initiallize motor ################
m = motor.motor_ctrl()
step = 14 # 14: 1.05cm

loc = [0,0]
loc_start = [-10,-10]
step_size = [2,2]
num_step = [15,10]

######### Move Scanner to Start Point ##########################
move = np.array(loc_start) - np.array(loc)
if move[0] > 0:
	m.move_X_positive(step*move[0])
elif move[0] < 0:
	m.move_X_negative(-step*move[0])
if move[1] < 0:
	m.move_Y_positive(-step*move[1])
elif move[1] > 0:
	m.move_Y_negative(step*move[1])
loc = loc_start
print('Moved to start point. ('+datetime.now().strftime("%H:%M:%S")+")")
time.sleep(5)

######### Scan Start ##########################

print('Start scanning. ('+datetime.now().strftime("%H:%M:%S")+")")

for _yscan in range(num_step[1]+1):

	for _xscan in range(num_step[0]+1):
		print('******* Current location: ('+str(loc[0])+','+str(loc[1])+') ********')
		######## run data capture script ####
		print('Start to run main_v4.py in background. ('+datetime.now().strftime("%H:%M:%S")+")")
		# os.system("python main_v4.py")
		# os.system("python main_v4.py > main_v4.log")
		######## X scanner move ####
		if _xscan < num_step[0]:
			m.move_X_positive(step*step_size[0])
			loc[0] += step_size[0]
			time.sleep(1)
			print('Scanner moved to the next step! ('+datetime.now().strftime("%H:%M:%S")+")")
		else:
			m.move_X_negative(step*step_size[0]*num_step[0])
			loc[0] -= step_size[0]*num_step[0]
			time.sleep(4)

	######## Y scanner move ####
	m.move_Y_negative(step*step_size[1])
	loc[1] += step_size[1]
	print('Scanner moved to the next **line** ! ('+datetime.now().strftime("%H:%M:%S")+")")
	time.sleep(2)

######### Move Scanner to Origin ##########################
move = -np.array(loc)
if move[0] > 0:
	m.move_X_positive(step*move[0])
elif move[0] < 0:
	m.move_X_negative(-step*move[0])
if move[1] < 0:
	m.move_Y_positive(-step*move[1])
elif move[1] > 0:
	m.move_Y_negative(step*move[1])