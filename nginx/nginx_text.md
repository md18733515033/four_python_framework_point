## 安装: sudo apt-get install nginx

## 相关程序及文件路径
    - 程序文件: 放在/usr/sbin/nginx
    - 全局配置文件: /etc/nginx/nginx.conf
    - 访问日志文件: /var/log/nginx/access.log
    - 错误日志文件: /var/log/nginx/error.log
    - 站点配置文件: /etc/nginx/sites-enabled/default

## 启动命令
    - 启动nginx服务器: sudo service nginx start
    - 停止nginx服务器: sudo service nginx stop 
    - 查看nginx状态: sudo service nginx status
    - 重启nginx服务器: sudo service nginx restart

## Nginx配置文件   (/etc/nginx/nginx.conf)
```
user www-data;         ## 定义运行nginx的用户
worker_processes auto;  ## nginx进程数 应设置与系统cpu相等的数值
work_rlimit_nofile 65535;  ## 每个nginx进程可以打开的最大文件数
pid /run/nginx.pid;
include /etc/nginx/modules-enabled/*.conf;

events {
	worker_connections 768;  ## 每个nginx进程允许的最大的客户端连接数
	# multi_accept on;       ## 在nginx接到一个新连接通知后调用accept()来接受尽量多的连接
}

http {

	##
	# Basic Settings
	##

	sendfile on;                  ## 是否允许文件上传
    client_header_buffer_size 32k;     ## 上传文件大小限制
	tcp_nopush on;                 ## 防止网络阻塞
	tcp_nodelay on;                ## 防止网络阻塞
	keepalive_timeout 65;          ## 允许客户端长连接的最大秒数
	types_hash_max_size 2048;      ## nginx散列表大小,本值越大,占用的内存空间越大,但路由速度越快
	# server_tokens off;

	# server_names_hash_bucket_size 64;
	# server_name_in_redirect off;

	include /etc/nginx/mime.types;
	default_type application/octet-stream;

	##
	# SSL Settings
	##

	ssl_protocols TLSv1 TLSv1.1 TLSv1.2; # Dropping SSLv3, ref: POODLE
	ssl_prefer_server_ciphers on;

	##
	# Logging Settings
	##

	access_log /var/log/nginx/access.log;     ## 访问日志文件路径名
	error_log /var/log/nginx/error.log;       ## 错误日志文件路径名

	##
	# Gzip Settings
	##

	gzip on;

	# gzip_vary on;
	# gzip_proxied any;
	# gzip_comp_level 6;
	# gzip_buffers 16 8k;
	# gzip_http_version 1.1;
	# gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

	##
	# Virtual Host Configs
	##

	include /etc/nginx/conf.d/*.conf;     ## 加载站点配置文件
	include /etc/nginx/sites-enabled/*;    ## 加载站点配置文件
}

server {
	listen 80;             ## 配置站点监听的端口
	listen [::]:80;

	server_name example.com;  ## 站点监听的IP地址,默认的localhost只可用于本机访问,一般需要讲其更改为真实的IP

	root /var/www/example.com;  ## 配置HTTP根页面目录
	index index.html;           ## 配置HTTP根目录中的默认页面
    
    ##  location用于配置url的转发接口
	location /user/ {
        proxy_pass http://127.0.0.1:8080    ## 此处配置http://server_name/user/的转发地址
		try_files $uri $uri/ =404;
	}
    error_page 404 /404.html   ## 错误页面配置,如下配置定义HTTP 404 错误的显示页面为/404.html
}

#mail {
#	# See sample authentication script at:
#	# http://wiki.nginx.org/ImapAuthenticateWithApachePhpScript
# 
#	# auth_http localhost/auth.php;
#	# pop3_capabilities "TOP" "USER";
#	# imap_capabilities "IMAP4rev1" "UIDPLUS";
# 
#	server {
#		listen     localhost:110;
#		protocol   pop3;
#		proxy      on;
#	}
# 
#	server {
#		listen     localhost:143;
#		protocol   imap;
#		proxy      on;
#	}
#}
```