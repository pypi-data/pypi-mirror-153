from random import randrange, choices, shuffle
import numpy as np
import matplotlib.pyplot as plt
import os
from tifffile import imread
from glob import glob

from tensorflow.keras.callbacks import CSVLogger, EarlyStopping, ReduceLROnPlateau, TensorBoard, ModelCheckpoint
from tensorflow.config.experimental import list_physical_devices, set_memory_growth
import shutil
import tqdm
import time
import gc
import datetime
from datetime import datetime

from tensorflow.keras.layers import Dropout, concatenate, Multiply, Dense, GlobalMaxPooling1D, Add, UpSampling1D, MaxPooling1D, AveragePooling1D, GlobalAveragePooling1D, Conv1D, Activation, UpSampling2D, Conv2DTranspose, BatchNormalization, Flatten,Reshape, Conv2D, MaxPooling2D, Input, Concatenate, LeakyReLU, add
from tensorflow.keras import metrics, Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import to_categorical, plot_model

from keras.layers import Concatenate
from tensorflow.keras.utils import plot_model

gpus = list_physical_devices('GPU')
for gpu in gpus:
	set_memory_growth(gpu, True)

def create_dataset(folder, augmentation=True, channel_option="all", normalization="minmax", model_signal_length = 63, output_dir=""):
	
	# Load the data from folder
	set_paths = glob(f"{folder}/*.npy")
	sets = [np.load(s,allow_pickle=True)[:,:6] for s in set_paths]
	sets_corrected = []
	for s in sets:
		#print(s.shape)
		if s.shape[1]==6:
			s = s[:,[0,1,2,4,5]]
			sets_corrected.append(s)
		else:
			sets_corrected.append(s)

	print(f"{len(sets)} sub sets have been loaded...")
	data = np.array(np.concatenate(sets_corrected))
	print(f"The number of input cells = {len(data)}...")
	
	#Define input / output
	inputs = data[:,1:3] #signals
	print(f"Shape of the input : {inputs.shape}")
	outputs = np.array(data[:,0]) #class
	print(f"Shape of the output : {outputs.shape}")
	#Initialize the death times of non dead cells
	classes = outputs
	death_times = np.array(data[:,-1],dtype=np.float64)
	death_times[(classes!=0.0)] = -1
	death_times[(death_times==0.0)] = -1

	#Reshape the input and pad with zeros
	inputs_reshaped = np.zeros((len(inputs),model_signal_length,2))
	for k in range(len(inputs)):
		blue_temp = inputs[k,0]; red_temp = inputs[k,1];
		if len(blue_temp)<model_signal_length:
			blue_temp = np.concatenate([blue_temp,np.zeros(model_signal_length - len(blue_temp))])
			red_temp = np.concatenate([red_temp,np.zeros(model_signal_length - len(red_temp))])
		inputs_reshaped[k,:,0] = blue_temp
		inputs_reshaped[k,:,1] = red_temp
	print(f"Shape of the reshaped input: {inputs_reshaped.shape}")
	
	if augmentation:
		
		nbr_augment = 150000
		randomize = np.arange(len(inputs_reshaped))
		indices = choices(randomize,k=nbr_augment)

		illum_shift_blue = np.linspace(0,0.5,1000)
		illum_shift_red = np.linspace(0,0.5,1000)
		noise_fluct = np.linspace(0,0.05,1000)
		pm = [-1,1]

		data_augment = np.zeros((nbr_augment,model_signal_length,2)); outputs_augment = []; death_times_augment = [];
		
		for k in range(len(indices)):
			random_noise_b = np.array(choices(noise_fluct,k=model_signal_length))
			random_noise_r = np.array(choices(noise_fluct,k=model_signal_length))
			sign_noise_b = np.array(choices(pm,k=model_signal_length),dtype='int')
			sign_noise_r = np.array(choices(pm,k=model_signal_length),dtype='int')

			blue_src = np.array(inputs_reshaped[indices[k]][:,0])
			red_src = np.array(inputs_reshaped[indices[k]][:,1])

			#plt.plot(blue_src,c='b')
			#plt.plot(red_src,c='r')

			blue_transform = blue_src*(1+random_noise_b*sign_noise_b)
			red_transform = red_src*(1+random_noise_r*sign_noise_r)   

			death_time = int(outputs[indices[k]])
			if (death_time>0.0)*(death_time<(model_signal_length-3)):
				randextinction = randrange(death_time+3,model_signal_length)
			elif (death_time<0.0):
				randextinction=randrange(15,model_signal_length)
			else:
				randextinction = len(blue_transform)

			blue_transform[randextinction:] = 0.0
			red_transform[randextinction:] = 0.0

			data_augment[k,:,0] = blue_transform
			data_augment[k,:,1] = red_transform
			outputs_augment.append(outputs[indices[k]])
			death_times_augment.append(death_times[(indices[k])])
			

		outputs_augment = np.array(outputs_augment)
		inputs_reshaped = np.concatenate([inputs_reshaped,data_augment])
		outputs = np.concatenate([outputs,outputs_augment])
		outputs2 = np.concatenate([death_times, death_times_augment])
		
		print(f"Shape of the augmented input: {inputs_reshaped.shape}")
		print(f"Shape of the augmented output (classes): {outputs.shape}")
		print(f"Shape of the augmented output (death times): {outputs2.shape}")
		
	if normalization=="minmax":

		inputs_rescale = np.copy(inputs_reshaped)
		min_max_rescaler = []
		for i in range(2):
			maxx = np.amax(inputs_reshaped[:,:,i])
			minn = np.amin(inputs_reshaped[:,:,i])
			MaxMin = maxx - minn
			inputs_rescale[:,:,i] = (inputs_reshaped[:,:,i]-minn) / MaxMin
			min_max_rescaler.append([minn,maxx])

		inputs_rescale = np.array(inputs_rescale)
		np.save(output_dir+f"min_max_rescaler_combined_{model_signal_length}.npy",min_max_rescaler)

		outputs2_rescale = np.copy(outputs2)
		min_max_rescaler_dt = []
		maxx = np.amax(outputs2)
		minn = np.amin(outputs2)
		MaxMin = maxx - minn
		outputs2_rescale = (outputs2-minn) / MaxMin
		min_max_rescaler_dt.append([minn,maxx])

		outputs2_rescale = np.array(outputs2_rescale)
		np.save(output_dir+f"min_max_rescaler_combined_death_times_{model_signal_length}.npy",min_max_rescaler_dt)

