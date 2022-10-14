
# Definitions
with open("def.py", 'r') as f: exec(f.read())

# Initializations
os.system("py -3.10-32 pll_init_v1.py")
with open("init.py", 'r') as f: exec(f.read())

# Data Capture
with open("capture.py", 'r') as f: exec(f.read())

# Create Save Dir
file_dir_data = r"C:\To_Share\Captured_Data\M3100A"+"\\"+datetime.now().strftime("%m%d")+"\\"+datetime.now().strftime("%H%M%S")
create_dir(file_dir_data)
print("*** Save Path: "+file_dir_data+" ***")

# Data Processing and Save
with open("proc.py", 'r') as f: exec(f.read())

####### 
eng.quit()