import asyncio
import threading
import time

import tornado.web
import tornado.gen
import tornado.websocket
import tornado.ioloop

from tornado.options import define, options, parse_command_line

define("port", default=8888, help="run on the given port", type=int)

# 用来保存客户端的字典
clients = dict()


class IndexHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        self.render("websocket.html")


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self, *args):
        """有新链接的时候被调用"""
        self.id = self.get_argument("ID")
        self.stream.set_nodelay(True)
        clients[self.id] = {"id": self.id, "object": self}

    def on_message(self, message):
        """
        收到消息的时候被调用
        """
        print("Client %s received a message : %s" % (self.id, message))

    def on_close(self):
        """关闭连接时调用"""
        if self.id in clients:
            del clients[self.id]
            print("Client %s is closed" % (self.id))

    def check_origin(self, origin):
        """返回True允许所有的连接,返回False所有请求返回403"""
        return True


app = tornado.web.Application([
    (r'/', IndexHandler),
    (r'/websocket', WebSocketHandler),
])


def send_time():
    """启动单独的线程运行此函数,每隔1s向所有的客户端推送当前时间"""
    import datetime
    # 启动一个异步的事件
    asyncio.set_event_loop(asyncio.new_event_loop())
    while True:
        for key in clients.keys():
            msg = str(datetime.datetime.now())
            clients[key]["object"].write_message(msg)
            print("write to client %s: %s" % (key, msg))
        time.sleep(5)


if __name__ == '__main__':
    # 启动推送时间线程
    threading.Thread(target=send_time).start()
    parse_command_line()
    app.listen(options.port)
    # 挂起运行
    tornado.ioloop.IOLoop.instance().start()
