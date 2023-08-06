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


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        super(DecimalEncoder, self).default(o)

@use_scope('content',clear=True)
def myFackData():
    '''
    generate the fake data by using this app, when you test
    :return:
    '''
    
    try:
        session.set_env(title='testToolKit')
        clear('content')
        all_options={
        "city_suffix":"市，县",
        "country":"国家",
        "country_code":"国家编码",
        "district":"区",
        "latitude":"地理坐标(纬度)",
        "longitude":"地理坐标(经度)",
        "postcode":"邮编",
        "province":"省份 (zh_TW没有此方法)",
        "address":"详细地址",
        "street_address":"街道地址",
        "street_name":"街道名",
        "street_suffix":"街、路",
        "ssn":"生成身份证号",
        "bs":"随机公司服务名",
        "company":"随机公司名（长）",
        "company_prefix":"随机公司名（短）",
        "company_suffix":"公司性质",
        "credit_card_expire":"随机信用卡到期日",
        "credit_card_full":"生成完整信用卡信息",
        "credit_card_number":"信用卡号",
        "credit_card_provider":"信用卡类型",
        "credit_card_security_code":"信用卡安全码",
        "job":"随机职位",
        "first_name":"名",
        "first_name_female":"女性名",
        "first_name_male":"男性名",
        "first_romanized_name":"罗马名",
        "last_name":"姓",
        "last_name_female":"女姓",
        "last_name_male":"男姓",
        "last_romanized_name":"随机",
        "name":"随机生成全名",
        "name_female":"男性全名",
        "name_male":"女性全名",
        "romanized_name":"罗马名",
        "msisdn":"移动台国际用户识别码，即移动用户的ISDN号码",
        "phone_number":"随机生成手机号",
        "phonenumber_prefix":"随机生成手机号段",
        "ascii_company_email":"随机ASCII公司邮箱名",
        "ascii_email":"随机ASCII邮箱",
        "ascii_free_email":"二进制免费邮件",
        "ascii_safe_email":"二进制安全邮件",
        "company_email":"公司邮件",
        "email":"电子邮件",
        "free_email":"免费电子邮件",
        "free_email_domain":"免费电子邮件域名",
        "safe_email":"安全邮箱",
        "domain_name":"生成域名",
        "domain_word":"域词(即，不包含后缀)",
        "ipv4":"随机IP4地址",
        "ipv6":"随机IP6地址",
        "mac_address":"随机MAC地址",
        "tld":"网址域名后缀(.com,.net.cn,等等，不包括.)",
        "uri":"随机URI地址",
        "uri_extension":"网址文件后缀",
        "uri_page":"网址文件（不包含后缀）",
        "uri_path":"网址文件路径（不包含文件名）",
        "url":"随机URL地址",
        "user_name":"随机用户名",
        "image_url":"随机URL地址",
        "chrome":"随机生成Chrome的浏览器user_agent信息",
        "firefox":"随机生成FireFox的浏览器user_agent信息",
        "internet_explorer":"随机生成IE的浏览器user_agent信息",
        "opera":"随机生成Opera的浏览器user_agent信息",
        "safari":"随机生成Safari的浏览器user_agent信息",
        "linux_platform_token":"随机Linux信息",
        "user_agent":"随机user_agent信息",
        "file_extension":"随机文件扩展名",
        "file_name":"随机文件名（包含扩展名，不包含路径）",
        "file_path":"随机文件路径（包含文件名，扩展名）",
        "mime_type":"随机mime Type",
        "numerify":"三位随机数字",
        "random_digit":"0~9随机数",
        "random_digit_not_null":"1~9的随机数",
        "random_int":"随机数字，默认0~9999，可以通过设置min,max来设置",
        "random_number":"随机数字，参数digits设置生成的数字位数",
        "pyfloat":"left_digits=5 #生成的整数位数, right_digits=2 #生成的小数位数, positive=True #是否只有正数",
        "pyint":"随机Int数字（参考random_int=参数）",
        "pydecimal":"随机Decimal数字（参考pyfloat参数）",
        "pystr":"随机字符串",
        "random_element":"随机字母",
        "random_letter":"随机字母",
        "paragraph":"随机生成一个段落",
        "paragraphs":"随机生成多个段落，通过参数nb来控制段落数，返回数组",
        "sentence":"随机生成一句话",
        "sentences":"随机生成多句话，与段落类似",
        "text":"随机生成一篇文章（不要幻想着人工智能了，至今没完全看懂一句话是什么意思）",
        "word":"随机生成词语",
        "words":"随机生成多个词语，用法与段落，句子，类似",
        "binary":"随机生成二进制编码",
        "boolean":"True/False",
        "language_code":"随机生成两位语言编码",
        "locale":"随机生成语言/国际 信息",
        "md5":"随机生成MD5",
        "null_boolean":"NULL/True/False",
        "password":"随机生成密码,可选参数：length：密码长度；special_chars：是否能使用特殊字符；digits：是否包含数字；upper_case：是否包含大写字母；lower_case：是否包含小写字母",
        "sha1":"随机SHA1",
        "sha256":"随机SHA256",
        "uuid4":"随机UUID",
        "am_pm":"AM/PM",
        "century":"随机世纪",
        "date":"随机日期",
        "date_between":"随机生成指定范围内日期，参数：start_date，end_date取值：具体日期或者today,-30d,-30y类似",
        "date_between_dates":"随机生成指定范围内日期，用法同上",
        "date_object":"随机生产从1970-1-1到指定日期的随机日期。",
        "date_this_month":"当月",
        "date_this_year":"当年",
        "date_time":"随机生成指定时间（1970年1月1日至今）",
        "date_time_ad":"生成公元1年到现在的随机时间",
        "date_time_between":"用法同dates",
        "future_date":"未来日期",
        "future_datetime":"未来时间",
        "month":"随机月份",
        "month_name":"随机月份（英文）",
        "past_date":"随机生成已经过去的日期",
        "past_datetime":"随机生成已经过去的时间",
        "time":"随机24小时时间",
        "time_object":"随机24小时时间，time对象",
        "time_series":"随机TimeSeries对象",
        "timezone":"随机时区",
        "unix_time":"随机Unix时间",
        "year":"随机年份",
        "profile":"随机生成档案信息",
        "simple_profile":"随机生成简单档案信息",
        "currency_code":"货币编码",
        "color_name":"随机颜色名",
        "hex_color":"随机HEX颜色",
        "rgb_color":"随机RGB颜色",
        "safe_color_name":"随机安全色名",
        "safe_hex_color":"随机安全HEX颜色",
        "isbn10":"随机ISBN(10位)",
        "isbn13":"随机ISBN(13位)",
        "lexify":"替换所有问号?带有随机字母的事件"
        }
        
        num=input("生成几组数据，默认是1组", type=NUMBER, value=1)
        # print(f'num is {num}')
        myformat=radio(label='选择生成数据格式：支持csv,json',options=['csv','json'],value=['json'])
        # print(f'format is {myformat}')

        choose=checkbox(label='从下列选项中，选择你想生成的数据：',options=all_options.values())
        
        # put_row([input('自定义键值：'),checkbox(options=[''])])
        allDict={}
        for i in range(0,num):
            restDict={}
            for one in choose:
                funcName=list(all_options.keys())[list(all_options.values()).index(one)]
                restDict[one]=CFacker().get_it(funcName)
            allDict[i]=restDict
        
        # put_text(allDict)
        
        if myformat=='json':
            put_code(json.dumps(allDict,cls=DecimalEncoder, indent=4,ensure_ascii=False), language='json',rows=20) 
        elif myformat=='csv':
            outStr=""
            for k,v in allDict.items():
                for vv in v.values():
                    # print(f"vv {vv}")
                    outStr=outStr+str(vv)+","
                outStr=outStr+"\n"
                
            put_text(outStr) 
    except Exception as e:
        toast(e)
        clear('content')


