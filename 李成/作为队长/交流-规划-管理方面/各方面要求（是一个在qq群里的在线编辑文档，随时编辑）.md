# 思路整理

符号申明

粗体字内容必须实现

## 前言

以下内容基于我的角度，很大可能与实际情况不符，所以要你们自己改正。

## 基本任务

### 数据采集

1、采集一些实验报告（明确知道其中的那一些是抄袭，那一些不是（这个可以通过人工注入的方式进行产生））

2、待定

### 文本代码提取（帅哥等）

1、输入：**doc文档集合**，或者zip压缩包、**文件地址路径**（文件夹下可能有其他的文档怎么办？（不管））。

输出：字符串，或者是**txt文本文件**也可以。输出可以分开（文章+代码）

2、可以**分别提取代码**与文本

3、可以按照要求（例如：**去掉注释**，去掉变量名等相关操作）进行内容提取

建议将其写成一个方法，到时候直接调用方法即可。

4、图片识别，要求再合适的位置，不要单独拿出来。（**单独**）

5、格式规范化：包括且不限于，去掉一些文章中的标点符号（不难实现，我实现了）**去掉代码中的空行**等等（可以保留原有结构、或者直接将他们转换成一个没有空行以及空格的字符串）

6、多种文档的适应性（pdf，**doc**等等，标粗原因：在开始的时候已经吹下牛皮了）

7、待定

### 代码检测（桓哥等）

1. 输入：代码.txt等文本格式，或者字符串，或者其他（我不清楚你们的输入需要什么）

输入：项目（文件夹）的路径，里面存放一个实验全部学生的代码，语言需要一致且有正确的文件扩展名

输出：粗略的评判代码的质量，每一个文本所对应的代码质量可以评分（不难实现，百分制，减分制）输出到数据库中。

输出：现在可以输出项目中每个文件出错的行数以及错误描述，尽量实现评分机制，但可能会非常简单，比如一个bug扣1分，一个异味（代码规范）扣0.5分这样

1. 多样性：可以实现不同语言，批量的检测。

2.**多样性：这个已经可以实现**

1. 输出，错误类型（**静态错**，编译错，运行错）

3.输出：上面有说（只实现了静态错，编译以及运行错误的检测暂未实现）

4、现在还在考虑检测时服务器的运作情况以及各个工具的集成是否会导致程序过于冗杂

### 文本代码查重（me，可以来个打工仔，小丑竟是我自己，有代码量，没有代码量的人可以和我联系）

1. 输入：字符串，（或者文档地址集合）目前只有字符串。有需要可以添加，没需要暂不考虑。

输出，找到和该文档最相似的文档，然后输出相似度。也可以单独的对比才行。

2、抄袭分类：

（1）不修改								正常的方法即可解决

（2）修改注释，空白区域					可以通过一定的方法将其中的注释去掉

（3）更改变量名，方法名，类名				去掉这些名称（实现起来有一定的难度）

（4）更改变量声明的位置					算法的实现与位置无关即可

（5）更改数据类型						难以察觉

（6）更改程序语句 例如 i++ 变成 i+=1			难以察觉

（7）修改程序的控制逻辑					难以察觉

其中，如果有（6）（7），说明抄袭者对于程序是有一定的理解的。

3、对于一些阈值的处理，尽量弄完吧，可以做一个图表，然后合理的测试一些数据。对于一些实验样本的采集。

3、对内容进行分析：（防止有人挂羊头卖狗肉）

目前的一个想法是，提取文本的关键字，如果很多人的关键字一致，只有那么一两个人的关键字和整体不同，可以合理的怀疑他们有问题（存在挂羊头卖狗肉的嫌疑）。

4、基于语法树，图等进行结构性分析。

一些高级的查重方法不是基于文本的，而是基于代码逻辑结构的，语法树，程序流程图等。（暂未实现）

### 其他任务（牛哥负责，如果工作量比较大可以找团队成员做打工仔）

**前端设计**

1、风格简约大方即可

2、接口定义良好，便于实现，基本一个按钮对应一个方法（视情况而定）。

3、多线程（不能直接一个任务卡死了）

查重部分还未完成。

**数据库设计**

需要和各方沟通联系！！！

1、选择合适的数据库（Mysql等挑选合适的），自己连接测试一波**云端数据库**

2、数据库的表（个人偏见，有好的方法，以下不用采用）

（1）基本（可以多分几个不同的文件，代码的，源文件等等）



| 文件ID  | 文件路径 |
| ------- | -------- |
| varchar | varchar  |



1. 文本代码提取（王帅根据别人的要求，或者自己的需求更改一下）



| 学号ID      | 提取文件ID | 提取出的文本ID | 提取出的代码ID |
| ----------- | ---------- | -------------- | -------------- |
| varchar(12) | varchar    | varchar        | varchar        |



1. 代码检测



| 代码文件ID | 分数（百分制） |
| ---------- | -------------- |
| varchar    | varchar        |



这两个可以酌情添加



| 行数 | 错误描述 |
| ---- | -------- |
| int  | varchar  |



1. 文本代码查重



| 文本ID  | (文本ID2)与某文本的相似度>k(阈值)  多值{} |
| ------- | ----------------------------------------- |
| varchar | 类似一个人有多个电话号码                  |



**代码整合**

1、先集成一波，看看效果，所有人将自己的代码放到git里面，注意是团队的git

