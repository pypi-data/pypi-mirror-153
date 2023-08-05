from __future__ import print_function, unicode_literals, absolute_import, division
import sys
import numpy as np
import matplotlib
matplotlib.rcParams["image.interpolation"] = None
import matplotlib.pyplot as plt

from glob import glob
from tqdm import tqdm
from tifffile import imread
from csbdeep.utils import Path, normalize
import os
from stardist import fill_label_holes, random_label_cmap, calculate_extents, gputools_available
from stardist.matching import matching, matching_dataset
from stardist.models import Config2D, StarDist2D, StarDistData2D
from natsort import natsorted
from tensorflow.config.experimental import list_physical_devices
from csbdeep.utils.tf import limit_gpu_memory
import gc
from tensorflow.keras.backend import clear_session
from tensorflow.compat.v1.keras.backend import get_session

from numba import cuda


home_dir = os.path.expanduser('~')
home_dir+="/"
np.random.seed(42)
lbl_cmap = random_label_cmap()

def random_fliprot(img, mask): 
    assert img.ndim >= mask.ndim
    axes = tuple(range(mask.ndim))
    perm = tuple(np.random.permutation(axes))
    img = img.transpose(perm + tuple(range(mask.ndim, img.ndim))) 
    mask = mask.transpose(perm) 
    for ax in axes: 
        if np.random.rand() > 0.5:
            img = np.flip(img, axis=ax)
            mask = np.flip(mask, axis=ax)
    return img, mask 

def random_intensity_change(img):
    img = img*np.random.uniform(0.6,2) + np.random.uniform(-0.2,0.2)
    return img


def augmenter(x, y):
    """Augmentation of a single input/label image pair.
    x is an input image
    y is the corresponding ground-truth label image
    """
    x, y = random_fliprot(x, y)
    x = random_intensity_change(x)
    # add some gaussian noise
    sig = 0.02*np.random.uniform(0,1)
    x = x + sig*np.random.normal(0,1,x.shape)
    return x, y

def create_dataset(folder,option="tc"):
	labels = [imread(im) for im in natsorted(glob(folder+"/labels/*_labelled.tif"))]
	images = [imread(im) for im in natsorted(glob(folder+"/images/*.tif"))]

	images_channel_first = []
	for im in images:
		if im.shape[0]==4:
			images_channel_first.append(im[[0,1,3]])
		elif im.shape[0]==3:
			images_channel_first.append(im)
		elif im.shape[-1]==3:
			im = np.moveaxis(im,-1,0)
			images_channel_first.append(im)

	print(f"Concatenated data shape = {np.shape(images_channel_first)}")
	X = np.array(images_channel_first,dtype=int)
	Y = np.array(labels,dtype=int)
	X = np.moveaxis(X,1,-1)

	if option=="tc":
		X = X[:,:,:,1:]
	elif option=="nk":
		X = X[:,:,:,[0]]

	print(f"Input shape: {X.shape}")

	n_channel = 1 if X[0].ndim == 2 else X[0].shape[-1]
	print(f"Number of channels: {n_channel}")

	axis_norm = (0,1)   # normalize channels independently

	X = [normalize(x,1,99.9,axis=axis_norm,clip=True) for x in tqdm(X)]
	Y = [fill_label_holes(y) for y in tqdm(Y)]	

	rng = np.random.RandomState(42)
	ind = rng.permutation(len(X))
	n_val = max(1, int(round(0.2 * len(ind))))
	ind_train, ind_val = ind[:-n_val], ind[-n_val:]
	X_val, Y_val = [X[i] for i in ind_val]  , [Y[i] for i in ind_val]
	X_trn, Y_trn = [X[i] for i in ind_train], [Y[i] for i in ind_train] 
	print('number of images: %3d' % len(X))
	print('- training:       %3d' % len(X_trn))
	print('- validation:     %3d' % len(X_val))

	return(X_trn, Y_trn, X_val, Y_val, n_channel)

def createStarDist(model_name, output_dir, nbr_epochs=100, n_channel=3,dropout_rate=0.3,batch_size=8):

	n_rays = 32
	gpus = list_physical_devices("GPU")
	if gpus:
		use_gpu = True
	else:
		use_gpu = False

	grid = (2,2)
	conf = Config2D (
	    n_rays       = n_rays,
	    grid         = grid,
	    use_gpu      = use_gpu,
	    n_channel_in = n_channel,
	    unet_dropout = dropout_rate,
	    unet_batch_norm = False,
	    unet_n_conv_per_depth=3,
	    train_epochs = nbr_epochs,
	    train_reduce_lr = {'factor': 0.1, 'patience': 40, 'min_delta': 0},
	    unet_n_depth = 2,
	    train_batch_size = batch_size,
	)

	if use_gpu:
		limit_gpu_memory(None, allow_growth=True)

	model = StarDist2D(conf, name=model_name, basedir=output_dir)

	return(model)

def train_StarDist(model_name, dataset_folder, output_dir, nbr_epochs, batch_size, option="tc"):

	X_trn, Y_trn, X_val, Y_val, n_channel = create_dataset(dataset_folder,option=option)
	print(np.shape(X_trn), n_channel)
	model = createStarDist(model_name, output_dir, n_channel=n_channel, nbr_epochs=nbr_epochs, batch_size=batch_size)
	model.train(X_trn, Y_trn, validation_data=(X_val,Y_val), augmenter=augmenter)

	model.optimize_thresholds(X_val, Y_val)
	
	del model; del X_trn; del Y_trn; del X_val; del Y_val;

	try:
		cuda.select_device(0)
		cuda.close()
	except:
		pass

	gc.collect()