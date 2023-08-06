import datetime,time
import json
import threading
from kafka import KafkaConsumer,KafkaProducer
from kafka.structs import TopicPartition
from kafka.client_async import KafkaClient
from core.utils import isJson
import jmespath
import threading
from loguru import logger
import re
import websockets
import asyncio
from concurrent.futures import ThreadPoolExecutor
from collections import deque

logger.add('run_log.txt',encoding='utf-8')

class kafkaOper(object):
    '''
    main class for kafka general operator, which not tested if you are connect kafka with credentials
    '''
    def __init__(self,topic,bootstrapserver):
        self.topic=topic
        self.bootstrapserver=bootstrapserver
        self.kafkaConnection=None
    def getConsumer(self,clientid="kafkaOper",auto_offset_reset="latest",**args):
        '''
        get consumer
        :param clientid:
        :param auto_offset_reset:
        :param args:
        :return:
        '''
        self.kafkaConnection=KafkaConsumer(self.topic,bootstrap_servers=self.bootstrapserver,client_id=clientid,auto_offset_reset=auto_offset_reset)
        return self
    def getProducer(self,clientid="kafkaOper"):
        '''
        get producer
        :param clientid:
        :return:
        '''
        self.kafkaConnection=KafkaProducer(bootstrap_servers=self.bootstrapserver,client_id=clientid)
        return self
    def getSubscribe(self):
        '''
        get subscriber
        :return:
        '''
        self.kafkaConnection=KafkaConsumer(bootstrap_servers=self.bootstrapserver)
        return self
    def jsonFilter(self,allStr,pattern,key):
        '''
        filter string by json
        :param allStr: origianl string
        :param pattern: jmeshpath parttern str
        :param key: target key to match
        :return:
        '''
        if isJson(allStr.value.decode()):
            try:
            # print(flag)
                allStr = json.loads(allStr.value.decode())
                flag=jmespath.search(pattern,allStr)
                if flag==key:
                    logger.warning(f'Topic: {self.topic} 在时间：{datetime.datetime.now()}->结果匹配到: {key}了')
                    logger.info(f'Total String is: {allStr}')
                # else:
                #     logger.info(f'{allStr}')
            except Exception as e:
                logger.error('json 解析失败')
                logger.error(f'{allStr}')
        logger.error(f"{allStr} isn't a string.")

    def returnJsonFilter(self,allStr,pattern,key):
        '''
        filter string by json and return the result
        :param allStr:
        :param pattern:
        :param key:
        :return:
        '''
        if isJson(str(allStr.value.decode())):
            try:
                allStr = json.loads(allStr.value.decode())
                flag=jmespath.search(pattern,allStr)
                # print(f'flag: {flag}')
                # print(f'key: {key}')
                if flag in key:
                    return allStr
            except Exception as e:
                logger.error('json 解析失败')
                logger.error(f'{allStr}')
        else:
            logger.error(f"{allStr} isn't a string.")
            return False

    def returnRegxFilter(self,allStr,pattern, key):
        '''
        filter string by regx and return the string
        :param allStr: orignal string
        :param pattern: match parttern
        :param key: target str to match
        :return:
        '''
        try:
            allStr = allStr.value.decode()
            flag=re.compile(pattern)
            res=flag.findall(allStr)
            # print(f'res: {res}')
            # print(f'key: {key}')
            if key in "".join(res):
                return allStr
            # else:
            #     logger.info(f'{allStr}')
        except Exception as e:
            logger.error('regx 解析失败')
            logger.error(f'{allStr}') 
            return False

    def regxFilter(self,allStr,pattern, key):
        '''
        filter string by regx
        :param allStr:
        :param pattern:
        :param key:
        :return:
        '''
        try:
            allStr = allStr.value.decode()
            flag=re.compile(pattern)
            res=flag.findall(allStr)
            # print(res)
            if key in "".join(res):
                logger.warning(f'Topic: {self.topic} 在时间：{datetime.datetime.now()}->结果匹配到: {res}了')
                logger.info(f'Total String is: {allStr}')
            # else:
            #     logger.info(f'{allStr}')
        except Exception as e:
            logger.error('regx 解析失败')
            logger.error(f'{allStr}') 

    def doFileterFromComsumer(self,flag="",pattern="",matchStr="",keepListen=False,store=False):
        '''
        conbine the filter way in one function
        :param flag:
        :param pattern:
        :param matchStr:
        :param keepListen:
        :param store:
        :return:
        '''
        '''
            flag = "json"
            or
            flag ="regx"
        '''
        logger.info('Start filter....')
        resStore=[]
        for one in self.kafkaConnection:
            # print(one)
            # print(flag)
            if flag=="json":
                # logger.info(f"json {one}")
                self.jsonFilter(allStr=one,pattern=pattern,key=matchStr)
            elif flag=="regx":
                # logger.info(f"regx {one}")
                self.regxFilter(allStr=one,pattern=pattern,key=matchStr)
            elif flag=="":
                logger.warning(f'Topic: {self.topic} 在时间：{datetime.datetime.now()}->未加入匹配的消息是: {one}了')
                
    def doSendFromProducer(self,message,partition=None,key=None):
        '''
        send kafka messeage
        :param message:
        :param partition:
        :param key:
        :return:
        '''
        self.kafkaConnection.send(self.topic,value=bytes(message,encoding='utf-8'),partition=partition,key=key)

    def retrivalFixedMsg(self,interval_ms,getNum):
        '''
        get fixed number message from topic
        :param interval_ms:
        :param getNum:
        :return:
        '''
        self.kafkaConnection.subscribe(self.topic)
        # print(self.kafkaConnection.poll(timeout_ms=interval_ms,max_records=getNum,update_offsets=False).items())
        # return self.kafkaConnection.poll(timeout_ms=interval_ms,max_records=getNum,update_offsets=False).items()
        resList=[]
        while len(resList)<getNum:
            for k,v in self.kafkaConnection.poll(timeout_ms=interval_ms,max_records=getNum,update_offsets=True).items():
                # print(f"{k}--->{v}")
                for one in v:
                    # print(f"data is : {one}")
                    resList.append(one.value.decode())
            # print(len(resList))
        return resList

    def retrivalFixedMsgWithFilter(self,interval_ms,getNum,filterFlag,pattern,matchStr):
        '''
        get fixed number of message from topic with filter
        :param interval_ms:
        :param getNum:
        :param filterFlag:
        :param pattern:
        :param matchStr:
        :return:
        '''
        self.kafkaConnection.subscribe(self.topic)
        # print(self.kafkaConnection.poll(timeout_ms=interval_ms,max_records=getNum,update_offsets=False).items())
        # return self.kafkaConnection.poll(timeout_ms=interval_ms,max_records=getNum,update_offsets=False).items()
        resList=[]
        while len(resList)<getNum:
            for k,v in self.kafkaConnection.poll(timeout_ms=interval_ms,max_records=getNum,update_offsets=True).items():
                # print(f"{k}--->{v}")
                for one in v:
                    print(f"data is : {one}")
                    if filterFlag=='json':
                        try:
                            print(filterFlag)
                            allStr = json.loads(one.value.decode())
                            flag=jmespath.search(pattern,allStr)
                            if flag==matchStr:
                                print(f'got json:::{allStr}')
                                resList.append(one.value.decode())
                        except Exception as e:
                            logger.error('json 解析失败')
                            logger.error(f'{allStr}')
                    elif filterFlag=='regx':
                        try:
                            allStr = one.value.decode()
                            flag=re.compile(pattern)
                            res=flag.findall(allStr)
                            if matchStr in "".join(res):
                                resList.append(one.value.decode())
                        except Exception as e:
                            logger.error('regx 解析失败')
                            logger.error(f'{allStr}') 
            # print(len(resList))
        return resList
    
    def retrivalFlowMsg(self,flag,pattern,key):
        '''
        continue get message from topic with filter
        :param flag:
        :param pattern:
        :param key:
        :return:
        '''
        self.kafkaConnection.subscribe(self.topic)
        while True:
        # now = datetime.datetime.utcnow().isoformat() + 'Z'
            msg=self.kafkaConnection.poll(timeout_ms=0,max_records=10)
            for k,v in msg.items():
                for one in v:
                    if flag=="json":
                        yield self.returnJsonFilter(one, pattern, key)
                    elif flag=="regx":
                        yield self.returnRegxFilter(one, pattern, key)
                    else:
                        yield one.value.decode()
    
    def getStartFromTimeStamp(self,minutes=1,flag="",pattern="",key=""):
        '''search from timestamp_ms, minuts 1 means 1 mins ago'''
        print('in getFromTimeStamp')
        resList=[]
        timestamp_ms=round(datetime.datetime.timestamp(datetime.datetime.now()+datetime.timedelta(minutes=-minutes))*1000)
        print(timestamp_ms)
        try:
            # topic = 'my_favorite_topic'
            # bootstrap_servers = 'localhost:9092'
            # consumer = KafkaConsumer(topic=self.topic, bootstrap_servers=self.bootstrapserver, auto_offset_reset='earliest')
            self.getConsumer(auto_offset_reset='earliest')
            # 通过主题获取分区集
            partition_set = self.kafkaConnection.partitions_for_topic(self.topic)
            # 通过主题和分区根据时间戳获取相应的偏移量
            offsets = self.kafkaConnection.offsets_for_times({TopicPartition(self.topic, partition): timestamp_ms for partition in partition_set})
            # 手动偏移
            for partition, oat in offsets.items():
                self.kafkaConnection.seek(partition, oat.offset)

            # return consumer
            for msg in self.kafkaConnection:
                (res,origStr)=self.checkFromTimeStamp(msg, flag, pattern, key)
                if res==True:
                    self.kafkaConnection.close()
                    return True, origStr
                else:
                    return False, origStr 
                # print(msg.value.decode())
                # if searchStr in msg.value.decode():
                #     print(msg.value.decode())
                #     self.kafkaConnection.close()
                #     return True
                # yield msg.value.decode()
            #     resList.append(msg.value.decode())
            #     print(resList)
            # return resList
        except AssertionError:
            # Unassigned partition
            self.kafkaConnection.close()
            return seek_offsets_for_timestamp(timestamp)

    def checkFromTimeStamp(self,one,flag,pattern,key):
        '''check data from timestamp'''
        print('in checkFromTimeStamp')
        if flag=="json":
            if self.returnJsonFilter(one, pattern, key)!=False:
                return True, one.value.decode()
            else:
                return False, one.value.decode()
        elif flag=="regx":
            if self.returnRegxFilter(one, pattern, key)!=False:
                return True, one.value.decode()
            else:
                return False, one.value.decode()
        elif flag=="contain":
            if key in one.value.decode():
                return True, one.value.decode()

    def get_offset_time_window(self, begin_time, end_time):
        partitions_structs = []
        
        for partition_id in self.kafkaConnection.partitions_for_topic(self.topic):
            partitions_structs.append(TopicPartition(self.topic, partition_id))

        begin_search = {}
        for partition in partitions_structs:
            begin_search[partition] = begin_time if isinstance(begin_time, int) else self.__str_to_timestamp(begin_time)
        begin_offset = self.kafkaConnection.offsets_for_times(begin_search)

        end_search = {}
        for partition in partitions_structs:
            end_search[partition] = end_time if isinstance(end_time, int) else self.__str_to_timestamp(end_time)
        end_offset = self.kafkaConnection.offsets_for_times(end_search)

        for topic_partition, offset_and_timestamp in begin_offset.items():
            b_offset = 'null' if offset_and_timestamp is None else offset_and_timestamp[0]
            e_offset = 'null' if end_offset[topic_partition] is None else end_offset[topic_partition][0]
            print('Between {0} and {1}, {2} offset range = [{3}, {4}]'.format(begin_time, end_time, topic_partition,
                                                                              b_offset, e_offset))
        return topic_partition,b_offset, e_offset

    @staticmethod
    def __str_to_timestamp(timeStr, format_style='%Y-%m-%d %H:%M:%S'):
        # time_array = time.strptime(str_time, format_type)
        # return int(time.mktime(time_array)) * 1000
        datetime_obj = datetime.strptime(timeStr, format_style)
        ret_stamp = int(time.mktime(datetime_obj.timetuple()) * 1000.0 + datetime_obj.microsecond / 1000.0)
        return ret_stamp

    def kafkaMsgCompareBettwenTimeByKey(self,startTime:str,endTime:str):
        '''
        :param kafkaComsumer:
        :param startTime: '2022-03-31 19:27:05.000'
        :param endTime:'2022-03-31 19:28:33.999'
        :return:res: dict string
        '''
        from collections import deque
        res={}
        # k_in = kafkaOper(topic='tacos-kernel-driver-topic', bootstrapserver=host).getConsumer()
        par, start, end = self.kafkaConnection.get_offset_time_window(begin_time=startTime, end_time=endTime)
        self.kafkaConnection.kafkaConnection.seek(par, start)

        for msg in self.kafkaConnection.kafkaConnection:
            id=json.loads(msg.value.decode().replace("\n","").replace("\t",""))['id']
            q = deque()
            if msg.offset >= end:
                break
            else:
                if id not in res.keys():
                    q.append(msg.timestamp)
                    res[id]=q
                else:
                    q.append(msg.timestamp)
                    res[id].extend(q)
        return res


