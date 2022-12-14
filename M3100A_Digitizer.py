import keysightSD1
import numpy as np
import matplotlib.pyplot as plt
import time

class M3100A:
	def __init__(self, points_per_cycle, num_cycles, delay_in, list_chn, prescaler):
		self.PRODUCT = ""
		self.CHASSIS = 0
		self.SLOT_IN = 2 # digitizer slot in chassis

		# CREATE AND OPEN MODULE IN
		self.digitizer = keysightSD1.SD_AIN()
		self.digitizerID = self.digitizer.openWithSlot(self.PRODUCT, self.CHASSIS, self.SLOT_IN)
		if self.digitizerID < 0:
  			print("Module open error:", self.digitizerID)
		# else:
		# 	print("===== Digitizer =====")
		# 	print("ID:\t\t", self.digitizerID)
		# 	print("Product name:\t", self.digitizer.getProductName())
		# 	print("Serial number:\t", self.digitizer.getSerialNumber())
		# 	print("Chassis:\t", self.digitizer.getChassis())
		# 	print("Slot:\t\t", self.digitizer.getSlot())

		# CONFIGURATION CONSTANTS
		self.FULL_SCALE = 1 # half peak to peak voltage
		self.READ_TIMEOUT = 100 # 0 means infinite timeout
		self.WAITER_TIMEOUT_SECONDS = 0.1

		# CONFIGURATION CONSTANTS
		self.NUM_POINTS_PER_CYCLE = int(points_per_cycle)
		self.NUM_CYCLES = int(num_cycles)
		self.TOTAL_POINTS = self.NUM_POINTS_PER_CYCLE*self.NUM_CYCLES
		self.TRG_SOURCE = 0
		self.DELAY_IN = int(delay_in) # Number of samples that trigger is delayed 

		# Config TRG as a trigger input
		self.digitizer.triggerIOconfig(1) 

		# Config each channel
		for CH in list_chn:
		  self.digitizer.channelInputConfig(CH, self.FULL_SCALE , keysightSD1.AIN_Impedance.AIN_IMPEDANCE_50, keysightSD1.AIN_Coupling.AIN_COUPLING_AC)
		  self.digitizer.DAQconfig(CH, self.NUM_POINTS_PER_CYCLE, self.NUM_CYCLES, self.DELAY_IN, keysightSD1.SD_TriggerModes.HWDIGTRIG)
		  self.digitizer.DAQdigitalTriggerConfig(CH,self.TRG_SOURCE, keysightSD1.SD_TriggerBehaviors.TRIGGER_RISE)

		# Config the prescaler to 6
		mask = 255
		self.digitizer.channelPrescalerConfigMultiple(mask, prescaler)

	def acqisition(self):
		# DAQ ACQUISITION
		mask = 255
		self.digitizer.DAQflushMultiple(mask)
		self.digitizer.DAQstartMultiple(mask)
		time.sleep(1)
		# waitUntilPointsRead(digitizer, 1, TOTAL_POINTS, WAITER_TIMEOUT_SECONDS)

		readPoints = self.digitizer.DAQread(1, self.TOTAL_POINTS, self.READ_TIMEOUT)/32767*self.FULL_SCALE
		print('points read successfully')
		return readPoints

	def daq_start(self):
		mask = 255
		self.digitizer.DAQflushMultiple(mask)
		self.digitizer.DAQstartMultiple(mask)
		time.sleep(0.1)

	def daq_wait(self, ch):
		cnt = 0
		while self.digitizer.DAQcounterRead(ch) != self.TOTAL_POINTS:
			time.sleep(0.02)
			cnt += 1
			if cnt%25 == 1:
				print("Captured: " + str(self.digitizer.DAQcounterRead(ch)))
		time.sleep(0.05)
		print("Captured: " + str(self.digitizer.DAQcounterRead(ch)))
		print("Waited for " + str(cnt*0.02) + "sec.")

	def daq_acqisition(self, ch):
		if self.digitizer.DAQcounterRead(ch) == self.TOTAL_POINTS:
			data = self.digitizer.DAQread(ch, self.TOTAL_POINTS, self.READ_TIMEOUT)/32767*self.FULL_SCALE
		else:
			print("Error: CH" + str(ch) + " data not ready!!!!")
		return data

	def acqisition_wait(self, ch):
		
		cnt = 0
		while self.digitizer.DAQcounterRead(ch) != self.TOTAL_POINTS:
			time.sleep(0.02)
			cnt += 1
			print(self.digitizer.DAQcounterRead(ch))
		print("Waited for " + str(cnt*0.02) + "sec.")
		time.sleep(0.05)
		if self.digitizer.DAQcounterRead(ch) == self.TOTAL_POINTS:
			readPoints = self.digitizer.DAQread(ch, self.TOTAL_POINTS, self.READ_TIMEOUT)/32767*self.FULL_SCALE
		print('points read successfully')
		return readPoints

	def acqisition_wait_1(self, ch, run, input_array):
		mask = 255
		self.digitizer.DAQflushMultiple(mask)
		self.digitizer.DAQstartMultiple(mask)
		time.sleep(1)
		print("Capture Start.")
		run.PXI6534_run(input_array, 2+len(input_array))
		while self.digitizer.DAQcounterRead(ch) != self.TOTAL_POINTS:
			time.sleep(0.02)
			print(self.digitizer.DAQcounterRead(ch))
		if self.digitizer.DAQcounterRead(ch) == self.TOTAL_POINTS:
			readPoints = self.digitizer.DAQread(ch, self.TOTAL_POINTS, self.READ_TIMEOUT)/32767*self.FULL_SCALE
		print('points read successfully')
		return readPoints