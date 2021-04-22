

@[TOC](文章目录)


<hr style=" border:solid; width:100px; height:1px;" color=#000000 size=1">

# 前言
由于发现网上对于sonarqube的使用并不是很多尤其是api这方面，于是笔者把自己通过sonarqube的web_api对项目bug进行提取时走的一些弯路记录下来

# 一、web_api
## 1.初步感觉
虽然说sonarqube提供了web_api的库，但是他没有给调用的示例，只给了每个参数的规则和调用结果的例子，对于没用过的我来说看感觉根本就不会用

## 2.前人总结
去网上找了一些前人对于sonar api的调用方法，发现了一些总结的内容
### api的常见问题
sonar的Api一些主要问题，提前列出，避免入坑
1.sonar的api各版本差异较大，向下兼容性差
2.sonar的api不是很人性化，其Post的接口，参数不是写body中，而是写URL中。
3.当接口返回400/404时通常是你接口参数错了，并不能简单理解为接口地址不存在，而是应该先检查参数值，对api讲大概率是数据不存在

### 常用的一些api
参考文章：[https://www.136.la/nginx/show-86177.html](https://www.136.la/nginx/show-86177.html)

## 3.实例借鉴
于是我去网上找了一些相关的实例，先看到一篇文章和我在做的是类似的事情，
链接：[https://blog.csdn.net/qq_41528502/article/details/113418504](https://blog.csdn.net/qq_41528502/article/details/113418504)
他给出了一个url的参考格式
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210326214833429.png)
我尝试之后结果如下：

![在这里插入图片描述](https://img-blog.csdnimg.cn/20210326214921563.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQzOTU4Njk5,size_16,color_FFFFFF,t_70)
可惜结果并不满足需求，因为希望得到的是具体的错误描述
最后在这篇文章中找到了url的格式，链接如下：
[https://blog.csdn.net/weixin_30510153/article/details/95714914](https://blog.csdn.net/weixin_30510153/article/details/95714914)
成功后的结果：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210326215324405.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQzOTU4Njk5,size_16,color_FFFFFF,t_70)接下来只需要写个小程序获取这个数据就可以了


# 二、获得web_api数据
## 1.初步思路
一看到这个就想到python的requests爬取网页信息应该就可以了，但是写好后运行一直报错401，上网看了后说是未认证，并且如果不先登录服务器那么即使调用上面的接口也是看不到数据的，看来需要解决这个问题



## 2.解决认证问题
### 走的一点弯路
一开始自己从未接触过请求认证方面的知识，看到又说是可以通过token认证解决的，于是自己就尝试根据postman去获取sonar项目的token，在这里卡了很久都没有成功
### 解决方法：Basic Auth
发现对于部分的sonar api功能需要依靠权限使用,sonar采用的是Basic Auth,如果使用POSTMAN测试接口需要认证的sonar GET接口,可以在postman的认证里,选basic auth,然后填login和password,再发GET请求就可以了.
于是在postman中测试一下结果
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210326222435405.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQzOTU4Njk5,size_16,color_FFFFFF,t_70)
# 三、提取数据
写了个小程序打印结果
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210326223439274.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQzOTU4Njk5,size_16,color_FFFFFF,t_70)



