#!/usr/bin/env python
"""
Licensed to the Apache Software Foundation (ASF) under one or more
contributor license agreements.  See the NOTICE file distributed with
this work for additional information regarding copyright ownership.
The ASF licenses this file to You under the Apache License, Version 2.0
(the "License"); you may not use this file except in compliance with
the License.  You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import os
import sys
import time

from twisted.internet import defer, reactor

from stompest.config import StompConfig
from stompest.sync import Stomp

user = os.getenv('ACTIVEMQ_USER') or 'admin'
password = os.getenv('ACTIVEMQ_PASSWORD') or 'password'
host = os.getenv('ACTIVEMQ_HOST') or '127.0.0.1'
# host = os.getenv('ACTIVEMQ_HOST') or '192.168.1.188'
# host = os.getenv('ACTIVEMQ_HOST') or '39.108.169.211'
port = int(os.getenv('ACTIVEMQ_PORT') or 61613)
destination = sys.argv[1:2] or ['/topic/event']
destination = destination[0]

messages = 10000
data = 'Hello World from Python'

@defer.inlineCallbacks
def run():
    try:
        config = StompConfig('tcp://%s:%d' % (host, port), login=user, passcode=password, version='1.1')
        client = Stomp(config)
        yield client.connect(host='mybroker',headers={"client-id":"hancheng_mac_push1"})

        count = 0
        start = time.time()

        for _ in range(messages):
            _data = data + "%s" % _
            client.send(destination=destination, body=_data.encode(), headers={'persistent': 'true',"client-id":"hancheng_mac_push"})
            print(_data.encode())
            count += 1
            time.sleep(0.1)

        diff = time.time() - start
        print ('Sent %s frames in %f seconds' % (count, diff))

        yield client.disconnect(receipt='bye')
    except Exception as e:
        print(e)

if __name__ == '__main__':
    run()
    reactor.run()