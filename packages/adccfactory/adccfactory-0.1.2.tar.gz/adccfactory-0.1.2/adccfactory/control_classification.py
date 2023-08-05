#!/usr/bin/python

import sys

import os

from functions import *

import sys
import random
import time
from screeninfo import get_monitors
import shutil

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
from matplotlib.lines import Line2D
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

import numpy as np
import pandas as pd

from glob import glob
from natsort import natsorted
from tqdm import tqdm
from tifffile import imread

from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QApplication, QAction, QMenu, QWidget, QGridLayout, QLabel, QPushButton, QRadioButton, QLineEdit
from PyQt5.QtCore import QSize, Qt, QTimer
from PyQt5.QtGui import QIcon, QImage, QDoubleValidator, QKeySequence
from datetime import datetime
from pathlib import Path, PurePath

for m in get_monitors():
	res_w = int(m.width*0.75)
	res_h = int(m.height*0.75)

table_path = str(sys.argv[1]) #"/media/limozin/HDD/Storage_Bea_stuff/JanExp/W1/100/"
pos = os.path.split(table_path)[0]
print(pos,table_path)

# MOVIE PARAMETERS
parent1 = Path(pos).parent
expfolder = parent1.parent
print(parent1, expfolder)
config = PurePath(expfolder,Path("config.ini"))
print("config path = ",config)

PxToUm = float(ConfigSectionMap(config,"MovieSettings")["pxtoum"])
FrameToMin = float(ConfigSectionMap(config,"MovieSettings")["frametomin"])
len_movie = int(ConfigSectionMap(config,"MovieSettings")["len_movie"])
shape_x = int(ConfigSectionMap(config,"MovieSettings")["shape_x"])
shape_y = int(ConfigSectionMap(config,"MovieSettings")["shape_y"])
movie_prefix = ConfigSectionMap(config,"MovieSettings")["movie_prefix"]

blue_channel = int(ConfigSectionMap(config,"MovieSettings")["blue_channel"]) - 1
red_channel = int(ConfigSectionMap(config,"MovieSettings")["red_channel"]) - 1

try:
	green_channel = int(ConfigSectionMap(config,"MovieSettings")["green_channel"]) - 1
except:
	print("No green channel detected...")

fraction = int(ConfigSectionMap(config,"Display")["fraction"])
time_dilation = int(ConfigSectionMap(config,"BinningParameters")["time_dilation"])
len_movie = len_movie//time_dilation

# DISPLAY PARAMETERS
blue_percentiles = [float(s) for s in ConfigSectionMap(config,"Display")["blue_percentiles"].split(",")]
red_percentiles = [float(s) for s in ConfigSectionMap(config,"Display")["red_percentiles"].split(",")]


df0 = pd.read_csv(table_path)
df = df0.copy()
print(df, "df loaded")

stack_path = glob(pos+f"/movie/{movie_prefix}*.tif")[0]
movie_name = os.path.split(stack_path)[-1]
stack = imread(stack_path)[::time_dilation,1:,:,:]

stack = light_rgb_from_stack(stack,blue_channel,red_channel,green_channel=green_channel,blue_percentiles = blue_percentiles, red_percentiles = red_percentiles, fraction=fraction)

xscats = []
yscats = []
cscats0 = []
class0 = []

df.loc[df['CLASS_COLOR'].isna(), 'CLASS_COLOR'] = "yellow"
df.loc[df['STATUS_COLOR'].isna(), 'STATUS_COLOR'] = "yellow"

