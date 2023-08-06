import random,time
import os,sys
import platform as pf
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from time import sleep
import shutil
# print("###"+os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# print("###"+os.path.abspath(os.path.dirname(os.getcwd())))
# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# sys.path.append(os.path.abspath(os.path.dirname(os.getcwd())))
from loguru import logger
from pywebio.input import input, FLOAT,NUMBER,input_group,select, textarea,file_upload,checkbox,radio,actions
from pywebio.output import close_popup, output, put_file, put_html, put_image, put_markdown, put_text,popup,put_link,put_code,put_row,put_processbar,set_processbar,put_error,put_warning,toast,put_grid,put_button,put_table,use_scope,span,clear,remove,get_scope
from pywebio import start_server,session,platform
# from core.bladeTest.main import RemoteRunner,generateHtmlReport,running
# from core.jmeterTool.swagger2jmeter import swagger2jmeter
# from core.jmeterTool.har2jmeter import har2jmeter
# from core.xmind2excel import makeCase
# from core.utils import CFacker,getDateTime,parseJmeterXml
# from core.mqttUtil import NormalMqttGetter,NormalMqttSender
# from core.kafkaUtil import general_sender,continue_orderMsg,general_orderMsg,general_orderMsgWithFilter,kafkaFetchServerWithFilter,kafkaFetchServer
# from functools import partial
from multiprocessing import Process
import decimal,websockets,asyncio
import json
from functools import partial
from core.bladeTest.interactive_blade import oneCheck,onePageInput
from core.bladeTest.interactive_jmeter import jmeterScriptGen
from core.bladeTest.interactive_testUtil import kafkaListener,mqttListener,myFackData
from core.bladeTest.interactive_xmind import uploadXmind

def clearAndCall(func):
    # print(get_scope())
    clear('content')
    # use_scope('ROOT',clear=True)
    use_scope('main',clear=True)
    func()
    # clear(get_scope(-2))
    use_scope('main',clear=True)
@use_scope(name='main',clear=True,create_scope=True)
def myapp2():
    try:
        session.set_env(title='testToolKit')
        
        put_table([
            ['功能相关',span('高可用(主机、docker)',col=2),'自动化相关',span('数据链路检查',col=2),'测试辅助'],
            [put_button("xmind转excel", onclick=lambda: clearAndCall(uploadXmind)),
            put_button("混沌测试-交互式", onclick=lambda: clearAndCall(oneCheck)),
            put_button("混沌测试-直输式", onclick=lambda: clearAndCall(onePageInput)),
            put_button("jmeter自动化", onclick=lambda: clearAndCall(jmeterScriptGen)),
            put_button("kafka操作", onclick=lambda: clearAndCall(kafkaListener)),
            put_button("mqtt操作", onclick=lambda: clearAndCall(mqttListener)),
            put_button("测试数据",onclick=lambda: clearAndCall(myFackData))]
        ],scope='main')

    except Exception as e:
        toast(e)

# def myapp():
#     '''
#     this main function for enter the whole functions of pywebio
#     :return:
#     '''
#     session.set_env(title='testToolKit')

#     select_type = select("选择你要做的操作:",["xmind转excel","混沌测试-交互式","混沌测试-直接输入(推荐)","jmeter脚本生成","假数据构造","kafka操作","mqtt操作"])
#     try:
#         if select_type=="xmind转excel":
#             uploadXmind()
#         elif select_type=="混沌测试-交互式":
#             oneCheck()
#         elif select_type=="混沌测试-直接输入(推荐)":
#             onePageInput()
#         elif select_type=="jmeter脚本生成":
#             jmeterScriptGen()
#         elif select_type=="假数据构造":
#             myFackData()
#         elif select_type=="kafka操作":
#             kafkaListener()
#         elif select_type=="mqtt操作":
#             mqttListener()
#     except Exception as e:
#         put_text(e)



def run(portNum=8899):
    '''
    running application by command
    :param portNum:
    :return:
    '''
    userPath=os.path.expanduser('~')
    reportDir=userPath+os.sep+"report"
    if not os.path.exists(reportDir):
        os.mkdir(reportDir)
    # shutil.rmtree(reportDir)
    start_server(myapp2, port=portNum,static_dir=reportDir,cdn=False,static_hash_cache=False,reconnect_timeout=3600)
    # start_server(myapp, port=portNum)






if __name__ == '__main__':
    userPath=os.path.expanduser('~')
    reportDir=userPath+os.sep+"report"
    if not os.path.exists(reportDir):
        os.mkdir(reportDir)
    # shutil.rmtree(reportDir)
    start_server(myapp2, port=8899,static_dir=reportDir,cdn=False,static_hash_cache=False,reconnect_timeout=3600)
    # myapp2()
    # jmeterRun()
    # mqttListener()
    # print(session.info["server_host"].split(":")[0])
    # kafkaListener()
    # myFackData()