#     elif normalization=="standardization":

#         inputs_rescale = np.copy(inputs_reshaped)
#         standardizer = []
#         for i in range(2):
#             mean = np.mean(inputs_reshaped[:,:,i])
#             std = np.std(inputs_reshaped[:,:,i])

#             inputs_rescale[:,:,i] = (inputs_reshaped[:,:,i]-mean) / std
#             standardizer.append([mean,std])

#         inputs_rescale = np.array(inputs_rescale)
#         np.save("standardizer_rescaler.npy",standardizer)

	dataX = np.array(inputs_rescale)
	dataY = np.array(outputs)
	dataY2 = np.array(outputs2_rescale)

	randomize = np.arange(len(dataX))
	shuffle(randomize)
	dataX_sub = dataX[randomize[:]]
	dataY_sub = dataY[randomize[:]]
	dataY2_sub = dataY2[randomize[:]]

	if channel_option=="blue":
		dataX_sub = dataX_sub[:,:,0]
		dataX_sub = np.reshape(dataX_sub,(dataX_sub.shape[0], dataX_sub.shape[1], 1))
	elif channel_option=="red":
		dataX_sub = dataX_sub[:,:,1]
		dataX_sub = np.reshape(dataX_sub,(dataX_sub.shape[0], dataX_sub.shape[1], 1))

	print(f"dataX_sub shape: {dataX_sub.shape}")
	dataY_sub = to_categorical(dataY_sub)

	return(dataX_sub, dataY_sub, dataY2_sub)

def subModel(inputs,n_slices,dense_neurons,dropout_rate, name):
    x = Conv1D(8, 6,activation="relu")(inputs)
    if n_slices>1:
        for i in range(n_slices-1):
            x = Conv1D(16, 7,activation="relu",padding="same")(x)
    x = MaxPooling1D()(x)
    x = Dropout(dropout_rate)(x)
    for i in range(n_slices):
        x = Conv1D(32, 3,activation="relu",padding="same")(x)
    x = MaxPooling1D()(x)
    x = Dropout(dropout_rate)(x)
    for i in range(n_slices):    
        x = Conv1D(64, 3,activation="relu",padding="same")(x)
    x = MaxPooling1D()(x)
    x = Dropout(dropout_rate)(x)
    for i in range(n_slices):
        x = Conv1D(128, 3,activation="relu",padding="same")(x)
    x = MaxPooling1D()(x)
    x = Dropout(dropout_rate)(x)
    x = GlobalMaxPooling1D()(x)
    x = Dense(dense_neurons,activation="relu")(x)
    model = Model(inputs, x, name=name)
    #print(model.summary())
    return model

