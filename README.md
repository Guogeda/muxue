# muxue
### python3.6+django2.0+xadmin+阿里云部署

* #### 项目参考教程：[百度云下载链接](https://pan.baidu.com/s/18A1k8pIigGITc-3FXAu3aQ)
* #### 项目需要准备
    * [ ] pycharm 
    * [ ] navicat
    * [ ] mysql 
    * [ ] python3.6
    * [ ] django2.0(>2.0版本会出现插件报错)

* #### 项目运行
    1. 下载到本地，然后配置自己数据库
        ```python
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': '数据库名称',
                'USER': 'root',
                'PASSWORD': '数据库密码,
                'HOST': '127.0.0.1',
                'PORT': '3306',
            },
        }
        ```
     2. 进行模型迁移

        ``` python
        python manage.py makemigrations
        python manage.py migrate
        ```
    3. 创建超级用户进入后台,默认网址127.0.0.1:8000/xadmin
   
        ```
        python manage.py createsuperuser
        ```
 * #### 项目用到的插件
    1. 验证码[django-simple-captcha](https://github.com/mbi/django-simple-captcha)
    2. 分页[django-pure-pagination](https://github.com/jamespacileo/django-pure-pagination)
    3. 后台管理[xadmin](https://github.com/sshwsfc/xadmin)
    4. 富文本编辑器[DjangoUeditor](https://github.com/twz915/DjangoUeditor3)

* #### 项目创建遇到的bug
    1.  django.db.migrations.exceptions.InconsistentMigrationHistory: Migration admin.0001_initial is applied before its dependency users.0001_initial on database 'default' [解决参考]( https://my.oschina.net/u/1446823/blog/861712)
    2.  Django在根据models生成数据库表时报 __init__() missing 1 required positional argument: 'on_delete' [解决参考](https://www.cnblogs.com/phyger/p/8035253.html)
    3.  分页时显示错误页码1与页码2的大小不一样,可能class == page的问题
        ```
        <li class="active"><a class="page" href="?page=2">2</a></li>
        <li class="active"><a href="?page=1">1</a></li>
        ```
        
   4. form 传值问题， 这里POST必须得大写 ，不然报错 Django错误：AttributeError: 'WSGIRequest' object has no attribute 'Post'
   5. Forbidden (CSRF token missing or incorrect.):.........;在csrf_token 配置的情况下，可能是 html 问题，注意url部分
   6. 关于video.js 配置问题：目前只探索到mp4 格式播放。
        ```
        <source src="{{ MEDIA_URL }}{{ video.file }}" type='video/mp4'>  ##设置文件路径上传播放
        <source src="{{ video.url }}" type='video/mp4'> ## 将文件传输到阿里云，并且开启公共读权限
        ```
    7. 关于pycharm 修改js 文件，浏览器加载失败问题，将浏览器端设置为不加载缓冲，清除浏览器缓冲，Ctrl+F5 强制刷新也可以
    8. DEBUG = False 后 解决xadmin 后台js 样式丢失 [参考解决方案](https://blog.csdn.net/SL_World/article/details/89713329)
    9. xadmin 添加插件报错，No modul named xadmin.plugs.** ,检查是不是忘记写逗号了！

#### 关于项目的阿里云部署(仅供参考)

* 第一步，在服务器安装MySQL，然后本地用Nacicat访问远程数据库。  
   1. [参考教程](https://www.cnblogs.com/xiaofanke/p/10611526.html)
   2. [安装MySQL教程](https://www.cnblogs.com/zhuyp1015/p/3561470.html)
   3. [MySQL my.cnf配置教程](https://www.cnblogs.com/EasonJim/p/7158466.html)
   4. [Mysql卸载教程](https://blog.csdn.net/w3045872817/article/details/77334886)
   
 * 期间遇到了Ubuntu python2 与 python3 的问题，顺便解决了
    1. [ubuntu python2 与 python3 默认值设置](https://blog.csdn.net/weixin_40293491/article/details/81183491)
    2. [pip3的安装与升级](https://blog.csdn.net/tiweeny/article/details/78384633)
 
 * 第二步 pycharm连接服务器并且上传文件
    1. [ssh传文件命令](https://www.jianshu.com/p/c43105320695)
    2. [pycharm 连接服务器](https://blog.csdn.net/Dengdew/article/details/92248089)
    3. 在我的电脑上配置过私钥与公钥，不用密码连接，如果用密码连接服务器可能会出现连接失败问题，可以参考配置![5a7b92cac4a10fd8f5ac2dc641d4771b.png](en-resource://database/2276:1)，最后不要忘记Mapping，不然不能上传文件。


* 第三步 重点如何配置服务器，参考

    1. [第一参考资料，按照博主顺序走一遍](
https://www.jianshu.com/p/774c92d13c7a)
    2. [第二参考博主文章](
https://www.jianshu.com/p/1b4c5e57cd92)

* #### 最后总结遇到的问题。

    1. 遇到django 执行命令后没有反应，比如`process finish with exit code 0`.遇到此错误是django有语法错误，可以使用pycharm 的查看历史，对比自己不小心修改的部分。
    2. 解决杀进程的问题，提供两个非常有用的代码
        1. ` sudo lsof -t -i tcp:8000 | xargs kill -9`杀掉占用8000端口的进程
        2. `# ps aux|grep uwsgi `查看进程uwsgi
        3. `killall -s INT /usr/local/bin/uwsgi`杀掉uwsgi 进程

    3. 在阿里云上部署Django应用后，页面403错误，始终无法加载静态文件的解决方案.
        1. 可能是项目部署在了root路径下，ngnix没有root权限，将文件移动到/srv路径下
        2. 传送门[utuntu移动文件](https://www.jianshu.com/p/9b98378c5936)
        3. [403错误解决参考文档](https://blog.csdn.net/heatdeath/article/details/70558800)


    4. 在配置成功后发现只能访问首页，其他时候显示503错误，这个时候反应为语法错误，进入uwsgi配置的log文件中，找到进程的log，找到原因为invalid request block size
        1. 解决方案，配置加载数据过少，在uwsgi.ini文件中添加`buffer-size = 8192`,大一点舒服。[点击参考博客](https://blog.csdn.net/dipolar/article/details/31736105)

    5. 错误 django.db.utils.OperationalError: (1366, "Incorrect string value: '\\xE8\\xBD\\xAE\\xE6\\x92\\xAD...' for column 'name' at row 1")
        1. [参考文档](https://blog.csdn.net/tianfs/article/details/51775051)
        2. [参考2](https://blog.csdn.net/qq_34472372/article/details/80707092)
  
    
  