def general_orderMsg(topic,serverAndPort,interval_ms,getNum,callbackFlag=False,callbackFuc=None):
    if callbackFlag==False:
        return kafkaOper(topic,serverAndPort).getSubscribe().retrivalFixedMsg(interval_ms,getNum)
    else:
        callbackFuc(kafkaOper(topic,serverAndPort).getSubscribe().retrivalFixedMsg(interval_ms,getNum))


def general_orderMsgWithFilter(topic,serverAndPort,interval_ms,getNum,filterFlag,pattern,matchStr,callbackFlag=False,callbackFuc=None):
    if callbackFlag==False:
        return kafkaOper(topic,serverAndPort).getSubscribe().retrivalFixedMsgWithFilter(interval_ms,getNum,filterFlag,pattern,matchStr)
    else:
        callbackFuc(kafkaOper(topic,serverAndPort).getSubscribe().retrivalFixedMsgWithFilter(interval_ms,getNum,filterFlag,pattern,matchStr))

def continue_orderMsg(topic,serverAndPort,flag,pattern,key):
    yield kafkaOper(topic,serverAndPort).getSubscribe().retrivalFlowMsg(flag,pattern,key)


def continue_orderMsg2(topic,serverAndPort,flag,pattern,key):
    print(f'{topic},{serverAndPort},{flag},{pattern},{key}')
    yield kafkaOper(topic,serverAndPort).getSubscribe().retrivalFlowMsg(flag,pattern,key)


