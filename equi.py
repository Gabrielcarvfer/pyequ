# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\equi.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
sampleQueue = []


class Ui_Dialog(object):
    progressBars = []
    gainTable = []
    sampleQueue = []
    controlDictionary = []
    def setupUi(self, Dialog, globalGainTable, globalSampleQueue, globalControlDictionary):
        self.controlDictionary = globalControlDictionary
        self.gainTable = globalGainTable
        self.sampleQueue = globalSampleQueue
        Dialog.setObjectName("Dialog")
        Dialog.resize(330, 300)
        self.progressBar = QtWidgets.QProgressBar(Dialog)
        self.progressBar.setGeometry(QtCore.QRect(20, 20, 21, 101))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setOrientation(QtCore.Qt.Vertical)
        self.progressBar.setObjectName("progressBar")
        self.progressBar_2 = QtWidgets.QProgressBar(Dialog)
        self.progressBar_2.setGeometry(QtCore.QRect(50, 20, 21, 101))
        self.progressBar_2.setProperty("value", 0)
        self.progressBar_2.setOrientation(QtCore.Qt.Vertical)
        self.progressBar_2.setObjectName("progressBar_2")
        self.progressBar_3 = QtWidgets.QProgressBar(Dialog)
        self.progressBar_3.setGeometry(QtCore.QRect(80, 20, 21, 101))
        self.progressBar_3.setProperty("value", 0)
        self.progressBar_3.setOrientation(QtCore.Qt.Vertical)
        self.progressBar_3.setObjectName("progressBar_3")
        self.progressBar_4 = QtWidgets.QProgressBar(Dialog)
        self.progressBar_4.setGeometry(QtCore.QRect(110, 20, 21, 101))
        self.progressBar_4.setProperty("value", 0)
        self.progressBar_4.setOrientation(QtCore.Qt.Vertical)
        self.progressBar_4.setObjectName("progressBar_4")
        self.progressBar_5 = QtWidgets.QProgressBar(Dialog)
        self.progressBar_5.setGeometry(QtCore.QRect(140, 20, 21, 101))
        self.progressBar_5.setProperty("value", 0)
        self.progressBar_5.setOrientation(QtCore.Qt.Vertical)
        self.progressBar_5.setObjectName("progressBar_5")
        self.progressBar_6 = QtWidgets.QProgressBar(Dialog)
        self.progressBar_6.setGeometry(QtCore.QRect(230, 20, 21, 101))
        self.progressBar_6.setProperty("value", 0)
        self.progressBar_6.setOrientation(QtCore.Qt.Vertical)
        self.progressBar_6.setObjectName("progressBar_6")
        self.progressBar_7 = QtWidgets.QProgressBar(Dialog)
        self.progressBar_7.setGeometry(QtCore.QRect(170, 20, 21, 101))
        self.progressBar_7.setProperty("value", 0)
        self.progressBar_7.setOrientation(QtCore.Qt.Vertical)
        self.progressBar_7.setObjectName("progressBar_7")
        self.progressBar_8 = QtWidgets.QProgressBar(Dialog)
        self.progressBar_8.setGeometry(QtCore.QRect(200, 20, 21, 101))
        self.progressBar_8.setProperty("value", 0)
        self.progressBar_8.setOrientation(QtCore.Qt.Vertical)
        self.progressBar_8.setObjectName("progressBar_8")
        self.progressBar_9 = QtWidgets.QProgressBar(Dialog)
        self.progressBar_9.setGeometry(QtCore.QRect(290, 20, 21, 101))
        self.progressBar_9.setProperty("value", 0)
        self.progressBar_9.setOrientation(QtCore.Qt.Vertical)
        self.progressBar_9.setObjectName("progressBar_9")
        self.progressBar_10 = QtWidgets.QProgressBar(Dialog)
        self.progressBar_10.setGeometry(QtCore.QRect(260, 20, 21, 101))
        self.progressBar_10.setProperty("value", 0)
        self.progressBar_10.setOrientation(QtCore.Qt.Vertical)
        self.progressBar_10.setObjectName("progressBar_10")
        self.verticalSlider = QtWidgets.QSlider(Dialog)
        self.verticalSlider.setGeometry(QtCore.QRect(20, 140, 22, 101))
        self.verticalSlider.setProperty("value", 50)
        self.verticalSlider.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider.setObjectName("verticalSlider")
        self.verticalSlider_2 = QtWidgets.QSlider(Dialog)
        self.verticalSlider_2.setGeometry(QtCore.QRect(50, 140, 22, 101))
        self.verticalSlider_2.setProperty("value", 50)
        self.verticalSlider_2.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider_2.setObjectName("verticalSlider_2")
        self.verticalSlider_3 = QtWidgets.QSlider(Dialog)
        self.verticalSlider_3.setGeometry(QtCore.QRect(80, 140, 22, 101))
        self.verticalSlider_3.setProperty("value", 50)
        self.verticalSlider_3.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider_3.setObjectName("verticalSlider_3")
        self.verticalSlider_4 = QtWidgets.QSlider(Dialog)
        self.verticalSlider_4.setGeometry(QtCore.QRect(110, 140, 22, 101))
        self.verticalSlider_4.setProperty("value", 50)
        self.verticalSlider_4.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider_4.setObjectName("verticalSlider_4")
        self.verticalSlider_5 = QtWidgets.QSlider(Dialog)
        self.verticalSlider_5.setGeometry(QtCore.QRect(140, 140, 22, 101))
        self.verticalSlider_5.setProperty("value", 50)
        self.verticalSlider_5.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider_5.setObjectName("verticalSlider_5")
        self.verticalSlider_6 = QtWidgets.QSlider(Dialog)
        self.verticalSlider_6.setGeometry(QtCore.QRect(200, 140, 22, 101))
        self.verticalSlider_6.setProperty("value", 50)
        self.verticalSlider_6.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider_6.setObjectName("verticalSlider_6")
        self.verticalSlider_7 = QtWidgets.QSlider(Dialog)
        self.verticalSlider_7.setGeometry(QtCore.QRect(230, 140, 22, 101))
        self.verticalSlider_7.setProperty("value", 50)
        self.verticalSlider_7.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider_7.setObjectName("verticalSlider_7")
        self.verticalSlider_8 = QtWidgets.QSlider(Dialog)
        self.verticalSlider_8.setGeometry(QtCore.QRect(170, 140, 22, 101))
        self.verticalSlider_8.setProperty("value", 50)
        self.verticalSlider_8.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider_8.setObjectName("verticalSlider_8")
        self.verticalSlider_9 = QtWidgets.QSlider(Dialog)
        self.verticalSlider_9.setGeometry(QtCore.QRect(260, 140, 22, 101))
        self.verticalSlider_9.setProperty("value", 50)
        self.verticalSlider_9.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider_9.setObjectName("verticalSlider_9")
        self.verticalSlider_10 = QtWidgets.QSlider(Dialog)
        self.verticalSlider_10.setGeometry(QtCore.QRect(290, 140, 22, 101))
        self.verticalSlider_10.setProperty("value", 50)
        self.verticalSlider_10.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider_10.setObjectName("verticalSlider_10")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(10, 270, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.play)
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(90, 270, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.pause)

        self.progressBars = [self.progressBar,
                             self.progressBar_2,
                             self.progressBar_3,
                             self.progressBar_4,
                             self.progressBar_5,
                             self.progressBar_6,
                             self.progressBar_7,
                             self.progressBar_8,
                             self.progressBar_9,
                             self.progressBar_10,]


        self.verticalSlider.valueChanged.connect(self.updateGain)
        self.verticalSlider_2.valueChanged.connect(self.updateGain_2)
        self.verticalSlider_3.valueChanged.connect(self.updateGain_3)
        self.verticalSlider_4.valueChanged.connect(self.updateGain_4)
        self.verticalSlider_5.valueChanged.connect(self.updateGain_5)
        self.verticalSlider_6.valueChanged.connect(self.updateGain_6)
        self.verticalSlider_7.valueChanged.connect(self.updateGain_7)
        self.verticalSlider_8.valueChanged.connect(self.updateGain_8)
        self.verticalSlider_9.valueChanged.connect(self.updateGain_9)
        self.verticalSlider_10.valueChanged.connect(self.updateGain_10)


        self.timer = QtCore.QTimer()
        self.timer.setInterval(100)  # Throw event timeout with an interval of 1000 milliseconds
        self.timer.timeout.connect(self.updateProgress)  # each time timer counts a second, call self.blink


        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def play(self):
        self.controlDictionary["playingBool"] = True
        self.timer.start()


    def pause(self):
        self.controlDictionary["playingBool"] = False
        self.timer.stop()


    def updateGain(self):
        self.gainTable[0] = (self.verticalSlider.value() - 50) / 16.5
    def updateGain_2(self):
        self.gainTable[1] = (self.verticalSlider_2.value() - 50) / 16.5
    def updateGain_3(self):
        self.gainTable[2] = (self.verticalSlider_3.value() - 50) / 16.5
    def updateGain_4(self):
        self.gainTable[3] = (self.verticalSlider_4.value() - 50) / 16.5
    def updateGain_5(self):
        self.gainTable[4] = (self.verticalSlider_5.value() - 50) / 16.5
    def updateGain_6(self):
        self.gainTable[5] = (self.verticalSlider_6.value() - 50) / 16.5
    def updateGain_7(self):
        self.gainTable[6] = (self.verticalSlider_7.value() - 50) / 16.5
    def updateGain_8(self):
        self.gainTable[7] = (self.verticalSlider_8.value() - 50) / 16.5
    def updateGain_9(self):
        self.gainTable[8] = (self.verticalSlider_9.value() - 50) / 16.5
    def updateGain_10(self):
        self.gainTable[9] = (self.verticalSlider_10.value() - 50) / 16.5

    def updateProgress(self):
        if not self.sampleQueue.empty():
            values = self.sampleQueue.get()
            if values:
                for bar in range(len(self.progressBars)):
                    self.progressBars[bar].setProperty("value", values[bar])

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "Tocar"))
        self.pushButton_2.setText(_translate("Dialog", "Pausar"))


def qt_load(gainTable, sampleQueue, controlDictionary):
    app = QtWidgets.QApplication([""])
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog, gainTable, sampleQueue, controlDictionary)
    Dialog.show()
    app.exec_()
    pass
