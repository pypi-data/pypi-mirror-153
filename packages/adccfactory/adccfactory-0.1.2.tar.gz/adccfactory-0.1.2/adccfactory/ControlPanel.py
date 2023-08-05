#!/usr/bin/env python3

import sys
import os
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QApplication, QTabWidget,  QMessageBox, QSizePolicy, QComboBox, QFrame, QAction, QCheckBox, QTextBrowser, QMenu, QSlider, QFileDialog, QLabel, QPushButton, QLineEdit, QWidget, QDialog, QMainWindow, QGridLayout
from PyQt5.QtGui import QImage, QIcon, QDoubleValidator, QPixmap
from screeninfo import get_monitors
from configparser import ConfigParser
from glob import glob
import configparser
from lifelines import KaplanMeierFitter,CoxPHFitter

from functions import *
#from .control_classification import VisualInspectionApp
from natsort import natsorted
from tifffile import imread
import numpy as np
import time
import matplotlib.pyplot as plt
from stardist.models import StarDist2D
from csbdeep.utils import normalize
from RetrainModels import TrainCellModel, TrainStarDistTCModel, TrainStarDistNKModel
from csbdeep.io import save_tiff_imagej_compatible
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
from matplotlib.lines import Line2D
import shutil
from tqdm import tqdm
import gc
import btrack
from btrack.constants import BayesianUpdates
import pandas as pd
from waiting import wait
import shutil
pd.options.mode.chained_assignment = None  # default='warn'
from matplotlib.widgets import Slider, Button
import logging
import subprocess


from tensorflow.keras.models import load_model

home_dir = os.path.expanduser('~')
home_dir+="/"
current_path = os.getcwd()

logger = logging.getLogger()

class QHSeperationLine(QFrame):
  '''
  a horizontal seperation line\n
  '''
  def __init__(self):
    super().__init__()
    self.setMinimumWidth(1)
    self.setFixedHeight(20)
    self.setFrameShape(QFrame.HLine)
    self.setFrameShadow(QFrame.Sunken)
    self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
    return

