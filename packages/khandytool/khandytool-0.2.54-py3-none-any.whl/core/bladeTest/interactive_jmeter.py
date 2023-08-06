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
import getpass



@use_scope('content',clear=True)
def jmeterRule():
    session.set_env(title='testToolKit')
    
    put_markdown(r'''
    # 使用须知：
    ## 1.从本地址下载jmeter.zip包，已经下载并支持http,jdbc,kafka,mqtt等消息的发送插件，无需再次下载
    ## 2.支持直接拷贝开发出获得的代码进行运行，如缺少maven依赖包，可以用groovy进行包依赖管理，本下载包已经加入了包管理
    ```
    引入包参考：
    @Grapes([
        @Grab(group='org.apache.kafka', module='kafka-clients', version='2.5.1'),
        @Grab(group='org.apache.kafka', module='kafka_2.13', version='2.5.1'),
        @Grab(group='com.fasterxml.jackson.core', module='jackson-core', version='2.12.3')
        ])
    ```
    ## 3.如需要使用平台运行脚本，并需要运行时修改特定的参数项，可以按照如下格式修改：
    ```
    参数名称：authDbName  值：${__P(authDbName,auth_center)} 备注：xxx
    ```
    ## 4.如果需要查看结果，需要将请求的sampler命名格式 以名称+路径的方式存储，如：
    登录/login/index
    ''', lstrip=True).show()

@use_scope('content',clear=True)
def jmeterDownload():
    session.set_env(title='testToolKit')
    # userPath=os.path.expanduser('~')
    filename='apache-jmeter-5.4.1.zip'
    libpath=sys.path
    print(f'libpath: {libpath}')
    for one in libpath:
        if one.endswith("site-packages"):
            location1Prefx=one
            print(f"location1Prefx: {location1Prefx}")
    location1=location1Prefx+os.sep+"core"+os.sep+"jmeterTool"+os.sep+"jmeterzip"+os.sep
    print(f"location1: {location1}")
    if os.path.exists(location1+filename):
        put_file(content=open(location1+filename,mode="rb").read(),name=filename,label="点击下载软件")
    else:
        jmeterzip = file_upload("如果你是管理员，上传你的jmeter压缩包，注意jmeter压缩包解压后直接可以看到bin目录，多层级可能导致运行问题",accept="*.jmx",placeholder='选择jmeter zip文件')
        scriptName="apache-jmeter-5.4.1.zip"#jmeterzip['filename']
        # user = getpass.getuser()
        # passwd = getpass.getpass("请输入您的密码:")
        open(location1+scriptName, 'wb').write(jmeterzip['content'])


