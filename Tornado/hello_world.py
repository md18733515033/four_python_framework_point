# 引入tornado的ioloop和web类,引入这两个类是tornado程序的基础
import tornado.ioloop
import tornado.web


# 实现一个web.RequestHandler子类,重载get()函数,该函数负责处理相应定位到该RequestHandler的HTTP GET请求,本例中通过简单的self.write()函数输出
class MainHandler(tornado.web.RequestHandler):
    def get(self, name):
        print(name)
        self.write("hello,world")


def make_app():
    # 返回一个Application对象,第一个参数用于定义Tornado程序的路由映射
    return tornado.web.Application([(r"/ss/([^/]+)", MainHandler)])


def main():
    app = make_app()
    # 指定监听端口
    app.listen(8888)
    # 启动IOLoop,处理客户端的请求
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
