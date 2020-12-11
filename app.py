#!/usr/bin/python
#coding:utf-8
import tornado.ioloop
import tornado.web
from tornado import web,gen,httpclient
from tornado.options import define, options
import time 
import subprocess
import uuid 
import redis
import os
env_dist = os.environ
rds=redis.StrictRedis(host=env_dist.get('RD'),port=int(env_dist.get('RD_PORT',6379)),db=int(env_dist.get('RD_DB',0)),password=env_dist.get('RD_PW'))
define("URLDICT", default={},type=dict)
class Handler(tornado.web.RequestHandler):
    @gen.coroutine
    def conv(self,response):
        if response.error:
            with open("/opt/Error.pdf", 'rb') as f:
                res=f.read()
            options.URLDICT[self.path]="/opt/Error.pdf"
            self.set_header("Content-type", "application/pdf")
            self.write(res)
            self.finish()
	else:
            filepath='/mnt/'+uuid.uuid4().hex
            with open(filepath, 'wb') as f:
                f.write(response.body)
            convcmd=["unoconv","-f","pdf","-o",filepath+".pdf",filepath]
            subprocess.call(convcmd)
            with open(filepath+".pdf", 'rb') as f:
                res=f.read()
            rds.set(self.path,filepath+".pdf")
            self.set_header("Content-type", "application/pdf")
            self.write(res)
    @gen.coroutine
    def get(self):
        self.path = self.get_argument('u0')
	if not rds.get(self.path):
            http = httpclient.AsyncHTTPClient()
            yield http.fetch(self.path,self.conv)
	else:
            try:
                with open(rds.get(self.path),'rb') as f:
                   res=f.read()
                   self.set_header("Content-type", "application/pdf")
                   self.write(res)
            except IOError:
                print "Error: can\'t find file or read data"
                http = httpclient.AsyncHTTPClient()
                yield http.fetch(self.path,self.conv)
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