def combined_model(n_channels,n_slices,dense_neurons,dropout_rate, name, model_signal_length = 128):
    
    inputs = Input(shape=(model_signal_length,n_channels,))

    regressor_branch = subModel(inputs, n_slices, dense_neurons, dropout_rate, "regressor_branch")
    classifier_branch = subModel(inputs, n_slices, dense_neurons, dropout_rate, "classifier_branch")
    
    classifier_latent = Concatenate(axis=-1)([classifier_branch.outputs[0],regressor_branch.outputs[0]])
    classifier_latent = Dense(8)(classifier_latent)
    classifier_latent = Dense(3, activation='sigmoid', name='classifier')(classifier_latent)

    regressor_latent = Concatenate(axis=-1)([regressor_branch.outputs[0],classifier_branch.outputs[0]])
    regressor_latent = Dense(8)(regressor_latent)
    regressor_latent = Dense(1, activation='linear', name='regressor')(regressor_latent)

    model = Model(regressor_branch.inputs, [regressor_latent,classifier_latent])

    return(model)

def test_train_split(data_x, data_y1, data_y2, test_size=0.25):
    
    n_values = len(data_x)
    randomize = np.arange(n_values)
    np.random.shuffle(randomize)

    train_percentage = 1-test_size

    x_train = data_x[randomize[:int(train_percentage*n_values)]]
    y1_train = data_y1[randomize[:int(train_percentage*n_values)]]
    y2_train = data_y2[randomize[:int(train_percentage*n_values)]]
    

    x_test = data_x[randomize[int(train_percentage*n_values):]]
    y1_test = data_y1[randomize[int(train_percentage*n_values):]]
    y2_test = data_y2[randomize[int(train_percentage*n_values):]]
    
    #print(x_train.shape,y1_train.shape,y2_train.shape)

    return(x_train,x_test,y1_train,y1_test,y2_train,y2_test)

model_signal_length = 128

def train_cell_model(dataset_dir, output_dir, model_name, model_signal_length, nbr_epochs=200, batch_size=128):

	############################
	##### PREPARE DATASET ######
	############################

	path = output_dir+model_name+"/"
	if os.path.exists(path):
		shutil.rmtree(path)
	os.mkdir(path)

	data_x, data_y, data_y2 = create_dataset(dataset_dir, augmentation=True, channel_option="all", normalization="minmax", model_signal_length = model_signal_length, output_dir=path)
	x_train, x_test, y1_train, y1_test,y2_train, y2_test = test_train_split(np.asarray(data_x).astype(np.float32), np.asarray(data_y).astype(np.float32),np.asarray(data_y2).astype(np.float32), test_size=0.25,)

	############################
	##### CREATE THE MODEL #####
	############################

	model = combined_model(2,1,4,0.1,"combined",model_signal_length)
	reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.1,patience=30, cooldown=0, min_lr=5e-06, min_delta=1.0E-06,verbose=1,mode="min")
	model.compile(loss={'classifier':'categorical_crossentropy', 'regressor':'mse'},loss_weights=[50,1],optimizer=Adam(),metrics=["acc","mae"])

	############################
	##### TRAIN THE MODEL ######
	############################

	csv_logger = CSVLogger(path+'log.csv', append=True, separator=';')
	checkpoint_path = path+f"combined_{model_signal_length}.h5"
	cp_callback = ModelCheckpoint(checkpoint_path,monitor="val_loss",mode="min",verbose=1,save_best_only=True,save_weights_only=False,save_freq="epoch")
	callback_stop = EarlyStopping(monitor='val_loss', patience=40)

	history = model.fit(x=x_train, y=[y2_train,y1_train], batch_size=batch_size, epochs=nbr_epochs, validation_data=(x_test,[y2_test,y1_test]), callbacks=[cp_callback,csv_logger,reduce_lr,callback_stop], verbose=1)
	
	print("Training completed!")
	del x_train; del x_test;
	del y1_train; del y1_test;
	del y2_train; del y2_test;
	gc.collect()

#Parameters to use in GUI to retrain auto
#dataset_dir = "/home/limozin/ADCCFactory_2.0/src/datasets/cell_signals"
#output_dir = "/home/limozin/ADCCFactory_2.0/src/models/combined/"
#model_name = "new_test2_"+datetime.today().strftime('%Y-%m-%d')
#model_signal_length = 128
#train_cell_model(dataset_dir, output_dir, model_name, model_signal_length)
