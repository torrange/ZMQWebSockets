#!/usr/bin/env python2
import zmq
from json import loads, dumps

from time import sleep

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5999")

json_posts = open("posts.json")
posts = loads(json_posts.read())

for post in posts:
    message = '%s::%s' % ("101", dumps(post))
    print message
    socket.send(message)
    sleep(2)