def continue_orderMultiMsg(topics=[],serverAndPorts=[],flags=[],patterns=[],keys=[]):

    if type(topics)!=list or type(serverAndPorts)!=list or type(flags)!=list or type(patterns)!=list or type(keys)!=list:
        return f'input not the type of list'

    pool=ThreadPoolExecutor(len(topics))
    all=[pool.map(continue_orderMsg2,a,b,c,d,e) for a,b,c,d,e in zip(topics,serverAndPorts,flags,patterns,keys)]
    # print(len(all))
    for ttt in all:
        print(f"ttt {ttt}")
        yield ttt






def general_sender(topic="",serverAndPort="localhost:9092",message=""):
    kafkaOper(topic,serverAndPort).getProducer().doSendFromProducer(message)

def general_listener(topic="",serverAndPort="localhost:9092",flag="",pattern="",key=""):
    kafkaOper(topic,serverAndPort).getConsumer().doFileterFromComsumer(flag,pattern,key)

def multi_topic_listener(topicList=[],serverAndPortList=[],flagList=[],patternList=[],keyList=[]):
    threadList=[]
    for one in zip(topicList,serverAndPortList,flagList,patternList,keyList):
        (a,b,c,d,e)=one
        # print(f"{a},{b},{c},{d}")
        temp=threading.Thread(target=general_listener,args=(a,b,c,d,e))
        temp.start()
        threadList.append(temp)
    for one in threadList:
        one.join()




