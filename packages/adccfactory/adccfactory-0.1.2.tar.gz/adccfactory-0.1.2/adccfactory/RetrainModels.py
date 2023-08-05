import sys
import os
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QApplication, QTabWidget,  QComboBox, QFrame, QAction, QCheckBox, QTextBrowser, QMenu, QSlider, QFileDialog, QLabel, QPushButton, QLineEdit, QWidget, QDialog, QMainWindow, QGridLayout
from PyQt5.QtGui import QImage, QIcon, QDoubleValidator, QPixmap
from screeninfo import get_monitors
from configparser import ConfigParser
from glob import glob
from functions import *
from retrain_cell_model import train_cell_model
from retrain_stardist import train_StarDist
import time
from datetime import datetime

home_dir = os.path.expanduser('~')
home_dir+="/"
current_path = os.getcwd()

class TrainCellModel(QMainWindow):

	training_end = pyqtSignal(int)

	def __init__(self):
		super().__init__()

		w = QWidget()
		grid = QGridLayout(w)
		self.setWindowTitle(f"Retrain model")
		self.setGeometry(0,0,600,250)
		self.setWindowIcon(QIcon(f"{home_dir}ADCCFactory_2.0/src/icons/icon.png"))
		self.center_window()

		LogoLabel = QLabel()
		logo = QPixmap(f"{home_dir}ADCCFactory_2.0/src/icons/combined_model_figure.png")
		logo = logo.scaledToHeight(256, mode=Qt.SmoothTransformation)
		LogoLabel.setPixmap(logo)
		grid.addWidget(LogoLabel, 2, 3, 7, 1, alignment=Qt.AlignCenter)

		grid.addWidget(QLabel("Dataset folder:"), 0, 0, 1, 3)
		self.dataFolder = QLineEdit()
		self.dataFolder.setAlignment(Qt.AlignLeft)	
		self.dataFolder.setEnabled(True)
		self.dataFolder.setText(f"{home_dir}ADCCFactory_2.0/src/datasets/cell_signals")
		grid.addWidget(self.dataFolder, 1, 0, 1, 3)

		self.browse_button = QPushButton("Browse...")
		self.browse_button.clicked.connect(self.browse_dataset_folder)
		grid.addWidget(self.browse_button, 1, 3, 1, 1)

		grid.addWidget(QLabel("New model name:"), 2, 0, 1, 3)
		self.ModelName = QLineEdit()
		self.ModelName.setAlignment(Qt.AlignLeft)	
		self.ModelName.setEnabled(True)
		self.ModelName.setText(f"Untitled_model_{datetime.today().strftime('%Y-%m-%d')}")
		grid.addWidget(self.ModelName, 3, 0, 1, 3)

		grid.addWidget(QLabel("Number of epochs:"), 4, 0, 1, 3)
		self.NbrEpochs = QLineEdit()
		self.NbrEpochs.setAlignment(Qt.AlignLeft)	
		self.NbrEpochs.setEnabled(True)
		self.NbrEpochs.setText(f"100")
		grid.addWidget(self.NbrEpochs, 5, 0, 1, 3)

		self.confirm_button = QPushButton("Submit")
		self.confirm_button.clicked.connect(self.retrain)
		grid.addWidget(self.confirm_button, 6, 1, 1, 1)

		self.setCentralWidget(w)

	def center_window(self):
		frameGm = self.frameGeometry()
		screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
		centerPoint = QApplication.desktop().screenGeometry(screen).center()
		frameGm.moveCenter(centerPoint)
		self.move(frameGm.topLeft())

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

		self.training_end.emit(1)

