
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
from pywebio.output import close_popup, output, put_file, put_html, put_image, put_markdown, put_text,popup,put_link,put_code,put_row,put_processbar,set_processbar,put_error,put_warning,toast,put_grid,put_button,put_table,use_scope,span,clear,remove
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
def onePageInput():
    clear('content')
    '''
    using formated json script to generate the blade test and run it
    :return:
    '''
    try:
        session.set_env(title='testToolKit')
        clear('content')
        put_markdown(r'''# 基础指令参考：
            ## blade create cpu load [flags]
                                --timeout string   设定运行时长，单位是秒，通用参数
                                --cpu-count string     指定 CPU 满载的个数
                                --cpu-list string      指定 CPU 满载的具体核，核索引从 0 开始 (0-3 or 1,3)
                                --cpu-percent string   指定 CPU 负载百分比，取值在 0-100
            ##                blade create disk burn
                                --path string      指定提升磁盘 io 的目录，会作用于其所在的磁盘上，默认值是 /
                                --read             触发提升磁盘读 IO 负载，会创建 600M 的文件用于读，销毁实验会自动删除
                                --size string      块大小, 单位是 M, 默认值是 10，一般不需要修改，除非想更大的提高 io 负载
                                --timeout string   设定运行时长，单位是秒，通用参数
                                --write            触发提升磁盘写 IO 负载，会根据块大小的值来写入一个文件，比如块大小是 10，则固定的块的数量是 100，则会创建 1000M 的文件，销毁实验会自动删除
            ##                blade create disk fill
                                --path string      需要填充的目录，默认值是 /
                                --size string      需要填充的文件大小，单位是 M，取值是整数，例如 --size 1024
                                --reserve string   保留磁盘大小，单位是MB。取值是不包含单位的正整数，例如 --reserve 1024。如果 size、percent、reserve 参数都存在，优先级是 percent > reserve > size
                                --percent string   指定磁盘使用率，取值是不带%号的正整数，例如 --percent 80
                                --retain-handle    是否保留填充
                                --timeout string   设定运行时长，单位是秒，通用参数
            ##                blade create mem load
                                --mem-percent string    内存使用率，取值是 0 到 100 的整数
                                --mode string   内存占用模式，有 ram 和 cache 两种，例如 --mode ram。ram 采用代码实现，可控制占用速率，优先推荐此模式；cache 是通过挂载tmpfs实现；默认值是 --mode cache
                                --reserve string    保留内存的大小，单位是MB，如果 mem-percent 参数存在，则优先使用 mem-percent 参数
                                --rate string 内存占用速率，单位是 MB/S，仅在 --mode ram 时生效
                                --timeout string   设定运行时长，单位是秒，通用参数
            ##                blade create network delay
                                --destination-ip string   目标 IP. 支持通过子网掩码来指定一个网段的IP地址, 例如 192.168.1.0/24. 则 192.168.1.0~192.168.1.255 都生效。你也可以指定固定的 IP，如 192.168.1.1 或者 192.168.1.1/32，也可以通过都号分隔多个参数，例如 192.168.1.1,192.168.2.1。
                                --exclude-port string     排除掉的端口，默认会忽略掉通信的对端端口，目的是保留通信可用。可以指定多个，使用逗号分隔或者连接符表示范围，例如 22,8000 或者 8000-8010。 这个参数不能与 --local-port 或者 --remote-port 参数一起使用
                                --exclude-ip string       排除受影响的 IP，支持通过子网掩码来指定一个网段的IP地址, 例如 192.168.1.0/24. 则 192.168.1.0~192.168.1.255 都生效。你也可以指定固定的 IP，如 192.168.1.1 或者 192.168.1.1/32，也可以通过都号分隔多个参数，例如 192.168.1.1,192.168.2.1。
                                --interface string        网卡设备，例如 eth0 (必要参数)
                                --local-port string       本地端口，一般是本机暴露服务的端口。可以指定多个，使用逗号分隔或者连接符表示范围，例如 80,8000-8080
                                --offset string           延迟时间上下浮动的值, 单位是毫秒
                                --remote-port string      远程端口，一般是要访问的外部暴露服务的端口。可以指定多个，使用逗号分隔或者连接符表示范围，例如 80,8000-8080
                                --time string             延迟时间，单位是毫秒 (必要参数)
                                --force                   强制覆盖已有的 tc 规则，请务必在明确之前的规则可覆盖的情况下使用
                                --ignore-peer-port        针对添加 --exclude-port 参数，报 ss 命令找不到的情况下使用，忽略排除端口
                                --timeout string          设定运行时长，单位是秒，通用参数
            ##                blade create network loss
                                --destination-ip string   目标 IP. 支持通过子网掩码来指定一个网段的IP地址, 例如 192.168.1.0/24. 则 192.168.1.0~192.168.1.255 都生效。你也可以指定固定的 IP，如 192.168.1.1 或者 192.168.1.1/32，也可以通过都号分隔多个参数，例如 192.168.1.1,192.168.2.1。
                                --exclude-port string     排除掉的端口，默认会忽略掉通信的对端端口，目的是保留通信可用。可以指定多个，使用逗号分隔或者连接符表示范围，例如 22,8000 或者 8000-8010。 这个参数不能与 --local-port 或者 --remote-port 参数一起使用
                                --exclude-ip string       排除受影响的 IP，支持通过子网掩码来指定一个网段的IP地址, 例如 192.168.1.0/24. 则 192.168.1.0~192.168.1.255 都生效。你也可以指定固定的 IP，如 192.168.1.1 或者 192.168.1.1/32，也可以通过都号分隔多个参数，例如 192.168.1.1,192.168.2.1。
                                --interface string        网卡设备，例如 eth0 (必要参数)
                                --local-port string       本地端口，一般是本机暴露服务的端口。可以指定多个，使用逗号分隔或者连接符表示范围，例如 80,8000-8080
                                --percent string          丢包百分比，取值在[0, 100]的正整数 (必要参数)
                                --remote-port string      远程端口，一般是要访问的外部暴露服务的端口。可以指定多个，使用逗号分隔或者连接符表示范围，例如 80,8000-8080
                                --force                   强制覆盖已有的 tc 规则，请务必在明确之前的规则可覆盖的情况下使用
                                --ignore-peer-port        针对添加 --exclude-port 参数，报 ss 命令找不到的情况下使用，忽略排除端口
                                --timeout string          设定运行时长，单位是秒，通用参数
            ##                blade create network occupy
                                --port string             指定被占用的端口，（必填项）
                                --force                   强制占用此端口，会将已使用此端口的进程杀掉
                                --timeout string          设定运行时长，单位是秒，通用参数
            ##                blade create process kill
                                --process string       进程关键词，会在整个命令行中查找
                                --process-cmd string   进程命令，只会在命令中查找
                                --count string      限制杀掉进程的数量，0 表示无限制
                                --signal string     指定杀进程的信号量，默认是 9，例如 --signal 15
                                --timeout string   设定运行时长，单位是秒，通用参数
            ##                blade create process stop
                                --process string       进程关键词，会在整个命令行中查找
                                --process-cmd string   进程命令，只会在命令中查找
                                --timeout string   设定运行时长，单位是秒，通用参数
            ##                blade create docker cpu
                                --blade-override           是否覆盖容器内已有的 chaosblade 工具，默认是 false，表示不覆盖，chaosblade 在容器内的部署路径为 /opt/chaosblade
                                --blade-tar-file string    指定本地 chaosblade-VERSION.tar.gz 工具包全路径，用于拷贝到容器内执行
                                --container-id string      目标容器 ID
                                --docker-endpoint string   Docker server 地址，默认为本地的 /var/run/docker.sock
            ##                blade create docker network
                                --container-id string      目标容器 ID
                                --docker-endpoint string   Docker server 地址，默认为本地的 /var/run/docker.sock
                                --image-repo string        chaosblade-tool 镜像仓库地址，默认是从 `registry.cn-hangzhou.aliyuncs.com/chaosblade`
            ##                blade create docker process
                                --blade-override           是否覆盖容器内已有的 chaosblade 工具，默认是 false，表示不覆盖，chaosblade 在容器内的部署路径为 /opt/chaosblade
                                --blade-tar-file string    指定本地 chaosblade-VERSION.tar.gz 工具包全路径，用于拷贝到容器内执行
                                --container-id string      目标容器 ID
                                --docker-endpoint string   Docker server 地址，默认为本地的 /var/run/docker.sock
            ##                blade create docker container
                                --container-id string      要删除的容器 ID
                                --docker-endpoint string   Docker server 地址，默认为本地的 /var/run/docker.sock
                                --force                    是否强制删除
            ''', lstrip=True).show()
        json_str = textarea('请输入json串',rows=30,value=r'''{
        "data":[
        {
            "description": "主机网络限制延迟查看接口响应",
            "flag":"true", 是否运行
            "type": "docker", 类型是host 或者 docker
            "host":"192.168.xxxx.xxx",
            "port": 22,
            "user":"root",
            "passwd": "xxxxxx",
            "execCommand":"blade create network delay --time 1000 --interface eth0 --local-port 18086", 需要执行的命令
            "execCommandExpect": "success", 通常为success，可以不用改
            "dockerName": "",  如果是docker需要知道docker名称，一定要是唯一标识
            "checkCommand": "", 执行命令后的检查命令，比如CPU是否达到 70%
            "checkExpect": "", 检查的期望值
            "httpCheckCommand": { 通过http的方式进行检查，以及发送的内容，目前不支持需要登录的方式，建议手动添加token到header
            "url":"http://192.168.xxxx.xxx:18086/query",
            "method":"POST",
            "header":{},
            "cookie":{},
            "params":{"q":"show databases"},
            "json":{}
            },
            "httpExpect": "results" http检查值的返回
        },{}]}''',code={
                'mode': "json",
                'theme': 'darcula'
            })
        put_code(json_str, language='json') 
        runAndGetReport(json.loads(json_str))
    except Exception as e:
        toast(e)
        clear('content')







