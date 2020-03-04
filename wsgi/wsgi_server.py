# 引入python的wsgi包
from wsgiref.simple_server import make_server
# 引入服务器端程序的代码
from .webapp import application

server = make_server('', 8080, application)
server.serve_forever()
