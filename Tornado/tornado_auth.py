import os

import tornado.web
import tornado.escape
import tornado.ioloop
import uuid

# 保存所有登录的Session
dict_sessions = {}


# 公共基类
class BaseHeader(tornado.web.RequestHandler):
    # 写入current_user的函数
    def get_current_user(self):
        if self.get_secure_cookie("session_id") is None:
            return None
        session_id = self.get_secure_cookie("session_id").decode("utf-8")
        return dict_sessions.get(session_id)


class MainHandler(BaseHeader):
    # 需要身份认证才能访问的处理器
    @tornado.web.authenticated
    def get(self):
        name = tornado.escape.xhtml_escape(self.current_user)
        self.write("hello, " + name)


class LoginHandle(BaseHeader):
    # 登录界面
    def get(self):
        self.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <form action="/login" method="post">
        Name: <input type="text" name="name">
        <input type="submit" value="sign in">
    </form>
</body>
</html>""")

    def post(self):
        if len(self.get_argument("name")) < 3:
            self.redirect("/login")
            return
        session_id = str(uuid.uuid1())
        dict_sessions[session_id] = self.get_argument("name")
        self.set_secure_cookie("session_id", session_id)
        self.redirect("/")

# debug=True 等同于同时设置了
# autoreload=True, 开启文件的自动加载
# complied_template_cache=False 开启Html等模板文件的自动加载
# static_hash_cache=False, 开启站点静态文件的自动加载
# serve_traceback=True  显示调试信息
application = tornado.web.Application(
    # 定义url映射
    [
        (r"/", MainHandler),
        (r"/login", LoginHandle),
    ],
    # 设置静态文件的路径,此处为相对路径,也可直接等于绝对路径
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    cookie_secret="SECRET_DONT_LEAK",            # Cookie加密秘钥
    login_url="/login",                           # 定义登录界面
    debug=True
)


def main():
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