class ControlPanel(QMainWindow):

	def __init__(self, exp_dir=""):
		super().__init__()

		self.exp_dir = exp_dir
		self.exp_dir += "/"

		self.setWindowIcon(QIcon(f"{home_dir}ADCCFactory_2.0/src/icons/icon.png"))
		logger.debug(f"Icon path = {f'{home_dir}ADCCFactory_2.0/src/icons/icon.png'}")

		self.center_window()
		self.wells = natsorted(glob(self.exp_dir + "W*/"))
		self.load_configuration()

		self.setWindowTitle("Control panel")

		self.stack = None
		condition_label = QLabel("condition: ")
		position_label = QLabel("position: ")

		self.positions = []
		for w in self.wells:
			logger.debug(f"Search positions as: {w+f'{w[-2]}*/'}")
			positions_path = natsorted(glob(w+f"{w[-2]}*/"))
			self.positions.append([os.path.split(pos[:-1])[1] for pos in positions_path])

		self.well_list = QComboBox()
		self.well_list.addItems(self.well_labels)
		self.well_list.addItems(["*"])
		self.well_list.activated.connect(self.display_positions)

		self.position_list = QComboBox()
		self.position_list.addItems(["*"])
		self.position_list.addItems(self.positions[0])

		w = QWidget()
		grid = QGridLayout(w)
		grid.addWidget(QLabel("Well:"), 0, 0, 1,1)
		grid.addWidget(self.well_list, 1, 0, 1, 3)
		grid.addWidget(QLabel("Position:"),2,0,1,1)
		grid.addWidget(self.position_list, 3,0,1,3)
		hsep = QHSeperationLine()
		grid.addWidget(hsep, 4, 0, 1, 3)

		ProcessTC = self.ProcessTCWidget()
		ProcessNK = self.ProcessNKWidget()
		#ProcessNeigh = self.ProcessNeighWidget()

		CheckClass = self.CheckClassificationWidget()

		ProcessFrame = QFrame()
		grid_process = QGridLayout(ProcessFrame)
		grid_process.addWidget(ProcessTC, 0, 0, 1, 1)
		grid_process.addWidget(ProcessNK, 1, 0, 1, 1)
		#grid_process.addWidget(ProcessNeigh, 2, 0, 1, 1)

		# CheckFrame = QFrame()
		# grid_check = QGridLayout(CheckFrame)
		# grid_check.addWidget(CheckClass, 0, 0, 1, 1)

		AnalyzeFrame = QFrame()
		grid_analyze = QGridLayout(AnalyzeFrame)
		NeighboursW = self.ProcessNeighWidget()
		SurvivalW = self.ProcessSurvivalWidget()
		grid_analyze.addWidget(NeighboursW, 0, 0, 1, 1)
		grid_analyze.addWidget(SurvivalW, 1, 0, 1, 1)		

		tabWidget = QTabWidget()
		tabWidget.addTab(ProcessFrame, "Process")
		#tabWidget.addTab(CheckFrame, "Control")
		tabWidget.addTab(AnalyzeFrame, "Analyze")

		grid.addWidget(tabWidget, 6,0,1,3)

		self.setCentralWidget(w)

	def load_configuration(self):

		'''
		This methods load the configuration read in the config.ini file of the experiment.
		'''

		config = self.exp_dir + "config.ini"
		self.PxToUm = float(ConfigSectionMap(config,"MovieSettings")["pxtoum"])
		self.FrameToMin = float(ConfigSectionMap(config,"MovieSettings")["frametomin"])
		self.len_movie = int(ConfigSectionMap(config,"MovieSettings")["len_movie"])
		self.shape_x = int(ConfigSectionMap(config,"MovieSettings")["shape_x"])
		self.shape_y = int(ConfigSectionMap(config,"MovieSettings")["shape_y"])
		self.movie_prefix = ConfigSectionMap(config,"MovieSettings")["movie_prefix"]
		self.blue_channel = int(ConfigSectionMap(config,"MovieSettings")["blue_channel"])
		self.red_channel = int(ConfigSectionMap(config,"MovieSettings")["red_channel"])

		try:
			self.green_channel = int(ConfigSectionMap(config,"MovieSettings")["green_channel"])
		except:
			self.green_channel = np.nan


		self.search_radius_tc = int(ConfigSectionMap(config,"SearchRadii")["search_radius_tc"])
		self.search_radius_nk = int(ConfigSectionMap(config,"SearchRadii")["search_radius_nk"])
		self.time_dilation = int(ConfigSectionMap(config,"BinningParameters")["time_dilation"])

		self.intensity_measurement_radius = int(ConfigSectionMap(config,"Thresholds")["intensity_measurement_radius"])
		self.intensity_measurement_radius_nk = int(ConfigSectionMap(config,"Thresholds")["intensity_measurement_radius_nk"])
		self.minimum_tracklength = int(ConfigSectionMap(config,"Thresholds")["minimum_tracklength"])
		self.model_signal_length = int(ConfigSectionMap(config,"Thresholds")["model_signal_length"])

		try:
			self.hide_frames_for_tracking = np.array([int(s) for s in ConfigSectionMap(config,"Thresholds")["hide_frames_for_tracking"].split(",")])
		except:
			self.hide_frames_for_tracking = np.array([])

		self.well_labels = ConfigSectionMap(config,"Labels")["label_wells"].split(",")
		number_of_wells = len(self.wells)
		if number_of_wells != len(self.well_labels):
			self.well_labels = [str(s) for s in np.linspace(0,number_of_wells-1,number_of_wells)]

		self.concentrations = ConfigSectionMap(config,"Labels")["concentrations"].split(",")
		if number_of_wells != len(self.concentrations):
			self.concentrations = [str(s) for s in np.linspace(0,number_of_wells-1,number_of_wells)]		

		self.cell_types = ConfigSectionMap(config,"Labels")["cell_types"].split(",")
		if number_of_wells != len(self.cell_types):
			self.cell_types = [str(s) for s in np.linspace(0,number_of_wells-1,number_of_wells)]		

		self.modelpath = ConfigSectionMap(config,"Paths")["modelpath"]



	def center_window(self):

		'''
		This method centers the window horizontally and vertically
		'''

		frameGm = self.frameGeometry()
		screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
		centerPoint = QApplication.desktop().screenGeometry(screen).center()
		frameGm.moveCenter(centerPoint)
		self.move(frameGm.topLeft())

	def display_positions(self):
		if self.well_list.currentText()=="*":
			self.position_list.clear()
			self.position_list.addItems(["*"])
			position_linspace = np.linspace(0,len(self.positions[0])-1,len(self.positions[0]),dtype=int)
			position_linspace = [str(s) for s in position_linspace]
			self.position_list.addItems(position_linspace)
		else:
			pos_index = self.well_labels.index(str(self.well_list.currentText()))
			self.position_list.clear()
			self.position_list.addItems(["*"])
			self.position_list.addItems(self.positions[pos_index])

	def ProcessTCWidget(self):

		FrameTC = QFrame()
		FrameTC.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)

		grid_tc = QGridLayout(FrameTC)
		grid_tc.addWidget(QLabel("Process TCs:"), 0, 0, 1, 1)
		self.all_tc_actions = QCheckBox("Check all")
		self.all_tc_actions.toggled.connect(self.tick_all_tc_actions)
		grid_tc.addWidget(self.all_tc_actions, 0, 2, 1, 1)

		self.segment_action_tc = QCheckBox("segment TCs")
		self.segment_action_tc.setIcon(QIcon(f"{home_dir}ADCCFactory_2.0/src/icons/segment_icon.png"))
		self.segment_action_tc.toggled.connect(self.enable_segmentation_model_list_tc)

		grid_tc.addWidget(self.segment_action_tc, 1, 0, 1, 1)
		grid_tc.addWidget(QLabel("Model zoo:"),2,0,1,1)
		self.tc_seg_model_list = QComboBox()

		self.train_button_tc = QPushButton("Train new...")
		grid_tc.addWidget(self.train_button_tc, 2, 2, 1, 1)
		self.train_button_tc.clicked.connect(self.train_stardist_model_tc)

		tc_seg_models = glob(self.modelpath+"segmentation_tc/*/")
		self.tc_seg_model_list.addItems([os.path.split(s[:-1])[-1] for s in tc_seg_models])
		self.tc_seg_model_list.setEnabled(False)
		grid_tc.addWidget(self.tc_seg_model_list, 3, 0, 1, 3)

		self.track_action_tc = QCheckBox("track TCs")
		self.track_action_tc.setIcon(QIcon(f"{home_dir}ADCCFactory_2.0/src/icons/tracking_icon.png"))
		grid_tc.addWidget(self.track_action_tc, 4, 0,1,1)

		self.measure_action_tc = QCheckBox("measure TCs")
		self.measure_action_tc.setIcon(QIcon(f"{home_dir}ADCCFactory_2.0/src/icons/measure_icon.png"))
		self.measure_action_tc.toggled.connect(self.enable_cell_model_list)
		grid_tc.addWidget(self.measure_action_tc, 5,0,1,1)

		grid_tc.addWidget(QLabel("Model zoo:"),6,0,1,1)
		cell_models = glob(self.modelpath+"combined/*/")
		self.cell_models_list = QComboBox()
		self.cell_models_list.addItems([os.path.split(s[:-1])[-1] for s in cell_models])
		self.cell_models_list.setEnabled(False)
		grid_tc.addWidget(self.cell_models_list, 7, 0, 1, 3)

		self.train_button_cell = QPushButton("Train new...")
		grid_tc.addWidget(self.train_button_cell, 6, 2, 1, 1)
		self.train_button_cell.clicked.connect(self.train_cell_model)

		self.submit_button_tc = QPushButton("Submit")
		grid_tc.addWidget(self.submit_button_tc, 8,1,1,1)
		self.submit_button_tc.clicked.connect(self.process_tcs)

		grid_tc.addWidget(QHSeperationLine(), 9, 0, 1, 3)

		self.control_classification = QPushButton("Control class && regression")
		self.control_classification.setIcon(QIcon(f"{home_dir}ADCCFactory_2.0/src/icons/segment_icon.png"))
		grid_tc.addWidget(self.control_classification, 10,0,1,3)
		self.control_classification.clicked.connect(self.control_class_and_reg)

		return(FrameTC)


	def ProcessNKWidget(self):

		FrameNK = QFrame()
		FrameNK.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
		grid_nk = QGridLayout(FrameNK)	

		grid_nk.addWidget(QLabel("Process NKs:"), 0, 0, 1, 1)
		self.all_nk_actions = QCheckBox("Check all")
		self.all_nk_actions.toggled.connect(self.tick_all_nk_actions)
		grid_nk.addWidget(self.all_nk_actions, 0, 2, 1, 1)

		self.segment_action_nk = QCheckBox("segment NKs")
		self.segment_action_nk.setIcon(QIcon(f"{home_dir}ADCCFactory_2.0/src/icons/segment_icon.png"))
		self.segment_action_nk.toggled.connect(self.enable_segmentation_model_list_nk)

		self.cfse_segment = QCheckBox("CFSE")
		self.cfse_segment.toggled.connect(self.set_cfse_models)
		self.cfse_segment.setEnabled(False)

		grid_nk.addWidget(self.segment_action_nk, 1, 0, 1, 1)
		grid_nk.addWidget(self.cfse_segment, 1, 2, 1, 1)

		grid_nk.addWidget(QLabel("Model zoo:"),2,0,1,1)
		self.nk_seg_model_list = QComboBox()

		self.train_button_nk = QPushButton("Train new...")
		grid_nk.addWidget(self.train_button_nk, 2, 2, 1, 1)
		self.train_button_nk.clicked.connect(self.train_stardist_model_nk)

		nk_seg_models = glob(self.modelpath+"segmentation_nk//[!cfse]*/")
		self.nk_seg_model_list.addItems([os.path.split(s[:-1])[-1] for s in nk_seg_models])
		self.nk_seg_model_list.setEnabled(False)
		grid_nk.addWidget(self.nk_seg_model_list, 3, 0, 1, 3)

		self.classify_action_nks = QCheckBox("classify NKs")
		self.classify_action_nks.setIcon(QIcon(f"{home_dir}ADCCFactory_2.0/src/icons/measure_icon.png"))
		self.classify_action_nks.toggled.connect(self.enable_pi_thresh)				
		grid_nk.addWidget(self.classify_action_nks, 4, 0,1,1)

		#self.neigh_action_nk = QCheckBox("match neighbours")
		#self.neigh_action_nk.setIcon(QIcon(f"{home_dir}ADCCFactory_2.0/src/icons/neighbour.png"))
		#grid_nk.addWidget(self.neigh_action_nk, 5,0,1,1)

		self.pi_thresh_option = QCheckBox("set PI threshold")
		self.pi_thresh_option.toggled.connect(self.show_pi_thresh)
		self.pi_thresh_option.setEnabled(False)
		grid_nk.addWidget(self.pi_thresh_option, 4,2,1,1)

		self.pi_thresh_line = QLineEdit("500")
		grid_nk.addWidget(self.pi_thresh_line, 5,2,1,1)
		self.pi_thresh_line.hide()

		self.submit_button_nk = QPushButton("Submit")
		grid_nk.addWidget(self.submit_button_nk, 6,1,1,1)
		self.submit_button_nk.clicked.connect(self.process_nks)

		return(FrameNK)	

	def enable_pi_thresh(self):
		if self.classify_action_nks.isChecked():
			self.pi_thresh_option.setEnabled(True)
		else:
			self.pi_thresh_option.setEnabled(False)

	def show_pi_thresh(self):
		if self.pi_thresh_option.isChecked():
			self.pi_thresh_line.show()
		else:
			self.pi_thresh_line.hide()
				

	def ProcessNeighWidget(self):

		FrameNeigh = QFrame()
		FrameNeigh.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
		grid_neigh = QGridLayout(FrameNeigh)	

		grid_neigh.addWidget(QLabel("Neighbourhood:"), 0, 0, 1, 1)

		self.neigh_action = QPushButton("match neighbours\n(effector && target)")
		self.neigh_action.setIcon(QIcon(f"{home_dir}ADCCFactory_2.0/src/icons/neighbour.png"))
		self.neigh_action.clicked.connect(self.process_neighbours)
		grid_neigh.addWidget(self.neigh_action, 1,0,1,1)

		return(FrameNeigh)	

	def ProcessSurvivalWidget(self):

		FrameSurv = QFrame()
		FrameSurv.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
		grid_surv = QGridLayout(FrameSurv)	

		grid_surv.addWidget(QLabel("Survival:"), 0, 0, 1, 1)

		self.fit_km = QPushButton("plot survival\nKaplan-Meier estimator")
		self.fit_km.setIcon(QIcon(f"{home_dir}ADCCFactory_2.0/src/icons/heart.png"))
		self.fit_km.clicked.connect(self.fit_km_estimator)
		grid_surv.addWidget(self.fit_km, 1,0,1,3)

		self.fit_cox = QPushButton("Fit Cox model")
		self.fit_cox.setIcon(QIcon(f"{home_dir}ADCCFactory_2.0/src/icons/heart.png"))
		self.fit_cox.clicked.connect(self.fit_cox_model)
		grid_surv.addWidget(self.fit_cox, 2,0,1,3)

		self.btn_nk_normalized_survival = QPushButton("Plot NK normalized target survival")
		self.btn_nk_normalized_survival.setIcon(QIcon(f"{home_dir}ADCCFactory_2.0/src/icons/heart.png"))
		self.btn_nk_normalized_survival.clicked.connect(self.nk_normalized_survival)
		grid_surv.addWidget(self.btn_nk_normalized_survival, 3,0,1,3)

		return(FrameSurv)	

	def fit_km_estimator(self):
		option_pool=True

		print("kaplan there")
		plt.close()

		if self.well_list.currentText()=="*":
			self.well_index = np.linspace(0,len(self.wells)-1,len(self.wells),dtype=int)
		else:
			self.well_index = [self.well_labels.index(str(self.well_list.currentText()))]

		survival_data = []

		for w_idx in self.well_index:

			pos = self.positions[w_idx]
			if self.position_list.currentText()=="*":
				pos_indices = np.linspace(0,len(pos)-1,len(pos),dtype=int)
			else:
				pos_indices = natsorted([pos.index(self.position_list.currentText())])

			well = self.wells[w_idx]

			for pos_idx in pos_indices:

				self.pos = natsorted(glob(well+f"{well[-2]}*/"))[pos_idx]
				
				try:
					df = pd.read_csv(self.pos+"visual_table_checked.csv")

				except:
					msgBox = QMessageBox()
					msgBox.setIcon(QMessageBox.Warning)
					msgBox.setText(f"No checked table had been found for position {pos_idx}.\nWill skip.")
					msgBox.setWindowTitle("Warning")
					msgBox.setStandardButtons(QMessageBox.Ok)
					returnValue = msgBox.exec()
					if returnValue == QMessageBox.Ok:
						continue

				unique_tracks = np.unique(df["TID"].to_numpy())
				position_name = pos_idx #self.pos.split("/")[-2]
				well_name = w_idx #self.pos.split("/")[-3]
				concentration = int(self.concentrations[w_idx])
				cell_type = str(self.cell_types[w_idx])
				print(well_name,concentration,cell_type)

				for cell in unique_tracks:
					df_at_track = df[(df["TID"]==cell)]
					cell_class = df_at_track["CLASS"].to_numpy()[0]
					cell_death_time = df_at_track["T0"].to_numpy()[0]

					if cell_class==0.0:
						time = cell_death_time
						event = 1
						survival_data.append([cell,time,event,concentration,cell_type,well_name,position_name])
					elif cell_class==1.0:
						time = self.len_movie
						event = 0
						survival_data.append([cell,time,event,concentration,cell_type,well_name,position_name])

		
		df_survival = pd.DataFrame(survival_data,columns=["cell","time","event","concentration","cell_type","well","position"])
		df_survival["time"] *= self.FrameToMin

		print(df_survival.head(10))

		kmf = KaplanMeierFitter()
					
		if (self.well_list.currentText()=="*")*(self.position_list.currentText()=="*"):
			
			fig,ax = plt.subplots(1,1,figsize=(8,8))
			unique_cell_types = np.unique(df_survival["cell_type"].to_numpy())
			print("unique_cell_types",unique_cell_types)
			for ct in unique_cell_types:

				df_ct = df_survival[(df_survival["cell_type"]==ct)]
				unique_concentrations = np.unique(df_ct["concentration"].to_numpy())
				print(unique_concentrations)

				for c in unique_concentrations:

					df_at_concentration = df_ct[(df_ct["concentration"]==c)]
					kmf.fit(df_at_concentration["time"], event_observed=df_at_concentration["event"])

					kmf.plot_survival_function(ax=ax,label=f"cell type: {ct}; concentration: {c} pM")
			ax.set_xlabel("time [min]")
			ax.set_ylabel("survival")
			plt.show()

		if (self.well_list.currentText()!="*")*(self.position_list.currentText()=="*"):

			#w_idx = self.well_labels.index(str(self.well_list.currentText()))
			fig,ax = plt.subplots(1,1,figsize=(8,8))

			df_at_well = df_survival[(df_survival["well"]==w_idx)]
			kmf.fit(df_at_well["time"], event_observed=df_at_well["event"])
			kmf.plot_survival_function(ax=ax,label=f"Pool",c="k")

			for pos in np.unique(df_at_well["position"].to_numpy()):
				df_at_position = df_at_well[(df_at_well["position"]==pos)]
				kmf.fit(df_at_position["time"], event_observed=df_at_position["event"])
				kmf.plot_survival_function(ax=ax,label=f"position: {pos}",linewidth=0.5)				

			ax.set_xlabel("time [min]")
			ax.set_ylabel("survival")
			ax.set_ylim(0.1,1.05)
			plt.show()

		if (self.well_list.currentText()!="*")*(self.position_list.currentText()!="*"):

			#pos_idx = pos.index(self.position_list.currentText())

			fig,ax = plt.subplots(1,1,figsize=(8,8))
			df_at_position = df_survival[(df_survival["position"]==pos_idx)]
			kmf.fit(df_at_position["time"], event_observed=df_at_position["event"])
			print(kmf.survival_function_, kmf.timeline)
			kmf.plot_survival_function(ax=ax,c="k")
			ax.set_xlabel("time [min]")
			ax.set_ylabel("survival")
			ax.set_ylim(0.1,1.05)
			plt.show()


	def fit_cox_model(self):
		"""
		Fit a Cox model for the chosen positions
		"""

		if not (self.well_list.currentText()=="*")*(self.position_list.currentText()=="*"):

			msgBox = QMessageBox()
			msgBox.setIcon(QMessageBox.Warning)
			msgBox.setText("Please select all wells and positions\nto perform a fit of the Cox model...")
			msgBox.setWindowTitle("Error")
			msgBox.setStandardButtons(QMessageBox.Ok)
			returnValue = msgBox.exec()
			if returnValue == QMessageBox.Ok:
				return(None)

		if self.well_list.currentText()=="*":
			self.well_index = np.linspace(0,len(self.wells)-1,len(self.wells),dtype=int)
		else:
			self.well_index = [self.well_labels.index(str(self.well_list.currentText()))]

		survival_data = []

		for w_idx in self.well_index:

			pos = self.positions[w_idx]
			if self.position_list.currentText()=="*":
				pos_indices = np.linspace(0,len(pos)-1,len(pos),dtype=int)
			else:
				pos_indices = natsorted([pos.index(self.position_list.currentText())])

			well = self.wells[w_idx]

			for pos_idx in pos_indices:

				self.pos = natsorted(glob(well+f"{well[-2]}*/"))[pos_idx]
				
				try:
					df = pd.read_csv(self.pos+"output/tables/tc_w_neighbours.csv")

				except:
					print("Checked table not found... Skipping.")
					continue

				unique_tracks = np.unique(df["TID"].to_numpy())
				position_name = pos_idx #self.pos.split("/")[-2]
				well_name = w_idx #self.pos.split("/")[-3]
				concentration = int(self.concentrations[w_idx])
				cell_type = str(self.cell_types[w_idx])
				print(well_name,concentration,cell_type)

				for cell in unique_tracks:
					df_at_track = df[(df["TID"]==cell)]
					cell_class = df_at_track["CLASS"].to_numpy()[0]
					cell_death_time = df_at_track["T0"].to_numpy()[0]
					nk_neigh = df_at_track["MEAN_NK_NEIGH_ALIVE"].to_numpy()[0]
					tc_neigh = df_at_track["MEAN_TC_NEIGH"].to_numpy()[0]

					if cell_class==0.0:
						time = cell_death_time
						event = 1
						survival_data.append([cell,time,event,nk_neigh,tc_neigh,concentration,cell_type,well_name,position_name])
					elif cell_class==1.0:
						time = self.len_movie
						event = 0
						survival_data.append([cell,time,event,nk_neigh,tc_neigh,concentration,cell_type,well_name,position_name])

		
		df_survival = pd.DataFrame(survival_data,columns=["cell","time","event","nk_neigh","tc_neigh","concentration","cell_type","well","position"])
		df_survival["time"] *= self.FrameToMin
		df_survival["cell_type"] = np.array([0 if s=="WT" else 1 for s in df_survival["cell_type"]])

		df_to_fit = df_survival[["time","event","nk_neigh","tc_neigh","concentration","cell_type"]]

		cph = CoxPHFitter()
		cph.fit(df_to_fit, duration_col='time', event_col='event')
		cph.print_summary()
		cph.check_assumptions(df_to_fit)
		cph.plot()
		plt.tight_layout()
		plt.show()

	def nk_normalized_survival(self):

		print("nk normalized stuff")
		plt.close()

		def derivative(signal,n,dt):
			
			if n<2:
				print("Please give n>1")

			out = np.zeros(len(signal))
			for k in range(n//2,len(out)-n//2):
				out[k] = (signal[k+n//2] - signal[k-n//2]) / (n*dt)
			return(out)

		if self.well_list.currentText()=="*":
			self.well_index = np.linspace(0,len(self.wells)-1,len(self.wells),dtype=int)
		else:
			self.well_index = [self.well_labels.index(str(self.well_list.currentText()))]

		survival_data = []
		df_all_wells = []

		for w_idx in self.well_index:

			pos = self.positions[w_idx]
			if self.position_list.currentText()=="*":
				pos_indices = np.linspace(0,len(pos)-1,len(pos),dtype=int)
			else:
				pos_indices = natsorted([pos.index(self.position_list.currentText())])

			well = self.wells[w_idx]

			fig,ax = plt.subplots(1,2,figsize=(12,6))

			for pos_idx in pos_indices:

				self.pos = natsorted(glob(well+f"{well[-2]}*/"))[pos_idx]
				
				try:
					df = pd.read_csv(self.pos+"output/tables/tc_w_neighbours.csv")

				except:
					msgBox = QMessageBox()
					msgBox.setIcon(QMessageBox.Critical)
					msgBox.setText(f"The table with NK \\& TC neighbours is not found.\n Please run the neighbouring module.")
					msgBox.setWindowTitle("Data not found")
					msgBox.setStandardButtons(QMessageBox.Ok)
					returnValue = msgBox.exec()
					if returnValue == QMessageBox.Ok:
						continue

				times = np.unique(df["T"].to_numpy())
				cells_alive_series = np.zeros_like(times)
				nk_neigh_alive_series = np.zeros_like(times)

				processed_df = pd.DataFrame(columns=['time', 'T', 'dT/dt','N','lysis','well','position'], index=range(len(times)))

				for t_idx,t in enumerate(times):
					df_at_t = df[(df["T"]==t)&(df["CLASS"]!=2.0)]
					status = df_at_t["STATUS"].to_numpy()
					nk_neigh_alive = df_at_t["NK_NEIGHS_ALIVE_COUNT"].to_numpy()
					mean_nk = np.mean(nk_neigh_alive)
					stat, cell_counts = np.unique(status,return_counts=True)
					cells_alive = cell_counts[np.where(stat==1.0)[0]]
					cells_alive_series[t_idx] = cells_alive
					nk_neigh_alive_series[t_idx] = mean_nk

				derivative_smooth = 2
				fm1 = derivative(cells_alive_series, derivative_smooth, 1)
				fm1[:derivative_smooth//2] = np.nan
				fm1[-derivative_smooth//2:] = np.nan

				lysis = np.zeros_like(times)
				for n in range(derivative_smooth//2, len(times) - derivative_smooth//2):
					lysis[n] = - 1.0 / cells_alive_series[n] * 1.0 / nk_neigh_alive_series[n] * fm1[n]

				lysis[:derivative_smooth//2] = np.nan
				lysis[-derivative_smooth//2:] = np.nan

				processed_df["time"] = times
				processed_df["T"] = cells_alive_series
				processed_df["dT/dt"] = fm1
				processed_df["N"] = nk_neigh_alive_series
				processed_df["well"] = w_idx
				processed_df["position"] = pos_idx
				processed_df["lysis"] = lysis

				df_all_wells.append(processed_df)

				#plt.close()
				ax[0].plot(times[derivative_smooth//2:-derivative_smooth//2],lysis[derivative_smooth//2:-derivative_smooth//2])
				ax[1].plot(times,cells_alive_series/cells_alive_series[0])


			plt.show()





	def set_cfse_models(self):
		self.nk_seg_model_list.clear()
		if self.cfse_segment.isChecked():
			nk_seg_models = glob(self.modelpath+"segmentation_nk/cfse*/")
			self.nk_seg_model_list.addItems([os.path.split(s[:-1])[-1] for s in nk_seg_models])
		else:
			nk_seg_models = glob(self.modelpath+"segmentation_nk//[!cfse]*/")
			self.nk_seg_model_list.addItems([os.path.split(s[:-1])[-1] for s in nk_seg_models])

	def CheckClassificationWidget(self):

		CheckClassFrame = QFrame()
		CheckClassFrame.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
		grid_check_class = QGridLayout(CheckClassFrame)	

		self.control_classification = QPushButton("Control class && regression")
		self.control_classification.setIcon(QIcon(f"{home_dir}ADCCFactory_2.0/src/icons/segment_icon.png"))
		grid_check_class.addWidget(self.control_classification, 0,0,1,3)
		self.control_classification.clicked.connect(self.control_class_and_reg)

		return(CheckClassFrame)	


	def process_nks(self):
		if self.well_list.currentText()=="*":
			self.well_index = np.linspace(0,len(self.wells)-1,len(self.wells),dtype=int)
			#self.logchoices.emit(f"You chose to analyze all wells...")
		else:
			self.well_index = [self.well_labels.index(str(self.well_list.currentText()))]

		to_disable = [self.well_list, self.position_list, self.all_tc_actions, self.train_button_tc, self.train_button_cell,
		self.segment_action_tc, self.track_action_tc, self.measure_action_tc,
		self.tc_seg_model_list, self.cell_models_list, self.submit_button_tc, self.all_nk_actions,
		self.classify_action_nks, self.train_button_nk, self.segment_action_nk, self.nk_seg_model_list, self.submit_button_nk,
		self.neigh_action]
		for obj in to_disable:
			obj.setEnabled(False)
			obj.repaint()

		for w_idx in self.well_index:

			pos = self.positions[w_idx]
			if self.position_list.currentText()=="*":
				pos_indices = np.linspace(0,len(pos)-1,len(pos),dtype=int)
			else:
				pos_indices = natsorted([pos.index(self.position_list.currentText())])

			well = self.wells[w_idx]

			for pos_idx in pos_indices:

				self.pos = natsorted(glob(well+f"{well[-2]}*/"))[pos_idx]
				logger.info(f"Processing position: {self.pos}")

				try:
					file = glob(self.pos+f"movie/{self.movie_prefix}*.tif")[0]
					logger.info(f"Well {well}; position {self.pos}; {file} has been successfully loaded..")
				except IndexError:
					logger.info(f"Position {self.pos}; No movie has been found for this position... Skipping...")
					continue

				if self.segment_action_nk.isChecked():
					self.stack = imread(file)

					if not self.cfse_segment.isChecked():
						seg_channel = 0
					else:
						seg_channel = self.green_channel

					if self.stack.shape[1]<5:
						try:
							self.stack = self.stack[:,[seg_channel, self.red_channel],:,:]
							self.stack = np.moveaxis(self.stack, 1, -1)

						except:
							print("Failed to isolate the red and blue channels")
							continue

					elif self.stack.shape[-1]<5:
						try:
							self.stack = self.stack[:,:,:,[seg_channel,self.red_channel]]
						except:
							print(f"Channel numbers are incompatible with the movie of shape {self.stack.shape}: red_channel:{self.red_channel}, blue_channel:{self.blue_channel}...")
							continue

					else:
						print(f"Stack format unrecognized, shape = {self.stack.shape}. Skipping...")
						continue						


				self.in_process = False

				if self.segment_action_nk.isChecked():
					logger.info("Segmenting the NKs...")
					self.segment_nks()

				if self.classify_action_nks.isChecked():
					logger.info("Classifying the NKs...")
					if not self.pi_thresh_option.isChecked():
						self.classify_nks()
						if self.break_plot:
							print("breaking plot!")
					else:
						self.classify_nks_threshold()
						if self.thresh_error:
							break

		self.stack = None
		gc.collect()		

		for obj in to_disable:
			obj.setEnabled(True)
			obj.repaint()

	def process_neighbours(self):
		print("there")
		if self.well_list.currentText()=="*":
			self.well_index = np.linspace(0,len(self.wells)-1,len(self.wells),dtype=int)
			#self.logchoices.emit(f"You chose to analyze all wells...")
		else:
			self.well_index = [self.well_labels.index(str(self.well_list.currentText()))]

		to_disable = [self.well_list, self.position_list, self.all_tc_actions, self.train_button_tc, self.train_button_cell,
		self.segment_action_tc, self.track_action_tc, self.measure_action_tc,
		self.tc_seg_model_list, self.cell_models_list, self.submit_button_tc, self.all_nk_actions,
		self.classify_action_nks, self.train_button_nk, self.segment_action_nk, self.nk_seg_model_list, self.submit_button_nk,
		self.neigh_action]
		for obj in to_disable:
			obj.setEnabled(False)
			obj.repaint()

		for w_idx in self.well_index:

			pos = self.positions[w_idx]
			if self.position_list.currentText()=="*":
				pos_indices = np.linspace(0,len(pos)-1,len(pos),dtype=int)
			else:
				pos_indices = natsorted([pos.index(self.position_list.currentText())])

			well = self.wells[w_idx]

			for pos_idx in pos_indices:

				self.pos = natsorted(glob(well+f"{well[-2]}*/"))[pos_idx]
				logger.info(f"Processing position: {self.pos}")

				logger.info("Finding the NK neighbours...")
				self.find_nk_neighbours()
				logger.info("Finding the TC neighbours...")
				self.find_tc_neighbours()

		for obj in to_disable:
			obj.setEnabled(True)
			obj.repaint()			

	def control_class_and_reg(self):

		if self.well_list.currentText()=="*":
			msgBox = QMessageBox()
			msgBox.setIcon(QMessageBox.Critical)
			msgBox.setText("Please select a single well...")
			msgBox.setWindowTitle("Error")
			msgBox.setStandardButtons(QMessageBox.Ok)
			returnValue = msgBox.exec()
			if returnValue == QMessageBox.Ok:
				return(None)
		else:
			self.well_index = [self.well_labels.index(str(self.well_list.currentText()))]

		for w_idx in self.well_index:

			pos = self.positions[w_idx]
			if self.position_list.currentText()=="*":
				msgBox = QMessageBox()
				msgBox.setIcon(QMessageBox.Critical)
				msgBox.setText("Please select a single position...")
				msgBox.setWindowTitle("Error")
				msgBox.setStandardButtons(QMessageBox.Ok)
				returnValue = msgBox.exec()
				if returnValue == QMessageBox.Ok:
					return(None)
			else:
				pos_indices = natsorted([pos.index(self.position_list.currentText())])

			well = self.wells[w_idx]

			for pos_idx in pos_indices:
				self.pos = natsorted(glob(well+f"{well[-2]}*/"))[pos_idx]

				if not os.path.exists(self.pos+"visual_table.csv"):

					msgBox = QMessageBox()
					msgBox.setIcon(QMessageBox.Critical)
					msgBox.setText("No visual table has been found.\nPlease run the previous modules.")
					msgBox.setWindowTitle("Error")
					msgBox.setStandardButtons(QMessageBox.Ok)

					returnValue = msgBox.exec()
					if returnValue == QMessageBox.Ok:
						return(None)

				print(f"python adccfactory/control_classification.py {self.pos}")
				if os.path.exists(self.pos+"visual_table_checked.csv"):

					msgBox = QMessageBox()
					msgBox.setIcon(QMessageBox.Information)
					msgBox.setText("An annotated version has been found.\nDo you want to load it?")
					msgBox.setWindowTitle("Info")
					msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.No | QMessageBox.Cancel)

					returnValue = msgBox.exec()
					if returnValue == QMessageBox.Cancel:
						return(None)			
					elif returnValue == QMessageBox.Ok:
						table_path = self.pos+"visual_table_checked.csv"
					elif returnValue == QMessageBox.No:
						table_path = self.pos+"visual_table.csv"			
					
					subprocess.call(f"python adccfactory/control_classification.py {table_path}", shell=True)

				else:
					subprocess.call(f"python adccfactory/control_classification.py {self.pos+'visual_table.csv'}", shell=True)


	def tick_all_tc_actions(self):
		if self.all_tc_actions.isChecked():
			self.segment_action_tc.setChecked(True)
			self.track_action_tc.setChecked(True)
			self.measure_action_tc.setChecked(True)
		else:
			self.segment_action_tc.setChecked(False)
			self.track_action_tc.setChecked(False)
			self.measure_action_tc.setChecked(False)

	def tick_all_nk_actions(self):
		if self.all_nk_actions.isChecked():
			self.segment_action_nk.setChecked(True)
			self.classify_action_nks.setChecked(True)
			#self.neigh_action_nk.setChecked(True)
		else:
			self.segment_action_nk.setChecked(False)
			self.classify_action_nks.setChecked(False)
			#self.neigh_action_nk.setChecked(False)

	def enable_segmentation_model_list_tc(self):
		if self.segment_action_tc.isChecked():
			self.tc_seg_model_list.setEnabled(True)
		else:
			self.tc_seg_model_list.setEnabled(False)

	def enable_segmentation_model_list_nk(self):
		if self.segment_action_nk.isChecked():
			self.nk_seg_model_list.setEnabled(True)
			self.cfse_segment.setEnabled(True)

		else:
			self.nk_seg_model_list.setEnabled(False)	
			self.cfse_segment.setEnabled(False)


	def enable_cell_model_list(self):
		if self.measure_action_tc.isChecked():
			self.cell_models_list.setEnabled(True)
		else:
			self.cell_models_list.setEnabled(False)	


	def train_stardist_model_tc(self):
		self.retrainSDtc = TrainStarDistTCModel()
		self.retrainSDtc.show()
		endTrain = self.retrainSDtc.training_end
		endTrain.connect(self.update_SD_model_list_on_train_end)

	def train_stardist_model_nk(self):
		self.retrainSDnk = TrainStarDistNKModel()
		self.retrainSDnk.show()
		endTrain = self.retrainSDnk.training_end
		endTrain.connect(self.update_SD_nk_model_list_on_train_end)

	def train_cell_model(self):
		self.retrain = TrainCellModel()
		self.retrain.show()
		endTrain = self.retrain.training_end
		endTrain.connect(self.update_model_list_on_train_end)

	def process_tcs(self):
		if self.well_list.currentText()=="*":
			self.well_index = np.linspace(0,len(self.wells)-1,len(self.wells),dtype=int)
			logger.info(f"You chose to analyze all wells...")
		else:
			self.well_index = [self.well_labels.index(str(self.well_list.currentText()))]

		to_disable = [self.well_list, self.position_list, self.all_tc_actions, self.train_button_tc, self.train_button_cell,
		self.segment_action_tc, self.track_action_tc, self.measure_action_tc,
		self.tc_seg_model_list, self.cell_models_list, self.submit_button_tc, self.all_nk_actions,
		self.classify_action_nks, self.train_button_nk, self.segment_action_nk, self.nk_seg_model_list, self.submit_button_nk,
		self.neigh_action]
		for obj in to_disable:
			obj.setEnabled(False)
			obj.repaint()

		for w_idx in self.well_index:

			pos = self.positions[w_idx]
			if self.position_list.currentText()=="*":
				pos_indices = np.linspace(0,len(pos)-1,len(pos),dtype=int)
			else:
				pos_indices = natsorted([pos.index(self.position_list.currentText())])

			well = self.wells[w_idx]

			for pos_idx in pos_indices:
				self.pos = natsorted(glob(well+f"{well[-2]}*/"))[pos_idx]
				logger.info(f"Processing position: {self.pos}")
				print(f"Processing position {self.pos}...")

				try:
					file = glob(self.pos+f"movie/{self.movie_prefix}*.tif")[0]
					logger.info(f"Well {well}; position {self.pos}; {file} has been successfully loaded..")
				except IndexError:
					logger.info(f"Position {self.pos}; No movie has been found for this position... Skipping...")
					continue

				self.stack = imread(file)

				if self.stack.shape[1]<5:
					try:
						self.stack = self.stack[:,[self.red_channel,self.blue_channel],:,:]
						self.stack = np.moveaxis(self.stack, 1, -1)

					except:
						print("Failed to isolate the red and blue channels")
						continue

				elif self.stack.shape[-1]<5:
					try:
						self.stack = self.stack[:,:,:,[self.red_channel,self.blue_channel]]
					except:
						print(f"Channel numbers are incompatible with the movie of shape {self.stack.shape}: red_channel:{self.red_channel}, blue_channel:{self.blue_channel}...")
						continue

				else:
					print(f"Stack format unrecognized, shape = {self.stack.shape}. Skipping...")
					continue						

				if self.segment_action_tc.isChecked():
					self.segment_tcs()

				if self.track_action_tc.isChecked():
					self.track_tcs()

				if self.measure_action_tc.isChecked():
					self.measure_tcs()

		self.stack = None
		gc.collect()		

		for obj in to_disable:
			obj.setEnabled(True)
			obj.repaint()

	def segment_tcs(self):

		modelname = self.tc_seg_model_list.currentText()

		try:
			logger.info(f'Segmenting {self.pos} using model: segmentation_tc/{modelname};\nNumber of channels = {self.stack.shape[-1]}')
			model = StarDist2D(None, name=f'segmentation_tc/{modelname}', basedir=self.modelpath)
			axis_norm = (0,1)

			if os.path.exists(self.pos+"labels/"):
				shutil.rmtree(self.pos+"labels/")
			os.mkdir(self.pos+"labels/")

			for i in tqdm(range(len(self.stack))):
				X_pred = normalize(self.stack[i],1,99.9,axis=axis_norm)
				Y_pred,details = model.predict_instances(X_pred, n_tiles=model._guess_n_tiles(X_pred), show_tile_progress=False)
				save_tiff_imagej_compatible(self.pos+"labels/"+f"{str(i).zfill(4)}.tif", Y_pred, axes='YX')

			del model
			logger.info("Segmentation successful!")
			gc.collect()

		except Exception as e:
			logger.critical(f"Error: {e}")
			return(None)

	def segment_nks(self):

		modelname = self.nk_seg_model_list.currentText()

		try:
			print(f'Segmenting using model: segmentation_nk/{modelname}')
			model = StarDist2D(None, name=f'segmentation_nk/{modelname}', basedir=self.modelpath)
			axis_norm = (0,1)
			mask = create_circular_mask(2*self.intensity_measurement_radius_nk,2*self.intensity_measurement_radius_nk,
		((2*self.intensity_measurement_radius_nk)//2,(2*self.intensity_measurement_radius_nk)//2),self.intensity_measurement_radius_nk)
			

			if os.path.exists(self.pos+"labels_nk/"):
				shutil.rmtree(self.pos+"labels_nk/")
			os.mkdir(self.pos+"labels_nk/")

			if not os.path.exists(self.pos+"output/"):
				os.mkdir(self.pos+"output/")

			if not os.path.exists(self.pos+"output/tables/"):
				os.mkdir(self.pos+"output/tables/")

			nk_index = 0
			rows = []
			row_labels = ["NK_ID","X","Y","T","IR"]
			for i in tqdm(range(len(self.stack))):
				X_pred = normalize(self.stack[i,:,:,0],1,99.9,axis=axis_norm)
				Y_pred,details = model.predict_instances(X_pred, n_tiles=model._guess_n_tiles(X_pred), show_tile_progress=False)
				save_tiff_imagej_compatible(self.pos+"labels_nk/"+f"{str(i).zfill(4)}.tif", Y_pred, axes='YX')
				
				coords = details["coord"]
				ireds = [];

				pad_red = np.pad(self.stack[i,:,:,1],[self.intensity_measurement_radius_nk+1,self.intensity_measurement_radius_nk+1],mode="constant")

				for co in coords:
					# Measure PI & CFSE signal around each NK in disk
					x = np.mean(co[1,:])
					y = np.mean(co[0,:])

					xmin = int(x) + (self.intensity_measurement_radius_nk + 1) - self.intensity_measurement_radius_nk
					xmax = int(x) +  (self.intensity_measurement_radius_nk + 1) + self.intensity_measurement_radius_nk
					ymin = int(y) + (self.intensity_measurement_radius_nk + 1) - self.intensity_measurement_radius_nk
					ymax = int(y) +  (self.intensity_measurement_radius_nk + 1) + self.intensity_measurement_radius_nk

					local_red = np.multiply(pad_red[ymin:ymax,xmin:xmax],mask)
					red_measurement = np.mean(local_red[local_red!=0.])
					
					ireds.append(red_measurement)
					row = [nk_index,x,y,float(i),red_measurement]
					rows.append(row)
					
					nk_index+=1

			df_nk = pd.DataFrame(rows,columns=row_labels)

			df_nk.to_csv(self.pos+"/output/tables/table_nks.csv")

			del X_pred
			del Y_pred
			del details
			del model
			del pad_red

			gc.collect()

		except Exception as e:
			print(f"Error: {e}")
			return(None)	

	def classify_nks(self):

		def accept_value(event):
			self.I_thresh = self.slider.val
			print(f"The chosen threshold for the dead NK is: {self.I_thresh}...")
			test = np.array([ir <= self.I_thresh for ir in self.df_nk.IR.to_numpy()],dtype=np.int8)
			self.df_nk["STATUS"] = test
			self.df_nk.to_csv(self.pos+"output/tables/table_nks_w_death.csv")
			print(f"Table {self.pos+'output/tables/table_nks_w_death.csv'} successfully exported!")
			self.break_plot = True
			#plt.close()
			#return(None)

		# Load NK measurement table
		if not os.path.exists(str(self.pos)+"output/tables/table_nks.csv"):
			print("Measurement table for the NKs not found. \n Please run the NK segmentation module first. Abort. ")

		self.df_nk = pd.read_csv(self.pos+"output/tables/table_nks.csv")
		self.df_nk.sort_values(by="T")

		times = np.unique(self.df_nk["T"].to_numpy())		

		t0 = times[0]; tf = times[-1];
		df0 = self.df_nk[(self.df_nk["T"]==t0)]
		dff = self.df_nk[(self.df_nk["T"]==tf)]

		Ir0 = df0.IR.to_numpy()
		Irf = dff.IR.to_numpy()

		self.break_plot = False
		self.I_thresh = 500


		plt.close()
		self.fig = plt.figure()
		self.ax = self.fig.add_subplot(111)
		self.plot_loghist(Ir0, 50, color="tab:blue", label=r"$t_{0}$")
		self.plot_loghist(Irf, 50, color="tab:red",label=r'$t_{f}$')
		_, y_max = self.ax.get_ylim()
		_, x_max = self.ax.get_xlim()
		self.line, = self.ax.plot([self.I_thresh, self.I_thresh], [0, y_max], lw=1, linestyle="dotted", color="k")
		plt.subplots_adjust(left=0.25, bottom=0.25)
		
		axslider = plt.axes([0.25, 0.1, 0.65, 0.03])
		self.slider = Slider(
			ax=axslider,
			label=r'$I_R$ threshold',
			valmin=0.,
			valmax=x_max,
			valinit=self.I_thresh,
		)
		
		self.slider.on_changed(self.update_plot)
		
		submit_ax = plt.axes([0.8, 0.025, 0.1, 0.04])
		self.button = Button(submit_ax, 'Submit', hovercolor='0.975')
		self.button.on_clicked(accept_value)
		
		self.ax.set_xscale('log')
		#ax.hist(Ir0,alpha=0.1,color="tab:blue",label="t0")
		#ax.hist(Irf,alpha=0.1,color="tab:red",label='tf')
		self.ax.set_xlabel("intensity red [a.u.]")
		self.ax.set_ylabel("#")
		self.ax.legend()

		while not self.break_plot:
			plt.pause(1)

		plt.close()

		## This part is never run...
		print("here we are")
		plt.close()
		return(None)

	def classify_nks_threshold(self):
		self.thresh_error = False
		try:
			self.I_thresh = float(self.pi_thresh_line.text())
		except:
			msgBox = QMessageBox.warning(self, 'Error','Input can only be a number')
			self.thresh_error = True
			return(None)

		# Load NK measurement table
		if not os.path.exists(str(self.pos)+"output/tables/table_nks.csv"):
			print("Measurement table for the NKs not found. \n Please run the NK segmentation module first. Abort. ")

		self.df_nk = pd.read_csv(self.pos+"output/tables/table_nks.csv")
		self.df_nk.sort_values(by="T")

		print(f"The chosen threshold for the dead NK is: {self.I_thresh}...")
		test = np.array([ir <= self.I_thresh for ir in self.df_nk.IR.to_numpy()],dtype=np.int8)
		self.df_nk["STATUS"] = test
		self.df_nk.to_csv(self.pos+"output/tables/table_nks_w_death.csv")
		print(f"Table {self.pos+'output/tables/table_nks_w_death.csv'} successfully exported!")

		return(None)


	def check_break_plot(self):
		return(self.break_plot)

	def update_plot(self,val):
		self.line.set_xdata([self.slider.val,self.slider.val])
		self.fig.canvas.draw_idle()

	def plot_loghist(self, x, bins, color, label):
		hist, bins = np.histogram(x, bins=bins)
		logbins = np.logspace(np.log10(bins[0]),np.log10(bins[-1]),len(bins))
		self.ax.hist(x, bins=logbins, color=color, label=label, alpha=0.5)


	def find_nk_neighbours(self):

		# LOAD THE TWO RELEVANT TABLES
		if not os.path.exists(self.pos+"visual_table_checked.csv"):
			print("No checked table for the TC has been found (visual_table_checked.csv). Please perform the TC analysis first.")
			return(None)

		df_tc = pd.read_csv(self.pos+"visual_table_checked.csv")
		df_tc = df_tc[(df_tc["CLASS"]!=2.0)]

		if not os.path.exists(self.pos+"output/tables/table_nks_w_death.csv"):
			print("The NK table with death has not been found. Please run the NK classification module.")
			return(None)

		df_nk = pd.read_csv(self.pos+"output/tables/table_nks_w_death.csv")


		# GET UNIQUE TCS & TIMES
		unique_tc = np.unique(df_tc.TID.to_numpy())
		unique_times = np.unique(df_tc["T"].to_numpy())
		unique_times_nk = np.unique(df_nk["T"].to_numpy())

		for tid in tqdm(unique_tc):

			# SUB TABLE FOR GIVEN TC
			df_tc_at_track = df_tc[(df_tc["TID"]==tid)]
			df_tc_at_track.sort_values(by=["T"])
			indices = df_tc_at_track.index

			x_array = df_tc_at_track.X.to_numpy()
			y_array = df_tc_at_track.Y.to_numpy()
			cell_class = df_tc_at_track.CLASS.to_numpy()[0]
			try:
				death_time = df_tc_at_track.T0.to_numpy()[0]
			except:
				death_time = df_tc_at_track.X0.to_numpy()[0]				

			# Exclude TCs for which neighbourhood is unmeasureable
			border_cdt = np.all([np.all(x_array>self.search_radius_nk),np.all(y_array>self.search_radius_nk),
			np.all(x_array<(self.shape_y - self.search_radius_nk)),np.all(y_array<(self.shape_x - self.search_radius_nk))])
			
			number_nk_neigh = np.zeros_like(unique_times_nk)
			if border_cdt:

				for t,time in enumerate(unique_times_nk):

					tc_time = int(time//self.time_dilation)

					df_nk_at_t = df_nk[(df_nk["T"]==time)]
					x_nks = df_nk_at_t.X.to_numpy()
					y_nks = df_nk_at_t.Y.to_numpy()
					nk_indices = df_nk_at_t.NK_ID.to_numpy()
					nk_status = df_nk_at_t.STATUS.to_numpy()
					
					radius_test = ((x_nks - x_array[t])**2 + (y_nks - y_array[t])**2 < self.search_radius_nk**2)
					
					neighbours = np.array(nk_indices[np.where(radius_test)[0]])
					neighbours_status = np.array(nk_status[np.where(radius_test)[0]])

					neighbours_alive = neighbours[(neighbours_status==1)]
					neighbours_dead = neighbours[(neighbours_status==0)]

					df_tc.loc[indices[t], "NK_NEIGHS"] = str(neighbours)
					df_tc.loc[indices[t], "NK_NEIGHS_STATUS"] = str(neighbours_status)
					df_tc.loc[indices[t], "NK_NEIGHS_COUNT"] = len(neighbours)
					df_tc.loc[indices[t], "NK_NEIGHS_ALIVE_COUNT"] = len(neighbours_alive)
					df_tc.loc[indices[t], "NK_NEIGHS_DEAD_COUNT"] = len(neighbours_dead)
					
					number_nk_neigh[t] = len(neighbours_alive)

			if cell_class==0:
				until_death = number_nk_neigh[:int(self.time_dilation*death_time)]
				if len(until_death)>0:
					mean_nk_neigh = np.mean(until_death)
				else:
					mean_nk_neigh = 0.0
			elif cell_class==1:
				if len(number_nk_neigh)>0:
					mean_nk_neigh = np.mean(number_nk_neigh)
				else:
					mean_nk_neigh = 0.0

			df_tc.loc[indices,"MEAN_NK_NEIGH_ALIVE"] = mean_nk_neigh

		df_tc.dropna(inplace=True)
		df_tc = remove_unnamed_col(df_tc)
		df_tc.to_csv(self.pos+"output/tables/tc_w_neighbours.csv")

	def find_tc_neighbours(self):

		# LOAD THE TABLES
		try:
			df_tc = pd.read_csv(self.pos+"output/tables/tc_w_neighbours.csv")
		except:
			print("Table not found, please run the previous steps first.")
			return(None)

		df_tc = df_tc[(df_tc["CLASS"]!=2.0)]

		# GET UNIQUE TCS & TIMES
		unique_tc = np.unique(df_tc.TID.to_numpy())
		unique_times = np.unique(df_tc["T"].to_numpy())

		for tid in tqdm(unique_tc):

			# SUB TABLE FOR GIVEN TC
			df_tc_at_track = df_tc[(df_tc["TID"]==tid)]
			df_tc_at_track.sort_values(by=["T"])

			df_tc_neighs = df_tc[(df_tc["TID"]!=tid)]
			df_tc_neighs.sort_values(by=["T"])

			indices = df_tc_at_track.index
			x_array = df_tc_at_track.X.to_numpy()
			y_array = df_tc_at_track.Y.to_numpy()
			cell_class = df_tc_at_track.CLASS.to_numpy()[0]

			try:
				death_time = df_tc_at_track.T0.to_numpy()[0]
			except:
				death_time = df_tc_at_track.X0.to_numpy()[0]				

			# Exclude TCs for which neighbourhood is unmeasureable
			border_cdt = np.all([np.all(x_array>self.search_radius_tc),np.all(y_array>self.search_radius_tc),
			np.all(x_array<(self.shape_y - self.search_radius_tc)),np.all(y_array<(self.shape_x - self.search_radius_tc))])

			number_tc_neigh_alive = np.zeros_like(unique_times)
			number_tc_neigh_dead = np.zeros_like(unique_times)
			number_tc_neigh = np.zeros_like(unique_times)

			if border_cdt:

				for t,time in enumerate(unique_times):

					tc_neigh_at_t = df_tc_neighs[(df_tc_neighs["T"]==time)]
					x_neigh = tc_neigh_at_t.X.to_numpy()
					y_neigh = tc_neigh_at_t.Y.to_numpy()
					neigh_indices = tc_neigh_at_t.TID.to_numpy()
					neigh_status = tc_neigh_at_t.STATUS.to_numpy()	

					radius_test = ((x_neigh - x_array[t])**2 + (y_neigh - y_array[t])**2 < self.search_radius_tc**2)
					
					neighbours = np.array(neigh_indices[np.where(radius_test)[0]])
					neighbours_status = np.array(neigh_status[np.where(radius_test)[0]])

					neighbours_alive = neighbours[(neighbours_status==1)]
					neighbours_dead = neighbours[(neighbours_status==0)]

					df_tc.loc[indices[t], "TC_NEIGHS"] = str(neighbours)
					df_tc.loc[indices[t], "TC_NEIGHS_STATUS"] = str(neighbours_status)
					df_tc.loc[indices[t], "TC_NEIGHS_COUNT"] = len(neighbours)
					df_tc.loc[indices[t], "TC_NEIGHS_ALIVE_COUNT"] = len(neighbours_alive)
					df_tc.loc[indices[t], "TC_NEIGHS_DEAD_COUNT"] = len(neighbours_dead)
					
					number_tc_neigh_alive[t] = len(neighbours_alive)
					number_tc_neigh_dead[t] = len(neighbours_dead)
					number_tc_neigh[t] = len(neighbours)

			if cell_class==0:
				until_death_all = number_tc_neigh[:int(self.time_dilation*death_time)]
				until_death_alive = number_tc_neigh_alive[:int(self.time_dilation*death_time)]
				until_death_dead = number_tc_neigh_dead[:int(self.time_dilation*death_time)]

				if len(until_death_all)>0:
					mean_tc_neigh = np.mean(until_death_all)
					mean_tc_neigh_alive = np.mean(until_death_alive)
					mean_tc_neigh_dead = np.mean(until_death_dead)
				else:
					mean_tc_neigh = 0.0
					mean_tc_neigh_alive = 0.0
					mean_tc_neigh_dead = 0.0

			elif cell_class==1:
				if len(number_tc_neigh)>0:
					mean_tc_neigh = np.mean(number_tc_neigh)
					mean_tc_neigh_alive = np.mean(number_tc_neigh_alive)
					mean_tc_neigh_dead = np.mean(number_tc_neigh_dead)
				else:
					mean_tc_neigh = 0.0
					mean_tc_neigh_alive = 0.0
					mean_tc_neigh_dead = 0.0

			df_tc.loc[indices,"MEAN_TC_NEIGH"] = mean_tc_neigh
			df_tc.loc[indices,"MEAN_TC_NEIGH_ALIVE"] = mean_tc_neigh_alive
			df_tc.loc[indices,"MEAN_TC_NEIGH_DEAD"] = mean_tc_neigh_dead

		df_tc.dropna(inplace=True)
		df_tc = remove_unnamed_col(df_tc)
		df_tc.to_csv(self.pos+"output/tables/tc_w_neighbours.csv")


	def track_tcs(self):
		print("tracking...")
		label_path = natsorted(glob(self.pos+"labels/*.tif"))
		if len(label_path)>0:
			print(f"Found {len(label_path)} segmented frames...")
		else:
			print(f"No segmented frames have been found. Please run segmentation first, skipping...")
			return(None)
		
		labels = np.array([imread(f) for f in label_path])

		try:
			labels[hide_frames_for_tracking] = 0
		except:
			pass

		objects = btrack.utils.segmentation_to_objects(
		  labels, properties=('area', 'major_axis_length')
		)

		with btrack.BayesianTracker() as tracker:

			# configure the tracker using a config file
			tracker.configure_from_file(current_path+'/adccfactory/cell_config.json')
			tracker.update_method = BayesianUpdates.APPROXIMATE
			tracker.max_search_radius = 200

			# append the objects to be tracked
			tracker.append(objects)

			# set the volume (Z axis volume is set very large for 2D data)
			tracker.volume=((0, 2048), (0, 2048), (-1e5, 1e5))

			# track them (in interactive mode)
			tracker.track_interactive(step_size=100)

			# generate hypotheses and run the global optimizer
			tracker.optimize()

			# store the data in an HDF5 file
			#tracker.export('tracks/tracks.h5', obj_type='obj_type_1')

			# get the tracks as a python list
			tracks = tracker.tracks

			# optional: get the data in a format for napari
			data, properties, graph = tracker.to_napari(ndim=2)

		df = pd.DataFrame(data,columns=["TRACK_ID","FRAME","POSITION_Y","POSITION_X"])
		df["SPOT_ID"] = np.linspace(0,len(df)-1,len(df),dtype=np.int32)
		df["POSITION_X"] = df["POSITION_X"]*self.PxToUm
		df["POSITION_Y"] = df["POSITION_Y"]*self.PxToUm
		df = df.sort_values(by=['TRACK_ID','FRAME'])
		df.to_csv(self.pos+"trajectories.csv")

		del data; del properties; del graph; del tracks; del tracker; del objects; del labels; del df;natsorted
		gc.collect()

	def measure_tcs(self):
		print("measuring tcs...")
		# Load trajectories for measurement
		trajectory_path = self.pos+"trajectories.csv"
		if os.path.exists(trajectory_path):
			print(f"Trajectory table found...")
			trajectories = pd.read_csv(self.pos+"trajectories.csv")
		else:
			print(f"The trajectory table has not been found. Please run tracking first, skipping...")
			return(None)

		# Load death event detecting models
		try:
			model = load_model(self.modelpath+f"combined/{self.cell_models_list.currentText()}/combined_{self.model_signal_length}.h5")
		except:
			msgBox = QMessageBox()
			msgBox.setIcon(QMessageBox.Critical)
			msgBox.setText(f"The .h5 model file has not been found in the combined/ folder.")
			msgBox.setWindowTitle("Model not found")
			msgBox.setStandardButtons(QMessageBox.Ok)
			returnValue = msgBox.exec()
			if returnValue == QMessageBox.Ok:
				return(None)


		if not os.path.exists(self.pos+"output/"):
			os.mkdir(self.pos+"output/")
		
		# Perform intensity measurements
		df = measure_cell_intensities(trajectories, self.intensity_measurement_radius, self.stack[:,:,:,1], self.stack[:,:,:,0], self.PxToUm, len(self.stack))

		# Detect death events
		df = measure_death_events(df, model, len(self.stack), model_signal_length = self.model_signal_length)
		
		del model;
		gc.collect()

		#Initialize new columns
		df["STATUS"] = np.empty(len(df))
		df["STATUS_COLOR"] = np.empty(len(df))
		df["CLASS_COLOR"] = np.empty(len(df))

		for tid in tqdm(np.unique(df.TID.to_numpy()),total=len(np.unique(df.TID.to_numpy()))):
			
			df_at_track = df[(df["TID"]==tid)]
			track_indices = df_at_track.index
			
			frames = df_at_track["T"].to_numpy()
			cclass = df_at_track.CLASS.to_numpy()[0]
			class_color = get_class_color(cclass)
			t0 = df_at_track.T0.to_numpy()[0]
			for j in range(len(self.stack)):
				status,status_color = get_status_color(cclass,frames[j],t0,len(self.stack))
				df.loc[track_indices[j],"STATUS"] = status
				df.loc[track_indices[j],"STATUS_COLOR"] = status_color
			
			df.loc[track_indices,"CLASS_COLOR"] = class_color
		
		df.to_csv(self.pos+"visual_table.csv")
		print(f"Table has been succesfully saved to {self.pos+'visual_table.csv'}")

		return(None)

	def update_SD_model_list_on_train_end(self, value):
		if value:
			seg_models = glob(self.modelpath+"segmentation_tc/*/")
			self.tc_seg_model_list.clear()
			self.tc_seg_model_list.addItems([os.path.split(s[:-1])[-1] for s in seg_models])	

	def update_SD_nk_model_list_on_train_end(self, value):
		if value:
			seg_models = glob(self.modelpath+"segmentation_nk/*/")
			self.nk_seg_model_list.clear()
			self.nk_seg_model_list.addItems([os.path.split(s[:-1])[-1] for s in seg_models])		


	def update_model_list_on_train_end(self, value):
		if value:
			cell_models = glob(self.modelpath+"combined/*/")
			self.cell_models_list.clear()
			self.cell_models_list.addItems([os.path.split(s[:-1])[-1] for s in cell_models])		


# class SurvivalFigure(FigureCanvas):

# 	def __init__(self, parent=None, width=5, height=4, dpi=100,len_movie=0,FrameToMin=0):

# 		self.time_axis = np.linspace(0,len_movie-1,len_movie)*FrameToMin
# 		self.fig = Figure(tight_layout=True, figsize=(4,3))
# 		self.ax = self.fig.add_subplot(111)

# 		self.ax.set_xlabel("time [min]")
# 		self.ax.set_ylabel("survival [%]")
# 		self.survival_curve, = self.ax.plot(self.time_axis,np.ones_like(self.time_axis),c="tab:blue")
# 		self.ax.set_xlim(0,len_movie*FrameToMin)
# 		_, ymax = self.ax.get_ylim()
# 		self.ax.set_ylim(0,ymax)
# 		super(SurvivalFigure, self).__init__(self.fig)


# class SurvivalWidget(QWidget):

# 	def __init__(self, exp_dir=""):

# 		super().__init__()
		
# 		self.exp_dir = exp_dir
# 		self.pos = None

# 		grid = QGridLayout(self)
# 		self.load_configuration()
# 		FrameSurvival = QFrame()
# 		FrameSurvival.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
# 		grid_survival = QGridLayout(FrameSurvival)

# 		grid_survival.addWidget(QLabel("Survival:"), 0,0,1,1)

# 		self.fit_km = QPushButton("plot survival\nKaplan-Meier estimator")
# 		self.fit_km.setIcon(QIcon(f"{home_dir}ADCCFactory_2.0/src/icons/heart.png"))
# 		self.fit_km.clicked.connect(self.fit_km_estimator)
# 		grid_survival.addWidget(self.fit_km, 1,0,1,3)


# 		option_pos_survival = QCheckBox("Survival within position")
# 		option_pos_survival.toggled.connect(self.plot_pos_survival)

# 		grid_survival.addWidget(QLabel("Show survival:"), 2, 0, 1, 1)
# 		grid_survival.addWidget(option_pos_survival, 3, 0, 1, 1)

# 		survival_figure = SurvivalFigure(len_movie=self.len_movie, FrameToMin=self.FrameToMin)
# 		grid.addWidget(FrameSurvival, 0, 0, 1, 1)
# 		grid.addWidget(survival_figure, 1, 0, 1, 1)

# 	def plot_pos_survival(self):
# 		pass

# 	def fit_km_estimator(self):

# 		print("kaplan there")
# 		if self.well_list.currentText()=="*":
# 			self.well_index = np.linspace(0,len(self.wells)-1,len(self.wells),dtype=int)
# 		else:
# 			self.well_index = [self.well_labels.index(str(self.well_list.currentText()))]

# 		for w_idx in self.well_index:

# 			pos = self.positions[w_idx]
# 			if self.position_list.currentText()=="*":
# 				pos_indices = np.linspace(0,len(pos)-1,len(pos),dtype=int)
# 			else:
# 				pos_indices = natsorted([pos.index(self.position_list.currentText())])

# 			well = self.wells[w_idx]

# 			for pos_idx in pos_indices:

# 				self.pos = natsorted(glob(well+f"{well[-2]}*/"))[pos_idx]
# 				print(self.pos)

# 	def load_configuration(self):

# 		config = self.exp_dir + "config.ini"
# 		self.PxToUm = float(ConfigSectionMap(config,"MovieSettings")["pxtoum"])
# 		self.FrameToMin = float(ConfigSectionMap(config,"MovieSettings")["frametomin"])
# 		self.len_movie = int(ConfigSectionMap(config,"MovieSettings")["len_movie"])