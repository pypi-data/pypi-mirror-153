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
from stompest.async import Stomp
from stompest.async.listener import SubscriptionListener

user = os.getenv('ACTIVEMQ_USER') or 'admin'
password = os.getenv('ACTIVEMQ_PASSWORD') or 'password'
host_backup = os.getenv('ACTIVEMQ_HOST') or '39.108.169.211'
host1 = os.getenv('ACTIVEMQ_HOST') or '39.108.169.211'
# host_backup = os.getenv('ACTIVEMQ_HOST') or '192.168.1.188'
# host1 = os.getenv('ACTIVEMQ_HOST') or '192.168.1.188'
port = int(os.getenv('ACTIVEMQ_PORT') or 61613)
destination = sys.argv[1:2] or ['/topic/event']
destination = destination[0]

messages = 10000


class Listener(object):
    @defer.inlineCallbacks
    def run(self):
        # config = StompConfig('tcp://%s:%d' % (host1, port), login=user, passcode=password, version='1.1')

        config = StompConfig(
            'failover:(tcp://%s:%d,tcp://%s:%d)?randomize=false,startupMaxReconnectAttempts=-1,startupMaxReconnectAttempts=-1,priorityBackup=true' %
            (host1, port, host_backup, port), login=user, passcode=password, version='1.1')
        self.client = Stomp(config)
        a = yield self.client.connect(host='mybroker',headers = {"client-id":"hancheng_mac_lst"})
        print(a)
        self.count = 0
        self.start = time.time()
        print(self.start)
        self.client.subscribe(destination, listener=SubscriptionListener(self.handleFrame), headers={'ack': 'auto', 'id': 'required-for-STOMP-1.1'})
        
    @defer.inlineCallbacks
    def handleFrame(self, client, frame):
        # print(self.count)
        self.count += 1
        if self.count%10==0:
            print(self.count,frame.body)
        if self.count == messages:
            self.stop(client)
    
    @defer.inlineCallbacks
    def stop(self):
        print( 'Disconnecting. Waiting for RECEIPT frame ...',)
        yield self.client.disconnect(receipt='bye')
        print ('ok')
        
        diff = time.time() - self.start
        print ('Received %s frames in %f seconds' % (self.count, diff))
        reactor.stop()


if __name__ == '__main__':

    def aSillyBlockingMethod(x,l):
        n=0
        while 1:
            import time
            time.sleep(3)
            print(x)
            print("n",n)
            n+=1
            if n==2:
                l.stop()
            if n == 10:
                print("111")
                l.run()
                print("2222")
    from threading import Thread
    l = Listener()
    # a = Thread(target=aSillyBlockingMethod,args=["2 secodns have passed",l ])
    # a.start()
    reactor.callInThread(aSillyBlockingMethod,"2 secodns have passed", l)
    l.run()
    reactor.run()