################# Call Matlab ########
print("Start Matlab Processing. ("+datetime.now().strftime("%H:%M:%S")+")")
BlockData = matlab.double(BlockData)
Raw_sig_9 = eng.M3100A_Resample_9(BlockData,capture_points,num_of_doppler*num_of_int_avg,num_of_int_avg)
Raw_sig = eng.data_reform(Raw_sig_9,1)
T0 = capture_delay/capture_fs
Fs = capture_fs*4/5
# file_path = file_dir_data+"\\"+'Raw_sig_9.mat'
# mdic = {"Raw_sig_9": Raw_sig_9, "T0": T0, "Fs": Fs}
# savemat(file_path, mdic)
file_path = file_dir_data+"\\"+'Raw_sig.mat'
mdic = {"Raw_sig": Raw_sig, "T0": T0, "Fs": Fs}
savemat(file_path, mdic)

################# Release Memory ########
print("Finished and Realse Memory. ("+datetime.now().strftime("%H:%M:%S")+")")
del BlockData
del Raw_sig_9
del Raw_sig
del Data
gc.collect()