import asyncio
import websockets
import kafka
import random
from functools import partial

async def kafkaMsgRecv(websocket=None, serverPath='0.0.0.0:9092',topic="testTopic",interval=0,nums=None):
    k_conn=kafka.KafkaConsumer(bootstrap_servers=serverPath)
    k_conn.subscribe(topic)
    while True:
        # now = datetime.datetime.utcnow().isoformat() + 'Z'
        msg=k_conn.poll(timeout_ms=interval,max_records=nums)
        for k,v in msg.items():
            for one in v:
                # print(one.value.decode())
                await websocket.send(one.value.decode())
                await asyncio.sleep(random.random() * 3)


async def kafkaMsgRecvWithFilter(websocket=None,flag="",pattern="",key="", serverPath='0.0.0.0:9092', topic="testTopic", interval=0, nums=None):
    for one in continue_orderMsg(flag=flag,pattern=pattern,key=key,topic=topic,serverAndPort=serverPath):
        for a in one:
            # print(f'a is:{a}')
            if a is not None:
                print(a)
                try:
                    await websocket.send(json.dumps(a,ensure_ascii=False))
                    await asyncio.sleep(0)
                except Exception as e:
                    print(e)
                    print(a)

async def muiltiKafkaMsgRecvWithFilter(websocket=None,flag="",pattern="",key="", serverPath='0.0.0.0:9092', topic="testTopic", interval=0, nums=None):
    for one in continue_orderMsg(flag=flag,pattern=pattern,key=key,topic=topic,serverAndPort=serverPath):
        for a in one:
            # print(f'a is:{a}')
            if a is not None:
                try:
                    await websocket.send(json.dumps(a))
                    await asyncio.sleep(0)
                except Exception as e:
                    print(e)
                    print(a)

