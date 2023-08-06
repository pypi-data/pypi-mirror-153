import json
import ssl
import time
import paho.mqtt.client as mqtt

import asyncio
from Crypto.Cipher import AES
import msgpack
import base64,requests
from base64 import b64encode,b64decode
from loguru import logger
from collections import namedtuple
# from mqtt.mqtt_info import mqtt_info,mqtt_command_list_test_response
import jmespath
import threading
from concurrent.futures import ThreadPoolExecutor

import queue
msg_q=queue.Queue()


class NormalMqttGetter(object):
    def __init__(self,host,port,topic,user="",passwd="",timeout=600,qos=0):
        self.host=host
        self.port=port
        self.user=user
        self.passwd=passwd
        self.topic=topic
        self.timeout=timeout
        self.qos=qos
        self.flag=False
        # self.client=None

    def getClient(self,func):
        client = mqtt.Client()
        if self.user!="" or self.user!=None:
            client.username_pw_set(self.user, self.passwd)
        client._topic=self.topic
        client._userdata=func
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.connect(self.host,self.port)
        client.subscribe(self.topic, qos=self.qos)
        while self.flag==False:
            client.loop_forever()


    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code: " + str(rc))
        client.subscribe(self.topic)

    def on_message(self, client, userdata, msg):
        strMsg=msg.payload.decode()
        userdata(strMsg)


class NormalMqttSender(object):
    def __init__(self,host,port,topic,user="",passwd="",timeout=600,qos=0):
        self.host=host
        self.port=port
        self.user=user
        self.passwd=passwd
        self.topic=topic
        self.timeout=timeout
        self.qos=qos
        # self.msg=msg

    def getClient(self,msg):
        client = mqtt.Client()
        client.on_connect = self.on_connect
        # client.on_message = self.on_message
        client.connect(self.host, self.port, self.timeout)
        client.publish(self.topic,payload=msg)

    def on_connect(self,client, userdata, flags, rc):
        print("Connected with result code: " + str(rc))


def justPrint(str):
    print(str)

if __name__=='__main__':
    NormalMqttGetter(host='127.0.0.1',port=1883,topic='fifa').getClient(justPrint)
    # while True:
    #     time.sleep(1)
    #     NormalMqttSender(host='127.0.0.1', port=1883, timeout=600, topic='fifa').getClient(str(datetime.datetime.now()))