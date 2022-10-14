################# Start Data Capture ########
print('Capture Start! ('+datetime.now().strftime("%H:%M:%S")+")")
BlockData = [ [0]*int(capture_points*num_cycles) for i in range(len(list_chn))]
for i in range(num_run):
	pxi_scope.daq_start()
	data_gen_run.PXI6534_run(input_arr_run, 2+len(input_arr_run))
	pxi_scope.daq_wait(list_chn[0])
	for idx_chn in list_chn:
		Data = pxi_scope.daq_acqisition(idx_chn)
		BlockData[idx_chn-1] = BlockData[idx_chn-1] + Data
	print('**** Capture Progress ('+datetime.now().strftime("%H:%M:%S")+'): RUN-'+str(i+1)+'/'+str(num_run)+' ****')
BlockData = np.array(BlockData)/num_run
print('Capture Finished! ('+datetime.now().strftime("%H:%M:%S")+")")