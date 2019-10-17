# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'try1.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.price_box = QtWidgets.QTextEdit(self.centralwidget)
        self.price_box.setGeometry(QtCore.QRect(160, 130, 104, 71))
        self.price_box.setObjectName("price_box")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(80, 160, 47, 13))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.tax_rate = QtWidgets.QSpinBox(self.centralwidget)
        self.tax_rate.setGeometry(QtCore.QRect(170, 260, 42, 22))
        self.tax_rate.setProperty("value", 20)
        self.tax_rate.setObjectName("tax_rate")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(70, 270, 47, 13))
        self.label_2.setObjectName("label_2")
        self.calc_tax_button = QtWidgets.QPushButton(self.centralwidget)
        self.calc_tax_button.setGeometry(QtCore.QRect(160, 320, 75, 23))
        self.calc_tax_button.setObjectName("calc_tax_button")
        self.results_window = QtWidgets.QTextEdit(self.centralwidget)
        self.results_window.setGeometry(QtCore.QRect(140, 390, 104, 71))
        self.results_window.setObjectName("results_window")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(170, 30, 261, 51))
        font = QtGui.QFont()
        font.setPointSize(22)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Price"))
        self.label_2.setText(_translate("MainWindow", "Tax Rate"))
        self.calc_tax_button.setText(_translate("MainWindow", "Calculate Tax"))
        self.label_3.setText(_translate("MainWindow", "Sales Tax Calculator"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
