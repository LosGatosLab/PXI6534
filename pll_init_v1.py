import usb2any_lib_joe_v1 as u2a

################# Define the files  ########
file_dir_hex = r"C:\LP_Lab\RSOC2\Registers\LMX2492"
file_name1 = r"NoV2_002_Chirp_4700M_4900M_115us_3us_2us_20220616.txt"
# file_name1 = r"NoV2_002_CW_4780MHz.txt"
file_hex1 = file_dir_hex+"\\"+file_name1

################# Initialize the PLL(s)  ########
# pll_serial_num_list = [b'6F938B6E28015103100800',b'6F938B6E10001B00']
pll_serial_num_list = [b'6F938B6E10001B00']
A = u2a.usb2any(pll_serial_num_list)

A.u2aSPI_RW_fromfile(0,file_hex1)
# A.u2aSPI_RW_fromfile(1,file_hex1)