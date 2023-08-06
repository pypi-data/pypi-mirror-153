import random,time
import os,sys
import platform as pf
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from time import sleep
import shutil

from loguru import logger
from pywebio.input import input, FLOAT,NUMBER,input_group,select, textarea,file_upload,checkbox,radio,actions
from pywebio.output import close_popup, output, put_file, put_html, put_image, put_markdown, put_text,popup,put_link,put_code,put_row,put_processbar,set_processbar,put_error,put_warning,toast,put_grid,put_button,put_table,use_scope,span,clear,remove,get_scope
from pywebio import start_server,session,platform
from core.bladeTest.main import RemoteRunner,generateHtmlReport,running
from core.jmeterTool.swagger2jmeter import swagger2jmeter
from core.jmeterTool.har2jmeter import har2jmeter
from core.xmind2excel import makeCase
from core.utils import CFacker,getDateTime,parseJmeterXml
from core.mqttUtil import NormalMqttGetter,NormalMqttSender
from core.kafkaUtil import general_sender,continue_orderMsg,general_orderMsg,general_orderMsgWithFilter,kafkaFetchServerWithFilter,kafkaFetchServer
from functools import partial
from multiprocessing import Process
import decimal,websockets,asyncio
import json
from functools import partial

@use_scope('content',clear=True)
def uploadXmind():
    '''
    generate excel of test case from a xmind file
    :return:
    '''
    clear('content')
    
    try:
        session.set_env(title='testToolKit')
        
        # Upload a file and save to server      
        # print(os.path.abspath(os.path.dirname(__file__)))
        curPath = os.path.abspath(os.path.dirname(__file__))
        rootPath = os.path.split(curPath)[0]

        img = open(os.path.join(curPath,'xmindStructure.jpg'), 'rb').read()  
        put_image(img,scope='content')              
        f = file_upload("上传xmind文件，注意xmind节点中不要有特殊字符，空的节点使用NA标记",accept="*.xmind",placeholder='选择xmind文件')                  
        # open('asset/'+f['filename'], 'wb').write(f['content'])  
        if f:
            open('temp.xmind', 'wb').write(f['content']) 
            makeCase('temp.xmind',f"{f['filename']}_testcase.xlsx")
            location=os.path.abspath('.')+os.path.sep+f"{f['filename']}_testcase.xlsx"
            put_file(content=open(location,mode="rb").read(),name=f"{f['filename']}_testcase.xlsx",label="点击下载Excel用例")
        else:
            toast('没有上传文件')
            exit()
    except Exception as e:
        toast(e)
        clear('content')