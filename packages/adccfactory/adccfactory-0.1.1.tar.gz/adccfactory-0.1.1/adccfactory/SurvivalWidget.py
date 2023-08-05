import sys
import os
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QApplication, QTabWidget,  QComboBox, QFrame, QAction, QCheckBox, QTextBrowser, QMenu, QSlider, QFileDialog, QLabel, QPushButton, QLineEdit, QWidget, QDialog, QMainWindow, QGridLayout
from PyQt5.QtGui import QImage, QIcon, QDoubleValidator, QPixmap
from screeninfo import get_monitors
from configparser import ConfigParser
from glob import glob
import configparser
from .functions import *
from natsort import natsorted
from tifffile import imread
import numpy as np
import time
import matplotlib.pyplot as plt
from stardist.models import StarDist2D
from csbdeep.utils import normalize
from .RetrainModels import TrainCellModel, TrainStarDistTCModel, TrainStarDistNKModel
from csbdeep.io import save_tiff_imagej_compatible
import shutil
from tqdm import tqdm
#from .ControlPanel import ControlPanel
import gc
import btrack
from btrack.constants import BayesianUpdates
import pandas as pd
from waiting import wait
import shutil
pd.options.mode.chained_assignment = None  # default='warn'
from matplotlib.widgets import Slider, Button
import logging

from tensorflow.keras.models import load_model

home_dir = os.path.expanduser('~')
home_dir+="/"
current_path = os.getcwd()

logger = logging.getLogger()

class SurvivalWidget(ControlPanel):

	def __init__(self):
		super().__init__()
		print(self.exp_dir)
		print(self.FrameToMin)