@use_scope('content',clear=True)
def jmeterRun():
    '''this is using jmeter.bat or jmeter.sh to run the script you have generated and share with other'''
    session.set_env(title='testToolKit')
    clear('content')
    userPath=os.path.expanduser('~')
    resultFile=userPath+os.sep+"out.jtl"
    if os.path.exists(resultFile):
        os.remove(resultFile)

    reportDir=userPath+os.sep+"report"

    if not os.path.exists(reportDir):
        os.mkdir(reportDir)
        tmp = os.popen('chmod -R 755 '+reportDir+os.sep).readlines()
    else:
        shutil.rmtree(reportDir)
        os.mkdir(reportDir)
        tmp = os.popen('chmod -R 755 '+reportDir+os.sep).readlines()

    script_f = file_upload("上传jmx脚本文件",accept="*.jmx",placeholder='选择jmx文件')
    scriptName=script_f['filename']

    open(userPath+os.sep+scriptName, 'wb').write(script_f['content'])

    

    flag = actions('确认', ['是', '否'],
                        help_text='是否需要参数文件?')
    if flag=="是":
        while flag=="是":
            data_f = file_upload("上传脚本文件所需的数据文件",accept="*.csv",placeholder='选择csv文件')
            open(userPath+os.sep+data_f['filename'], 'wb').write(data_f['content'])
            # 简单的操作
            flag = actions('确认', ['是', '否'],
                            help_text='是否需要继续上传参数文件?')

    filename='apache-jmeter-5.4.1.zip'
    plat=pf.platform().split('-')[0]
    # location1=os.path.join(sys.exec_prefix, 'jmeterTool')+os.sep+"jmeterzip"+os.sep
    libpath=sys.path
    print(f'libpath: {libpath}')
    for one in libpath:
        if one.endswith("site-packages"):
            location1Prefx=one
            # print(location1Prefx)

    # if "core" in location1Prefx:
    #     location1=location1Prefx+os.sep+"jmeterTool"+os.sep+"jmeterzip"+os.sep
    # else:
    #     location1=location1Prefx+os.sep+"core"+os.sep+"jmeterTool"+os.sep+"jmeterzip"+os.sep
    location1=location1Prefx+os.sep+"core"+os.sep+"jmeterTool"+os.sep+"jmeterzip"+os.sep
    location=os.path.abspath(os.getcwd())+os.sep
    # print(plat)
    # print(location)
    print(f"location1: {location1}")

    if "wind" in plat.lower():
        import time
        put_processbar(label='准备中',name='bar',init=0.15,auto_close=True)
        shutil.unpack_archive(location1+filename, userPath)
        for i in range(2, 11):
            set_processbar('bar', i / 10)
            time.sleep(0.1)
    else:
        import time
        put_processbar(label='准备中',name='bar',init=0.15,auto_close=True)
        shutil.unpack_archive(location1+filename, userPath)
        for i in range(2, 11):
            set_processbar('bar', i / 10)
            time.sleep(0.1)
        tmp = os.popen('chmod -R 777 '+userPath+os.sep+"apache-jmeter-5.4.1"+os.sep).readlines()

    jmxFilePath=userPath+os.sep+scriptName
    # print(f'path: {jmxFilePath}')
    jmxParamList=parseJmeterXml(jmxFilePath)

    # print(type(jmxParamList))
    print(jmxParamList)


    if jmxParamList==False or jmxParamList==None:
        toast('jmx脚本没有参数,即将直接运行')
        runComd=userPath+os.sep+"apache-jmeter-5.4.1"+os.sep+"bin"+os.sep+"jmeter -n -t "+jmxFilePath+" "+"-l "+reportDir+os.sep+scriptName+getDateTime(format='%Y%m%d%H%M%S')+".jtl"+" -e -o "+reportDir
        # reportComd=userPath+os.sep+"apache-jmeter-5.4.1"+os.sep+"bin"+os.sep+"jmeter -g out.jtl -o "+reportDir
        print(runComd)
        # tmp = os.popen(runComd).readlines()
        
        put_processbar(label='运行中',name='bar',init=0.15,auto_close=True)
        tmp = os.popen(runComd).readlines()
        # os.popen(reportComd)
        for i in range(2, 11):
            set_processbar('bar', i / 10)
            time.sleep(0.1)
        put_text("\n".join(tmp))
    else:
        paraList=[]
        for one in jmxParamList:
            if len(one)==3:
                paraList.append(input(label=one[0]+": "+one[2], name=one[0]+str(CFacker().get_it("random_number",8)),value=one[1]))
            elif len(one)<=2:
                paraList.append(input(label=one[0]+": "+"No Desc", name=one[0]+str(CFacker().get_it("random_number",8)),value=one[1]))

        info = input_group(scriptName+": 脚本参数",paraList)

        paramStr=""
        for k, v in info.items():
            paramStr=paramStr+("-J"+k+" "+v+" ")
        # print(paramStr)

        runComd=userPath+os.sep+"apache-jmeter-5.4.1"+os.sep+"bin"+os.sep+"jmeter -n -t "+jmxFilePath+" "+paramStr+"-l "+reportDir+os.sep+scriptName+getDateTime(format='%Y%m%d%H%M%S')+".jtl"+" -e -o "+reportDir
        print(runComd)
        # reportComd=userPath+os.sep+"apache-jmeter-5.4.1"+os.sep+"bin"+os.sep+"jmeter -g out.jtl -o "+reportDir
    

        put_processbar(label='运行中',name='bar',init=0.15,auto_close=True)
        tmp = os.popen(runComd).readlines()
        # os.popen(reportComd)
        for i in range(2, 11):
            set_processbar('bar', i / 10)
            time.sleep(0.1)
        put_text("\n".join(tmp))

    # shutil.make_archive("report", "zip",reportDir)
    put_link('查看报告',url='/static/index.html',new_window=True)

@use_scope('content',clear=True)
def jmeterScriptGen():
    '''
    this just invoke the lib for generate jmeter script
    :return:
    '''
    session.set_env(title='testToolKit')
    clear('content')
    select_type = select("选择你要做的操作:",["自动化规范","标准包下载","swagger转脚本","har转脚本","自测工作台","分布式部署(未开始）","docker打包部署(未开始)","标准包添加插件(未开始)"])
    if select_type=="自动化规范":
        jmeterRule()
    elif select_type=="标准包下载":
        jmeterDownload()
    elif select_type=="swagger转脚本":
        url=input('输入swagger地址：example:http://192.168.xxx.xxx:port/space_name/v2/api-docs')
        # print(url)
        location=os.path.join(sys.exec_prefix, 'jmx')+os.sep
        # print(location)
        swagger2jmeter(url,location)
        file_location=None
        # location=os.path.abspath(os.path.dirname(__file__))+os.sep+'jmx'+os.sep
        # print(location)
        for x,y,z in os.walk(location):
            file_location=location+"".join(z)
            break
        # print(file_location)
        put_file(content=open(file_location,mode="rb").read(),name=file_location.split(os.sep)[-1],label="点击下载jmeter脚本")
        os.remove(file_location)
    elif select_type=="har转脚本":
        f = file_upload("上传har文件，可以从fidder, charlse, chrome开发者工具中导出",accept="*.har",placeholder='选择har文件')
        open('temp.har', 'wb').write(f['content'])
        har2jmeter('temp.har')
        location=os.path.abspath('.')+os.path.sep+"autoGen.jmx"
        # print(location)
        put_file(content=open(location,mode="rb").read(),name="autoGen.jmx",label="点击下载jmeter脚本")
    elif select_type=="自测工作台":
        jmeterRun()