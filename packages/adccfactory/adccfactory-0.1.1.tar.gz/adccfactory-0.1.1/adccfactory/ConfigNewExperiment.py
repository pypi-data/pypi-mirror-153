#!/usr/bin/env python3

import sys
import os
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QApplication, QComboBox, QAction, QCheckBox, QTextBrowser, QMenu, QSlider, QFileDialog, QLabel, QPushButton, QLineEdit, QWidget, QDialog, QMainWindow, QGridLayout
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
from csbdeep.io import save_tiff_imagej_compatible
import shutil
from tqdm import tqdm
import gc
import btrack
from btrack.constants import BayesianUpdates
import pandas as pd
import shutil
pd.options.mode.chained_assignment = None  # default='warn'

from tensorflow.keras.models import load_model

home_dir = os.path.expanduser('~')
current_path = os.getcwd()

class ConfigNewExperiment(QDialog):
	
	logtext = pyqtSignal(str)
	experiment_path = pyqtSignal(str)

	def __init__(self):
		super().__init__()

		self.newExpFolder = ""
		self.setWindowTitle("Configure new experiment...")
		
		grid = QGridLayout(self)

		self.newExpFolder = str(QFileDialog.getExistingDirectory(self, 'Select directory'))
		
		grid.addWidget(QLabel("Folder:"), 0, 0, 1, 3)
		self.supFolder = QLineEdit()
		self.supFolder.setAlignment(Qt.AlignLeft)	
		self.supFolder.setEnabled(True)
		self.supFolder.setText(self.newExpFolder)
		grid.addWidget(self.supFolder, 1, 0, 1, 2)

		self.browse_button = QPushButton("Browse...")
		self.browse_button.clicked.connect(self.browse_experiment_folder)
		grid.addWidget(self.browse_button, 1, 2, 1, 1)

		grid.addWidget(QLabel("Experiment name:"), 2, 0, 1, 3)
		self.expName = QLineEdit()
		self.expName.setAlignment(Qt.AlignLeft)	
		self.expName.setEnabled(True)
		self.expName.setFixedWidth(400)
		self.expName.setText("Untitled_Experiment")
		grid.addWidget(self.expName, 3, 0, 1, 3)

		self.number_of_wells = QLabel("Number of wells: 1")
		grid.addWidget(self.number_of_wells, 4, 0, 1, 3)

		self.SliderWells = QSlider(Qt.Horizontal, self)
		#mySlider.setGeometry(30, 40, 200, 30)
		self.SliderWells.valueChanged[int].connect(self.changeWellValue)
		self.SliderWells.setMinimum(1)
		self.SliderWells.setMaximum(9)

		grid.addWidget(self.SliderWells, 5, 0, 1, 3)

		self.number_of_positions = QLabel("Number of positions per well: 1")
		grid.addWidget(self.number_of_positions, 6, 0, 1, 3)

		self.SliderPos = QSlider(Qt.Horizontal, self)
		#mySlider.setGeometry(30, 40, 200, 30)
		self.SliderPos.valueChanged[int].connect(self.changePosValue)
		self.SliderPos.setMinimum(1)
		self.SliderPos.setMaximum(9)

		grid.addWidget(self.SliderPos, 7, 0, 1, 3)

		grid.addWidget(QLabel("Calibration from pixel to µm:"), 8, 0, 1, 3)
		self.PxToUm_field = QLineEdit()
		self.PxToUm_field.setAlignment(Qt.AlignLeft)	
		self.PxToUm_field.setEnabled(True)
		self.PxToUm_field.setFixedWidth(400)
		self.PxToUm_field.setText("0.3112")
		grid.addWidget(self.PxToUm_field, 9, 0, 1, 3)

		grid.addWidget(QLabel("Calibration from frame to minutes:"), 10, 0, 1, 3)
		self.FrameToMin_field = QLineEdit()
		self.FrameToMin_field.setAlignment(Qt.AlignLeft)	
		self.FrameToMin_field.setEnabled(True)
		self.FrameToMin_field.setFixedWidth(400)
		self.FrameToMin_field.setText("2.0")
		grid.addWidget(self.FrameToMin_field, 11, 0, 1, 3)

		self.movie_length = QLabel("Number of frames: 1")
		grid.addWidget(self.movie_length, 12, 0, 1, 3)
		self.MovieLengthSlider = QSlider(Qt.Horizontal, self)
		self.MovieLengthSlider.valueChanged[int].connect(self.changeMovieLength)
		self.MovieLengthSlider.setMinimum(2)
		self.MovieLengthSlider.setMaximum(128)
		grid.addWidget(self.MovieLengthSlider, 13, 0, 1, 3)

		grid.addWidget(QLabel("Prefix for the movies:"), 14, 0, 1, 3)
		self.movie_prefix_field = QLineEdit()
		self.movie_prefix_field.setAlignment(Qt.AlignLeft)	
		self.movie_prefix_field.setEnabled(True)
		self.movie_prefix_field.setFixedWidth(400)
		self.movie_prefix_field.setText("Aligned")
		grid.addWidget(self.movie_prefix_field, 15, 0, 1, 3)

		grid.addWidget(QLabel("X shape in pixels:"), 16, 0, 1, 3)
		self.shape_x_field = QLineEdit()
		self.shape_x_field.setAlignment(Qt.AlignLeft)	
		self.shape_x_field.setEnabled(True)
		self.shape_x_field.setFixedWidth(400)
		self.shape_x_field.setText("2048")
		grid.addWidget(self.shape_x_field, 17, 0, 1, 3)

		grid.addWidget(QLabel("Y shape in pixels:"), 18, 0, 1, 3)
		self.shape_y_field = QLineEdit()
		self.shape_y_field.setAlignment(Qt.AlignLeft)	
		self.shape_y_field.setEnabled(True)
		self.shape_y_field.setFixedWidth(400)
		self.shape_y_field.setText("2048")
		grid.addWidget(self.shape_y_field, 19, 0, 1, 3)

		self.hoescht_index = QLabel("Hoescht channel: 0")
		grid.addWidget(self.hoescht_index, 20, 0, 1, 3)
		self.SliderBlue = QSlider(Qt.Horizontal, self)
		self.SliderBlue.valueChanged[int].connect(self.changeBlueValue)
		self.SliderBlue.setMinimum(0)
		self.SliderBlue.setMaximum(3)
		grid.addWidget(self.SliderBlue, 21, 0, 1, 3)

		self.pi_index = QLabel("Propidium Iodine channel: 0")
		grid.addWidget(self.pi_index, 22, 0, 1, 3)
		self.SliderRed = QSlider(Qt.Horizontal, self)
		self.SliderRed.valueChanged[int].connect(self.changeRedValue)
		self.SliderRed.setMinimum(0)
		self.SliderRed.setMaximum(3)
		grid.addWidget(self.SliderRed, 23, 0, 1, 3)

		self.green_check = QCheckBox("CFSE channel")
		self.green_check.toggled.connect(self.show_green_slider)
		grid.addWidget(self.green_check, 24,0,1,1)
		self.SliderGreen = QSlider(Qt.Horizontal, self)
		self.SliderGreen.valueChanged[int].connect(self.changeGreenValue)
		self.SliderGreen.setMinimum(0)
		self.SliderGreen.setMaximum(3)
		grid.addWidget(self.SliderGreen, 25, 0, 1, 3)
		self.SliderGreen.hide()

		self.validate_button = QPushButton("Submit")
		self.validate_button.clicked.connect(self.create_config)
		grid.addWidget(self.validate_button, 26, 1, 1, 1, alignment = Qt.AlignCenter)

	def show_green_slider(self):
		if self.green_check.isChecked():
			self.SliderGreen.show()
		else:
			self.green_check.setText("CFSE channel")
			self.SliderGreen.hide()

	def changeMovieLength(self, value):
		self.movie_length.setText(f"Number of frames: {value}")

	def changeWellValue(self, value):
		self.number_of_wells.setText(f"Number of wells: {value}")

	def changeGreenValue(self, value):
		self.green_check.setText(f"CFSE channel: {value}")

	def changeRedValue(self, value):
		self.pi_index.setText(f"Propidium Iodine channel: {value}")

	def changeBlueValue(self, value):
		self.hoescht_index.setText(f"Hoescht channel: {value}")

	def changePosValue(self, value):
		self.number_of_positions.setText(f"Number of positions per well: {value}")

	def browse_experiment_folder(self):
		self.newExpFolder = str(QFileDialog.getExistingDirectory(self, 'Select directory'))
		self.supFolder.setText(self.newExpFolder)

	def create_config(self):
		try:
			directory = self.supFolder.text()+"/"+self.expName.text()
			os.mkdir(directory)
			os.chdir(directory)
			self.create_subfolders()
			self.create_config_file()
			for_log = (f"Experiment {self.expName.text()} successfully created in directory {self.supFolder.text()}...\n"
				f"Number of wells: {self.SliderWells.value()}\n"
				f"Number of positions per well: {self.SliderPos.value()}\n"
				f"Pixel width calibration: 1 px = {self.PxToUm_field.text()} µm\n"
				f"Interval between two frames: 1 frame = {self.FrameToMin_field.text()} min\n"
				f"Number of frames per movie: {self.MovieLengthSlider.value()}\n"
				f"Prefix for the movies: {self.movie_prefix_field.text()}\n"
				f"Shape of the movies: ({self.shape_x_field.text()},{self.shape_y_field.text()})\n"
				f"Hoescht channel: {self.SliderBlue.value()}\n"
				f"Propidium Iodine channel: {self.SliderRed.value()}\n"
				)
			if self.green_check.isChecked():
				for_log+=f"CFSE channel: {self.SliderGreen.value()}"
			else:
				for_log+="You did not set a CFSE channel"
			self.logtext.emit(for_log)
			self.experiment_path.emit(directory)
		except FileExistsError:
			self.logtext.emit("This experiment already exists... Please select another name.")

	def create_subfolders(self):
		self.nbr_wells = self.SliderWells.value()
		self.nbr_positions = self.SliderPos.value()
		#self.logtext.emit(f"{self.nbr_wells} wells with {self.nbr_positions} position subfolders have been created...")
		for k in range(self.nbr_wells):
			well_name = f"W{k+1}/"
			os.mkdir(well_name)
			for p in range(self.nbr_positions):
				position_name = well_name+f"{k+1}0{p}/"
				os.mkdir(position_name)
				os.mkdir(position_name+"/movie/")

	def create_config_file(self):
		config = ConfigParser()

		# add a new section and some values
		config.add_section('MovieSettings')
		config.set('MovieSettings', 'PxToUm', self.PxToUm_field.text())
		config.set('MovieSettings', 'FrameToMin', self.FrameToMin_field.text())
		config.set('MovieSettings', 'len_movie', str(self.MovieLengthSlider.value()))
		config.set('MovieSettings', 'shape_x', self.shape_x_field.text())
		config.set('MovieSettings', 'shape_y', self.shape_y_field.text())
		config.set('MovieSettings', 'transmission', str(0))		
		config.set('MovieSettings', 'blue_channel', str(self.SliderBlue.value()))
		config.set('MovieSettings', 'red_channel', str(self.SliderRed.value()))
		if self.green_check.isChecked():
			config.set('MovieSettings', 'green_channel', str(self.SliderGreen.value()))
		else:
			config.set('MovieSettings', 'green_channel', "-1")
		config.set('MovieSettings', 'movie_prefix', self.movie_prefix_field.text())

		config.add_section('SurvivalFit')
		config.set('SurvivalFit', 'survival_fit_min', "0")
		config.set('SurvivalFit', 'survival_fit_max', str(self.MovieLengthSlider.value()))

		config.add_section('SearchRadii')
		config.set('SearchRadii', 'search_radius_tc', "100")
		config.set('SearchRadii', 'search_radius_nk', "75")

		config.add_section('BinningParameters')
		config.set('BinningParameters', 'dtc', "1")
		config.set('BinningParameters', 'dnk', "1")
		config.set('BinningParameters', 'dt_frame', "1")
		config.set('BinningParameters', 'time_dilation', "1")


		config.add_section('Thresholds')
		config.set('Thresholds', 'cell_nbr_threshold', "10")
		config.set('Thresholds', 'intensity_measurement_radius', "26")
		config.set('Thresholds', 'intensity_measurement_radius_nk', "10")
		config.set('Thresholds', 'minimum_tracklength', "0")
		config.set('Thresholds', 'model_signal_length', "128")
		config.set('Thresholds', 'hide_frames_for_tracking', "")


		config.add_section('Labels')
		label_str=""
		for k in range(self.nbr_wells):
			label_str+=str(k)+","
			config.set('Labels', 'label_wells', label_str[:-1])

		config.set('Labels', 'concentrations', "")
		config.set('Labels', 'cell_types', "")


		config.add_section('Paths')
		print("path = ",os.path.join(home_dir, "ADCCFactory_2.0/src/models/"))
		config.set('Paths', 'modelpath', os.path.join(home_dir, "ADCCFactory_2.0/src/models/")) #f"{home_dir}ADCCFactory_2.0/src/models/"

		config.add_section('Display')
		config.set('Display', 'blue_percentiles', "1,99")
		config.set('Display', 'red_percentiles', "1,99.5")
		config.set('Display', 'fraction', "4")

		# save to a file
		with open('config.ini', 'w') as configfile:
			config.write(configfile)
		self.close()
