
import json
import os
import tornado.web
import tornado.httpserver
from pymongo import Connection

import conf
    

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", HomeHandler),
            (r"/report/abstract", AbstractHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
            cookie_secret="GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__", #TODO
            debug=True,
        )
        super(Application, self).__init__(handlers, **settings)
        connection = Connection(conf.MONGODB_SERVER, conf.MONGODB_PORT)
        self.db = connection[conf.MONGODB_DB]


class BaseHandler(tornado.web.RequestHandler):
    
    @property
    def db(self):
        return self.application.db


class HomeHandler(BaseHandler):
    def get(self):
        self.write("Welcome to gtja report website.")


class AbstractHandler(BaseHandler):
    
    @property
    def collection(self):
        return self.db[conf.MONGODB_COLLECTION_REPORT_ABSTRACT]
    
    def get(self):
        item = self.collection.find_one({"url":"http://www.gtja.com/fyInfo/contentForJunhong.jsp?id=694164"})
        if item is None:
            result = {}
        else:
            result = {
                "title":item["title"],
                "date":str(item["date"]),
                "abstract":item["abstract"],
                "url":item["url"],
            }
        self.write(json.dumps(result))


def make_app():
    return Application()

def main():
    app = make_app()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(conf.SERVER_PORT)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