for k in range(len(stack)):
	dft = df[(df["T"]==k)]
	cscats0.append(dft.STATUS_COLOR.to_numpy())
	class0.append(dft.CLASS_COLOR.to_numpy())
	xscats.append(dft.X.to_numpy()//fraction)
	yscats.append(dft.Y.to_numpy()//fraction)

cscats = np.copy(cscats0)
cclass = np.copy(class0)

class RetrainWindow(QMainWindow):
	def __init__(self):
		super().__init__()

		w = QWidget()
		grid = QGridLayout(w)
		self.setWindowTitle(f"Retrain model")

		grid.addWidget(QLabel("Dataset folder:"), 0, 0, 1, 3)
		self.dataFolder = QLineEdit()
		self.dataFolder.setAlignment(Qt.AlignLeft)	
		self.dataFolder.setEnabled(True)
		self.dataFolder.setText(f"{home_dir}ADCCFactory_2.0/src/datasets/cell_signals")
		grid.addWidget(self.dataFolder, 1, 0, 1, 2)

		self.browse_button = QPushButton("Browse...")
		self.browse_button.clicked.connect(self.browse_dataset_folder)
		grid.addWidget(self.browse_button, 1, 2, 1, 1)

		grid.addWidget(QLabel("New model name:"), 2, 0, 1, 3)
		self.ModelName = QLineEdit()
		self.ModelName.setAlignment(Qt.AlignLeft)	
		self.ModelName.setEnabled(True)
		self.ModelName.setText(f"Untitled_model_{datetime.today().strftime('%Y-%m-%d')}")
		grid.addWidget(self.ModelName, 3, 0, 1, 2)

		grid.addWidget(QLabel("Number of epochs:"), 4, 0, 1, 3)
		self.NbrEpochs = QLineEdit()
		self.NbrEpochs.setAlignment(Qt.AlignLeft)	
		self.NbrEpochs.setEnabled(True)
		self.NbrEpochs.setText(f"100")
		grid.addWidget(self.NbrEpochs, 5, 0, 1, 2)

		self.confirm_button = QPushButton("Submit")
		self.confirm_button.clicked.connect(self.retrain)
		grid.addWidget(self.confirm_button, 6, 1, 1, 1)

		self.setCentralWidget(w)

	def browse_dataset_folder(self):
		self.newDataFolder = str(QFileDialog.getExistingDirectory(self, 'Select directory'))
		self.dataFolder.setText(self.newDataFolder)

	def retrain(self):
		dataset_dir = self.dataFolder.text()
		output_dir = f"{home_dir}ADCCFactory_2.0/src/models/combined/"
		model_name = self.ModelName.text()
		model_signal_length = 128
		nbr_epochs = int(self.NbrEpochs.text())

		to_freeze = [self.dataFolder, self.browse_button, self.ModelName, self.confirm_button, self.NbrEpochs]
		for q in to_freeze:
			q.setEnabled(False)
			q.repaint()

		train_cell_model(dataset_dir, output_dir, model_name, model_signal_length, nbr_epochs=nbr_epochs)

		for q in to_freeze:
			q.setEnabled(True)
			q.repaint()

class CustomFigCanvas(FigureCanvas, FuncAnimation):

	def __init__(self):

		# The data
		self.len_movie = len_movie
		self.shape_x = shape_x//fraction
		self.shape_y = shape_y//fraction
		self.title_label = QLabel()
		self.iter_val = 0
		self.speed = 1
		#print(self.speed)
		
		# The window
		self.fig = Figure(tight_layout=True)
		self.ax = self.fig.add_subplot(111)

		# ax settings
		self.im = self.ax.imshow(stack[0]) #, aspect='auto'
		self.scat = self.ax.scatter(xscats[0], yscats[0], c=cscats[0], marker='x', edgecolors='r',s=50)
		self.scat2 = self.ax.scatter(xscats[0],yscats[0],facecolors='none',edgecolors=cclass[0],s=200)
		#self.titi = self.ax.text(0.5,1.01, "", fontsize=30, bbox={'facecolor':'w', 'alpha':1, 'pad':5},transform=self.ax.transAxes, ha="center")
		self.fig.patch.set_facecolor('black')		
		
		for ax in [self.ax]:
			ax.set_aspect("equal")
			ax.set_xticks([])
			ax.set_yticks([])

		#self.fig.tight_layout()
		self._canvas = FigureCanvas.__init__(self, self.fig)
		#TimedAnimation.__init__(self, self.fig, interval = 100, blit = True)
		self._toolbar = NavigationToolbar(self,self._canvas) 

		#self.patches = [self.im] + [self.scat] + [self.scat2]

		self.anim = FuncAnimation(
							   self.fig, 
							   self._draw_frame, 
							   frames = len_movie,
							   interval = self.speed, # in ms
							   blit=True,
							   )

		#print(dir(self.anim.event_source))
		#print(dir(self.fig.suptitle()))


	def new_frame_seq(self):
		# Use the generating function to generate a new frame sequence
		return self._iter_gen()

	#def new_frame_seq(self):
	#	return iter(range(self.len_movie))

	def _draw_frame(self, framedata):

		self.iter_val = framedata
		self.title_label.setText(f"Frame: {framedata}")
		self.im.set_array(stack[framedata])
		self.scat.set_offsets(np.swapaxes([xscats[framedata],yscats[framedata]],0,1))
		self.scat.set_color(cscats[framedata])
		
		self.scat2.set_offsets(np.swapaxes([xscats[framedata],yscats[framedata]],0,1))
		self.scat2.set_edgecolor(cclass[framedata])
		
		return(self.im,self.scat,self.scat2)

	def set_last_frame(self, framedata):
		
		self.anim._drawn_artists = self._draw_frame(len(stack)-1)
		self.anim._drawn_artists = sorted(self.anim._drawn_artists, key=lambda x: x.get_zorder())
		for a in self.anim._drawn_artists:
			a.set_visible(True)

		self.fig.canvas.draw()
		self.anim.event_source.stop()


	def _init_draw(self):
		self.im.set_array(stack[0])
		self.scat.set_offsets(np.swapaxes([xscats[0],yscats[0]],0,1))
		self.scat.set_color(cscats[0])
		
		self.scat2.set_offsets(np.swapaxes([xscats[0],yscats[0]],0,1))
		self.scat2.set_edgecolor(cclass[0])

		#self.titi = self.ax.set_title(f"Time: 0 s",fontsize=20)


	def start(self):
		'''
		Starts interactive animation. Adds the draw frame command to the GUI
		handler, calls show to start the event loop.
		'''
		self.anim.event_source.start()


	def stop(self):
		# # On stop we disconnect all of our events.
		self.anim.event_source.stop()

class MplCanvas(FigureCanvas):

	def __init__(self, parent=None, width=5, height=4, dpi=100):

		self.fig = Figure()
		self.ax = self.fig.add_subplot(111)

		self.max_signal = np.amax([df["BLUE_INTENSITY"].to_numpy(),df["RED_INTENSITY"].to_numpy()])

		spacing = 0.5 # This can be your user specified spacing. 
		minorLocator = MultipleLocator(1)
		self.ax.xaxis.set_minor_locator(minorLocator)
		self.ax.xaxis.set_major_locator(MultipleLocator(5))
		self.ax.grid(which = 'major')
		self.ax.set_xlabel("Frame")
		self.ax.set_ylabel("Intensity")
		self.line_blue, = self.ax.plot(np.linspace(0,len_movie-1,len_movie),np.zeros((len_movie)),c="tab:blue")
		self.line_red, = self.ax.plot(np.linspace(0,len_movie-1,len_movie),np.zeros((len_movie)),c="tab:red")
		self.line_dt, = self.ax.plot([-1,-1],[0,self.max_signal],c="tab:purple",linestyle="--")

		self.ax.set_ylim(0,self.max_signal)
		self.ax.set_xlim(0,len_movie)

		#self.fig.tight_layout()
		super(MplCanvas, self).__init__(self.fig)

class Window(QMainWindow):
	def __init__(self):
		super().__init__()

		self.setWindowTitle(f"User check: {movie_name}")

		icon = QImage('icon.png')

		self.setWindowIcon(QIcon("icon.png"))
		
		self.center_coords = []
		self.selected_x = 0
		self.selected_y = 0
		self.tc_index = 0
		self.track_selected = 0
		
		self.new_cell_class = -1
		self.new_cell_death_time = -1
		self.new_cell_color = "tab:cyan"

		self._createActions()
		self._createMenuBar()

		self.setGeometry(0,0,res_w,res_h)

		default_time = df[(df["T"]==0)]["T0"].to_numpy()[self.tc_index]
		track_selected = df[(df["T"]==0)]["TID"].to_numpy()[self.tc_index]
		classification_label = df[(df["TID"]==track_selected)]["CLASS"].to_numpy()[0]
		mean_x = np.mean(df[(df["TID"]==track_selected)]["X"].to_numpy())
		mean_y = np.mean(df[(df["TID"]==track_selected)]["Y"].to_numpy())

		w = QWidget()
		self.grid = QGridLayout(w)
		self.cell_info = QLabel("\n \n \n")
		self.cell_info.setText(f"Cell selected: track {track_selected}\nClassification = {classification_label}\nEstimated death time = {round(default_time,2)}")
		self.cell_info.setFixedSize(QSize(300, 50))
		self.grid.addWidget(self.cell_info,0,0,1,4,alignment=Qt.AlignVCenter)
		
		frameGm = self.frameGeometry()
		screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
		centerPoint = QApplication.desktop().screenGeometry(screen).center()
		frameGm.moveCenter(centerPoint)
		self.move(frameGm.topLeft())

		self.change_btn = QPushButton("Change class")
		self.change_btn.clicked.connect(self.buttonPress_change_class)
		self.grid.addWidget(self.change_btn,3,1,1,1)	

		self.cancel_btn = QPushButton("Cancel")
		self.cancel_btn.clicked.connect(self.cancel_cell_selection)
		self.grid.addWidget(self.cancel_btn,3,2,1,1)		
		
		self.red_btn = QRadioButton("red")
		self.red_btn.toggled.connect(self.buttonPress_red)
		self.dt_label = QLabel("Death time: ")
		
		self.blue_btn = QRadioButton("blue")
		self.blue_btn.setChecked(True)
		self.blue_btn.toggled.connect(self.buttonPress_blue)
		
		self.yellow_btn = QRadioButton("yellow")
		self.yellow_btn.toggled.connect(self.buttonPress_yellow)
		
		self.grid.addWidget(self.red_btn,1,1,1,1)
		self.grid.addWidget(self.dt_label,2,0,1,1)
		self.grid.addWidget(self.blue_btn,1,2,1,1)
		self.grid.addWidget(self.yellow_btn,1,3,1,1)
		
		self.red_btn.hide()
		self.blue_btn.hide()
		self.yellow_btn.hide()
		self.dt_label.hide()
		#self.change_btn.hide()
		self.change_btn.setEnabled(False)
		self.cancel_btn.setEnabled(False)

		self.save_btn = QPushButton("Save modifications")
		self.grid.addWidget(self.save_btn,10,1,1,1)
		self.save_btn.clicked.connect(self.save_csv)

		self.cell_plot = MplCanvas(self)
		self.grid.addWidget(self.cell_plot,5,0,4,4,alignment=Qt.AlignCenter)
		
		self.timer = QTimer()
		self.timer.setInterval(100)
		self.timer.timeout.connect(self.update_cell_plot)
		self.timer.start()

		self.e1 = QLineEdit()
		self.e1.setValidator(QDoubleValidator().setDecimals(2))
		self.e1.setFixedWidth(100)
		self.e1.setMaxLength(5)
		self.e1.setAlignment(Qt.AlignLeft)	
		self.grid.addWidget(self.e1,2,1,1,1)
		self.e1.setEnabled(False)
		self.e1.hide()
		
		self.myFigCanvas = CustomFigCanvas()
		self.grid.addWidget(self.myFigCanvas,1,4,10,12)
		

		self.grid.addWidget(self.myFigCanvas.title_label,0,10,1,1, alignment = Qt.AlignRight)

		self.grid.addWidget(self.myFigCanvas.toolbar,11,4)
		self.cid = self.myFigCanvas.mpl_connect('button_press_event', self.onclick)

		self.stop_btn = QPushButton("stop")
		self.stop_btn.clicked.connect(self.stop_anim)
		self.stop_btn.setFixedSize(QSize(80, 40))
		self.grid.addWidget(self.stop_btn,0,4,1,1,alignment=Qt.AlignLeft)

		self.start_btn = QPushButton("start")
		self.start_btn.clicked.connect(self.start_anim)
		self.start_btn.setFixedSize(QSize(80, 40))
		self.grid.addWidget(self.start_btn,0,4,1,1,alignment=Qt.AlignLeft)
		self.start_btn.hide()

		self.set_last_btn = QPushButton("last frame")
		self.set_last_btn.clicked.connect(self.set_last_frame)
		self.set_last_btn.setShortcut(QKeySequence("l"))
		self.set_last_btn.setFixedSize(QSize(100, 40))
		self.grid.addWidget(self.set_last_btn,0,5,1,1,alignment=Qt.AlignLeft)
		
		self.setCentralWidget(w)
		self.show()

	def set_last_frame(self):
		#self.set_last_btn.hide()
		self.set_last_btn.setEnabled(False)
		self.set_last_btn.disconnect()

		self.myFigCanvas.set_last_frame(49)
		#self.cell_plot.draw()
		self.stop_btn.hide()
		self.start_btn.show()
		self.stop_btn.clicked.connect(self.start_anim)

		self.start_btn.setShortcut(QKeySequence("l"))


	def update_cell_plot(self):
		global df
		global stack

		# Drop off the first y element, append a new one.
		track_selected = df[(df["T"]==0)]["TID"].to_numpy()[self.tc_index]
		df_at_track = df[(df["TID"]==track_selected)]
		time_array = df_at_track["T"].to_numpy()
		cclass = df_at_track.CLASS.to_numpy()[0]
		t0 = df_at_track.T0.to_numpy()[0]
		blue_signal = df_at_track["BLUE_INTENSITY"].to_numpy()
		red_signal = df_at_track["RED_INTENSITY"].to_numpy()
		xpos = df_at_track.X.to_numpy()
		ypos = df_at_track.Y.to_numpy()

		self.cell_plot.line_blue.set_ydata(blue_signal)
		self.cell_plot.line_red.set_ydata(red_signal)
		self.cell_plot.line_dt.set_xdata([t0,t0])
		self.cell_plot.draw()

	def stop_anim(self):
		self.stop_btn.hide()
		self.start_btn.show()
		self.myFigCanvas.stop()
		self.stop_btn.clicked.connect(self.start_anim)

	def start_anim(self):

		self.start_btn.setShortcut(QKeySequence(""))

		self.set_last_btn.setEnabled(True)
		self.set_last_btn.clicked.connect(self.set_last_frame)

		self.start_btn.hide()
		self.stop_btn.show()
		self.myFigCanvas.start()
		self.stop_btn.clicked.connect(self.stop_anim)
	
	def find_closest(self,blob,xclick0,yclick0):
		distance_all = []
		distance = np.sqrt((blob[0,:]-xclick0)**2+(blob[1,:]-yclick0)**2)
		distance_all.append(distance)
		index = np.argmin(distance_all)
		x,y = blob[:,index]
		return(x,y,index)
	
	def cancel_cell_selection(self):
		self.center_coords.pop(0)
		#self.center_coords.remove((self.selected_x,self.selected_y,self.tc_index))
		#self.cell_info.setText("")
		cscats[:,self.tc_index] = self.previous_color #cscats0[k][self.tc_index]
		#self.cancel_btn.hide()
		#self.change_btn.hide()
		self.cancel_btn.setEnabled(False)
		self.change_btn.setEnabled(False)


	def buttonPress_change_class(self):
		self.change_btn.disconnect()
		self.change_btn.setText("Submit")
		self.change_btn.clicked.connect(self.submit_action)
		self.change_btn.setShortcut(QKeySequence("Enter"))
		self.change_btn.setShortcut(QKeySequence("Return"))

		self.red_btn.show()
		self.blue_btn.show()
		self.yellow_btn.show()

		self.dt_label.show()
		self.e1.show()

		self.default_time = df[(df["T"]==0)]["T0"].to_numpy()[self.tc_index]
		
		self.e1.setText(str(self.default_time))
	
	def buttonPress_red(self):
	
		self.e1.setEnabled(True)
		
		self.default_time = df[(df["T"]==0)]["T0"].to_numpy()[self.tc_index]
		self.new_cell_class = 0
		self.new_cell_death_time = self.default_time
		self.new_cell_color = "tab:orange"
		

	def buttonPress_blue(self):
	
		self.e1.setEnabled(False)
		
		self.new_cell_class = 1
		self.new_cell_death_time = -1
		self.new_cell_color = "tab:cyan"


	def buttonPress_yellow(self):
	
		self.e1.setEnabled(False)
		
		self.new_cell_class = 2
		self.new_cell_death_time = -1
		self.new_cell_color = "y"

	def save_csv(self):
		path=pos+"/visual_table_checked.csv"
		if os.path.exists(path):
			msgBox = QMessageBox()
			msgBox.setIcon(QMessageBox.Warning)
			msgBox.setText("A checked version has been found.\nDo you want to rewrite it?")
			msgBox.setWindowTitle("Warning")
			msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

			returnValue = msgBox.exec()
			if returnValue == QMessageBox.Cancel:
				return(None)			
			elif returnValue == QMessageBox.Ok:
				os.remove(path)
				df.to_csv(path)
				print(f"Visual table saved in {path}")
		else:
			df.to_csv(path)
			print(f"Visual table saved in {path}")
	

	def submit_action(self):
	
		#Reinitialize change class button
		self.change_btn.disconnect()
		self.change_btn.clicked.connect(self.buttonPress_change_class)
		self.change_btn.setText("Change class")
		
		if self.red_btn.isChecked():
		
			try:
				self.new_cell_death_time = float(self.e1.text())
			except ValueError:
				self.new_cell_death_time = -1.0
			self.e1.setText("")
			if self.new_cell_death_time<0:
				self.new_cell_death_time=0
			elif self.new_cell_death_time>len(cscats):
				self.new_cell_death_time=len(cscats)
			for k in range(0,len(cclass)):
				cclass[k][self.tc_index] = self.new_cell_color			
			for k in range(0,int(self.new_cell_death_time)):
				cscats[k][self.tc_index] = "tab:cyan"
			for k in range(int(self.new_cell_death_time),len(cscats)):
				cscats[k][self.tc_index] = "tab:orange"
				
			c_array = np.array(cscats[:,self.tc_index])
			bin_status = [0 if c=="r" else 1 for c in c_array]
			df.loc[df.TID==self.track_selected,"STATUS"] = bin_status
			
			df_at_track = df[(df["TID"]==self.track_selected)]
			track_indices = df_at_track.index
			
			for j in range(len_movie):
				status,status_color = get_status_color(0,np.linspace(0,len_movie-1,len_movie)[j],self.new_cell_death_time,len_movie)
				df.loc[track_indices[j],"STATUS"] = status
				df.loc[track_indices[j],"STATUS_COLOR"] = status_color
			
		else:
			if self.blue_btn.isChecked():
				self.new_cell_class = 1
			elif self.yellow_btn.isChecked():
				self.new_cell_class = 2

			for k in range(0,len(cscats)):
				cscats[k][self.tc_index] = self.new_cell_color
				cclass[k][self.tc_index] = self.new_cell_color

			df.loc[df.TID==self.track_selected,"STATUS"] = 1
			df.loc[df.TID==self.track_selected,"STATUS_COLOR"] = get_class_color(self.new_cell_class)
						
		
		#self.track_selected = df[(df["T"]==0)]["TID"].to_numpy()[self.tc_index]
		print(self.track_selected, self.new_cell_class, self.new_cell_death_time)
		df.loc[df.TID==self.track_selected,"CLASS"] = self.new_cell_class
		df.loc[df.TID==self.track_selected,"T0"] = self.new_cell_death_time
		df.loc[df.TID==self.track_selected, "CLASS_COLOR"] = get_class_color(self.new_cell_class)
		
		#print(get_class_color(self.new_cell_class),self.new_cell_color)
		
		self.center_coords.remove(self.center_coords[-1])
		#self.cell_info.setText("")

		self.red_btn.hide()
		self.blue_btn.hide()
		self.yellow_btn.hide()

		self.change_btn.setEnabled(False)
		self.cancel_btn.setEnabled(False)

		#self.change_btn.hide()
		#self.cancel_btn.hide()
		self.e1.hide()
		self.dt_label.hide()
	
	def function_abort(self):
		self.save_message = QMessageBox()
		self.save_message.setText("Do you want to save your modifications?")
		self.save_message.setStandardButtons(QMessageBox.Cancel | QMessageBox.Discard | QMessageBox.Ok)
		returnValue = self.save_message.exec()
		if returnValue == QMessageBox.Ok:
			self.save_csv()
			os.abort()
		elif returnValue == QMessageBox.Discard:
			os.abort()
		else:
			pass
	
	def file_save(self):
		global df
		pathsave_custom = QFileDialog.getSaveFileName(self, "Select file name", pos, "CSV files (*.csv)")[0]
		if pathsave_custom.endswith(".csv"):
			df = remove_unnamed_col(df)
			df.to_csv(pathsave_custom)

	def export_training(self):
		#global df
		unique_tracks = np.unique(df["TID"].to_numpy())
		inputs = []
		for tid in unique_tracks:
			dft = df[(df["TID"]==tid)]
			signal_b = dft["BLUE_INTENSITY"].to_numpy()
			signal_r = dft["RED_INTENSITY"].to_numpy()
			x0track = dft["T0"].to_numpy()[0]
			class_track = dft["CLASS"].to_numpy()[0]
			inputs.append([class_track,signal_b,signal_r,tid,x0track])
		inputs = np.array(inputs,dtype=object)
		pathsave_ = QFileDialog.getSaveFileName(self, "Select file name", pos, "NPY files (*.npy)")[0]
		if pathsave_.endswith(".npy"):
			np.save(pathsave_,inputs)

	def retrain_model(self):
		self.retrain = RetrainWindow()
		self.retrain.show()

	
	def _createActions(self):
			# Creating action using the first constructor
			
			self.saveFile = QAction(self)
			self.saveFile.setText("&Save As...")
			self.saveFile.triggered.connect(self.file_save)
			self.saveFile.setShortcut("Ctrl+S")
			
			self.exitAction = QAction(self)
			self.exitAction.setText("&Exit")
			self.exitAction.triggered.connect(self.function_abort)

			self.exportAIset = QAction(self)
			self.exportAIset.setText("&Export training set...")
			self.exportAIset.triggered.connect(self.export_training)

			self.retrainAI = QAction(self)
			self.retrainAI.setText("&Retrain AI model...")
			self.retrainAI.triggered.connect(self.retrain_model)
			
			#self.helpContentAction = QAction(QIcon("/home/limozin/Downloads/test.svg"), "&Open...", self)
		
	def _createMenuBar(self):
		menuBar = self.menuBar()
		# Creating menus using a QMenu object
		fileMenu = QMenu("&File", self)
		menuBar.addMenu(fileMenu)
		fileMenu.addAction(self.saveFile)
		fileMenu.addAction(self.exportAIset)
		fileMenu.addAction(self.retrainAI)
		fileMenu.addAction(self.exitAction)

		#helpMenu = QMenu("&Help",self)
		#menuBar.addMenu(helpMenu)
		#helpMenu.addAction(self.helpContentAction)
		
	def onclick(self,event):
		"""
		This on-click function highlights in lime color the cell that has been selected and extracts its track ID.
		"""	
		if event.dblclick:
			global ix, iy
			global death_t
			global cscats
			
			ix, iy = event.xdata, event.ydata
			instant = self.myFigCanvas.iter_val
			self.selected_x,self.selected_y,temp_tc_index = self.find_closest(np.array([xscats[0],yscats[0]]),ix,iy)
			#print(self.center_coords)
			check_if_second_selection = len(self.center_coords)==1 #(self.selected_x,self.selected_y,temp_tc_index) in self.center_coords

			if len(self.center_coords)==0:
				self.cancel_btn.setShortcut(QKeySequence("Esc"))
				self.tc_index = temp_tc_index
				self.center_coords.append((self.selected_x, self.selected_y,self.tc_index))
				#print(cscats[:][self.tc_index])
				
				self.previous_color = np.copy(cscats[:,self.tc_index]) #cscats[0][self.tc_index]
				
				cscats[:,self.tc_index] = 'lime'
				#print(self.previous_color,cscats[:,self.tc_index])
				default_time = df[(df["T"]==0)]["T0"].to_numpy()[self.tc_index]
				self.track_selected = df[(df["T"]==0)]["TID"].to_numpy()[self.tc_index]
				classification_label = df[(df["TID"]==self.track_selected)]["CLASS"].to_numpy()[0]
				mean_x = np.mean(df[(df["TID"]==self.track_selected)]["X"].to_numpy())
				mean_y = np.mean(df[(df["TID"]==self.track_selected)]["Y"].to_numpy())

				self.cell_info.setText(f"Cell selected: track {self.track_selected}\nClassification = {classification_label}\nEstimated death time = {round(default_time,2)}")
				self.cell_plot.tc_index = self.tc_index
				
				self.update_cell_plot()
				self.show()

				self.change_btn.setEnabled(True)
				self.cancel_btn.setEnabled(True)

			elif (check_if_second_selection==True)*(self.center_coords[0][2]==temp_tc_index):
				self.cancel_btn.setShortcut(QKeySequence())

				cscats[:,self.tc_index] = self.previous_color #cscats0[k][self.tc_index]

				self.center_coords.pop(0)
				self.change_btn.setEnabled(False)
				self.cancel_btn.setEnabled(False)
			else:
				pass 

App = QApplication(sys.argv)
App.setStyle("Fusion")
window = Window()

sys.exit(App.exec())
