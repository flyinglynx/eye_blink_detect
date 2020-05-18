# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\sky\Desktop\大创\blink_detection_end.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.open_camera = QtWidgets.QPushButton(self.centralwidget)
        self.open_camera.setGeometry(QtCore.QRect(610, 190, 91, 41))
        self.open_camera.setObjectName("open_camera")
        self.exit_button = QtWidgets.QPushButton(self.centralwidget)
        self.exit_button.setGeometry(QtCore.QRect(610, 60, 91, 41))
        self.exit_button.setObjectName("exit_button")
        self.star_detection = QtWidgets.QPushButton(self.centralwidget)
        self.star_detection.setGeometry(QtCore.QRect(610, 280, 91, 41))
        self.star_detection.setObjectName("star_detection")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(590, 390, 81, 41))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(590, 440, 101, 16))
        self.label_2.setObjectName("label_2")
        self.camera_out = QtWidgets.QLabel(self.centralwidget)
        self.camera_out.setGeometry(QtCore.QRect(130, 90, 441, 391))
        self.camera_out.setText("")
        self.camera_out.setObjectName("camera_out")
        self.data_out = QtWidgets.QLabel(self.centralwidget)
        self.data_out.setGeometry(QtCore.QRect(200, 410, 291, 31))
        self.data_out.setText("")
        self.data_out.setObjectName("data_out")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(670, 400, 91, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(690, 440, 71, 20))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(590, 360, 81, 21))
        self.label_3.setObjectName("label_3")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_3.setGeometry(QtCore.QRect(670, 360, 91, 20))
        self.lineEdit_3.setObjectName("lineEdit_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.open_camera.clicked.connect(MainWindow.open_cama_click)
        self.star_detection.clicked.connect(MainWindow.start_dete_click)
        self.exit_button.clicked.connect(MainWindow.exit_button_click)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.open_camera.setText(_translate("MainWindow", "打开摄像头"))
        self.star_detection.setText(_translate("MainWindow", "开始检测"))
        self.label.setText(_translate("MainWindow", "眨眼次数(次)"))
        self.label_2.setText(_translate("MainWindow", "眨眼频率（次/分）"))
        self.label_3.setText(_translate("MainWindow", "检测时长（秒）"))
        self.exit_button.setText(_translate("MainWindow", "退出程序"))
