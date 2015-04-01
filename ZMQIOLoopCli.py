#!/usr/bin/env python2

import os
import zmq

from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application, url
from tornado.websocket import WebSocketHandler

from zmq.eventloop import zmqstream
from zmq.eventloop import ioloop  as zmq_ioloop
zmq_ioloop.install()


class ZMQListener(object):
    def __init__(self, callback, port_sub="5999"):
        self.callback = callback
        self.port_sub = port_sub

    def connect(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect ("tcp://127.0.0.1:%s" % self.port_sub)
        self.stream = zmqstream.ZMQStream(self.socket)
        self.stream.on_recv(self.callback)

    def subscribe(self, subscription):
        self.socket.setsockopt(zmq.SUBSCRIBE, subscription)



class WebSocket(WebSocketHandler):
    def open(self):
        print "opened websocket"
        self.test()
        self.zmq_listener = ZMQListener(self.received)
        self.zmq_listener.connect()
        self.zmq_listener.subscribe("101")

    def test(self):
        testmsg = '{ "text" : "Centralize, centrailize.", "username" : "John", "avatar" : "/static/images/avatar-04.svg"}'
        self.write_message(testmsg)

    def on_message(self, message):
        print message

    def on_close(self):
        print "WebSocket closed"

    def received(self, data):
        feed_item = data[0].split("::")[1]
        self.write_message(feed_item)
        print feed_item


class MainHandler(RequestHandler):
    def get(self):
        self.render("index.html")




settings = {
  "static_path": os.path.join(os.path.dirname(__file__), "static"),
  "template_path": os.path.join(os.path.dirname(__file__), "templates"),
  }


def main():
    app = Application([
        url(r"/", MainHandler),
        url(r"/zmqwebsocket", WebSocket), 
        ], **settings)
    app.listen(8888)
    IOLoop.instance().start()


if __name__ == '__main__':
    main()