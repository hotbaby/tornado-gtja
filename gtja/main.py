import tornado

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", HomeHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
            cookie_secret="GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__", #TODO
            debug=True,
        )
        super(Application, self).__init__(handlers, **settings)


class BaseHandler(tornado.web.RequestHandler):
    pass

class HomeHandler(BaseHandler):
    def get(self):
        self.write("Welcome to gtja report website")


def make_app():
    return Application()

def main():
    app = make_app()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(conf.SERVER_PORT)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
