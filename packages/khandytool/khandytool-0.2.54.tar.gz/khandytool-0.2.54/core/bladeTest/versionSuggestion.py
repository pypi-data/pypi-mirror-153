from loguru import logger
from pywebio.input import input, FLOAT,NUMBER,input_group,select
from pywebio.output import put_text
from pywebio import start_server
import os,time
from main import RemoteRunner,RunnerResult

def oneCheck():
    input_data={}
    go_on=True
    while go_on:
        server_data = input_group("禅道版本号创建向导",[
        input('产品编码，通常是英文或者拼音简称,如user_center', name='desc'),
        input('输入产品版本号，初次创建为V1.0.0', name='version'),
        ])
        desc=server_data['desc'].lower()
        version=server_data['version'].lower().strip('v')
        major,middle,miner=version.split('.')

        put_text(f'产品代号为：{desc}-V{major}00')
        put_text(f'产品计划名称为：{desc}-V{major}00R0{middle}')
        put_text(f'项目代号为：{desc}-V{major}00R0{middle}B0{miner}')

#docker run -itd -p 80:8080 6648f88023f4




if __name__ == '__main__':
    start_server(oneCheck, port=8080)



