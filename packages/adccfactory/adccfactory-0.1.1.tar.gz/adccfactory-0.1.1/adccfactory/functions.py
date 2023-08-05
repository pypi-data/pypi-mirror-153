#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt 

import matplotlib
import matplotlib.animation as animation
matplotlib.rcParams["image.interpolation"] = None
from matplotlib.ticker import MultipleLocator
import matplotlib as mpl

import pandas as pd
from glob import glob
from natsort import natsorted
from tqdm import tqdm
from scipy.interpolate import interp1d
from matplotlib.pyplot import cm
from tifffile import imwrite
import numpy.ma as ma
import configparser
import warnings
import shutil
import os
import gc
import cv2

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

def ConfigSectionMap(path,section):
	Config = configparser.ConfigParser()
	Config.read(path)
	dict1 = {}
	options = Config.options(section)
	for option in options:
		try:
			dict1[option] = Config.get(section, option)
			if dict1[option] == -1:
				DebugPrint("skip: %s" % option)
		except:
			print("exception on %s!" % option)
			dict1[option] = None
	return dict1

def reduce(li, time_dilation):
	if time_dilation==1:
		return(li)
	else:
		time_dilation = int(time_dilation)
		result = [(x+y)/2.0 for x, y in zip(li[::time_dilation], li[1::time_dilation])]
		if len(li) % time_dilation:
			result.append(li[-1])
		return result

def list_of_str_to_type(list0,dtype=int,sep=" "):
	output = np.empty(len(list0),dtype=object)
	for k,element in enumerate(list0):
		with warnings.catch_warnings():
			warnings.simplefilter("error")
			try:
				output[k] = np.fromstring(element[1:-1],dtype=dtype, sep=sep)
			except DeprecationWarning:
				print("heres one")
				output[k] = np.fromstring(element[1:-1],dtype=dtype, sep=" ")
	return(output)
	
