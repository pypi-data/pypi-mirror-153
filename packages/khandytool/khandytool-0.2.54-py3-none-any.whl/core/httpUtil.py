import requests,os
from loguru import logger
from core.utils import jsonFilter,regxFilter,containFilter,findBy
from dotenv import load_dotenv, find_dotenv
load_dotenv(verbose=True)

g_exportParam={}
class HttpOper:
    def __init__(self):
        """session管理器, 后续引入登录或者token处理"""
        self.session = requests.session()
        self.res=None
        self.exportParam={}

    def call(self, method, url, params=None, data=None, json=None, headers=None, **kwargs):
        logger.info(f'url : {url}')
        self.res=self.session.request(method, url, params=params, data=data, json=json, headers=headers,**kwargs)
        return self

    def resCheck(self,flag="",pattern="",key=""):
        logger.info(f'oriStr : {self.res.text}')
        if self.res:
            if flag=='json':
                if not jsonFilter(self.res.text, flag, pattern, key)[0]:
                    return False
                return True
            if flag=="regx":
                if not regxFilter(self.res.text, flag, pattern, key)[0]:
                    return False
                return True
            if flag=="contain":
                if not containFilter(self.res.text, key)[0]:
                    return False
                return True
        else:
            logger.error('please run call() first')

    def setExportParam(self,paramName,flag="",pattern=""):
        logger.info(f'oriStr is: {self.res.text}')
        temp=findBy(self.res.text,flag=flag,pattern=pattern)
        if temp!=False:
            self.exportParam[paramName]=temp
        else:
            logger.warning(f'can not set exportParm by pattern {pattern}')
        return self

    def getRes(self):
        return self.res
    
    def getExportParam(self,key):
        return self.exportParam[key]

    def updateExportParam(self,key,value):
        self.exportParam[key]=value

    def close_session(self):
        """关闭session"""
        self.session.close()

if __name__ == '__main__':
    host=os.getenv("test_ip1")

    url = 'http://'+host+':9499/device/v1/api/devices/926499854176743469'
    header={"content-type":"application/json;charset=UTF-8"}
    req = HttpOper()

    res = req.call("get", url, headers=header).resCheck(flag="json", pattern="data.id", key="926499854176743469")
    print(res)
    res = req.call("get", url, headers=header).resCheck(flag="regx", pattern="classifyName\":\"(.*)\"", key="水冷主机")
    print(res)
    res = req.call("get", url, headers=header).resCheck(flag="contain", key="926499854176743469")
    print(res)

    res = req.call("get", url, headers=header).setExportParam('p_name','json','data.productName')
    print(res.getExportParam('p_name'))