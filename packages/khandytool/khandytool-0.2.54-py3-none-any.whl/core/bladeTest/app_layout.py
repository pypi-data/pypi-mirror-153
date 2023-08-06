import random,time
import os,sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from time import sleep
from loguru import logger
from pywebio.input import input, FLOAT,NUMBER,input_group,select, textarea,file_upload,checkbox,radio
from pywebio.output import close_popup, output, put_file, put_html, put_image, put_markdown, put_text,popup,put_link,put_code,put_row,put_grid,span,put_table,put_button
from pywebio import start_server,session,platform
from core.bladeTest.main import RemoteRunner,generateHtmlReport,running
from core.jmeterTool.swagger2jmeter import swagger2jmeter
from core.jmeterTool.har2jmeter import har2jmeter
from core.xmind2excel import makeCase
from core.utils import CFacker,getDateTime
from core.mqttUtil import NormalMqttGetter
from core.kafkaUtil import general_sender,continue_orderMsg,general_orderMsg,general_orderMsgWithFilter,kafkaFetchServerWithFilter,kafkaFetchServer
from functools import partial
from multiprocessing import Process
import decimal,websockets,asyncio
import json


put_table([
    ['操作', '内容'],
    ['xmind转excel', put_button(['xmind转excel'],onclick=abc)]
    # ['混沌测试-交互式', '<hr/>'],
    # ['混沌测试-直接输入(推荐)', put_buttons(['A', 'B'], onclick=put_text)],  
    # ['jmeter脚本生成', put_markdown('`Awesome PyWebIO!`')],
    # ['假数据构造', put_file('hello.text', b'hello world')],
    # ['kafka操作', put_table([['A', 'B'], ['C', 'D']])],
    # ['mqtt操作', put_table([['A', 'B'], ['C', 'D']])]
])

put_grid([
    [put_text('A'), put_text('B'), put_text('C')],
    [None, span(put_text('D'), col=2, row=1)],
    [put_text('E'), put_text('F'), put_text('G')],
], cell_width='100px', cell_height='100px')

