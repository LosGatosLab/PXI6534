import Motor_module_for_GUI as motor
import numpy as np 

m = motor.motor_ctrl()
step = 14 ## 80 for small one 
# num_of_steps = 15
# for i in range(16):
# 	m.move_X_positive(step)
# for i in range(5):
# 	m.move_Y_negative(step)
# for i in range(10):
# 	m.move_Y_positive(step)
# for i in range(2):
# 	m.move_X_negative(step)

# m.move_Y_positive(step*10)
# m.move_Y_negative(step*1)
# m.move_X_positive(step*10)
# m.move_X_negative(step*30)

######## Move Scanner to Origin ##########################
move = [0, -4]
m.move_XY(step,move)

# if move[0] > 0:
# 	m.move_X_positive(step*move[0])
# elif move[0] < 0:
# 	m.move_X_negative(-step*move[0])
# if move[1] < 0:
# 	m.move_Y_positive(-step*move[1])
# elif move[1] > 0:
# 	m.move_Y_negative(step*move[1])