def multi_topic_listener(topicList=[],serverAndPortList=[],flagList=[],patternList=[],keyList=[]):
    threadList=[]
    for one in zip(topicList,serverAndPortList,flagList,patternList,keyList):
        (a,b,c,d,e)=one
        # print(f"{a},{b},{c},{d}")
        temp=threading.Thread(target=general_listener,args=(a,b,c,d,e))
        temp.start()
        threadList.append(temp)
    for one in threadList:
        one.join()



def kafkaFetchServer(interval=0,nums=None,serverPath='0.0.0.0:9092',topic="testTopic",local='0.0.0.0',port=8765):
    # print(serverPath)
    newloop=asyncio.new_event_loop()
    asyncio.set_event_loop(newloop)
    loop=asyncio.get_event_loop()
    start_server = websockets.serve(partial(kafkaMsgRecv,serverPath=serverPath,topic=topic), local, port)
    loop.run_until_complete(start_server)
    loop.run_forever()

def kafkaFetchServerWithFilter(interval=0,nums=None,serverPath='0.0.0.0:9092',topic="testTopic",flag="",pattern="",key="",local='0.0.0.0',port=8765):
    # print(serverPath)
    print('in kafka fetch server with filter:'.format(flag,pattern,key,serverPath,topic))
    newloop=asyncio.new_event_loop()
    asyncio.set_event_loop(newloop)
    loop=asyncio.get_event_loop()
    start_server = websockets.serve(
        partial(kafkaMsgRecvWithFilter, flag=flag, pattern=pattern, key=key, serverPath=serverPath, topic=topic), local,port)
    loop.run_until_complete(start_server)
    loop.run_forever()


