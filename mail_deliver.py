#!/usr/bin/env python
# coding:utf-8

import sys
import os
import re
import logging
import random

import gevent
import gevent.queue
import gevent.pywsgi
from bottle import route, app

class MailDeliver(object):
    def __init__(self, awsid, awskey):
        self.awsid = awsid
        self.awskey = awskey
        self.queue = gevent.queue.Queue()
        gevent.spawn(self.__deliver, self.queue)
    def deliver(self, item):
        self.queue.put(item)
    def __deliver(self, queue):
        need_deliver = []
        while 1:
            item = queue.get()
            need_deliver.append(item)
            if len(need_deliver) >= 20:
                gevent.spawn(self.__dodeliver, need_deliver)
                need_deliver = []
    def __dodeliver(self, need_deliver):
        print 'i begin deliver', need_deliver

mail_deliver = MailDeliver('', '')

@route('/test')
def test():
    item = random.randint(1, 100)
    mail_deliver.deliver(item)
    return 'i try deliver %d' % item

def main():
    server = gevent.pywsgi.WSGIServer(('',80), app())
    server.serve_forever()

if __name__ == '__main__':
    main()
