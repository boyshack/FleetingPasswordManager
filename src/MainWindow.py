# This file is part of Fleeting Password Manager (FleetingPM).
# Copyright (C) 2011 Jussi Lind <jussi.lind@iki.fi>
#
# FleetingPM is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# FleetingPM is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with FleetingPM. If not, see <http://www.gnu.org/licenses/>.

from PySide import QtCore, QtGui
from PySide.QtCore import Slot
from Engine import Engine
from AboutDlg import AboutDlg
from SettingsDlg import SettingsDlg

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent):
        QtGui.QMainWindow.__init__(self, parent)
        self.setWindowTitle("Fleeting Password Manager")
        self._defaultDelay = 5
        self._defaultLength = 8
        self.delay = self._defaultDelay
        self.length = self._defaultLength
        self.createWidgets()
        self.createMenu()
        self.engine = Engine()

    def createWidgets(self):
        self.layout = QtGui.QGridLayout()
        self.baseEdit = QtGui.QLineEdit()
        self.urlEdit = QtGui.QLineEdit()
        self.userEdit = QtGui.QLineEdit()
        self.passwdEdit = QtGui.QLineEdit()

        self.baseEdit.setEchoMode(QtGui.QLineEdit.Password)
        self.passwdEdit.setReadOnly(True)
        self.passwdEdit.setEnabled(False)

        self.layout.addWidget(self.baseEdit, 0, 1, 1, 2)
        self.layout.addWidget(self.urlEdit, 1, 1, 1, 2)
        self.layout.addWidget(self.userEdit, 2, 1, 1, 2)
        self.layout.addWidget(self.passwdEdit, 4, 1, 1, 2)

        frame = QtGui.QFrame()
        frame.setFrameShape(QtGui.QFrame.HLine)
        self.layout.addWidget(QtGui.QLabel("Base password:"), 0, 0)
        self.layout.addWidget(QtGui.QLabel("URL:"), 1, 0)
        self.layout.addWidget(QtGui.QLabel("User:"), 2, 0)
        self.layout.addWidget(frame, 3, 1, 1, 2)
        self.layout.addWidget(QtGui.QLabel("Password:"), 4, 0)

        self.genButton = QtGui.QPushButton("&Generate")
        self.layout.addWidget(self.genButton, 5, 1)
        
        self.quitButton = QtGui.QPushButton("&Quit")
        self.quitButton.clicked.connect(self.close)
        self.layout.addWidget(self.quitButton, 5, 2)

        dummy = QtGui.QWidget()
        dummy.setLayout(self.layout)
        self.setCentralWidget(dummy)
        
        self.genButton.clicked.connect(self.doGenerate)
        self.baseEdit.textChanged.connect(self.invalidate)
        self.urlEdit.textChanged.connect(self.invalidate)
        self.userEdit.textChanged.connect(self.invalidate)

        self.timer = QtCore.QTimeLine()
        self.timer.setDuration(self.delay * 1000)
        self.timer.frameChanged.connect(self.updateFrame)
        self.timer.setFrameRange(0, 255)

        self.settingsDlg = SettingsDlg(self)

    def createMenu(self):

        # Add file menu
        fileMenu = self.menuBar().addMenu("&File")

        # Add action for settings
        setAct = QtGui.QAction("&Settings..", fileMenu)
        setAct.triggered.connect(self.showSettings)
        fileMenu.addAction(setAct)
        
        # Add action for quit
        quitAct = QtGui.QAction("&Quit", fileMenu)
        quitAct.triggered.connect(self.close)
        fileMenu.addAction(quitAct)
        
        # Add help menu
        helpMenu = self.menuBar().addMenu("&Help")
        
        # Add action for help
        aboutAct = QtGui.QAction("&About", helpMenu)
        aboutAct.triggered.connect(self.showAbout)
        helpMenu.addAction(aboutAct)

    def showSettings(self):
        s = QtCore.QSettings("FleetingPM", "FleetingPM")
        d = self.settingsDlg
        d.lengthSpinBox.setValue(s.value("length", self._defaultLength))
        d.delaySpinBox.setValue(s.value("delay", self._defaultDelay))
        d.exec_()
        s.setValue("length", d.lengthSpinBox.value())
        s.setValue("delay", d.delaySpinBox.value())
        self.length = d.lengthSpinBox.value()
        self.delay = d.delaySpinBox.value()
        self.timer.setDuration(self.delay * 1000)

    def showAbout(self):
        aboutDlg = AboutDlg(self)
        aboutDlg.exec_()

    @Slot()
    def doGenerate(self):

        # Generate the passwd
        passwd = self.engine.generate(self.baseEdit.text(),
                                      self.urlEdit.text(),
                                      self.userEdit.text(),
                                      self.length)
        
        # Enable the text field, show the generated passwd
        # and start timer to slowly fade out the text
        self.passwdEdit.setEnabled(True)
        self.passwdEdit.setText(passwd)
        self.timer.stop()
        self.timer.start()

    @Slot(int)
    def updateFrame(self, frame):

        # Update aplha of the text color
        color = QtGui.QColor()
        color.setAlpha(255 - frame)
        palette = QtGui.QPalette(self.passwdEdit.palette())
        palette.setColor(QtGui.QPalette.Text, color)
        self.passwdEdit.setPalette(palette)

    @Slot()
    def invalidate(self):

        # Clear the text and disable the text field
        self.passwdEdit.setText("")
        self.passwdEdit.setEnabled(False)


