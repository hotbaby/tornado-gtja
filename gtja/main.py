#! /usr/bin/env python
import json
import os
import tornado.web
import tornado.httpserver
from pymongo import Connection

import conf
from time import sleep

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", HomeHandler),
            (r"/report/abstract", AbstractHandler),
            (r"/report/count", AbstractCountHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            #xsrf_cookies=True,
            #cookie_secret="GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__", #TODO
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
        self.render("base.html")
        #self.write("welcome to my report website")


class AbstractHandler(BaseHandler):
    LIMIT_NUMBER = 5
    
    @property
    def collection(self):
        return self.db[conf.MONGODB_COLLECTION_REPORT_ABSTRACT]
    
    def get(self):
        cursor = self.collection.find().sort([("date", 1)]).limit(self.LIMIT_NUMBER)
        
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
        response = {
            "number_results": len(result),
            "result": result,
        }
        self.write(json.dumps(response))
        
    def post(self):

        try:
            offset = self.get_argument("offset", 0)
            limit = self.get_argument("limit", self.LIMIT_NUMBER)
        except Exception:
            response = {"error": "argument error"}
            self.write(json.dumps(response))
        
        offset = int(offset)
        limit = int(limit)
        result = []
        cursor = self.collection.find().sort([("date", 1)])
        cursor = cursor.skip(offset).limit(limit)
        I = iter(cursor)
        while(True):
            try:
                item = next(I)
                result.append({
                    "title": item["title"],
                    "date": str(item["date"]),
                    "abstract": item["abstract"],
                    "url":item["url"]
                })
            except StopIteration:
                break
            except Exception:
                break
        response = {
            "number_results": len(result),
            "result": result,
        }
        self.write(json.dumps(response))


class AbstractCountHandler(BaseHandler):
    LIMIT_NUMBER = 5
    
    @property
    def collection(self):
        return self.db[conf.MONGODB_COLLECTION_REPORT_ABSTRACT]
    
    def get(self):
        number = self.collection.find().count()
        response = {"number":number}
        self.write(json.dumps(response))


def make_app():
    return Application()

def main():
    app = make_app()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(conf.SERVER_PORT)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
