#!/usr/bin/python
#coding:utf-8
import tornado.ioloop
import tornado.web
from tornado import web,gen,httpclient
import time 
import subprocess
class Handler(tornado.web.RequestHandler):
    @gen.coroutine
    def conv(self,response):
        filepath='/opt/'+str(int(time.time()))
        self.write(filepath)
        with open(filepath, 'wb') as f:
            f.write(response.body)
        convcmd=["unoconv","-f","pdf","-o",filepath+".pdf",filepath]
        subprocess.call(convcmd)
        with open(filepath+".pdf", 'rb') as f:
            res=f.read()
        self.set_header("Content-type", "application/pdf")
        self.write(res)
    @gen.coroutine
    def get(self):
        path = self.get_argument('u0')
        http = httpclient.AsyncHTTPClient()
        yield http.fetch(path,self.conv)
def make_app():
    return tornado.web.Application([
        (r"/", Handler),
    ])
if __name__ == "__main__":
    app = make_app()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.bind(888)
    http_server.start(8)
    tornado.ioloop.IOLoop.instance().start()
