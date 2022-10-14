from glob import glob
import os

folder = r"C:\To_Share\Captured_Data\M3100A\0922"
subfolders = [ f.path for f in os.scandir(folder) if f.is_dir() ]

# subdir = glob(r"C:\To_Share\Captured_Data\M3100A\0921\*\", recursive = True)

# subdir = os.walk(directory):
# subdir = subdir[1]
# print(subfolders)

filename = r"C:\To_Share\Captured_Data\M3100A\0922\list_dir"
f = open(filename, 'w')

for i in range(len(subfolders)):
  f.write(subfolders[i])
  f.write("\n")
f.close()