class TrainStarDistTCModel(QMainWindow):

	training_end = pyqtSignal(int)

	def __init__(self):
		super().__init__()

		w = QWidget()
		grid = QGridLayout(w)
		self.setWindowTitle(f"Retrain model")
		self.setGeometry(0,0,600,250)
		self.center_window()

		LogoLabel = QLabel()
		print(os.getcwd())
		logo = QPixmap(f"{home_dir}ADCCFactory_2.0/src/icons/stardist_logo.jpg")
		logo = logo.scaledToWidth(128, mode=Qt.SmoothTransformation)
		LogoLabel.setPixmap(logo)
		grid.addWidget(LogoLabel, 2, 3, 3, 1, alignment=Qt.AlignCenter)

		SegLabel = QLabel()
		seg = QPixmap(f"{home_dir}ADCCFactory_2.0/src/icons/label_segmentation.png")
		seg = seg.scaledToWidth(200, mode=Qt.SmoothTransformation)
		SegLabel.setPixmap(seg)
		grid.addWidget(SegLabel, 5, 3, 3, 1, alignment=Qt.AlignCenter)

		grid.addWidget(QLabel("Dataset folder:"), 0, 0, 1, 3)
		self.dataFolder = QLineEdit()
		self.dataFolder.setAlignment(Qt.AlignLeft)	
		self.dataFolder.setEnabled(True)
		self.dataFolder.setText(f"{home_dir}ADCCFactory_2.0/src/datasets/tc_nuclei")
		grid.addWidget(self.dataFolder, 1, 0, 1, 3)

		self.browse_button = QPushButton("Browse...")
		self.browse_button.clicked.connect(self.browse_dataset_folder)
		grid.addWidget(self.browse_button, 1, 3, 1, 1)

		grid.addWidget(QLabel("New model name:"), 2, 0, 1, 3)
		self.ModelName = QLineEdit()
		self.ModelName.setAlignment(Qt.AlignLeft)	
		self.ModelName.setEnabled(True)
		self.ModelName.setText(f"Untitled_model_{datetime.today().strftime('%Y-%m-%d')}")
		grid.addWidget(self.ModelName, 3, 0, 1, 3)

		grid.addWidget(QLabel("Number of epochs:"), 4, 0, 1, 3)
		self.NbrEpochs = QLineEdit()
		self.NbrEpochs.setAlignment(Qt.AlignLeft)	
		self.NbrEpochs.setEnabled(True)
		self.NbrEpochs.setText(f"100")
		grid.addWidget(self.NbrEpochs, 5, 0, 1, 3)

		grid.addWidget(QLabel("Batch size:"), 6, 0, 1, 3)
		self.BatchSize = QLineEdit()
		self.BatchSize.setAlignment(Qt.AlignLeft)	
		self.BatchSize.setEnabled(True)
		self.BatchSize.setText(f"8")
		grid.addWidget(self.BatchSize, 7, 0, 1, 3)

		self.confirm_button = QPushButton("Submit")
		self.confirm_button.clicked.connect(self.retrain)
		grid.addWidget(self.confirm_button, 8, 1, 1, 1)

		self.setCentralWidget(w)

	def center_window(self):
		frameGm = self.frameGeometry()
		screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
		centerPoint = QApplication.desktop().screenGeometry(screen).center()
		frameGm.moveCenter(centerPoint)
		self.move(frameGm.topLeft())

	def browse_dataset_folder(self):
		self.newDataFolder = str(QFileDialog.getExistingDirectory(self, 'Select directory'))
		self.dataFolder.setText(self.newDataFolder)

	def retrain(self):
		dataset_dir = self.dataFolder.text()
		output_dir = f"{home_dir}ADCCFactory_2.0/src/models/segmentation_tc"
		model_name = self.ModelName.text()
		nbr_epochs = int(self.NbrEpochs.text())
		batch_size = int(self.BatchSize.text())

		to_freeze = [self.dataFolder, self.browse_button, self.ModelName, self.confirm_button, self.NbrEpochs]
		for q in to_freeze:
			q.setEnabled(False)
			q.repaint()

		train_StarDist(model_name, dataset_dir, output_dir, nbr_epochs, batch_size, option="tc")

		for q in to_freeze:
			q.setEnabled(True)
			q.repaint()

		self.training_end.emit(1)

