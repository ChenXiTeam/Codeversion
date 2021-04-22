




@[TOC](文章目录)

# 前言
之前做了一次通过sonar提供的web_api获取已经测试项目的数据，这次就想能不能从开始测试到显示数据都通过python程序实现，形成一个完整的事件，为接下来做准备
<hr style=" border:solid; width:100px; height:1px;" color=#000000 size=1">

# 一、打开sonar服务器
```javascript
server_path="D:\\Program Files (x86)\\sonarqube-8.7.0.41497\\sonarqube-8.7.0.41497\\bin\\windows-x86-64\\StartSonar.bat"
# 打开StartSonar.bat
p = subprocess.Popen(server_path, shell=True, stdout = subprocess.PIPE)
stdout, stderr = p.communicate()
print(server_path.returncode) # is 0 if success
if server_path.returncode == 0:
    print("server start!")
else:
    print("server stop!")
```
# 二、选择文件路径
```javascript
project_path = input("请输入要检测项目的路径:")
# 获得项目名称
project_name = os.path.basename(project_path)
```
# 三、创建配置文件
由于配置文件中的路径需要//来分割，所以先用'/ /'替代‘/’，再把空格去掉
```javascript
# 新建配置文件sonar-project.propertiesq
full_path = project_path + "\\sonar-project.properties"
file = open(full_path, "w")
file.write("sonar.projectKey=" + project_name + "\n")
file.write("sonar.projectName=" + project_name + "\n")
file.write("sonar.projectVersion=1.0" + "\n")

project_path = project_path.replace("\\", "\ \\")
project_path = project_path.replace(" ", "")

file.write("sonar.sources=" + project_path + "\n")
file.write("sonar.java.binaries=.\\")
file.close()
```
# 四、执行命令行指令
```javascript
# 命令行输入扫描指令
result = os.system('cd /d ' + project_path + '&& sonar-scanner.bat -D"sonar.projectKey='
                   + project_name + '" -D"sonar.sources=." -D"sonar.host.url=http://localhost:9000" '
                                    ' -D"sonar.login=admin" -D"sonar.password=admin1"')
if result == 0:
    print("success")
else:
    print("failure")
```

<hr style=" border:solid; width:100px; height:1px;" color=#000000 size=1">




