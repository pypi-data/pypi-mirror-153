#!/usr/bin/env python3

import sys
import os
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot, QTimer
from PyQt5.QtWidgets import QApplication, QSizePolicy, QFrame, QMessageBox, QTabWidget, QComboBox, QAction, QCheckBox, QTextBrowser, QMenu, QSlider, QFileDialog, QLabel, QPushButton, QLineEdit, QWidget, QDialog, QMainWindow, QGridLayout
from PyQt5.QtGui import QImage, QIcon, QDoubleValidator, QPixmap
from screeninfo import get_monitors
from configparser import ConfigParser
from glob import glob
import configparser
from functions import *
from ControlPanel import ControlPanel
from ConfigNewExperiment import ConfigNewExperiment
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
import logging

from tensorflow.keras.models import load_model

Log_Format = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename = "log",
                    filemode = "w",
                    format = Log_Format, 
                    level = logging.INFO)

logger = logging.getLogger()

home_dir = os.path.expanduser('~')
home_dir+="/"
current_path = os.getcwd()

logger.debug(f"Home path = {home_dir}")
logger.debug(f"Current directory = {current_path}")

for m in get_monitors():
	logger.debug(f"Monitor resolution = ({m.width},{m.height})")
	res_w = int(m.width*0.2)
	res_h = int(m.height*0.15)

logger.debug(f"App size = ({res_w},{res_h})")

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

class ExpWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.source_dir = current_path

		self.setWindowTitle("ADCCFactory")
		self.setWindowIcon(QIcon(f"{home_dir}ADCCFactory_2.0/src/icons/icon.png"))
		#self.setGeometry(0,0,res_w,res_h)
		self.center_window()

		self._createActions()
		self._createMenuBar()

		central_widget = QWidget()
		self.grid = QGridLayout(central_widget)

		self.grid.addWidget(QLabel("Experiment folder:"), 0, 0, 1, 3)

		self.experiment_path_selection = QLineEdit()
		self.experiment_path_selection.setAlignment(Qt.AlignLeft)	
		self.experiment_path_selection.setEnabled(True)
		self.experiment_path_selection.setDragEnabled(True)
		self.experiment_path_selection.setFixedWidth(400)
		self.foldername = os.getcwd()
		self.experiment_path_selection.setText(self.foldername)
		self.grid.addWidget(self.experiment_path_selection, 1, 0, 1, 3)

		self.browse_button = QPushButton("Browse...")
		self.browse_button.clicked.connect(self.browse_experiment_folder)
		self.grid.addWidget(self.browse_button, 1, 4, 1, 1)

		self.validate_button = QPushButton("Submit")
		self.validate_button.clicked.connect(self.change_directory)
		self.grid.addWidget(self.validate_button, 2, 1, 1, 1, alignment = Qt.AlignCenter)

		self.timer = QTimer()
		self.timer.setInterval(500)
		self.timer.timeout.connect(self.update_log)
		self.timer.start()

		self.log = QTextBrowser()
		self.grid.addWidget(self.log, 3, 0, 1, 4)
		
		self.setCentralWidget(central_widget)
		self.show()

	def update_log(self):
		self.log.clear()
		try:
			with open('log') as f:
				lines = f.readlines()
				if isinstance(lines,list):
					for l in lines:
						self.log.append(l)
		except:
			pass

	def center_window(self):
		frameGm = self.frameGeometry()
		screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
		centerPoint = QApplication.desktop().screenGeometry(screen).center()
		frameGm.moveCenter(centerPoint)
		self.move(frameGm.topLeft())
		logger.debug("Moving window to the center of the screen...")

	def _createActions(self):
			self.newExp = QAction(QIcon(f"{home_dir}ADCCFactory_2.0/src/icons/icon.png"),"&New experiment...",self)
			self.newExp.triggered.connect(self.create_new_experiment)
			self.newExp.setShortcut("Ctrl+N")
					
	def _createMenuBar(self):
		menuBar = self.menuBar()
		fileMenu = QMenu("&File", self)
		menuBar.addMenu(fileMenu)
		fileMenu.addAction(self.newExp)

	def create_new_experiment(self):
		logger.info("Configuring new experiment...")
		self.new_exp_window = ConfigNewExperiment()
		self.new_exp_window.show()

		self.signal = self.new_exp_window.logtext
		self.signal.connect(self.logMessage)
		created_path = self.new_exp_window.experiment_path
		created_path.connect(self.reset_experiment_path)

	def change_directory(self):

		self.exp_dir = self.experiment_path_selection.text()
		#os.chdir(self.experiment_path_selection.text())

		logger.info(f"Setting current directory to {self.exp_dir}...")

		wells = glob(self.exp_dir+"/W*/")
		self.number_of_wells = len(wells)
		if self.number_of_wells==0:
			msgBox = QMessageBox()
			msgBox.setIcon(QMessageBox.Critical)
			msgBox.setText("No well was found in the experiment folder.\nPlease respect the W*/ nomenclature...")
			msgBox.setWindowTitle("Error")
			msgBox.setStandardButtons(QMessageBox.Ok)
			returnValue = msgBox.exec()
			if returnValue == QMessageBox.Ok:
				return(None)
			logger.info(f"No well was found in the experiment folder. Please respect the W*/ nomenclature...")		
		else:
			if self.number_of_wells==1:
				logger.info(f"Found {self.number_of_wells} well...")
			elif self.number_of_wells>1:
				logger.info(f"Found {self.number_of_wells} wells...")
			number_pos = []
			for w in wells:
				position_folders = glob(w+f"{w[1]}*/")
				number_pos.append(len(position_folders))
			logger.info(f"Number of positions per well: {number_pos}")

			self.control_panel = ControlPanel(self.exp_dir)
			self.control_panel.show()

			# controlchoices = self.control_panel.logchoices
			# controlchoices.connect(self.display_control_choice)
			# findmovie = self.control_panel.logfindmovie
			# findmovie.connect(self.is_movie_found)


	def browse_experiment_folder(self):
		self.foldername = str(QFileDialog.getExistingDirectory(self, 'Select directory'))
		self.experiment_path_selection.setText(self.foldername)
		if not os.path.exists(self.foldername+"/config.ini"):
			logger.info(f"{self.foldername} does not appear to be a valid experiment folder as it does not contain a configuration file...")
		logger.info(f"You selected experiment: {self.foldername}")

	def reset_experiment_path(self, message):
		self.experiment_path_selection.setText(message)

	def display_control_choice(self, message):
		self.log.append(message)
		self.show()

	def logMessage(self, message):
		self.log.append(message)
		self.show()

	def is_movie_found(self, message):
		self.log.append(message)
		self.show()

App = QApplication(sys.argv)
App.setStyle("Fusion")
window = ExpWindow()
sys.exit(App.exec())