class TrainStarDistNKModel(QMainWindow):

	training_end = pyqtSignal(int)

	def __init__(self):
		super().__init__()

		w = QWidget()
		grid = QGridLayout(w)
		self.setWindowTitle(f"Retrain model")
		self.setGeometry(0,0,600,250)
		self.center_window()

		LogoLabel = QLabel()
		print(os.getcwd())
		logo = QPixmap(f"{home_dir}ADCCFactory_2.0/src/icons/stardist_logo.jpg")
		logo = logo.scaledToWidth(128, mode=Qt.SmoothTransformation)
		LogoLabel.setPixmap(logo)
		grid.addWidget(LogoLabel, 2, 3, 3, 1, alignment=Qt.AlignCenter)

		SegLabel = QLabel()
		seg = QPixmap(f"{home_dir}ADCCFactory_2.0/src/icons/label_segmentation.png")
		seg = seg.scaledToWidth(200, mode=Qt.SmoothTransformation)
		SegLabel.setPixmap(seg)
		grid.addWidget(SegLabel, 5, 3, 3, 1, alignment=Qt.AlignCenter)

		grid.addWidget(QLabel("Dataset folder:"), 0, 0, 1, 3)
		self.dataFolder = QLineEdit()
		self.dataFolder.setAlignment(Qt.AlignLeft)	
		self.dataFolder.setEnabled(True)
		self.dataFolder.setText(f"{home_dir}ADCCFactory_2.0/src/datasets/nks")
		grid.addWidget(self.dataFolder, 1, 0, 1, 3)

		self.browse_button = QPushButton("Browse...")
		self.browse_button.clicked.connect(self.browse_dataset_folder)
		grid.addWidget(self.browse_button, 1, 3, 1, 1)

		grid.addWidget(QLabel("New model name:"), 2, 0, 1, 3)
		self.ModelName = QLineEdit()
		self.ModelName.setAlignment(Qt.AlignLeft)	
		self.ModelName.setEnabled(True)
		self.ModelName.setText(f"Untitled_model_{datetime.today().strftime('%Y-%m-%d')}")
		grid.addWidget(self.ModelName, 3, 0, 1, 3)

		grid.addWidget(QLabel("Number of epochs:"), 4, 0, 1, 3)
		self.NbrEpochs = QLineEdit()
		self.NbrEpochs.setAlignment(Qt.AlignLeft)	
		self.NbrEpochs.setEnabled(True)
		self.NbrEpochs.setText(f"100")
		grid.addWidget(self.NbrEpochs, 5, 0, 1, 3)

		grid.addWidget(QLabel("Batch size:"), 6, 0, 1, 3)
		self.BatchSize = QLineEdit()
		self.BatchSize.setAlignment(Qt.AlignLeft)	
		self.BatchSize.setEnabled(True)
		self.BatchSize.setText(f"8")
		grid.addWidget(self.BatchSize, 7, 0, 1, 3)

		self.confirm_button = QPushButton("Submit")
		self.confirm_button.clicked.connect(self.retrain)
		grid.addWidget(self.confirm_button, 8, 1, 1, 1)

		self.setCentralWidget(w)

	def center_window(self):
		frameGm = self.frameGeometry()
		screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
		centerPoint = QApplication.desktop().screenGeometry(screen).center()
		frameGm.moveCenter(centerPoint)
		self.move(frameGm.topLeft())

	def browse_dataset_folder(self):
		self.newDataFolder = str(QFileDialog.getExistingDirectory(self, 'Select directory'))
		self.dataFolder.setText(self.newDataFolder)

	def retrain(self):
		dataset_dir = self.dataFolder.text()
		output_dir = f"{home_dir}ADCCFactory_2.0/src/models/segmentation_nk"
		model_name = self.ModelName.text()
		nbr_epochs = int(self.NbrEpochs.text())
		batch_size = int(self.BatchSize.text())

		to_freeze = [self.dataFolder, self.browse_button, self.ModelName, self.confirm_button, self.NbrEpochs]
		for q in to_freeze:
			q.setEnabled(False)
			q.repaint()

		train_StarDist(model_name, dataset_dir, output_dir, nbr_epochs, batch_size, option="nk")

		for q in to_freeze:
			q.setEnabled(True)
			q.repaint()

		self.training_end.emit(1)