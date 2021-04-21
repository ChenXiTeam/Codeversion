import os
import sys

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem

import untitled as mw
from  userful import Algorithm

def check_start():
    if mainwindow_ui.lineEdit.text() == '':
        # mainwindow_ui.no_file_messagebox()
        print("地址栏是空的")
    database = Algorithm.get_databasebylist(in_filename)
    print(database)
    if mainwindow_ui.checkBox.isChecked():
        #调用算法1
        print("simhash算法")
        set_table2(Algorithm.get_simhash_similarity(database),1)
    if mainwindow_ui.checkBox_2.isChecked():
    # 调用算法2
        print("TFIDF_cosine算法")
        print(Algorithm.get_TFIDF_cosine(database))
    if mainwindow_ui.checkBox_3.isChecked():
    # 调用算法3
        print("SparseMS算法")
        print(Algorithm.get_SparseMS(database))
    if mainwindow_ui.checkBox_4.isChecked():
    # 调用算法4
        print("KgramHashim算法")
        print(Algorithm.get_KgramHashim(5, 4, 3, database))

def pick_in():
    try:
        filenames, filetype = QtWidgets.QFileDialog.getOpenFileNames(None,"选取文件", os.getcwd(),"Word Files(*.txt)")

        mainwindow_ui.lineEdit.setText(filenames[0] + "...")

        global in_filename
        in_filename = []
        global in_filetype

        global num
        num = 0
        while num < len(filenames):
            in_filename.append(filenames[num])
            num = num + 1

        in_filetype = filetype

    except:
        print('未选择文件')

def set_table2(result,number):
    mainwindow_ui.tableWidget.setColumnCount(9)
    # mainwindow_ui.tableWidget.setRowCount(len(total_events))
    # for index, event in enumerate(total_events):
    print(result)
    for i in range(len(result)):

        row_number = mainwindow_ui.tableWidget.rowCount()
        row_number = row_number + 1
        mainwindow_ui.tableWidget.setRowCount(row_number)
        print(result[i][0])

        mainwindow_ui.tableWidget.setItem(row_number - 1, 0, QTableWidgetItem(str(i)))
        mainwindow_ui.tableWidget.setItem(row_number - 1, number, QTableWidgetItem(str(result[i][0])))
    # mainwindow_ui.tableWidget.setItem(2, 2, QTableWidgetItem("123"))

        mainwindow_ui.tableWidget.setItem(row_number-1,number+1,QTableWidgetItem(str(result[i][1])))



if __name__ == '__main__':
    getProblems = pyqtSignal(str, int, int)
    insertRow = pyqtSignal()

    app = QApplication(sys.argv)
    mainwindow_ui = mw.Ui_MainWindow()
    qMainWindow = QMainWindow()
    mainwindow_ui.setupUi(qMainWindow)
    qMainWindow.show()

    # 设置按钮图标
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap("../img/file.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    mainwindow_ui.toolButton.setIcon(icon)

    # 设置按钮的事件监听

    mainwindow_ui.toolButton.clicked.connect(lambda:pick_in())
    mainwindow_ui.pushButton.clicked.connect(lambda:check_start())

    sys.exit(app.exec_())