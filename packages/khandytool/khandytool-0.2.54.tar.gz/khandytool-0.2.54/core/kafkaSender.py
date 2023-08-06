import sys
import os,time
# print("###"+os.path.abspath(os.path.dirname(os.path.dirname(os.getcwd()))))
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(os.getcwd())))) 

from loguru import logger
from pywebio.input import input, FLOAT,NUMBER,input_group,select, textarea,file_upload,checkbox
from pywebio.output import close_popup, output, put_file, put_html, put_image, put_markdown, put_text,popup,put_link,put_code,put_row
from pywebio import session
from pywebio import start_server
from core.bladeTest.main import RemoteRunner,generateHtmlReport,running
from core.kafkaUtil import kafkaOper,general_sender,multi_topic_listener,general_listener
import json
from core.xmind2excel import makeCase
from core.utils import swagger2jmeter,CFacker
import decimal,datetime
from random import randint



# def kafkaUi():
#     session.set_env(title='testToolKit')
#     check_data = input_group("kafka check tool",[
#             input("kafka topics", name="topic",help_text='which topic you want to send or listen'),
#             input("kafka server:port", name="address",help_text='format like 0.0.0.0:9092'),
#             input("credentials", name="credentials",help_text='password of the kafka'),
#             input("filter flag", name="flag",help_text='only allowed "json" or "regx"'),
#             input("filter pattern", name="pattern",help_text='how to find the key by this pattern'),
#             input("assert key", name="key",help_text='what key you want to find'),
#             input("messages",name="msg",help_text='fill only when you need send messages'),
#             ])
#     if check_data['msg']!="" or check_data['msg']!=None:
#         general_sender(check_data['topic'],check_data['address'],check_data['msg'])
#     else:
#         general_listener(check_data['topic'],check_data['address'],check_data['flag'],check_data['pattern'],check_data['key'])

def continueSend():
    while True:
        server="127.0.0.1:9092"
        time.sleep(5)
        num=datetime.datetime.now()
        msg={"data":{"date":"2021-01-15"}}

        general_sender('test2',server,json.dumps(msg))
        print(f"{msg} sent")
        # general_sender('vv', server, 'bbb'+str(num))
        # general_sender('dd', server, 'ccc'+str(num))

if __name__=="__main__":
    # kafkaUi()
    continueSend()