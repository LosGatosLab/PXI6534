import Motor_module_for_GUI as motor

# Definitions
with open("def.py", 'r') as f: exec(f.read())

# Initializations
os.system("py -3.10-32 pll_init_v1.py")
with open("init.py", 'r') as f: exec(f.read())

# Create Save Dir
file_dir = r"C:\To_Share\Captured_Data\M3100A"+"\\"+datetime.now().strftime("%m%d")+"\\"+datetime.now().strftime("%H%M%S")
create_dir(file_dir)

############# initiallize motor ################
m = motor.motor_ctrl()
step = 14 # 14: 1.05cm

loc = [0,0]
loc_start = [-10,-10]
step_size = [2,2]
num_step = [15,10]

######### Move Scanner to Start Point ##########################
move = np.array(loc_start) - np.array(loc)
m.move_XY(step,move)
loc = loc_start
print('Moved to start point. ('+datetime.now().strftime("%H:%M:%S")+")")
time.sleep(5)

######### Scan Start ##########################
print('Start scanning. ('+datetime.now().strftime("%H:%M:%S")+")")
for _yscan in range(num_step[1]+1):
	for _xscan in range(num_step[0]+1):
		print('******* Current location: ('+str(loc[0])+','+str(loc[1])+') ********')
		######## run data capture script ####
		print('Start to run data capture. ('+datetime.now().strftime("%H:%M:%S")+")")
		# with open("capture.py", 'r') as f: exec(f.read())
		file_dir_data = file_dir+"\\X"+str(loc[0])+'_Y'+str(loc[1])
		create_dir(file_dir_data)
		######## Scanner move ####
		if _xscan < num_step[0]:
			m.move_X_positive(step*step_size[0])
			loc[0] += step_size[0]
			# time.sleep(1)
			print('Scanner moved to the next step! ('+datetime.now().strftime("%H:%M:%S")+")")
		else:
			m.move_X_negative(step*step_size[0]*num_step[0])
			loc[0] -= step_size[0]*num_step[0]
			m.move_Y_negative(step*step_size[1])
			loc[1] += step_size[1]
			print('Scanner moved to the next **line** ! ('+datetime.now().strftime("%H:%M:%S")+")")
			# time.sleep(5)
		######## run data processing and save script ####
		print("*** Save Path: "+file_dir_data+" ***")
		# with open("proc.py", 'r') as f: exec(f.read())

######### Move Scanner to Origin ##########################
move = -np.array(loc)
m.move_XY(step,move)
print('Scan finished. Moved to origin! ('+datetime.now().strftime("%H:%M:%S")+")")

# ####### 
eng.quit()