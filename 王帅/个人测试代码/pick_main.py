import os
import sys
import os.path
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import pick_ui
import pick_method

class Start(QMainWindow, pick_ui.Ui_MainWindow):

    in_filename = []      #待处理文件
    out_filename =  []    #输出文件（名）
    num = 0               # 文件个数

    def __init__(self):
        QMainWindow.__init__(self)
        pick_ui.Ui_MainWindow.__init__(self)
        self.setupUi(self)

        # 设置按钮的事件监听
        self.in_pick.clicked.connect(self.pick_in)
        self.out_pick.clicked.connect(self.pick_out)
        self.submit.clicked.connect(self.submit_main)

    # 选择输入路径
    def pick_in(self):
        filenames, filetype = QtWidgets.QFileDialog.getOpenFileNames(self, "选取文件", os.getcwd(),
                                        "Word Files(*.docx *.doc);;PDF Files(*.pdf);;JPG Files(*.jpeg *.jpg *jfif);;PNG Files(*.png)")

        self.in_text.setText(filenames[0]+"...")

        global in_filename
        in_filename = []
        global in_filetype

        global num
        num = 0
        while num < len(filenames):
            in_filename.append(filenames[num])
            num = num + 1

        in_filetype = filetype

    # 选择输出路径
    def pick_out(self):
        global filepath
        filepath = QtWidgets.QFileDialog.getExistingDirectory(self, "选择目录", os.getcwd())
        self.out_text.setText(filepath+"/")

        global out_filename    # 正文txt
        out_filename = []

        if in_filetype == 'Word Files(*.docx *.doc)':
            t = 0
            while t < num:
                s = in_filename[t]
                temp = Start.set_out_file_name(s)
                out_filename.append(filepath + '/' + temp + '.txt')
                t = t + 1

        elif in_filetype == 'JPG Files(*.jpeg *.jpg *jfif)':
            t = 0
            while t < num:
                s = in_filename[t]
                temp = Start.set_out_file_name(s)
                out_filename.append(filepath + '/' + temp + '.txt')
                t = t + 1

    # 提交，生成结果
    def submit_main(self):
        # 如果没有选择文件，弹出提示框
        if (in_filename==0):
            print("if")
            msg_box = QMessageBox(QMessageBox.Warning, '出错', '请选择文件')
            msg_box.exec_()

        # 如果选择了文件
        else:

            if in_filetype == 'Word Files(*.docx *.doc)':

                for i in range(0, len(in_filename)):
                    pick_method.for_docx(in_filename[i], out_filename[i])
                    pick_method.get_pictures(in_filename[i], filepath)

                msg_box = QMessageBox(QMessageBox.Warning, '成功', '文件已输出')
                msg_box.exec_()


            elif in_filetype == 'JPG Files(*.jpeg *.jpg *jfif)':
                for i in range(0, len(in_filename)):
                    pick_method.for_picture(in_filename[i], out_filename[i])

                msg_box = QMessageBox(QMessageBox.Warning, '成功', '文件已输出')
                msg_box.exec_()

            print("complete")


    # 返回不含后缀的文件名
    def set_out_file_name(s):
        index_head = s.rfind("/")
        index_hail = s.rfind(".")
        result = s[index_head + 1:index_hail]
        return result


# 程序入口
if __name__ == '__main__':
    app = QApplication(sys.argv)
    s = Start()
    s.show()
    sys.exit(app.exec_())
