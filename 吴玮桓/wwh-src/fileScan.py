import os.path
import subprocess
from os import mkdir
from subprocess import Popen
import time

import requests


# 做好扫描的配置
def scan_config(project_path, project_name, language):
    # 新建配置文件sonar-project.properties
    full_path = project_path + "\\sonar-project.properties"
    file = open(full_path, "w")
    file.write("sonar.projectKey=" + project_name + "\n")
    file.write("sonar.projectName=" + project_name + "\n")
    file.write("sonar.projectVersion=1.0" + "\n")

    project_path = project_path.replace("\\", "\ \\")
    project_path = project_path.replace(" ", "")

    file.write("sonar.sources=" + project_path + "\n")
    file.write('sonar.sourceEncoding=UTF-8' + '\n')
    if language == 'java':
        file.write("sonar.java.binaries=.\\")
    elif language == 'python':
        file.write('sonar.language=python')
    elif language == 'c++':
        file.write('sonar.language=C++' + "\n")
        file.write("sonar.cxx.cppcheck.reportPath=cppcheck-result-1.xml" + "\n")
        file.write("sonar.cxx.includeDirestories=.\\")
    else:
        print("test")
    file.close()

    # 命令行输入扫描指令


def scan_cmd(project_path, project_name, language):
    global cpp_result
    sonar_scanner_path = "/../tools/sonar-scanner-cli-4.6.0.2311-windows/sonar-scanner-4.6.0.2311-windows/bin/sonar-scanner.bat "
    cppcheck_path = "/../tools/cppcheck/cppcheck.exe"
    if language == "c++":
        cpp_result = os.system(
            'cd /d' + project_path + '&&' + os.getcwd() + cppcheck_path + ' -j 1 --enable=all --xml ./* 1>cppcheck-result-1.xml 2>&1 ')

    result = os.system(
        'cd /d ' + project_path + '&& ' + os.getcwd() + sonar_scanner_path + ' -D"sonar.login=admin" -D"sonar.password=admin1"')
    if result == 0 and cpp_result == 0:
        print("success")
    else:
        print("failure")


if __name__ == "__main__":
    project_path = input("请输入要检测项目的路径:")
    # 获得项目名称
    project_name = os.path.basename(project_path)
    language = input("请输入项目的语言：(java,c++,python)")

    scan_config(project_path, project_name, language)
    scan_cmd(project_path, project_name, language)
