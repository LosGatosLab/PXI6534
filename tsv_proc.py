import csv
from decimal import Decimal

# open .tsv file
addr_arr = []
reg_arr = []
with open("RSOC_E2_Register_no002_out.tsv") as file:
       
    # Passing the TSV file to 
    # reader() function
    # with tab delimiter
    # This function will
    # read data from file
    tsv_file = csv.reader(file, delimiter="\t")
     
    # printing data line by line
    for line in tsv_file:
        addr_arr.append(int(float(line[1])))
        reg_arr.append(int(line[2],16))

print(addr_arr)
print(reg_arr)
fs = 10000000
time = 1e-6
N= int(round(time*fs))
print(N)
print(type(N))
A = [[0,2],[90,91],[30,20]]
B = [4,5,6]
print(A[1][0])
print(B)
print(A+B)

def abc(a,b,c):
    return int(a+b+c)

print(abc(a=1,b=2,c=3))
