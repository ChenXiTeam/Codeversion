# -*- coding: utf-8 -*-
import os
import random
import sys
import time

from PyQt5.QtCore import QThread, pyqtSignal, Qt, QSize
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QHeaderView, QTableWidgetItem, QAbstractItemView
from PyQt5 import QtWidgets, QtGui
from requests.auth import HTTPBasicAuth

import MainWindow as mw
import pick_method as pm
import startServer as ss
import fileScan as fs
import getData as gd
import Algorithm as ag

in_filename_pick = []  # 提取内容待处理文件
in_filetype_pick = ''  # 提取文件类型
in_filename_dc = []  # 相似度检测待处理文件
dict_in_filename_dc = {}  # 相似度检测文件序号-文件名字典
in_filetype_dc = ''  # 相似度文件类型
out_filename = []  # 输出文件（名）
filepath = ''  # 输出路径
num_pick = 0  # 提取文件个数
num_dc = 0  # 相似度检测文件个数


class Start(QMainWindow, mw.Ui_MainWindow):
    itemOrder = 1

    def __init__(self):
        QMainWindow.__init__(self)
        mw.Ui_MainWindow.__init__(self)
        self.setupUi(self)

        # 全屏
        self.setWindowState(Qt.WindowMaximized)

        # 设置按钮图标
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("img/file.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tb_input.setIcon(icon)
        self.tb_output.setIcon(icon)
        self.tb_prj_path.setIcon(icon)
        self.tb_dc_path.setIcon(icon)
        # 设置窗体图标
        icon.addPixmap(QtGui.QPixmap("img/check.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)

        # 设置按钮的事件监听
        self.tb_input.clicked.connect(self.pick_in_word)
        self.tb_output.clicked.connect(self.pick_out)
        self.tb_prj_path.clicked.connect(self.scan_path)
        self.pb_start_pick.clicked.connect(self.pick_start)
        self.pb_scan.clicked.connect(self.scan_start)
        self.pb_get.clicked.connect(self.get_start)
        self.tb_dc_path.clicked.connect(self.pick_in_txt)
        self.pb_dc_start.clicked.connect(self.dc_start)

        # 设置表格列宽自适应
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.tableWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.tableWidget.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.tableWidget.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        # 禁止编辑
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 点击表头排序
        self.tableWidget.horizontalHeader().sectionClicked.connect(self.VerSectionClicked)  # 表头单击信号




        # 设置表格列宽自适应
        self.tableWidget_2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget_2.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.tableWidget_2.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.tableWidget_2.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.tableWidget_2.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)
        self.tableWidget_2.horizontalHeader().setSectionResizeMode(7, QHeaderView.ResizeToContents)

        # 禁止编辑
        self.tableWidget_2.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # 打开服务器的线程 sonarqube
        self.server_starter = Server()
        self.server_starter.progressBarValue.connect(self.set_pgb)
        self.server_starter.workItem.connect(self.set_work_item)
        self.server_starter.workStatus.connect(self.set_work_statu)
        self.server_starter.buttonStop.connect(self.stop_button)
        self.server_starter.buttonStart.connect(self.start_button)
        self.server_starter.start()

    def VerSectionClicked(self, index):
        if index != 2:
            if self.itemOrder == 1:
                self.tableWidget.sortItems(index, Qt.DescendingOrder)
                self.itemOrder = 2
            else:
                self.tableWidget.sortItems(index, Qt.AscendingOrder)
                self.itemOrder = 1

    # 选择word输入路径
    def pick_in_word(self):
        try:
            filenames, filetype = QtWidgets.QFileDialog.getOpenFileNames(self, "选取文件", os.getcwd(),
                                                                         "Word Files(*.docx *.doc)")
            self.line_input.setText(filenames[0] + "...")

            global in_filename_pick
            in_filename_pick = []
            global in_filetype_pick

            global num_pick
            num_pick = 0
            while num_pick < len(filenames):
                in_filename_pick.append(filenames[num_pick])
                num_pick = num_pick + 1

            in_filetype_pick = filetype

        except:
            print('未选择文件')

    # 选择word输入路径
    def pick_in_txt(self):
        try:
            filenames, filetype = QtWidgets.QFileDialog.getOpenFileNames(self, "选取文件", os.getcwd(),
                                                                         "TXT Files(*.txt)")
            self.line_dc_path.setText(filenames[0] + "...")

            global in_filename_dc
            in_filename_dc = []
            global in_filetype_dc
            global dict_in_filename_dc
            dict_in_filename_dc = {}
            global num_dc
            num_dc = 0
            while num_dc < len(filenames):
                in_filename_dc.append(filenames[num_dc])
                dict_in_filename_dc[num_dc] = filenames[num_dc]
                num_dc = num_dc + 1

            in_filetype_dc = filetype

        except:
            print('未选择文件')

    # 选择输出路径
    def pick_out(self):

        global filepath
        filepath = QtWidgets.QFileDialog.getExistingDirectory(self, "选择目录", os.getcwd())
        if filepath != '':
            self.line_output.setText(filepath + "/")
            self.line_prj_path.setText(filepath)

        global out_filename  # 正文txt
        out_filename = []
        if in_filetype_pick == 'Word Files(*.docx *.doc)':
            t = 0
            while t < num_pick:
                f = in_filename_pick[t]
                temp = self.set_out_file_name(f)  # 获取去掉后缀的文件名
                out_filename.append(filepath + '/' + temp + '.txt')
                t = t + 1

        elif in_filetype_pick == 'JPG Files(*.jpeg *.jpg *jfif)':
            t = 0
            while t < num_pick:
                f = in_filename_pick[t]
                temp = self.set_out_file_name(f)
                out_filename.append(filepath + '/' + temp + '.txt')
                t = t + 1

    # 选择进行检测/获取结果的路径
    def scan_path(self):
        self.line_prj_path.setText(QtWidgets.QFileDialog.getExistingDirectory(self, "选择目录", os.getcwd()))

    # 返回不含后缀的文件名
    def set_out_file_name(self, s):
        index_head = s.rfind("/")
        index_hail = s.rfind(".")
        result = s[index_head + 1:index_hail]
        return result

    # 设置进度条进度的方法
    def set_pgb(self, i):
        self.pgb.setValue(i)

    # 设置工作项
    def set_work_item(self, str):
        self.label_work.setText('当前工作项：' + str)

    # 设置工作状态
    def set_work_statu(self, str):
        self.label_status.setText('工作状态：' + str)

    # 没有选择路径
    def no_file_messagebox(self):
        msg_box = QMessageBox.warning(self, '出错', '请选择文件或项目')
        print(msg_box)

    # 设置项目语言
    def set_file_type(self, type):
        if type == 1:
            self.rb_java.setChecked(True)
        elif type == 2:
            self.rb_cpp.setChecked(True)
        elif type == 3:
            self.rb_py.setChecked(True)

    # 设置表格内容
    def set_table_code(self, str, row, coloum):
        self.tableWidget.setItem(row, coloum, QTableWidgetItem(str))

    def table_insert_row(self):
        self.tableWidget.insertRow(self.tableWidget.rowCount())

    def remove_table_row(self):
        # 删除所有行
        rowPosition = self.tableWidget.rowCount()
        for rP in range(0, rowPosition)[::-1]:
            self.tableWidget.removeRow(rP)

    # 设置所有按钮禁用
    def stop_button(self):
        self.pb_get.setDisabled(True)
        self.pb_scan.setDisabled(True)
        self.pb_start_pick.setDisabled(True)
        self.pb_dc_start.setDisabled(True)

    # 设置所有按钮启用
    def start_button(self):
        self.pb_get.setDisabled(False)
        self.pb_scan.setDisabled(False)
        self.pb_start_pick.setDisabled(False)
        self.pb_dc_start.setDisabled(False)

    def get_file_name(self):
        dict_filename = {}
        for file in dict_in_filename_dc:
            dict_filename[file] = dict_in_filename_dc[file].split('/')[-1]
        return dict_filename

    # 将相似度检测结果显示在表格中
    def set_table_dc(self, result):
        # 删除所有行
        rowPosition = self.tableWidget_2.rowCount()
        print(rowPosition)
        for rP in range(0, rowPosition)[::-1]:
            print(rP)
            self.tableWidget_2.removeRow(rP)
            print(self.tableWidget_2.rowCount())

        dict_name = self.get_file_name()

        for file in dict_in_filename_dc:
            self.tableWidget_2.insertRow(self.tableWidget_2.rowCount())
            self.tableWidget_2.setItem(file, 0, QTableWidgetItem(dict_name[file]))  # 设置文件名
            if 'a' in result:
                self.tableWidget_2.setItem(file, 1, QTableWidgetItem(dict_name[result['a'][file][0]]))  # 设置文件名
                self.tableWidget_2.setItem(file, 2, QTableWidgetItem("%.2f" % result['a'][file][1]))  # 设置相似度
            if 'b' in result:
                self.tableWidget_2.setItem(file, 3, QTableWidgetItem(dict_name[result['b'][file][0]]))  # 设置文件名
                self.tableWidget_2.setItem(file, 4, QTableWidgetItem("%.2f" % result['b'][file][1]))  # 设置相似度
            if 'c' in result:
                self.tableWidget_2.setItem(file, 5, QTableWidgetItem(dict_name[result['c'][file][0]]))  # 设置文件名
                self.tableWidget_2.setItem(file, 6, QTableWidgetItem("%.2f" % result['c'][file][1]))  # 设置相似度
            if 'd' in result:
                self.tableWidget_2.setItem(file, 7, QTableWidgetItem(dict_name[result['d'][file][0]]))  # 设置文件名)
                self.tableWidget_2.setItem(file, 8, QTableWidgetItem("%.2f" % result['d'][file][1]))  # 设置相似度

    # 打开子线程
    def pick_start(self):
        # 创建并启用子线程
        self.pick_thread = Picker()
        self.pick_thread.progressBarValue.connect(self.set_pgb)
        self.pick_thread.buttonStop.connect(self.stop_button)
        self.pick_thread.buttonStart.connect(self.start_button)
        self.pick_thread.workStatus.connect(self.set_work_statu)
        self.pick_thread.workItem.connect(self.set_work_item)
        self.pick_thread.noFile.connect(self.no_file_messagebox)
        self.pick_thread.fileType.connect(self.set_file_type)
        self.pick_thread.start()

    # 打开子线程
    def scan_start(self):
        if self.line_prj_path.text() == '':
            self.no_file_messagebox()
        elif self.rb_java.isChecked():
            print(self.rb_java.text())
            # 创建并启用子线程
            self.scan_thread = Scanner(self.line_prj_path.text(), self.rb_java.text())
            self.scan_thread.progressBarValue.connect(self.set_pgb)
            self.scan_thread.buttonStop.connect(self.stop_button)
            self.scan_thread.buttonStart.connect(self.start_button)
            self.scan_thread.workStatus.connect(self.set_work_statu)
            self.scan_thread.workItem.connect(self.set_work_item)
            self.scan_thread.start()
        elif self.rb_cpp.isChecked():
            print(self.rb_cpp.text())
            # 创建并启用子线程
            self.scan_thread = Scanner(self.line_prj_path.text(), self.rb_cpp.text())
            self.scan_thread.progressBarValue.connect(self.set_pgb)
            self.scan_thread.buttonStop.connect(self.stop_button)
            self.scan_thread.buttonStart.connect(self.start_button)
            self.scan_thread.workStatus.connect(self.set_work_statu)
            self.scan_thread.workItem.connect(self.set_work_item)
            self.scan_thread.start()
        elif self.rb_py.isChecked():
            print(self.rb_py.text())
            # 创建并启用子线程
            self.scan_thread = Scanner(self.line_prj_path.text(), self.rb_py.text())
            self.scan_thread.progressBarValue.connect(self.set_pgb)
            self.scan_thread.buttonStop.connect(self.stop_button)
            self.scan_thread.buttonStart.connect(self.start_button)
            self.scan_thread.workStatus.connect(self.set_work_statu)
            self.scan_thread.workItem.connect(self.set_work_item)
            self.scan_thread.start()

    # 打开子线程
    def get_start(self):
        if self.line_prj_path.text() == '':
            self.no_file_messagebox()
        else:
            self.get_thread = Getter(self.line_prj_path.text())
            self.get_thread.progressBarValue.connect(self.set_pgb)
            self.get_thread.buttonStop.connect(self.stop_button)
            self.get_thread.buttonStart.connect(self.start_button)
            self.get_thread.workStatus.connect(self.set_work_statu)
            self.get_thread.workItem.connect(self.set_work_item)
            self.get_thread.getProblems.connect(self.set_table_code)
            self.get_thread.insertRow.connect(self.table_insert_row)
            self.get_thread.deleteRow.connect(self.remove_table_row)
            self.get_thread.start()

    def dc_start(self):
        if self.line_dc_path.text() == '':
            self.no_file_messagebox()
        else:
            pass
            choice = []
            if self.cb_a.isChecked():
                choice.append('a')
            if self.cb_b.isChecked():
                choice.append('b')
            if self.cb_c.isChecked():
                choice.append('c')
            if self.cb_d.isChecked():
                choice.append('d')
            self.dc_thread = Checker(choice)
            self.dc_thread.progressBarValue.connect(self.set_pgb)
            self.dc_thread.buttonStop.connect(self.stop_button)
            self.dc_thread.buttonStart.connect(self.start_button)
            self.dc_thread.workStatus.connect(self.set_work_statu)
            self.dc_thread.workItem.connect(self.set_work_item)
            self.dc_thread.resultDict.connect(self.set_table_dc)
            self.dc_thread.start()

    # 窗体关闭时的事件，重写了QWidget类的closeEvent()方法
    def closeEvent(self, event):
        super().closeEvent(event)
        # 结束java.exe进程，关闭sonarqube服务器，暴力美学
        os.system("taskkill /F /IM java.exe")


# 选择文件并提取代码与正文的线程类
class Picker(QThread):
    progressBarValue = pyqtSignal(int)  # 更新进度条
    workStatus = pyqtSignal(str)  # 设置工作状态
    workItem = pyqtSignal(str)  # 设置工作项
    noFile = pyqtSignal()  # 未选择文件
    fileType = pyqtSignal(int)
    buttonStop = pyqtSignal()  # 禁用所有按钮
    buttonStart = pyqtSignal()  # 启用所有按钮

    def __init__(self):

        super(Picker, self).__init__()

    def run(self):

        self.progressBarValue.emit(0)  # 发送进度条的值 信号
        # 如果没有选择文件，弹出提示框
        if not in_filename_pick:
            self.noFile.emit()  # 发送未选择文件信号
        # 如果选择了文件
        else:
            self.workItem.emit('提取实验报告代码、正文、图片')  # 发送工作项目信号
            self.workStatus.emit('正在进行')  # 发送工作状态信号
            self.buttonStop.emit()  # 发送按钮信号
            if in_filetype_pick == 'Word Files(*.docx *.doc)':
                for i in range(0, len(in_filename_pick)):
                    print(in_filename_pick[i])
                    print(out_filename[i])
                    type = pm.for_docx(in_filename_pick[i], out_filename[i])
                    pm.get_pictures(in_filename_pick[i], filepath)
                    self.progressBarValue.emit(i / len(in_filename_pick) * 100)  # 发送进度条的值 信号
            self.fileType.emit(type)
            self.progressBarValue.emit(100)  # 发送进度条的值 信号
            self.workStatus.emit('已完成')  # 发送工作状态信号
            self.buttonStart.emit()  # 发送按钮信号


class Scanner(QThread):
    progressBarValue = pyqtSignal(int)  # 更新进度条
    workStatus = pyqtSignal(str)  # 设置工作状态
    workItem = pyqtSignal(str)  # 设置工作项
    buttonStop = pyqtSignal()  # 禁用所有按钮
    buttonStart = pyqtSignal()  # 启用所有按钮

    prjp = ''
    prjn = ''
    language = ''

    def __init__(self, project_path, language):
        super(Scanner, self).__init__()
        self.prjp = project_path
        self.language = language

    def run(self):
        print('runrunrun')

        self.workItem.emit('项目代码检测')  # 发送工作项目信号
        self.workStatus.emit('正在进行')  # 发送工作状态信号
        self.buttonStop.emit()  # 发送按钮信号
        self.progressBarValue.emit(0)  # 发送进度条的值 信号

        self.prjn = os.path.basename(self.prjp)
        fs.scan_config(self.prjp, self.prjn, self.language)
        upper = random.randint(51, 71)
        for i in range(1, upper):
            time.sleep(0.2)
            self.progressBarValue.emit(i)  # 发送进度条的值 信号
        try:
            fs.scan_cmd(self.prjp, self.prjn, self.language)
        except:
            self.progressBarValue.emit(100)  # 发送进度条的值 信号
            self.workStatus.emit('已完成')  # 发送工作状态信号
            self.buttonStart.emit()  # 发送按钮信号


# 获取代码检测结果的线程类
class Getter(QThread):
    getProblems = pyqtSignal(str, int, int)
    insertRow = pyqtSignal()
    deleteRow = pyqtSignal()
    progressBarValue = pyqtSignal(int)  # 更新进度条
    workStatus = pyqtSignal(str)  # 设置工作状态
    workItem = pyqtSignal(str)  # 设置工作项
    buttonStop = pyqtSignal()  # 禁用所有按钮
    buttonStart = pyqtSignal()  # 启用所有按钮

    prjn = ''

    def __init__(self, project_path):
        super(Getter, self).__init__()
        self.prjn = os.path.basename(project_path)

    def run(self):

        self.workItem.emit('获取代码检测结果')  # 发送工作项目信号
        self.workStatus.emit('正在进行')  # 发送工作状态信号
        self.buttonStop.emit()  # 发送按钮信号

        auth = HTTPBasicAuth("admin".encode('utf-8'), "admin1")
        row = 0
        self.deleteRow.emit()
        for bug in gd.getBugs(self.prjn, auth):
            self.insertRow.emit()
            msg = bug.split('---')
            print(msg)
            col = 0
            bug_total = int(msg[0])
            msg.remove(msg[0])
            print(msg)
            for str in msg:
                self.getProblems.emit(str, row, col)
                col += 1
            row += 1
            self.progressBarValue.emit(int(row / bug_total * 50))
        self.progressBarValue.emit(50)  # 发送进度条的值 信号
        for code_smell in gd.getCodeSmell(self.prjn, auth):
            self.insertRow.emit()
            msg = code_smell.split('---')
            col = 0
            code_smell_total = int(msg[0])
            print(msg)
            msg.remove(msg[0])
            print(msg)
            for str in msg:
                self.getProblems.emit(str, row, col)
                col += 1
            row += 1
            self.progressBarValue.emit(int(row / code_smell_total * 50) + 50)
        self.workStatus.emit('已完成')  # 发送工作状态信号
        self.buttonStart.emit()  # 发送按钮信号
        self.progressBarValue.emit(100)  # 发送进度条的值 信号


# 打开sonarqube服务器的线程
class Server(QThread):
    progressBarValue = pyqtSignal(int)  # 更新进度条
    workStatus = pyqtSignal(str)  # 设置工作状态
    workItem = pyqtSignal(str)  # 设置工作项
    buttonStop = pyqtSignal()  # 禁用所有按钮
    buttonStart = pyqtSignal()  # 启用所有按钮

    def __init__(self):
        super(Server, self).__init__()

    def run(self):
        self.workStatus.emit('正在进行')
        self.workItem.emit('打开服务器')
        self.progressBarValue.emit(0)
        self.buttonStop.emit()
        ss.startSonarqubeServer()
        java_count = 0
        while java_count != 7:
            java_count = len(os.popen('tasklist /FI "IMAGENAME eq java.exe"').readlines())
            if java_count == 4:
                self.progressBarValue.emit(25)
            elif java_count == 5:
                self.progressBarValue.emit(50)
            elif java_count == 6:
                self.progressBarValue.emit(75)
            elif java_count == 7:
                self.progressBarValue.emit(100)
        self.buttonStart.emit()
        self.workStatus.emit('已完成')
        self.quit()


class Checker(QThread):
    choice = []
    result = {}

    progressBarValue = pyqtSignal(int)  # 更新进度条
    workStatus = pyqtSignal(str)  # 设置工作状态
    workItem = pyqtSignal(str)  # 设置工作项
    buttonStop = pyqtSignal()  # 禁用所有按钮
    buttonStart = pyqtSignal()  # 启用所有按钮
    resultDict = pyqtSignal(dict)  # 获得检测结果字典

    def __init__(self, alg):
        super(Checker, self).__init__()
        self.choice = alg

    def run(self):
        self.workStatus.emit('正在进行')
        self.workItem.emit('代码相似度检测')
        self.progressBarValue.emit(0)
        self.buttonStop.emit()

        self.result = {}

        if self.choice:
            self.database = ag.get_databasebylist(in_filename_dc)

        if 'a' in self.choice:
            dict_a = ag.get_simhash_similarity(self.database)
            print(dict_a)
            self.result['a'] = dict_a
        self.progressBarValue.emit(25)
        if 'b' in self.choice:
            dict_b = ag.get_TFIDF_cosine(self.database)
            print(dict_b)
            self.result['b'] = dict_b
        self.progressBarValue.emit(50)
        if 'c' in self.choice:
            dict_c = ag.get_SparseMS(self.database)
            print(dict_c)
            self.result['c'] = dict_c
        self.progressBarValue.emit(75)
        if 'd' in self.choice:
            dict_d = ag.get_KgramHashim(5, 4, 3, self.database)
            print(dict_d)
            self.result['d'] = dict_d
        self.progressBarValue.emit(100)
        self.resultDict.emit(self.result)
        self.buttonStart.emit()
        self.workStatus.emit('已完成')
        self.quit()


# 程序入口
if __name__ == '__main__':
    app = QApplication(sys.argv)
    s = Start()
    s.show()
    sys.exit(app.exec_())