@use_scope('content',clear=True)
def kafkaListener():
    '''
    to send kafka message or listener the kafka topic
    :return:
    '''
    try:
        session.set_env(title='testTools')
        clear('content')
        select_type = select("选择kafka操作:",["kafka发送消息","kafka持续接收消息"])

        if select_type=="kafka发送消息":
            data = input_group("kafka连接配置",[
                input("kafka topic，必填", name="topic"),
                input("kafka 地址，如ip:port，必填", name="address"),
                input("要发送的消息，必填",name="msg"),
                input("发送频率（秒），非必填",name="interval",value="3"),
                radio(label="持续发送",name="always",inline='true',options=('是','否'),value=('否'))
                ])
            if data['always']=="否":
                general_sender(data['topic'],data['address'],data['msg'])
                put_text('发送完成')
            elif data['always']=="是":
                counter=0
                while True:
                    counter=counter+1
                    general_sender(data['topic'],data['address'],data['msg'])
                    put_text(f"发送{counter}次, {getDateTime()}")
                    sleep(int(data['interval']))
        
        elif select_type=="kafka持续接收消息":
            # host=session.info["server_host"]
            put_text(
                "iotHub消息队列过滤，采用json方式，过滤虚拟设备号为：payload.virDevUid\n空间管理属性device_default_prop过滤，采用json方式，过滤虚拟设备号为payload.virDevUid\n空间管理状态device_default_state过滤，采用json方式，过滤实际设备号为payload.deviceId")
            data = input_group("kafka连接配置", [
                input("kafka topic，必填", name="topic",value='iotHub'),
                input("kafka 地址，如ip:port，必填", name="address",value='192.168.125.149:9092'),
                input("过滤方式，仅支持填json或regx，非必填", name="filter",value='json'),
                input("过滤表达式，json使用jmeshpath方式，regx采用abc(.*)bbb的方式，非必填", name="pattern",value="payload.name"),
                input("过滤后比对关键字，过滤后的值是否等于输入的值，非必填", name="key",value="status"),
            ])
            
            for one in continue_orderMsg(data['topic'], data['address'], data['filter'], data['pattern'], data['key']):
                for a in one:
                    if a is not None:
                        put_text(f"{getDateTime()} : {data['topic']} --> {a}")
                    # print(a)
    except Exception as e:
        toast(e)
        clear('content')


