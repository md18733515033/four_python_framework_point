### uwsgi可以在命令行启动,也可以编写uwsgi.ini文件保存配置
    - http: 指定了监听的端口
    - wsgi-file： 指定了服务器端的程序名
    - socket： 以WSGI的Socket方式运行，并指定连接地址和端口，该Socket端口是uWSGI与其他Web服务器（nginx， apache）进行对接的方式
    - chdir： 指定uWSGI启动后的当前目录
    - processes： 指定启动服务器端程序的进程数
    - threads： 指定每个服务器端程序的线程数，即服务器端的总线程数为processes×threads
    - uid： 指定运行uWSGI的Linux用户的id
## 出错:
```
failed to open python file webapp.py
unable to load app 0 (mountpoint='') (callable not found or import error)
*** no app loaded. going in full dynamic mode *** 
```
这里运行 uwsgi uwsgi.ini命令的终端位置必须和webapp.py的路径一致,否则就会找不到该文件