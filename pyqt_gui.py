## GUI for brewing 
#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import time
from threading import Timer
import pyqtgraph
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
#from PyQt5.QtOpenGL import *
from max6675 import MAX6675, MAX6675Error
from gui_mesh import mesh
'''##########################################
class PID_reg():
        def __init__(self):
                self.P = 10
                self.I = 0.1
                self.D = 0.0
                self.relayPin = 10
                self.WindowSize = 5000
                self.temp = temp().get_temp()

        def output(self):
                self.PID = mesh(self.P,self.I,self.D,self.relayPin,self.WindowSize,self.temp)
                self.logic = self.PID.regulator()
                self.output = self.PID.regulator()
                return self.logic,self.output ### FEIL

#########################################'''
        

class temp():

        def __init__(self, parent=None):
                self.cs_pin = 24
                self.clock_pin = 23
                self.data_pin = 22
                self.units = "c"
                self.get_temp()

        def get_temp(self):
                self.temp_sensor = MAX6675(self.cs_pin, self.clock_pin, self.data_pin, self.units)
                self.temp = self.temp_sensor.get()
                return self.temp
                
class Main(QMainWindow):

	def __init__(self, parent=None):
		super().__init__(parent)
		self.setval = 10
                # Read sensor
		self.sensor = temp()
		self.procval = self.sensor.get_temp()
		'''######################################### Read PID FEIL
		self.regulator = PID_reg()
		self.logic = self.regulator.output()
		self.output = self.regulator.output()
		#####################################'''
		self.other_window = None
		self.initMain()		
		

	def initMain(self):
		QToolTip.setFont(QFont('SansSerif',10))
		self.statusBar().showMessage('Ready')
		self.setToolTip('This is a <b>Mesh regulator</b> widget')
		self.menu()
		self.setGeometry(300, 300, 460, 320)
		self.setup(self.setval,self.procval)
		self.temperature()
		self.center()
		self.setWindowTitle('GUI')
		self.setWindowIcon(QIcon('web.png'))
		self.show()

	def setup(self, setval,procval):
                self.procValue = QTextEdit(self)
                self.procValue.setGeometry(QRect(370, 70, 60, 50))
                self.procValue.setObjectName("procValue")
                self.procValue.setText(str(self.procval))

                self.setValue = QTextEdit(self)
                self.setValue.setGeometry(QRect(370, 160, 60, 50))
                self.setValue.setObjectName("setValue")
                self.setValue.setText(str(self.setval))
                btn = QPushButton('Start',self)
                btn.setToolTip('This is a <b>Push Button</b> widget')
                btn.resize(btn.sizeHint())
                btn.move(50,80)
                btn.clicked.connect(self.newWinOpen)

                qbtn = QPushButton('Quit',self)
                qbtn.resize(btn.sizeHint())
                qbtn.move(370,10)
                qbtn.clicked.connect(QCoreApplication.instance().quit)

                tempbtn = QPushButton('Temp Button',self)
                tempbtn.setToolTip('This is a <b>Temp Button</b> widget')
                tempbtn.resize(btn.sizeHint())
                tempbtn.move(50,120)
                tempbtn.clicked.connect(self.temperature)

                btnOn = QPushButton('+',self)
                btnOn.setGeometry(QRect(250, 70, 71, 61))
                btnOn.setObjectName("btnOn")
                btnOn.clicked.connect(lambda: self.addValue(self.setval))

                btnOff = QPushButton('-',self)
                btnOff.setGeometry(QRect(250, 170, 71, 61))
                btnOff.setObjectName("btnOff")
                btnOff.clicked.connect(lambda: self.subValue(self.setval))
                
                return self.setval,self.procval
        
	def center(self):
		qr = self.frameGeometry()
		cp = QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

	def closeEvent(self,event):
		reply = QMessageBox.question(self, 'Message',
			"Are you sure to quit?", QMessageBox.Yes |
			QMessageBox.No, QMessageBox.No)

		if reply == QMessageBox.Yes:
			event.accept()
		else:
			event.ignore()

	def menu(self):

		exitAction = QAction(QIcon('exit.png'),'&Exit',self)
		exitAction.setShortcut('Ctrl+Q')
		exitAction.setStatusTip('Exit App')
		exitAction.triggered.connect(qApp.quit)

		menubar = self.menuBar()
		fileMenu = menubar.addMenu('&File')
		fileMenu.addAction(exitAction)

	def temperature(self):
                self.procval = self.sensor.get_temp()
                self.procValue.setText(str(self.procval))
                return self.procval
		
	def addValue(self,setval):
		self.setval += 1
		self.setValue.setText(str(setval))
		return self.setval
	def subValue(self,setval):
		self.setval -= 1
		self.setValue.setText(str(setval))
		return self.setval

	def newWinOpen(self):
		self.other_window = numpad()
		self.other_window.show()

	def newWinClear(self):
		del self.other_window
		self.other_window = None

class numpad(QWidget):

	def __init__(self, parent=None):
		super().__init__(parent)

		self.initNewWin()

	def initNewWin(self):
		
		self.setGeometry(300, 300, 460, 320)
		self.setWindowTitle('Num Pad')
		self.grid()
		self.center()

	def center(self):
		qr = self.frameGeometry()
		cp = QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

	def buttons(self):
		okButton = QPushButton("OK")
		okButton.clicked.connect(self.close)
		cancelButton = QPushButton("Cancel")

		cancelButton.clicked.connect(self.close)

		hbox = QHBoxLayout()
		hbox.addStretch(1)
		hbox.addWidget(okButton)
		hbox.addWidget(cancelButton)

		vbox = QVBoxLayout()
		vbox.addStretch(1)
		vbox.addLayout(hbox)

		self.setLayout(vbox)	

	def grid(self):
		grid = QGridLayout()
		self.setLayout(grid)

		numpad = ['7', '8', '9',
				'4', '5', '6',
				'1', '2', '3',
				'OK','0','Cancel']
		positions = [(i,j) for i in range(4) for j in range(3)]

		for position, numb in zip(positions, numpad):

			if numb == '':
				continue	
			button = QPushButton(numb)
			grid.addWidget(button, *position)

class progress(QWidget):
        def __init__(self):
                super().__init__()
                
                self.initProgress()

        def initProgress(self):
                self.pbar = QProgressBar(self)
                self.pbar.setGeometry(30,230,200,25)

                self.btn = QPushButton('Start',self)
                self.btn.move(30,180)
                self.btn.clicked.connect(self.doAction)

                self.timer = QBasicTimer()
                self.step = 0

        def timerEvenet(self, e):

                if self.step >= 100:
                        self.timer.stop()
                        self.btn.setTExt('Finished')
                        return

                self.step += 1
                self.pbar.setValue(self.step)

        def doAction(self):
                if self.timer.isActive():
                        self.timer.stop()
                        self.btn.setText('Start')
                else:
                        self.timer.start(100,self)
                        self.btn.setText('Stop')




if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Main()
	sys.exit(app.exec_())