from functools import partial
def filterPrint(oriStr,tarStr):
    if tarStr in oriStr:
        put_text(getDateTime()+" "+oriStr)

@use_scope('content',clear=True)
def mqttListener():
    try:
        session.set_env(title='testTools')
        clear('content')

        select_type = select("选择mqtt服务:",["自定义发送服务","自定义接收服务","本地固定服务(待定)"])
        if select_type=="自定义接收服务":
            data = input_group("mqtt信息",[
                input("mqtt主机，必填", name="host"),
                input("mqtt端口，必填（整数）", name="port"),
                input("mqtt topic，必填",name="topic"),
                input("mqtt用户", name="user"),
                input("mqtt密码", name="passwd"),
                input("消息包含", name="filter"),
                ])
            if data['filter']=="" or data['filter']==None:
                NormalMqttGetter(host=data['host'], port=int(data['port']), topic=data['topic'],user=data['user'],passwd=data['passwd']).getClient(partial(filterPrint, tarStr=data['filter']))
            NormalMqttGetter(host=data['host'], port=int(data['port']), topic=data['topic'],user=data['user'],passwd=data['passwd']).getClient(put_text)
        elif select_type=="自定义发送服务":
            data = input_group("mqtt信息",[
                input("mqtt主机，必填", name="host"),
                input("mqtt端口，必填（整数）", name="port"),
                input("mqtt topic，必填",name="topic"),
                input("mqtt用户", name="user"),
                input("mqtt密码", name="passwd"),
                input("mqtt消息", name="msg"),
                radio(label="持续发送",name="always",inline='true',options=('是','否'),value=('否'))
                ])
            if data['always']=="否":
                NormalMqttSender(host=data['host'], port=int(data['port']), topic=data['topic'],user=data['user'],passwd=data['passwd']).getClient(data['msg'])
                put_text('发送完成')
            elif data['always']=="是":
                counter=0
                while True:
                    counter=counter+1
                    NormalMqttSender(host=data['host'], port=int(data['port']), topic=data['topic'],user=data['user'],passwd=data['passwd']).getClient(data['msg'])
                    put_text(f"发送{counter}次, {getDateTime()}")
                    sleep(int(data['interval']))
        elif select_type == "本地固定服务(待定)":
            put_text('未暴露')
        
    except Exception as e:
        toast(e)
        clear('content')





