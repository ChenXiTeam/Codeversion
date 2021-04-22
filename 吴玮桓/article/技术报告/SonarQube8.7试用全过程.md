


@[TOC](SonarQube8.7试用全过程)


<hr style=" border:solid; width:100px; height:1px;" color=#000000 size=1">

# SonarQube8.7下载

下载地址：[https://www.sonarqube.org/downloads/](https://www.sonarqube.org/downloads/)
下载社区版就可以了

<hr style=" border:solid; width:100px; height:1px;" color=#000000 size=1">



# SonarQube安装
下载后解压缩进入/bin，效果如下：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210312222212888.png)
说明安装成功了，这里可以选择多种操作系统



# 使用步骤
## 1.localhost:9000
这里以windows为例，进去后点击StartSonar.bat
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210317093823955.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQzOTU4Njk5,size_16,color_FFFFFF,t_70)

这样代表成功开启sonar的服务器
然后登陆localhost:9000
第一次进入的时候初始账号密码都是admin，然后他会让你修改密码，进入后的界面如下:
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210317094040207.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQzOTU4Njk5,size_16,color_FFFFFF,t_70)
## 2.修改为中文
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210317141150676.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQzOTU4Njk5,size_16,color_FFFFFF,t_70)



## 3.做好测试配置
1.新增项目
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210317094158597.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQzOTU4Njk5,size_16,color_FFFFFF,t_70)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210317135143267.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQzOTU4Njk5,size_16,color_FFFFFF,t_70)
输入项目标识和显示名
注意：这里的名称与要测试的项目名称一样！！！

2.创建令牌
可以用创建好的，也可以新创建一个令牌

3.选择构建并配置sonar-scanner
![](https://img-blog.csdnimg.cn/20210317135558487.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQzOTU4Njk5,size_16,color_FFFFFF,t_70)第一步：将下载的压缩包解压缩到任意目录；
第二步：在系统变量中配置路径
![在这里插入图片描述](https://img-blog.csdnimg.cn/2021031714070543.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQzOTU4Njk5,size_16,color_FFFFFF,t_70)新建一个sonar-scanner 在windows的bin
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210317140800467.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQzOTU4Njk5,size_16,color_FFFFFF,t_70)
第三步：测试sonar-scanner配置情况
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210317140450286.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQzOTU4Njk5,size_16,color_FFFFFF,t_70)
说明安装成功


## 4.测试项目代码
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210317141416747.png)
## 5.测试结果
![在这里插入图片描述](https://img-blog.csdnimg.cn/202103171418294.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQzOTU4Njk5,size_16,color_FFFFFF,t_70)![在这里插入图片描述](https://img-blog.csdnimg.cn/20210317141841112.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQzOTU4Njk5,size_16,color_FFFFFF,t_70)![在这里插入图片描述](https://img-blog.csdnimg.cn/20210317141920998.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQzOTU4Njk5,size_16,color_FFFFFF,t_70)