def light_rgb_from_stack(stack,blue_channel,red_channel,green_channel=None,fraction=1, blue_percentiles=None, red_percentiles=None):
	
	if blue_percentiles is None:
		blue_percentiles = [1, 99.99]

	if red_percentiles is None:
		red_percentiles = [1, 99.99]

	stack = np.array(np.moveaxis(stack,1,-1),dtype=float)
	blue = stack[:,:,:,blue_channel]
	red = stack[:,:,:,red_channel]

	if green_channel is not None:
		green = stack[:,:,:,green_channel]

	del stack
	gc.collect()

	blue_min = np.percentile(blue[0].flatten(),blue_percentiles[0])
	blue_max = np.percentile(blue[0].flatten(),blue_percentiles[1])

	red_min = np.percentile(red[-1].flatten(),red_percentiles[0])
	red_max = np.percentile(red[-1].flatten(),red_percentiles[1])

	if green_channel is not None:
		green_min = np.percentile(green[0].flatten(),1)
		green_max = np.percentile(green[0].flatten(),99.99)

	blue -= blue_min
	blue /= (blue_max - blue_min)/255
	blue[blue > 255] = 255
	blue[blue < 0] = 0

	red -= red_min
	red /= (red_max - red_min)/255
	red[red > 255] = 255
	red[red < 0] = 0

	if green_channel is not None:
		green -= green_min
		green /= (green_max - green_min)/255
		green[green > 255] = 255
		green[green < 0] = 0

	else:
		green = np.zeros_like(blue, dtype=np.uint8)

	stack = np.array([red,green,blue],dtype=np.uint8)
	stack = np.moveaxis(stack,0,-1)
	res = np.array([cv2.resize(frame, dsize=(2048//fraction, 2048//fraction), interpolation=cv2.INTER_CUBIC) for frame in stack],dtype=np.uint8)

	print("RGB stack successfully loaded...")

	del blue; del green; del red; del stack;
	gc.collect()
	
	return(res)

	

def get_class_color(cclass):
	if cclass==0.0:
		return("tab:red")
	elif cclass==1.0:
		return("tab:blue")
	elif cclass==2.0:
		return("yellow")
		
def str_to_bool(var):
	if var=="y":
		var = True
	else:
		var = False
	return(var)
		
def get_status_color(cclass,t,t0,movie_length):
	if (cclass==0.0):
		if (t0>0.0)*(t0<=movie_length):
			if (cclass==0.0)*(int(t)>=int(t0)):
				status = 0
				color = "tab:red"
			elif (cclass==0.0)*(int(t)<int(t0)):
				status = 1
				color = "tab:blue"
		else:
			status = 3
			color = "white"

	elif (cclass==1.0):
		if (t0<0.0):
			status = 1
			color = "tab:blue"
		else:
			status = 3
			color = "white"

	elif (cclass==2.0):
		status = 2
		color = "yellow"

	return(status,color)

def plot_mean_vs_std(mean_dist,std_dist):
	mean_dist = np.array(mean_dist)
	mean_dist = mean_dist[mean_dist != -1.0]
	
	std_dist = np.array(std_dist)
	std_dist = std_dist[std_dist != -1.0]
	
	xspace = np.linspace(np.amin(mean_dist),np.amax(mean_dist),1000)
	coef = np.polyfit(mean_dist,std_dist,2)
	
	fig,ax = plt.subplots(1,1,figsize=(4,4))
	ax.plot(xspace, coef[0]*xspace**2+coef[1]*xspace+coef[2],c="tab:red",label=f"y = {round(coef[0],3)}*x**2+{round(coef[1],3)}*x+{round(coef[2],3)}")
	ax.plot(xspace,np.sqrt(xspace),c="k",label=r"y = $\sqrt{x}$")
	ax.scatter(mean_dist,std_dist,s=1)
	ax.set_xlabel("Mean # NK neigh per cell")
	ax.set_ylabel("STD in # NK neigh per cell")
	ax.set_xlim(0,4)
	ax.legend()
	plt.savefig("experiment_data/mean_std_nk_neigh.png",dpi=300,bbox_inches="tight")
	plt.pause(1)
	plt.close()	
	
	return(coef)
	
def find_time_stop(dt,cell_class,len_movie):
	if np.all([dt > 0.0,dt <= len_movie,cell_class==0]):
		time_stop = int(dt)
	else:
		time_stop = len_movie
	return(time_stop)
	
def nbr_nk_neigh_per_time(cell_times,nk_labels,nk_status):
	nk_counts = np.zeros(len(cell_times))
	for k,(nk_lbls, nk_stat) in enumerate(zip(nk_labels,nk_status)):
		if len(nk_lbls)>3:
			status = np.where(np.fromstring(nk_stat[1:-1],dtype=int,sep=" ")==1)[0]
			array_nk_labels = np.fromstring(nk_lbls[1:-1],dtype=int,sep=" ")
			nks_alive = len(array_nk_labels[status])
			nk_counts[k] = nks_alive
	return(nk_counts)
	
def nbr_tc_neigh_per_time(cell_times,tc_labels,tc_status,option="all"):
	tc_counts = np.zeros(len(cell_times))
	for k,(tc_lbls, tc_stat) in enumerate(zip(tc_labels,tc_status)):
		if len(tc_lbls)>3:
			
			array_tc_labels = np.fromstring(tc_lbls[1:-1],dtype=int,sep=" ")
			
			if option=="dead":
				status_dead = np.where(np.fromstring(tc_stat[1:-1],dtype=int,sep=" ")==0)[0]
				tcs_to_count = len(array_tc_labels[status_dead])
			elif option=="alive":
				status_alive = np.where(np.fromstring(tc_stat[1:-1],dtype=int,sep=" ")==1)[0]
				tcs_to_count = len(array_tc_labels[status_alive])
			elif option=="all":
				tcs_to_count = len(array_tc_labels)
			
			tc_counts[k] = tcs_to_count
	return(tc_counts)

def plot_nk_neighbours_distribution(nk_counts):
	plt.close()
	fig,ax = plt.subplots(1,1,figsize=(3,3))
	ax.hist(nk_counts)
	ax.set_xlabel("# NK neigh")
	ax.set_ylabel("#")
	plt.tight_layout()
	plt.show()

def create_circular_mask(h, w, center=None, radius=None,invert=False):

	if center is None: # use the middle of the image
		center = (int(w/2), int(h/2))
	if radius is None: # use the smallest distance between the center and image walls
		radius = min(center[0], center[1], w-center[0], h-center[1])

	Y, X = np.ogrid[:h, :w]
	dist_from_center = np.sqrt((X - center[0])**2 + (Y-center[1])**2)

	mask = dist_from_center <= radius
	if invert:
		mask = dist_from_center>radius
	return mask

def remove_unnamed_col(df):
	column_names = df.columns
	test_unnamed = np.array([s.startswith("Unnamed") for s in column_names])
	columns_to_drop = column_names[test_unnamed]
	for c in columns_to_drop:
		df.drop(c,inplace=True,axis=1)
	return(df)
	
def survival_fraction(cell_dts,cell_classes,bins_time,cell_nbr_threshold=0):
	
	"""
	Compute survival fraction sequence from a list of cell death times and
	and their associated class (dies or not).
	
	Parameters
	----------
	
	cell_dts: 1D numpy array
		the array of cell death times
	cell_classes: 1D numpy array
		the array of cell classes
	bins_time: 1D numpy array or list
		the time binning array for the building of the survival fraction
	cell_nbr_threshold: int
		the minimum number of cells to build the survival fraction
		
	
	Returns
	-------
	
	1D numpy array
		the survival fraction sequence
		if less cells than cell_nbr_threshold, returns empty list
	int
		the counted number of cells

	
	"""
	
	cell_dts = np.array(cell_dts)
	cell_classes = np.array(cell_classes)
	
	cell_dts = cell_dts[cell_classes != 2.0]
	cell_classes = cell_classes[cell_classes != 2.0]
	print(cell_classes)

	binned_death = np.zeros_like(bins_time)
	number_cells = len(cell_classes)
	
	if number_cells>cell_nbr_threshold:
		
		# Isolate the death times of the subpopulation of TC satisfying the condition

		cell_dts[cell_classes==1.0] = -1
		
		# Count cells as alive or dead
		nbr_tot = len(cell_dts)
		nbr_alive = len(np.where(cell_dts==-1)[0])
		
		# Iterate over dead cells
		sub_dt_dead = cell_dts[cell_dts != -1]
		for dt in sub_dt_dead:
			for l in range(len(bins_time)-1):
				if (dt>=bins_time[l])*(dt<bins_time[l+1]):
					binned_death[l+1] += 1
		
		# create survival from death events
		cumulative_death = np.cumsum(binned_death)
		survival = np.divide(np.subtract(nbr_tot,cumulative_death),nbr_tot)

		return survival,number_cells
	else:
		return [], number_cells
		
def tc_density(cell_dts,cell_classes,times):
	
	cell_dts = np.array(cell_dts)
	cell_classes = np.array(cell_classes)

	cell_dts = cell_dts[cell_classes==0.0]
	
	#Initialize counts
	number_tot = len(cell_classes)
	number_dead = np.zeros(len(times))
	
	for t_idx,t in enumerate(times):
		number_dead[t_idx] = len(np.where(cell_dts<=t)[0])
		
	number_alive = np.subtract(number_tot,number_dead)
	
	return number_tot, number_alive, number_dead
	
def recreate_folder(path):
	if os.path.exists(path):
		shutil.rmtree(path)
	os.mkdir(path)

def minmax(array):
	"""
	This function performs a MinMax rescaling on an array
	"""
	return((array-min(array))/(max(array)-min(array)))

def filter_by_tracklength(df,tracklength_threshold):
	tracklist_initial = np.unique(df["TRACK_ID"].to_numpy())
	df['LENGTH_TRACK'] = np.zeros(len(df))
	for tid in tracklist_initial:
		dft = df[(df["TRACK_ID"]==tid)]
		arr = dft["POSITION_X"].to_numpy()
		indices = dft.index
		df['LENGTH_TRACK'][indices] = len(arr)
	df = df[(df['LENGTH_TRACK']>tracklength_threshold)]
	return(df)

def handle_split_and_merge(df_track):
	positions_x = df_track.POSITION_X.to_numpy()
	positions_y = df_track.POSITION_Y.to_numpy()
	frames = df_track.FRAME.to_numpy()	
	unique_frames, counts = np.unique(frames,return_counts=True)
	duplicated_times = np.where(counts>1)[0]
	if len(duplicated_times)>0:
		reconstructed_frame = sorted(set(frames))
		reconstructed_x = np.zeros(len(unique_frames))
		reconstructed_y = np.zeros(len(unique_frames))
		doubled_frames = unique_frames[duplicated_times]
		for f in reconstructed_frame:
			indices = np.where(frames==f)[0]
			writing_position = np.where(reconstructed_frame==f)[0]
			xmean_t = np.mean(positions_x[indices]); ymean_t = np.mean(positions_y[indices])
			reconstructed_x[writing_position] = xmean_t
			reconstructed_y[writing_position] = ymean_t
		positions_x = reconstructed_x
		positions_y = reconstructed_y
		frames = reconstructed_frame
	return(positions_x,positions_y,frames)
	
def check_consecutive(frames,dt=1):
	"""
	This function looks for consecutive values in the array frames
	and organises them in chunks of consecutive values [[val1,val1+1,...,val1+n],[val2,val2+1,...]]
	with val2!=(val1+n)
	"""
	frames = np.sort(frames)
	slices = np.zeros(len(frames))
	key = 0
	for i in range(1,len(frames)):
		coef = int((frames[i] - frames[i-1]) / dt)
		if coef!=1:
			key+=1
			slices[i] = key

		elif coef==1:
			slices[i] = key
	return(np.array(slices),np.array(frames))
	
		
def interpolate_track(framediff,fullrange,frame_t,xlist,ylist,nbrpoints=5):
	#print(f"Frames missing = {framediff}")
	#print("The track seems incomplete, interpolating the gaps...")

	slices,framediff = check_consecutive(framediff) #check if the missing frames are consecutive

	unique_groups = np.unique(slices) #group by consecutiveness
	xlistnew = np.zeros(len(fullrange))
	ylistnew = np.zeros(len(fullrange))
	
	#Now accounts for list that does not start at 0
	for k in range(len(frame_t)):
		index = int(frame_t[k] - min(frame_t)) #if min=12, first index is 12 - 12 = 0
		xlistnew[index] = xlist[k]
		ylistnew[index] = ylist[k]

	
	for k in range(len(unique_groups)):

		lower_bound = np.amin(framediff[slices==unique_groups[k]]) #identify the bounds
		upper_bound = np.amax(framediff[slices==unique_groups[k]])

		try:
			loclb = int(np.where(frame_t==(lower_bound-1))[0]) #find the position of the nearest neighbors to the bounds in "times"
		except TypeError:
			loclb = 0
		
		try:
			locub = int(np.where(frame_t==(upper_bound+1))[0])
		except TypeError:
			print(upper_bound+1,frame_t)
			os.abort()
		
		nbrpoints = 5 #define number of points taken on both sides for the interpolation
		
		if loclb<nbrpoints:
			min_t = 0
		
		else:
			min_t = loclb - nbrpoints
		
		lower_x = frame_t[min_t:(loclb+1)]; upper_x = frame_t[(locub):locub+nbrpoints]
		interpolate_x = np.concatenate([lower_x,upper_x])
		lower_y1 = xlist[min_t:(loclb+1)]; upper_y1 = xlist[(locub):locub+nbrpoints]
		interpolate_y1 = np.concatenate([lower_y1,upper_y1])
		lower_y2 = ylist[min_t:(loclb+1)]; upper_y2 = ylist[(locub):locub+nbrpoints]
		interpolate_y2 = np.concatenate([lower_y2,upper_y2])

		interp_disp_x = interp1d(interpolate_x, interpolate_y1,fill_value="extrapolate")
		interp_disp_y = interp1d(interpolate_x, interpolate_y2,fill_value="extrapolate")

		x_to_interpolate = framediff[slices==unique_groups[k]]
		frames_to_modify = np.array(framediff[slices==unique_groups[k]],dtype=int)
		frames_to_modify -= min(np.array(frame_t,dtype=int))
		#print("frames to modify",frames_to_modify)

		xlistnew[frames_to_modify] = np.array([interp_disp_x(x) for x in x_to_interpolate])
		ylistnew[frames_to_modify] = np.array([interp_disp_y(x) for x in x_to_interpolate])

	return(xlistnew,ylistnew,fullrange)


def measure_cell_intensities(trajectories, intensity_measurement_radius, blue, red, PxToUm, len_movie, green = None, minimum_tracklength = 0):
	
	mask = create_circular_mask(2*intensity_measurement_radius,2*intensity_measurement_radius,
	((2*intensity_measurement_radius)//2,(2*intensity_measurement_radius)//2),intensity_measurement_radius)
	
	blue = np.array([np.pad(f,[intensity_measurement_radius+1,intensity_measurement_radius+1],mode="constant") for f in blue])	
	red = np.array([np.pad(f,[intensity_measurement_radius+1,intensity_measurement_radius+1],mode="constant") for f in red])
	if green is not None:
		green = np.array([np.pad(f,[intensity_measurement_radius+1,intensity_measurement_radius+1],mode="constant") for f in green])

	trajectories.reset_index
	trajectories = trajectories.sort_values(by=['TRACK_ID','FRAME'])
	trajectories = trajectories.set_index("SPOT_ID")
	
	# Apply track length filter
	trajectories = filter_by_tracklength(trajectories,minimum_tracklength)
	frames0 = trajectories.FRAME.to_numpy()
	print(f"Minimum frame = {min(frames0)}, Maximum frame = {max(frames0)}")
	print(f"Filtering tracks that do not start at frame {frames0[0]}...")
	tracklist = np.unique(trajectories.TRACK_ID.to_numpy()[frames0==0])
	print(f"Number of remaining tracks is {len(tracklist)}...")	
	
	# Initialize
	cells = []
	
	print("Measuring each cell...")
	for tid,track in tqdm(enumerate(tracklist),total=len(tracklist)):
	
		df_at_track = trajectories[(trajectories["TRACK_ID"]==track)]
		# Handle split and merge events
		positions_x, positions_y, frames = handle_split_and_merge(df_at_track)
		
		full_time_range = list(np.linspace(0,max(frames),int(max(frames))+1))
		frame_difference = list(set(full_time_range) - set(list(frames)))
		
		# Interpolate missing frames
		if len(frame_difference)>0:
			positions_x,positions_y,frames = interpolate_track(frame_difference,full_time_range,frames,positions_x,positions_y, 5)
		
		# Duplicate the last known position until the end of the movie
		while len(positions_x)<len_movie:
			frames = np.append(frames,max(frames)+1)
			positions_x = np.append(positions_x,positions_x[-1])
			positions_y = np.append(positions_y,positions_y[-1])
			
		blue_signal = np.zeros(len(frames))
		red_signal = np.zeros(len(frames))

		if green is not None:
			green_signal = np.zeros(len(frames))

		for idx,f in enumerate(frames):

			x = positions_x[frames==f]/PxToUm
			y = positions_y[frames==f]/PxToUm
			
			f = int(f)
			xmin = int(x) + (intensity_measurement_radius + 1) - intensity_measurement_radius
			xmax = int(x) +  (intensity_measurement_radius + 1) + intensity_measurement_radius
			
			ymin = int(y) + (intensity_measurement_radius + 1) - intensity_measurement_radius
			ymax = int(y) +  (intensity_measurement_radius + 1) + intensity_measurement_radius
						
			local_blue = np.multiply(blue[f,ymin:ymax,xmin:xmax],mask)
			local_red = np.multiply(red[f,ymin:ymax,xmin:xmax],mask)

			if green is not None:
				local_green = np.multiply(green[f,ymin:ymax,xmin:xmax],mask)
			
			if not local_blue[local_blue!=0].size==0:
				blue_measurement = np.mean(local_blue[local_blue!=0])
			else:
				blue_measurement = 0.0

			if not local_red[local_red!=0].size==0:
				red_measurement = np.mean(local_red[local_red!=0])
			else:
				red_measurement = 0.0

			red_signal[idx]=red_measurement
			blue_signal[idx]=blue_measurement

			if green is not None:
				if not local_green[local_green!=0].size==0:
					green_measurement = np.mean(local_green[local_green!=0])
				else:
					green_measurement = 0.0
				green_signal[idx]=green_measurement
				cells.append([track, x[0], y[0], f, blue_measurement, red_measurement, green_measurement])

			else:
				cells.append([track, x[0], y[0], f, blue_measurement, red_measurement])

	if green is not None:	
		df = pd.DataFrame(np.array(cells),columns=["TID","X","Y","T","BLUE_INTENSITY","RED_INTENSITY","GREEN_INTENSITY"])
	else:
		df = pd.DataFrame(np.array(cells),columns=["TID","X","Y","T","BLUE_INTENSITY","RED_INTENSITY"])		
	
	return(df)
	
def predict_signal_class(input_signals,frames,model,minmax, model_signal_length):
	"""
	This function automatically formats cell fluorescence signals, sends them to the 
	network and returns a class prediction. 
	"""

	blue_signal = input_signals[0]
	blue_signal = np.concatenate([blue_signal,np.zeros(model_signal_length - len(blue_signal))],axis=0)

	red_signal = input_signals[1]
	red_signal = np.concatenate([red_signal,np.zeros(model_signal_length - len(red_signal))],axis=0)

	inputs_reshaped = np.zeros((model_signal_length,2))

	max_value = np.amax(input_signals)
	min_value = np.amin(input_signals)
	inputs_reshaped[:,0] = (blue_signal-min_value)/(max_value - min_value)
	inputs_reshaped[:,1] = (red_signal-min_value)/(max_value - min_value)
	inputs_reshaped[inputs_reshaped < 0.0] = 0.0

	preds = model.predict(np.array([inputs_reshaped],dtype='float'))
	max_prob = np.amax(preds,axis=1)
	i = preds.argmax(axis=1)[0]
	return(i,max_prob)	

def check_model_signal_length(model_signal_length,models_path):
	models = glob(models_path+f"classifier_tc/*_{model_signal_length}.h5")
	if not models:
		print(f"Please set a signal length that is available in the configuration file\nThe available models are: {glob(models_path+'classifier_tc/*.h5')}")
		os.abort()
	else:
		print(f"The classifier model of signal length {model_signal_length} has been found...")
		return(model_signal_length)

def predict_signal_death_time(input_signals,frames,model,model_signal_length):
	"""
	This function automatically formats cell fluorescence signals, sends them to the 
	network and returns a death time estimate. 
	"""
	
	blue_signal = input_signals[0]
	blue_signal = np.concatenate([blue_signal,np.zeros(model_signal_length - len(blue_signal))],axis=0)

	red_signal = input_signals[1]
	red_signal = np.concatenate([red_signal,np.zeros(model_signal_length - len(red_signal))],axis=0)

	inputs_reshaped = np.zeros((model_signal_length,2))
	max_value = np.amax(input_signals)
	min_value = np.amin(input_signals)
	inputs_reshaped[:,0] = (blue_signal-min_value)/(max_value - min_value)
	inputs_reshaped[:,1] = (red_signal-min_value)/(max_value - min_value)
	inputs_reshaped[inputs_reshaped < 0.0] = 0.0

	preds = model.predict(np.array([inputs_reshaped],dtype='float'))[0]
	preds *= model_signal_length
	#preds += minmax_out[0]
	return(preds)	

def predict_signal(input_signals,frames,model,model_signal_length):
	"""
	This function automatically formats cell fluorescence signals, sends them to the 
	network and returns a class prediction and an estimate of the death time. 
	"""

	blue_signal = input_signals[0]
	blue_signal = np.concatenate([blue_signal,np.zeros(model_signal_length - len(blue_signal))],axis=0)

	red_signal = input_signals[1]
	red_signal = np.concatenate([red_signal,np.zeros(model_signal_length - len(red_signal))],axis=0)

	inputs_reshaped = np.zeros((model_signal_length,2))

	max_value = np.amax(input_signals)
	min_value = 0.0
	inputs_reshaped[:,0] = (blue_signal-min_value)/(max_value - min_value)
	inputs_reshaped[:,1] = (red_signal-min_value)/(max_value - min_value)
	inputs_reshaped[inputs_reshaped < 0.0] = 0.0
	
	death_time_pred, class_pred = model.predict(np.array([inputs_reshaped],dtype='float'))
	
	class_pred = class_pred[0]
	max_prob = np.amax(class_pred)
	i = class_pred.argmax()

	death_time_pred = death_time_pred[0][0]
	death_time_pred *= (model_signal_length - (-1.0))
	death_time_pred += -1.0

	return(i, death_time_pred)		

def measure_death_events(df, model, len_movie, model_signal_length=128):
	
	tracks = np.unique(df.TID.to_numpy())
	blue_signals = df.BLUE_INTENSITY.to_numpy()
	blue_signals = blue_signals.reshape(len(tracks),len_movie)
	red_signals = df.RED_INTENSITY.to_numpy()
	red_signals = red_signals.reshape(len(tracks),len_movie)
	frames = df["T"].to_numpy()
	frames.reshape(len(tracks),len_movie)
	
	classes_ = []
	times_ = []
	for k in tqdm(range(len(tracks))):
		input_ = np.array([blue_signals[k],red_signals[k]])
		frames_ = frames[k]
		class_prediction, death_time = predict_signal(input_,frames_,model,model_signal_length)
		#print(class_prediction, death_time)
		times_.extend([death_time]*len_movie)
		classes_.extend([class_prediction]*len_movie)
		
	df["CLASS"] = classes_
	df["T0"] = times_
	
	print(f"AI death event detection results: ")
	unique_classes,class_count = np.unique(classes_[0:len(classes_):len_movie],return_counts=True)
	where_alive = np.where(unique_classes==1)[0]
	where_dead = np.where(unique_classes==0)[0]
	where_else = np.where(unique_classes==2)[0]

	if len(where_alive)>0:
		print(f"{class_count[where_alive][0]} cells do not die during the movie...")
	if len(where_dead)>0:
		print(f"{class_count[where_dead][0]} cells die during the movie...")
	if len(where_else)>0:
		print(f"{class_count[where_else][0]} objects are miscellaneous...")
	
	return(df)

def set_size(width, fraction=1, subplots=(1, 1)):
	"""Set figure dimensions to avoid scaling in LaTeX.

	Parameters
	----------
	width: float or string
			Document width in points, or string of predined document type
	fraction: float, optional
			Fraction of the width which you wish the figure to occupy
	subplots: array-like, optional
			The number of rows and columns of subplots.
	Returns
	-------
	fig_dim: tuple
			Dimensions of figure in inches
	"""
	if width == 'thesis':
		width_pt = 426.79135
	elif width == 'beamer':
		width_pt = 307.28987
	else:
		width_pt = width

	# Width of figure (in pts)
	fig_width_pt = width_pt * fraction
	# Convert from pt to inches
	inches_per_pt = 1 / 72.27

	# Golden ratio to set aesthetic figure height
	# https://disq.us/p/2940ij3
	golden_ratio = (5**.5 - 1) / 2

	# Figure width in inches
	fig_width_in = fig_width_pt * inches_per_pt
	# Figure height in inches
	fig_height_in = fig_width_in * golden_ratio * (subplots[0] / subplots[1])

	return (fig_width_in, fig_height_in)
	
def plot_cell_signal(df_track,blue,red,green,PxToUm,max_signal,ax,path=None):
	
	xpos = df_track.X.to_numpy()
	ypos = df_track.Y.to_numpy()

	cclass = df_track.CLASS.to_numpy()[0]
	t0 = df_track.T0.to_numpy()[0]
	blue_signal = df_track.BLUE_INTENSITY.to_numpy()
	red_signal = df_track.RED_INTENSITY.to_numpy()
	frames = df_track["T"].to_numpy()
	tid = df_track.TID.to_numpy()[0]
	
	patch = 25
	blue = np.array([np.pad(f,[patch+1,patch+1],mode="constant") for f in blue])	
	red = np.array([np.pad(f,[patch+1,patch+1],mode="constant") for f in red])
	green = np.array([np.pad(f,[patch+1,patch+1],mode="constant") for f in green])

	xmin0 = int(xpos[0]) + (patch + 1) - patch
	xmax0 = int(xpos[0]) +  (patch + 1) + patch
	xminm1 = int(xpos[-1]) + (patch + 1) - patch
	xmaxm1 = int(xpos[-1]) +  (patch + 1) + patch
	
	ymin0 = int(ypos[0]) + (patch + 1) - patch
	ymax0 = int(ypos[0]) +  (patch + 1) + patch
	yminm1 = int(ypos[-1]) + (patch + 1) - patch
	ymaxm1 = int(ypos[-1]) +  (patch + 1) + patch

	mpl.rcParams.update(mpl.rcParamsDefault)
	#plt.style.use('tex')
	width = 469.75502
	fig= plt.figure(figsize=set_size(width, fraction=1.25,subplots=(5,3)))
	spec = plt.GridSpec(5, 3,wspace=0.) #wspace=0.2, hspace=0.,bottom=0.2  
	ax = fig.add_subplot(spec[1:4,:])
	ax.plot(frames,blue_signal,c='tab:blue',linewidth=3)
	ax.plot(frames,red_signal,c='tab:red',linewidth=3)
	ax.set_ylim(0,np.amax(max_signal))
	spacing = 0.5 # This can be your user specified spacing. 
	minorLocator = MultipleLocator(1)
	ax.xaxis.set_minor_locator(minorLocator)
	ax.xaxis.set_major_locator(MultipleLocator(5))
	if ((cclass==0)*(int(t0)>=0)*(int(t0)<=63))==1:
		ax.vlines(t0,0,np.amax(max_signal),linestyles='dashed',colors="purple",alpha=0.5)
	#ax1.grid(which = 'minor')
	ax.grid(which = 'major')
	ax.set_xlabel("Frame")
	ax.set_ylabel("Intensity")

	ax11 = fig.add_subplot(spec[0,0])
	ax11.imshow(blue[0,ymin0:ymax0,xmin0:xmax0],cmap='gray')
	ax11.set_xticks([])
	ax11.set_yticks([])

	ax12 = fig.add_subplot(spec[0,1])
	ax12.imshow(red[0,ymin0:ymax0,xmin0:xmax0],cmap='gray')
	ax12.set_xticks([])
	ax12.set_yticks([])

	ax13 = fig.add_subplot(spec[0,2])
	ax13.imshow(green[0,ymin0:ymax0,xmin0:xmax0],cmap='gray')
	ax13.set_xticks([])
	ax13.set_yticks([])

	ax11 = fig.add_subplot(spec[4,0])
	ax11.imshow(blue[-1,yminm1:ymaxm1,xminm1:xmaxm1],cmap='gray')
	ax11.set_xticks([])
	ax11.set_yticks([])

	ax12 = fig.add_subplot(spec[4,1])
	ax12.imshow(red[-1,yminm1:ymaxm1,xminm1:xmaxm1],cmap='gray')
	ax12.set_xticks([])
	ax12.set_yticks([])

	ax13 = fig.add_subplot(spec[4,2])
	ax13.imshow(green[-1,yminm1:ymaxm1,xminm1:xmaxm1],cmap='gray')
	ax13.set_xticks([])
	ax13.set_yticks([])


	plt.tight_layout()
	plt.savefig(path+"output/signal_images/"+str(tid)+".png")
	plt.close()
	
def prepare_cell_signal_plot():
	mpl.rcParams.update(mpl.rcParamsDefault)
	#plt.style.use('tex')
	width = 469.75502
	fig= plt.figure(figsize=set_size(width, fraction=1.25,subplots=(5,3)))
	spec = plt.GridSpec(5, 3,wspace=0.) #wspace=0.2, hspace=0.,bottom=0.2  
	ax = fig.add_subplot(spec[1:4,:])
	ax11 = fig.add_subplot(spec[0,0])
	ax11.set_xticks([])
	ax11.set_yticks([])
	ax12 = fig.add_subplot(spec[0,1])
	ax12.set_xticks([])
	ax12.set_yticks([])
	ax13 = fig.add_subplot(spec[0,2])
	ax13.set_xticks([])
	ax13.set_yticks([])
	ax11_ = fig.add_subplot(spec[4,0])
	ax11_.set_xticks([])
	ax11_.set_yticks([])
	ax12_ = fig.add_subplot(spec[4,1])
	ax12_.set_xticks([])
	ax12_.set_yticks([])
	ax13_ = fig.add_subplot(spec[4,2])
	ax13_.set_xticks([])
	ax13_.set_yticks([])
	axes = [ax,ax11,ax12,ax13,ax11_,ax12_,ax13_]
	return(fig,spec,axes)

def plot_cell_signal2(df_track,blue,red,green,PxToUm,max_signal,fig,spec,axes=None,path=None):
	
	xpos = df_track.X.to_numpy()
	ypos = df_track.Y.to_numpy()

	cclass = df_track.CLASS.to_numpy()[0]
	t0 = df_track.T0.to_numpy()[0]
	blue_signal = df_track.BLUE_INTENSITY.to_numpy()
	red_signal = df_track.RED_INTENSITY.to_numpy()
	frames = df_track["T"].to_numpy()
	tid = df_track.TID.to_numpy()[0]
	
	patch = 25
	blue = np.array([np.pad(f,[patch+1,patch+1],mode="constant") for f in blue])	
	red = np.array([np.pad(f,[patch+1,patch+1],mode="constant") for f in red])
	green = np.array([np.pad(f,[patch+1,patch+1],mode="constant") for f in green])

	xmin0 = int(xpos[0]) + (patch + 1) - patch
	xmax0 = int(xpos[0]) +  (patch + 1) + patch
	xminm1 = int(xpos[-1]) + (patch + 1) - patch
	xmaxm1 = int(xpos[-1]) +  (patch + 1) + patch
	
	ymin0 = int(ypos[0]) + (patch + 1) - patch
	ymax0 = int(ypos[0]) +  (patch + 1) + patch
	yminm1 = int(ypos[-1]) + (patch + 1) - patch
	ymaxm1 = int(ypos[-1]) +  (patch + 1) + patch

	for a in axes:
		a.clear()
	
	ax = axes[0]; ax11 = axes[1];
	ax12 = axes[2]; ax13 = axes[3];
	ax11_ = axes[4]; ax12_ = axes[5];
	ax13_ = axes[6];
	
	spacing = 0.5 # This can be your user specified spacing. 
	minorLocator = MultipleLocator(1)
	ax.xaxis.set_minor_locator(minorLocator)
	ax.xaxis.set_major_locator(MultipleLocator(5))
	ax.grid(which = 'major')
	ax.set_xlabel("Frame")
	ax.set_ylabel("Intensity")
	
	ax.plot(frames,blue_signal,c='tab:blue',linewidth=3)
	ax.plot(frames,red_signal,c='tab:red',linewidth=3)
	ax.set_ylim(0,np.amax(max_signal))
	if ((cclass==0)*(int(t0)>=0)*(int(t0)<=63))==1:
		ax.vlines(t0,0,np.amax(max_signal),linestyles='dashed',colors="purple",alpha=0.5)

	ax11.imshow(blue[0,ymin0:ymax0,xmin0:xmax0],cmap='gray')

	ax12.imshow(red[0,ymin0:ymax0,xmin0:xmax0],cmap='gray')

	ax13.imshow(green[0,ymin0:ymax0,xmin0:xmax0],cmap='gray')

	ax11_.imshow(blue[-1,yminm1:ymaxm1,xminm1:xmaxm1],cmap='gray')


	ax12_.imshow(red[-1,yminm1:ymaxm1,xminm1:xmaxm1],cmap='gray')

	ax13_.imshow(green[-1,yminm1:ymaxm1,xminm1:xmaxm1],cmap='gray')

	plt.tight_layout()
	fig.savefig(path+"output/signal_images/"+str(tid)+".png")

