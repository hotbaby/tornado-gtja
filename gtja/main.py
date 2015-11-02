
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

    def set_default_handlers(self):
        pass


class HomeHandler(BaseHandler):
    def get(self):
        #self.set_header("content-type", "text/plain")
        #self.write("<p>Welcome to gtja report website..</p>")
        self.render("base.html")


class AbstractHandler(BaseHandler):
    
    @property
    def collection(self):
        return self.db[conf.MONGODB_COLLECTION_REPORT_ABSTRACT]
    
    def get(self):
        cursor = self.collection.find().limit(10)
        
        result = []
        I = iter(cursor)
        while(True):
            try:
                item = next(I)
                result.append({
                    "title":item["title"],
                    "date":str(item["date"]),
                    "abstract":item["abstract"],
                    "url":item["url"]
                })
            except StopIteration:
                break
        
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
