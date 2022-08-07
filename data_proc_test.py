import data_proc as dp

object1 = dp.data_proc(["init_div_off.tsv", "tx_0.tsv","tx_1.tsv","tx_2.tsv","tx_3.tsv","tx_4.tsv","tx_5.tsv","tx_6.tsv","tx_7.tsv","tx_8.tsv"])
#object1 = dp.data_proc(["tx_0.tsv","tx_1.tsv"])

object1.PXI_seq_master(10000000, 125e-6, 1)
print(object1.addr_arr[1])
print(object1.reg_arr[1])
print(object1.PXI_arr)