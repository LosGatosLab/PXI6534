# Python Library to control SPI devices using USB2ANY controller
# June 6 2022
# Qian Zhong 
#
from ctypes import*
import os
import sys
import LUT_hexstring
import csv

class usb2any(object):

	def __init__(self,serialnum_list):
		# Basic DLL interaction
		try:
			self.usb2anydll = windll.LoadLibrary('USB2ANY.dll')
		except:
			self.usb2anydll = windll.LoadLibrary('C:\\LP_Lab\\RSOC2\\ATE\\USB2ANY.dll')

		self.serialnum_list = serialnum_list
		self.numcontrollers = self.usb2anydll.u2aFindControllers()
		self.u2ahandle_list = []
		# self.serialnum0 = b'6F938B6E28000800'
		# self.get_handle(self.serialnum0)
		# self.serialnum_list.append(self.get_serial_numbers(0))
		# print(self.get_serial_numbers(0))

		for i in range(len(self.serialnum_list)):
			print('device'+str(i))
			print(self.serialnum_list[i])
			self.u2ahandle_list.append(self.get_handle(self.serialnum_list[i]))
			if self.init_u2aSPI(i) == 0:
				print("device "+str(i)+" initialized successfully !")
			else:
				print("device "+str(i)+" initialized failed !")

			# if self.init_u2aSPI(i) == 0:
				# print("SPI"+str(i)+ "initialized successfully")
		# self.serial_u2a_map = {}
		# for i in self.serialnum_list:
		# 	self.serial_u2a_map[i] = self.u2ahandle_list[self.serialnum_list.index(i)]

	#Init function.
	def get_serial_numbers(self,device_index):
		#int u2aGetSerialNumber(int index, char *SerialNumber
		sernums = self.usb2anydll.u2aGetSerialNumber
		sernums.argtype = [c_int, c_char_p]
		serial = c_char_p(b'')
		sernums(device_index,serial)
		#print "USB2ANY<0> Device SerialNumber: ", serial.value
		return serial.value

	#Init function.
	def get_handle(self,serial_number):
		u2aopen_py = self.usb2anydll.u2aOpen
		u2aopen_py.argtype = [c_char_p]
		u2ahandle = u2aopen_py(serial_number)
		#print "Opening USB2ANY... Obtained handle for ",serial.value," as ",u2ahandle
		return u2ahandle

	def init_u2aSPI(self,index):
		return self.usb2anydll.u2aSPI_Control(self.u2ahandle_list[index],1,0,1,0,1,1,0,96)


	# def init_u2aSPI(self,u2ahandle):
	# 	SPI_ClockPhase = 1
	# 	SPI_ClockPolarity = 0
	# 	SPI_BitDirection = 1 # 1 =MSB firtst. 0 = LSB first
	# 	SPI_CharacterLength = 0
	# 	SPI_CSType = 1 # what is packet ?
	# 	SPI_CSPolarity = 1 # send data when enabele is low
	# 	DividerHigh = 0
	# 	DividerLow = 96
	# 	u2aSPI_init_py = self.usb2anydll.u2aSPI_Control
	# 	u2aSPI_init_py.argtype = [u2ahandle,c_uint,c_uint,c_uint,c_uint,c_uint,c_uint,c_uint,c_uint]
	# 	u2aSPI_init_py(
	# 		u2ahandle,
	# 		SPI_ClockPhase,
	# 		SPI_ClockPolarity,
	# 		SPI_BitDirection,
	# 		SPI_CharacterLength,
	# 		SPI_CSType,
	# 		SPI_CSPolarity,
	# 		DividerHigh,
	# 		DividerLow	
	# 	)

	def u2aSPI_RW(self,device_index,adr_data_str):
		u2aSPI_RW_py = self.usb2anydll.u2aSPI_WriteAndRead
		u2aSPI_RW_py.argtype = [self.u2ahandle_list[device_index],c_uint,c_char_p]
		data_array = [LUT_hexstring.LUT_hex2byte_C[adr_data_str[0:2]],LUT_hexstring.LUT_hex2byte_C[adr_data_str[2:4]],LUT_hexstring.LUT_hex2byte_C[adr_data_str[4:6]]]
		data_buffer = create_string_buffer(3)
		index = 0
		for eachItem in data_buffer:
			data_buffer[index] = data_array[index]
			index += 1
		return u2aSPI_RW_py(self.u2ahandle_list[device_index],3,data_buffer)

	def pll_hex_reader(self,filename):
		result = []
		with open(filename) as file:
			reader = csv.reader(file,delimiter = '\t')
			for row in reader:
				result.append(row[1][2:len(row[1])])
		return result


	def u2aSPI_RW_fromfile(self,device_index,filename):
		pll_hex = self.pll_hex_reader(filename)
		for i in pll_hex:
			self.u2aSPI_RW(device_index,i)
		print("PLL"+str(device_index)+" written successfully!")


	# Close the USB2ANY Module
	def close_SPI(self,u2ahandle):
		#print 'closing USB2ANY i2c handle'
		self.usb2anydll.u2aClose(u2ahandle)
