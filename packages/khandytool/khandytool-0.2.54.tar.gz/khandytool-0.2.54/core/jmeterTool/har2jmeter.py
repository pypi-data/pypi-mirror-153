#!/usr/bin/env python
# coding=UTF-8
import random,time
import os,sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

import json, codecs, re, argparse

from core.jmeterTool.har2jmeter_utils import loadTemplate 
import datetime, time






def har2jmeter(harfile):
    hardata = codecs.open(harfile, 'r', 'utf-8-sig').read()
    har = json.loads(hardata,encoding='utf-8-sig')
    harentries = har['log']['entries']

    urls = [urlparts2(entry['request']) for entry in harentries]
    urls = [url for url in urls if not url is None]
    # urls = [url for url in urls if targetUrl in url]
    template = loadTemplate()
    # t=datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d%H%M%S")
    curPath = os.path.abspath(os.path.dirname(__file__))
    
    fh=open('autoGen.jmx','w',encoding='utf-8')
    fh.writelines(template.render(urls=urls))
    fh.close()


# def urlparts(harrequest):
#     host_arr = [h['value'] for h in harrequest['headers'] if ('name' in h and h['name'] == 'Host')]
#     if len(host_arr) == 1:
#         host = host_arr[0]
#     else:
#         return None
#     url = harrequest['url']
#     get_parts = url.split('?')
#     if len(get_parts) > 1:
#         url = get_parts[0]
#         params = dict([p.split('=') for p in get_parts[1].split("&")])
#     else:
#         params = {}
#     pathstart = re.search(host, url).end()
#     path = url[pathstart:]
#     return {'url': url, 'host': host, 'path': path, 'params': params}

def urlparts2(harrequest):
    host_arr = [h['value'] for h in harrequest['headers'] if ('name' in h and h['name'] == 'Host')]
    if len(host_arr) == 1:
        host = host_arr[0]
    else:
        return None
    port=""
    try:
        host,port=host.split(":")
    except Exception as e:
        print(e)


    url = harrequest['url']

    get_parts = url.split('?')
    if len(get_parts) > 1:
        url = get_parts[0]
        params = dict([p.split('=') for p in get_parts[1].split("&")])
    else:
        params=dict(onlyone=harrequest['postData']['text'].replace('"',"&quot;"))
    
    # f=open('urlAndData.txt','a+',encoding='utf-8')
    # f.writelines(url+"\n")
    # f.writelines(harrequest['postData']['text']+"\n")
    # f.close()

    method=harrequest['method']

    # pathstart = re.search(host+":"+port, url).end()
    pathstart=url.find("/")
    path = url[pathstart:]
    return {'url': url, 'host': host, 'path': path, 'params': params, 'method':method,'port':port}


if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description='Python script to convert har (Http ARchive) files to jMeter load tests')
    # parser.add_argument(dest="file", help='har file to covert')
    # args = parser.parse_args()
    # har2jmeter(args.file)
    har2jmeter("bbb.har")
