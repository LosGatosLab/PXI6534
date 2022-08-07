import csv 
class data_proc(object) :
	addr_arr = []
	reg_arr = []
	PXI_arr = []
	def __init__(self, TSV_arr):
		for i in TSV_arr:
			addr, reg = self.MultiTSV(i)
			self.addr_arr.append(addr)
			self.reg_arr.append(reg)

	def PXI_seq_master(self,  fs, trig_period, num_of_doppler):
		self.PXI_arr += self.Write_in_reg(BUF_ENB = 6, MUX = 0, MUX_EN = 1, reg_index = 0)   ### write all register for once self, BUF_ENB, MUX, MUX_EN, reg_index
		self.PXI_arr += self.delay(BUF_ENB = 6, MUX = 0, MUX_EN = 1, fs = fs, time = 100e-6)  ### delay 100us to settle RSOC delay(self, BUF_ENB, MUX, MUX_EN, fs, time)
		for i in range(num_of_doppler):
			self.PXI_arr += self.PXI_arr_gen(fs, trig_period)

	def PXI_arr_gen(self, fs, trig_period):
		return_array = []
		num_of_sample_per_trig_period = int(round(fs*trig_period))
		## generate each TX in sequence
		for i in range(1,len(self.addr_arr),1):
			return_array += self.ChirpGen_ALL(fs, num_of_sample_per_trig_period, i)
		return return_array

	def ChirpGen_ALL(self, fs, num_of_sample_per_trig_period, tx_index):
		return_array = []
		trig_width = 5e-6
		num_of_trig_width =  int(round(fs*trig_width))
		if (tx_index == 0):
			return_array += self.ChirpGen_alloff(which_group = 0, num_of_trig_width = num_of_trig_width, num_of_sample_per_trig_period = num_of_sample_per_trig_period)
			return_array += self.ChirpGen_alloff(which_group = 1, num_of_trig_width = num_of_trig_width, num_of_sample_per_trig_period = num_of_sample_per_trig_period)
			return_array += self.ChirpGen_alloff(which_group = 2, num_of_trig_width = num_of_trig_width, num_of_sample_per_trig_period = num_of_sample_per_trig_period)
		return_array += self.ChirpGen(which_group = 0, TX_index =tx_index, num_of_trig_width = num_of_trig_width, num_of_sample_per_trig_period = num_of_sample_per_trig_period)
		return_array += self.ChirpGen(which_group = 1, TX_index =tx_index, num_of_trig_width = num_of_trig_width, num_of_sample_per_trig_period = num_of_sample_per_trig_period)
		return_array += self.ChirpGen(which_group = 2, TX_index =tx_index, num_of_trig_width = num_of_trig_width, num_of_sample_per_trig_period = num_of_sample_per_trig_period)
		return return_array


	def ChirpGen(self,which_group, TX_index, num_of_trig_width, num_of_sample_per_trig_period):
		return_array = []
		if (which_group == 0):
			trig1 = self.WriteTrig(BUF_ENB = 6, MUX = 0, MUX_EN = 1, trig_width = num_of_trig_width)
			return_array += trig1
			reg1 = self.Write_in_reg(BUF_ENB = 6, MUX = 0, MUX_EN = 1, reg_index = TX_index)
			return_array += reg1
			delay1 = self.delay_in_sample(BUF_ENB = 6, MUX = 0, MUX_EN = 1, num_of_sample= num_of_sample_per_trig_period - len(trig1)- len(reg1))
			return_array += delay1
		elif (which_group == 1):
			trig1 = self.WriteTrig(BUF_ENB = 5, MUX = 1, MUX_EN = 1, trig_width = num_of_trig_width)
			return_array += trig1
			reg1 = self.Write_in_reg(BUF_ENB = 5, MUX = 1, MUX_EN = 1, reg_index = TX_index)
			return_array += reg1
			delay1 = self.delay_in_sample(BUF_ENB = 5, MUX = 1, MUX_EN = 1, num_of_sample= num_of_sample_per_trig_period - len(trig1)- len(reg1))
			return_array += delay1
		else:
			trig1 = self.WriteTrig(BUF_ENB = 3, MUX = 2, MUX_EN = 1, trig_width = num_of_trig_width)
			return_array += trig1
			reg1 = self.Write_in_reg(BUF_ENB = 3, MUX = 2, MUX_EN = 1, reg_index = TX_index)
			return_array += reg1
			delay1 = self.delay_in_sample(BUF_ENB = 3, MUX = 2, MUX_EN = 1, num_of_sample= num_of_sample_per_trig_period - len(trig1)- len(reg1))
			return_array += delay1
		return return_array

	def ChirpGen_alloff(self,which_group, num_of_trig_width, num_of_sample_per_trig_period):
		return_array = []
		if (which_group == 0):
			trig1 = self.WriteTrig(BUF_ENB = 6, MUX = 0, MUX_EN = 1, trig_width = num_of_trig_width)
			return_array += trig1
			delay1 = self.delay_in_sample(BUF_ENB = 6, MUX = 0, MUX_EN = 1, num_of_sample= num_of_sample_per_trig_period - len(trig1))
			return_array += delay1
		elif (which_group == 1):
			trig1 = self.WriteTrig(BUF_ENB = 5, MUX = 1, MUX_EN = 1, trig_width = num_of_trig_width)
			return_array += trig1
			delay1 = self.delay_in_sample(BUF_ENB = 5, MUX = 1, MUX_EN = 1, num_of_sample= num_of_sample_per_trig_period - len(trig1))
			return_array += delay1
		else:
			trig1 = self.WriteTrig(BUF_ENB = 3, MUX = 2, MUX_EN = 1, trig_width = num_of_trig_width)
			return_array += trig1
			delay1 = self.delay_in_sample(BUF_ENB = 3, MUX = 2, MUX_EN = 1, num_of_sample= num_of_sample_per_trig_period - len(trig1))
			return_array += delay1
		return return_array



	def delay_TX_group(self,which_group, fs, time):
		return_array = []
		if (which_group == 0):
			return return_array.append(self.delay(6, 0, 1, fs, time)) ### delay(self, BUF_ENB, MUX, MUX_EN, fs, time)
		elif (which_group == 1):
			return return_array.append(self.delay(5, 1, 1, fs, time)) ### delay(self, BUF_ENB, MUX, MUX_EN, fs, time)
		else:
			return return_array.append(self.delay(3, 2, 1, fs, time)) ### delay(self, BUF_ENB, MUX, MUX_EN, fs, time)



	def WriteLine(self,Chirp_Start, BUF_ENB, MUX, MUX_EN, RST, STRB, Addr, Reg):
		return Chirp_Start*pow(2,30)+ BUF_ENB*pow(2,27) + MUX*pow(2,25) + MUX_EN*pow(2,24) + RST*pow(2,17) + STRB*pow(2,16) + Addr*pow(2,8) + Reg

	def WriteTrig(self, BUF_ENB, MUX, MUX_EN, trig_width):
		return_array = []
		for i in range(trig_width):
			return_array.append(self.WriteLine(1,BUF_ENB,MUX,MUX_EN,1,0,0,0)) ### WriteLine(self,Chirp_Start, BUF_ENB, MUX, MUX_EN, RST, STRB, Addr, Reg):
		return return_array

	def Write_in_time(self,Chirp_Start, BUF_ENB, MUX, MUX_EN, RST, STRB, Addr, Reg, fs,time):
		num_of_sample = int(round(fs*time))
		return_array = []
		for i in range(num_of_sample):
			return_array.append(self.WriteLine(Chirp_Start, BUF_ENB, MUX, MUX_EN, RST, STRB, Addr, Reg))
		return return_array

	def Write_in_samples(self,Chirp_Start, BUF_ENB, MUX, MUX_EN, RST, STRB, Addr, Reg, N):
		return_array = []
		for i in range(N):
			return_array.append(self.WriteLine(Chirp_Start, BUF_ENB, MUX, MUX_EN, RST, STRB, Addr, Reg))
		return return_array

	def Write_in_reg(self, BUF_ENB, MUX, MUX_EN, reg_index):
		return_array = []
		for i in range(len(self.reg_arr[reg_index])):
			return_array.append(self.WriteLine(0, BUF_ENB, MUX, MUX_EN, 1, 0, self.addr_arr[reg_index][i], self.reg_arr[reg_index][i]))
			return_array.append(self.WriteLine(0, BUF_ENB, MUX, MUX_EN, 1, 1, self.addr_arr[reg_index][i], self.reg_arr[reg_index][i]))
		return return_array

	def Write_Rest(self, BUF_ENB, MUX, MUX_EN):
		return_array = []
		return_array.append(self.WriteLine(0, BUF_ENB, MUX, MUX_EN, 0, 0, 0, 0))
		return_array.append(self.WriteLine(0, BUF_ENB, MUX, MUX_EN, 0, 0, 0, 0))
		return return_array

	def delay(self, BUF_ENB, MUX, MUX_EN, fs, time):
		num_of_sample = int(round(fs*time))
		if (num_of_sample == 0):
			num_of_sample = 1
		return_array = []
		for i in range(num_of_sample):
			return_array.append(self.WriteLine(0, BUF_ENB, MUX, MUX_EN, 1, 0, 0, 0))
		return return_array

	def delay_in_sample(self, BUF_ENB, MUX, MUX_EN, num_of_sample):
		if (num_of_sample == 0):
			num_of_sample = 1
		return_array = []
		for i in range(num_of_sample):
			return_array.append(self.WriteLine(Chirp_Start= 0, BUF_ENB = BUF_ENB, MUX= MUX, MUX_EN= MUX_EN, RST= 1, STRB= 0, Addr= 0, Reg= 0))  ### Chirp_Start, BUF_ENB, MUX, MUX_EN, RST, STRB, Addr, Reg
		return return_array

	def MultiTSV(self, filename):
		with open("RSOC_E2_Register_no002_out.tsv") as file:
			addr_arr = []
			reg_arr = []
			tsv_file = csv.reader(file, delimiter="\t")
			for line in tsv_file:
				addr_arr.append(int(float(line[1])))
				reg_arr.append(int(line[2],16))
			return addr_arr,reg_arr

