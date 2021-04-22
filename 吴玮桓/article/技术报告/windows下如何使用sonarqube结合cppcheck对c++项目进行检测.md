@[TOC](文章目录)


<hr style=" border:solid; width:100px; height:1px;" color=#000000 size=1">

# 背景
SonarQube的默认C/C++插件CFamily是收费的，而sonarqube只能检测java和一些web项目的问题，没有办法检测C++项目

# 工具的准备
1.sonarqube+sonar-scanner：可以去查看我之前写的试用的过程，[点击这里](https://blog.csdn.net/qq_43958699/article/details/114710092).
2.cppcheck：[https://sourceforge.net/projects/cppcheck/](https://sourceforge.net/projects/cppcheck/)

# 安装教程
## 1.配置cppcheck
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210422003652202.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQzOTU4Njk5,size_16,color_FFFFFF,t_70)然后测试一下
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210422003758898.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQzOTU4Njk5,size_16,color_FFFFFF,t_70)

## 1.插件cxx
虽然说sonar的C++是收费的，但是有个作者自己写了个开源的cxx插件
下载地址：[https://github.com/SonarOpenCommunity/sonar-cxx/releases](https://github.com/SonarOpenCommunity/sonar-cxx/releases)
下完后放到sonarqube的/extensions/plugins目录下

## 2.配置代码规则
登录：[localhost:9000](localhost:9000) ，然后点击代码规则，可以看到C++(Community)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210422002255339.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQzOTU4Njk5,size_16,color_FFFFFF,t_70)
## 3.质量配置
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210422002629619.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQzOTU4Njk5,size_16,color_FFFFFF,t_70)
## 4.激活规则
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210422002702324.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQzOTU4Njk5,size_16,color_FFFFFF,t_70)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210422002714699.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQzOTU4Njk5,size_16,color_FFFFFF,t_70)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210422002721675.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQzOTU4Njk5,size_16,color_FFFFFF,t_70)












# 问题
现在sonarqube上的规则配置已经可以了，但是测试时会发现依旧没有C++项目的对应bug，那是因为sonarqube只是读取cppcheck检测后的结果，因此我们需要写一个配置文件让sonar-scanner读取他

# 解决方案
## 1.生成配置文件
在需要分析的项目里面执行
```
cppcheck -j 1 --enable=all --xml ./* 1>cppcheck-result.xml 2>&1
```

## 2.编辑sonar-project.properties
在其中加入
```
sonar.cxx.cppcheck.reportPath=cppcheck-result.xml
soanr.cxx.includeDirectories=/
```
这是加之前的完整sonarqube配置文件
```
sonar.projectKey=项目名
sonar.projectName=项目名
sonar.projectVersion=1.0
sonar.sources=C:\\Users\\lenovo\\Desktop\\项目名
sonar.sourceEncoding=UTF-8
sonar.language=C++
```

## 3.执行sonar-scanner.bat
执行结果
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210422004611278.png)

