### 安装OpenSSL:
- sudo apt-get install openssl
- sudo apt-get install libssl-dev
- OpenSSL命令: /usr/bin/openssl
- 配置文件: /usr/lib/ssl/*
### 生成SSL密钥和证书(生成CA证书ca.crt 服务器密钥文件server.key和服务器证书server.crt)

1. 生成CA秘钥 `openssl genrsa -out ca.key 2048`
2. 生成CA证书,days参数以天为单位设置证书的有效期.在本过程中会要求输入证书的所在地 公司名 站点名等
`openssl req -x509 -new -nodes -key ca.key -days 365 -out ca.crt`
3. 生成服务器证书RSA的密钥对
`openssl genrsa -out server.key 2048`
4. 生成服务器端证书CSR,本过程中会要求输入证书所在地 公司名 站点名
`openssl req -new -key server.key -out server.csr`
5. 生成服务器端证书ca.crt
`openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 365`


### 配置nginx https服务器
在站点配置文件/etc/nginx/site-enabled/default中添加如下,可以定义一个基于https的接口,该接口的服务端程序依旧为uWSGI接口127.0.0.1:3301
```
server {
	listen 443;

	server_name 0.0.0.0;
        ssl         on;
        ssl_certificate   /etc/nginx/ssl/server.crt;    ## 服务器证书
        ssl_certificate_key  /etc/nginx/ssl/server.key;  ## 服务器密钥的全路径文件名

	location / {
		uwsgi_pass 127.0.0.1:3301;
	}
}
```
### 访问 (通过443端口访问)