@use_scope('content',clear=True)
def oneCheck():
    clear('content')
    '''
    using step by step way to execute blade test
    :return:
    '''
    try:
        session.set_env(title='testToolKit')
        #clear('content')
        input_data={"data":[]}
        temp_data={}
        
        go_on=True
        while go_on:
            http_check_data={}
            type_data={}

            server_data = input_group("请输入主机信息",[
            input('本次测试描述', name="description"),
            input('输入服务器IP', name="host"),
            input('输入服务器端口', name="port", type=NUMBER),
            input('输入服务器用户名', name="user"),
            input('输入服务器密码', name="passwd"),
            ])

            r=RemoteRunner(server_data["host"],server_data["port"],server_data["user"],server_data["passwd"])
            upload = select("是否已经上传chaos文件:",["是","否"])
            if upload=="否":
                popup(title="注意",content="部署命令安装中。。。")
                r.exec_cmd("cd /opt;rm -rf chaos*")
                r.upload_file("chaosblade.tar.gz", "/opt")
                r.exec_cmd('cd /opt; mkdir chaos;tar -xzvf chaosblade.tar.gz -C ./chaos;')
                r.exec_cmd('echo "export PATH=$PATH:/opt/chaos/chaosblade-1.2.0/">>~/.bashrc')
                r.exec_cmd('source ~/.bashrc')
                r.upload_file("chaosblade.tar.gz", "/opt")

            select_type = select("选择被检查类型:",["主机","docker"])

            if select_type=="主机":
                type_data["type"]="host"
                type_data["dockerName"]=""
            elif select_type=="docker":
                type_data["type"]="docker"
                type_data["dockerName"]=input("请输入docker名称", name="dockerName")
            # else:
            #     popup(title="注意",content="类型选择有误！！！")
            #     select_type=None

            chaos_data = input_group("请输入chaos命令",[
                
            input("注入命令",name="execCommand"),
            input("注入命令期望返回", name="execCommandExpect",value="success"),
            ])
            
            select_res = select("选择检查方式:",["主机命令检查","http请求检查"])

            if select_res=="主机命令检查":
                check_data = input_group("host命令检查",[
                input("检查命令", name="checkCommand"),
                input("检查命令期望返回", name="checkExpect"),
                ])
                http_check_data["httpCheckCommand"]=""
            elif select_res=="http请求检查":
                
                check_data = input_group("http检查",[
                input("http检查接口地址", name="httpCheckCommand"),
                input("http method", name="httpCheckCommand"),
                input("http header", name="httpCheckCommand"),
                input("http param", name="httpCheckCommand"),
                input("http cookie", name="httpCheckCommand"),
                input("http json", name="httpCheckCommand"),
                input("http检查期望返回", name="httpExpect"),
                ])
                http_check_data["httpCheckCommand"]=check_data
            else:
                popup(title="注意",content="检查方式选择：有误！！！")

            
            temp_data.update(server_data)
            temp_data.update(chaos_data)
            temp_data.update(check_data)
            temp_data.update(type_data)
            temp_data.update(http_check_data)
            temp_data["flag"]="true"
            input_data["data"].append(temp_data)



            popup(title="可直接忽略",content=json.dumps(input_data)) 

            go = select("是否继续输入下一个测试项:",["是","否"])
            if go=="是":
                go_on=True
            elif go=="否":
                go_on=False
                runAndGetReport(input_data)
                
    except Exception as e:
        toast(e)
        clear('content')

            

def runAndGetReport(input_data):
    clear('content')
    '''
    generate blade test report
    :param input_data:
    :return:
    '''
    session.set_env(title='testToolKit')
    popup(title="注意",content="正在运行测试。。。") 
    url=generateHtmlReport(running(jf=input_data))
    print(url)
    close_popup()
    # put_link(app='Result',new_window=True,name='Result')
    # put_html(html=open(url,encoding='utf-8').readlines())
    put_file(content=open(url,mode="rb").read(),name="result.html",label="点击下载简报")