if __name__ == '__main__':
    # multi_topic_listener(topicList=['topic','topic1','topic2'],serverAndPortList=["ip:port","ip:port","ip:port"]
    # ,patternList=["json.data.id","json.data.id","json.data.id"],keyList=["assertingData1","assertingData2","assertingData3"])


    # multi_topic_listener(topicList=['testTopic'],
    # serverAndPortList=["192.168.125.145:9092"],
    # flagList=["regx"],
    # partternList=["abb(.*)bba"],
    # keyList=["555"])


    # multi_topic_listener(topicList=['iotHub','device_default_prop','device_default_state'],
    # serverAndPortList=["192.168.125.145:9092","192.168.125.145:9092","192.168.125.145:9092"],
    # flagList=["json","json","json"],
    # patternList=["payload.virDevUid","payload.virDevUid","payload.deviceId"],
    # keyList=["914959009603264531","914959009603264531","914959009603264536"])

    
    # general_listener(topic="testTopic",serverAndPort="0.0.0.0:9092",flag="",pattern="",key="")


    # kafkaFetchServer(0,None,'192.168.2.101:9092','testTopic')
    # kafkaFetchServerWithFilter(0,None,'192.168.125.145:9092','testTopic','regx',"(\d{4}-\d{02}-\d{02})",'2022-01-04')
    # kafkaFetchServerWithFilter(0, None, '192.168.2.101:9092', 'testTopic', '', "",'')

    # for one in continue_orderMsg('aaa','192.168.2.101:9092','',"",''):
    #     for a in one:
    #         print(a)



    # for one in continue_orderMultiMsg(['bbb','ccc'], ['192.168.2.101:9092','192.168.2.101:9092'], ["",""], ["",""], ["",""]):
    #     print(f"one {one}")
    #     for m in one:
    #         print(f"mmm {m}")
    #         for i in t:
    #             print(f"iii {i}")



    # general_listener(topic="testTopic",serverAndPort="192.168.125.145:9092",flag="regx",pattern=r"abb(.*)bba",key="555")
    # general_sender(topic="testTopic",serverAndPort="192.168.125.145:9092",message='{"abc":{"bcd":"555"}}')
    
    # import time
    # k=kafkaOper(topic='test2',bootstrapserver='127.0.0.1:9092')
    # print(k.getFromTimeStamp(1, flag="contain", pattern="", key="data"))

    k=kafkaOper(topic='test0330', bootstrapserver='192.168.2.103:9092').getConsumer()
    par, start, end=k.get_offset_time_window(begin_time='2022-03-30 22:30:00', end_time='2022-03-30 22:35:00')
    print(par)
    print(type(par))
    print(start)
    print(end)
    # k.kafkaConnection.assign([par])
    k.kafkaConnection.seek(par, start)
    for msg in k.kafkaConnection:
        if msg.offset > end:
            break
        else:
            print(msg.timestamp,msg.value)
    # while True:
    #     try:
    #         value_ans = k.kafkaConnection.poll(max_records=20).values()
    #         if value_ans>0:
    #             for par in value_ans:
    #                 msg_offset=int(par.offset)
    #                 msg_partition=int(par.partition)
    #                 msg_topic = str(par.topic)
    #                 if par.offset==end:
    #                     break;
    #                 message_sets += par
    #     except Exception as e:
    #         print(e)