#!/anaconda3/envs/xxx/bin python3.7
# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @File: main.py
# @Author: oupeng
# @Time: 9月 23, 2021
# ---
import json
import time
import os
from fabric import Connection,SerialGroup
from loguru import logger
from requests import session
from copy import deepcopy
import csv
logger.add('执行日志.txt',rotation="10MB",encoding='utf-8',enqueue=True)
import pytest
import traceback

from jinja2 import Environment, FileSystemLoader


# class setEnvs():
#     f=open('.env','r')
#     for one in f.readlines():
#         k,v=one.split('=')
#         os.environ[k]=v


class RunnerResult(object):
    '''
    this just for generate result for the remote executor
    '''
    def __init__(self):
        
        self.testResTemp={"testTitle":"","chaosCommand":"","chaosId":"","checkCommand":"","expectResponse":"","realResponse":"","checkStatus":""}
        self.testResList=[]
    
    def clearTemp(self):
        self.testResTemp={"testTitle":"","chaosCommand":"","chaosId":"","checkCommand":"","expectResponse":"","realResponse":"","checkStatus":""}
    
    def clearResList(self):
        self.testResList=[]

    def printResList(self):
        for one in self.testResList:
            print('####################')
            for k,v in one.items():
                print(f"{k}-->{v}")
    
    def printResultTemp(self):
        for k,v in self.testResTemp.items():
                print(f"{k}-->{v}")

    def generaterReport(self):
        pass


class RemoteRunner(object):
    '''
    run command in remote host
    '''
    def __init__(self, host, port, user, passwd):
        '''

        :param host:
        :param port:
        :param user:
        :param passwd:
        result will be store in instance res variables
        '''
        self.host = host
        self.port = port
        self.user = user
        self.passwd = {"password": passwd}
        self.conn = Connection(host=self.host, user=self.user, port=self.port, connect_kwargs=self.passwd)
        self.res=""
        self.uid=None
        self.containerList=[]
        self.commandList=None
        self.testResult=RunnerResult()
        


    def __enter__(self):
        return self
        

    def __exit__(self,exc_type,exc_val,exc_tb):
        self.conn.close()

    def upload_file(self, localFilePath, remoteFilePath):
        '''
        :param localFilePath:
        :param remoteFilePath:
        :return:
        '''
        # logger.info(f"localFilePath: {localFilePath}")
        # logger.info(f"remoteFilePath: {remoteFilePath}")
        logger.info(f"localFilePath: {localFilePath}, remoteFilePath: {remoteFilePath}")
        self.conn.put(local=localFilePath, remote=remoteFilePath)
        return self

    def download_file(self, localFilePath, remoteFilePath):
        '''

        :param localFilePath:
        :param remoteFilePath:
        :return:
        '''
        logger.info(f"localFilePath: {localFilePath}, remoteFilePath: {remoteFilePath}")
        # logger.info(f"remoteFilePath: {remoteFilePath}")
        self.conn.get(remote=remoteFilePath, local=localFilePath)
        return self


    def get_chaos_id(self):
        if "success" in self.res.stdout.strip():
            id=json.loads(self.res.stdout.strip())['result']
            print(f"chaos id: < {id} >")
            self.uid=id
            
        return self

    def exec_cmd(self, cmd):
        '''
        :param cmd: command in running on the host
        :return:
        '''
        try:
            logger.info(f"exec cmd: < {cmd} >")
            self.commandList=cmd
            res = self.conn.run(cmd)
            # logger.info(f'cmd stdout is: {res.stdout.strip()}')
            # logger.error(f'cmd stdout is: {res.stderr.strip()}')
            self.res=res
            self.get_chaos_id()
            return self
        except Exception as e:
            logger.warning(e)

    def exec_on_multi(self,*hosts,cmd):
        '''

        :param hosts: host list,contain lots of host
        :param cmd: command in running on the host
        :return:
        '''
        logger.info(f"hosts: <{hosts}>")
        logger.info(f"multi cmd: <{cmd}>")
        self.commandList=cmd
        res=SerialGroup(hosts).run(cmd)
        # logger.info(f'cmd stdout is: {res.stdout.strip()}')
        # logger.error(f'cmd stdout is: {res.stderr.strip()}')
        self.res=res
        self.get_chaos_id()
        return self

    def exec_check_by_cmd(self,cmd,expect):
        '''

        :param cmd: command
        :param expect: command expect str
        :return:
        '''
        logger.info(f"check cmd is: < {cmd} >")
        self.exec_cmd(cmd)
        stdout = self.res.stdout.strip()
        logger.info(f"checking: result is: < {stdout} >, expect is: < {expect} >")
        # assert expect in stdout
        if expect in stdout or expect < stdout:
            return True
        else:
            
            return False

    def exec_check_contain(self,expect):
        '''
        :param expect: expect str
        :return:
        '''
        stdout=self.res.stdout.strip()
        logger.info(f"checking: result is: < {stdout} >, expect is: < {expect} >")
        # assert expect in stdout
        if expect in stdout:
            # logger.info(f"expect: {expect}")
            # logger.info(f"stdout: {stdout}")
            
            return True
        
        return False

    def exec_check_equal(self,expect):
        '''

        :param expect: expect str, exactly same
        :return:
        '''
        stdout=self.res.stdout.strip()
        logger.info(f"checking: result is: < {stdout} >, expect is: < {expect} >")
        # assert expect == stdout
        if expect == stdout:
            # logger.info(f"expect: {expect}")
            # logger.info(f"stdout: {stdout}")
            
            return True
        
        return False



    def exec_check_request_response(self,httpObj,expect="",*kwargs):
        '''
        check service ok, using response code by contain
        :param url:
        :param method:
        :param data:
        :param json:
        :param expect:
        :param kwargs:
        :return:
        '''
        '''
             url_str=http://mobile.abc.org/sfsf~post~urlparams~jsonparms~headers
             http://http://192.168.118.168:21368/api-dev/terminus-security/account/login~post~ ~{"loginName":"$loginName","password":"$loginPass","businessCode":"terminus","loginType":"ACCOUNT","ticket":"7c9db59cdc189b5d56ba21bf20e355fcc30c0049","rightCode":"dfdf"}~{"Content-Type": "application/json;charset=UTF-8"}
            '''
        # logger.info(type(httpObj))
        # logger.info(httpObj)
        logger.info(f'url is {httpObj["url"]}')
        logger.info(f'method is {httpObj["method"]}')
        logger.info(f'params is {httpObj["params"]}')
        logger.info(f'jsonstr is {httpObj["json"]}')
        logger.info(f'headers is {httpObj["header"]}')
        # requestFuncStr=f"session().{method}(url='{url}',data={params},json={jsonstr})"
        start_time=time.time()
        resp = session().request(url=httpObj['url'], method=httpObj['method'], params=httpObj['params'], data=httpObj['json'], headers=httpObj['header'])
        logger.info(f"http response: < {resp.text} >")
        logger.info(f"expect string is: < {expect} >")
        end_time=time.time()
        time_spend=end_time-start_time
        logger.info(f"request spend: < {time_spend} > ")


        # print(requestFuncStr)
        if resp.status_code != 200:
            
            return False
        else:
            if expect in resp.text:
                
                return True
                # assert True
            else: 
                
                return False
                # assert False

    def prepare_blade(self):
        '''
        :return: blade binaries will be placed in /opt/chaos/chaosblade-1.2.0/, and add blade in path
        '''
        self.exec_cmd("cd /opt;rm -rf chaos*")
        self.upload_file("chaosblade.tar.gz", "/opt")
        self.exec_cmd('cd /opt; mkdir chaos;tar -xzvf chaosblade.tar.gz -C ./chaos;')
        self.exec_cmd('echo "export PATH=$PATH:/opt/chaos/chaosblade-1.2.0/">>~/.bashrc')
        self.exec_cmd('source ~/.bashrc')
        return self

    def check_blade_exist(self):
        if self.exec_cmd("echo $PATH|grep chaosblade"):
            return True
        else:
            return False


    def get_docker_id(self):
        '''
        get docker id
        :return:
        '''
        res=self.conn.run("docker ps|awk '{if (NR>2) {print $1}}'")
        self.containerList=deepcopy(res.stdout.strip().split('\n'))
        logger.info(f"container list is: < {self.containerList} >")
        return self
        # print(type(self.containerList))
        # return self.containerList

    def run_docker_cmd_by_dockerName(self,cmd,uniq_docker_name):
        '''
        run docker command by name
        :param cmd:
        :param uniq_docker_name:
        :return:
        '''
        docker_id=self.conn.run("docker ps|grep "+uniq_docker_name+"|awk '{print $1}'").stdout.strip()
        logger.info(f"docker_id is:< {docker_id}>")
        logger.info(f"docker command :< {cmd} --container-id {docker_id} > will be execute")
        self.commandList=f"{cmd} --container-id {docker_id}"
        self.res=self.conn.run(f"{cmd} --container-id {docker_id}")
        self.get_chaos_id()
        return self

    def run_docker_cmd_by_dockerId(self,cmd,docker_id):
        '''
        run docker command by id
        :param cmd:
        :param docker_id:
        :return:
        '''
        # docker_id=self.conn.run("docker ps|grep "+uniq_docker_name+"|awk '{print $1}'").stdout.strip()
        logger.info(f"docker command: <{cmd} --container-id {docker_id} > will be execute")
        self.commandList=f"{cmd} --container-id {docker_id}"
        self.res=self.conn.run(f"{cmd} --container-id {docker_id}")
        self.get_chaos_id()
        return self

    def run_docker_cmd(self,cmd):
        '''
        run docker commmand directly by writed case
        :param cmd:
        :return:
        '''
        # docker_id=self.conn.run("docker ps|grep "+uniq_docker_name+"|awk '{print $1}'").stdout.strip()
        logger.info(f"docker command: < {cmd} > will be execute")
        self.commandList=f"{cmd}"
        self.res=self.conn.run(f"{cmd}")
        self.get_chaos_id()
        return self

    def destroy_chaos(self):
        logger.info(f"id:< {self.uid} > will destroy")
        self.conn.run(f"blade destroy {self.uid}")




def running(wait=1,jf=None):
    
    resList=[]
    # logger.info(f'\n' * 5)
    # logger.info("\n开始"+f'--' * 50)
    # f=open("config.json",encoding='utf-8')
    # jf=json.load(f)
    for one in jf['data']:
        # logger.info(f'\n\n\n\n@@@读取到的任务：@@@\n:{one["description"]}')
        try:
            if one['flag'] == "true":
                
                logger.info(f'\n+++++++将执行的任务：+++++++ :\n{one["description"]}')
                host=one['host']
                port=int(one['port'])
                user=one['user']
                passwd=one['passwd']

                r = RemoteRunner(host, port, user, passwd)
                if not r.check_blade_exist():
                    r.prepare_blade()

                r.testResult.testResTemp['testTitle']=one["description"]
                
                if one['httpCheckCommand'] == "":
                    if one['dockerName'] != "":
                        # r = RemoteRunner(host=host, port=port, user=user, passwd=passwd)
                        r.run_docker_cmd_by_dockerName(one['execCommand'], one['dockerName']).exec_check_contain(
                            one['execCommandExpect'])
                        r.testResult.testResTemp['realResponse']=r.res
                        r.testResult.testResTemp['chaosCommand']=r.commandList
                        r.testResult.testResTemp['chaosId']=r.uid
                        time.sleep(wait)
                        r.testResult.testResTemp["checkStatus"]=r.exec_check_by_cmd(one['checkCommand'], one['checkExpect'])
                        r.testResult.testResTemp['checkCommand']=one['checkCommand']
                        r.testResult.testResTemp['expectResponse']=one['checkExpect']
                        time.sleep(wait)
                        r.destroy_chaos()
                    else:
                        if "docker" in one['execCommand']:
                            # r = RemoteRunner(host=host, port=port, user=user, passwd=passwd)
                            r.run_docker_cmd(one['execCommand']).exec_check_contain(one['execCommandExpect'])
                            r.testResult.testResTemp['realResponse']=r.res
                            time.sleep(wait)
                            r.testResult.testResTemp['chaosCommand']=r.commandList
                            r.testResult.testResTemp['chaosId']=r.uid
                            r.testResult.testResTemp["checkStatus"]=r.exec_check_by_cmd(one['checkCommand'], one['checkExpect'])
                            r.testResult.testResTemp['realResponse']=r.res
                            r.testResult.testResTemp['checkCommand']=one['checkCommand']
                            r.testResult.testResTemp['expectResponse']=one['checkExpect']
                            r.testResult.testResTemp['realResponse']=r.res
                            time.sleep(wait)
                            r.destroy_chaos()
                        else:
                            # r = RemoteRunner(host=host, port=port, user=user,passwd=passwd)
                            r.exec_cmd(one['execCommand']).exec_check_contain(one['execCommandExpect'])
                            # r.testResult.testResTemp['realResponse']=r.res
                            time.sleep(wait)
                            r.testResult.testResTemp['chaosCommand']=r.commandList
                            r.testResult.testResTemp['chaosId']=r.uid
                            r.testResult.testResTemp["checkStatus"]=r.exec_check_by_cmd(one['checkCommand'], one['checkExpect'])
                            r.testResult.testResTemp['realResponse']=r.res
                            r.testResult.testResTemp['checkCommand']=one['checkCommand']
                            r.testResult.testResTemp['expectResponse']=one['checkExpect']
                            time.sleep(wait)
                            r.destroy_chaos()
                else:
                    
                    if one['dockerName'] != "":
                        # r = RemoteRunner(host=host, port=port, user=user, passwd=passwd)
                        r.testResult.testResTemp["checkStatus"]=r.run_docker_cmd_by_dockerName(one['execCommand'], one['dockerName']).exec_check_request_response(one['httpCheckCommand'],one['httpExpect'])
                        r.testResult.testResTemp['realResponse']=r.res
                        r.testResult.testResTemp['chaosCommand']=r.commandList
                        r.testResult.testResTemp['chaosId']=r.uid
                        r.testResult.testResTemp['checkCommand']=one['httpCheckCommand']
                        r.testResult.testResTemp['expectResponse']=one['httpExpect']
                        time.sleep(wait)
                        # r.exec_check_by_cmd(one['checkCommand'], one['checkExpect'])
                        time.sleep(wait)
                        r.destroy_chaos()
                    else:
                        if "docker" in one['execCommand']:
                            # r = RemoteRunner(host=host, port=port, user=user,passwd=passwd)
                            r.testResult.testResTemp["checkStatus"]=r.run_docker_cmd(one['execCommand']).exec_check_request_response(one['httpCheckCommand'],one['httpExpect'])
                            r.testResult.testResTemp['realResponse']=r.res
                            r.testResult.testResTemp['chaosCommand']=r.commandList
                            r.testResult.testResTemp['chaosId']=r.uid
                            r.testResult.testResTemp['checkCommand']=one['httpCheckCommand']
                            r.testResult.testResTemp['expectResponse']=one['httpExpect']
                            time.sleep(wait)
                            # r.exec_check_by_cmd(one['checkCommand'], one['checkExpect'])
                            time.sleep(wait)
                            r.destroy_chaos()
                        else:
                            # r = RemoteRunner(host=one['host'], port=port, user=user,passwd=passwd)
                            r.testResult.testResTemp["checkStatus"]=r.exec_cmd(one['execCommand']).exec_check_request_response(one['httpCheckCommand'],one['httpExpect'])
                            r.testResult.testResTemp['realResponse']=r.res
                            r.testResult.testResTemp['chaosCommand']=r.commandList
                            r.testResult.testResTemp['chaosId']=r.uid
                            r.testResult.testResTemp['checkCommand']=one['httpCheckCommand']
                            r.testResult.testResTemp['expectResponse']=one['httpExpect']
                            time.sleep(wait)
                            # r.exec_check_by_cmd(one['checkCommand'], one['checkExpect'])
                            time.sleep(wait)
                            r.destroy_chaos()
                    # requestStringParser(url_str=one['httpCheck'],loginRequire="no",checkResponse=one['httpExpect'])
                resList.append(r.testResult.testResTemp)
        except Exception as e:
            r.testResult.testResTemp['testTitle']=one["description"]
            r.testResult.testResTemp['chaosCommand']=one["execCommand"]
            r.testResult.testResTemp["realResponse"]=traceback.format_exc()
            r.testResult.testResTemp["checkStatus"]=False
            resList.append(r.testResult.testResTemp)
                # r.testResult.printResultTemp()
                # r.testResult.clearTemp()
        r.testResult.printResultTemp()
        r.testResult.clearTemp()
    logger.info("\n全部完成："+f'--' * 50)
    return resList

def generateHtmlReport(resList):
    from datetime import datetime
    passCounter=0
    failCounter=0
    total=0
    for one in resList:
        if one["checkStatus"]==True:
            passCounter+=1
        else:
            failCounter+=1
        total+=1

    exeTime=datetime.strftime(datetime.now(),"%y-%m-%d %H:%M:%S")

    env = Environment(loader=FileSystemLoader('./bootstrap'))
    template = env.get_template('template.html')
    with open("testResult.html", 'w+', encoding='utf-8') as f:
        out = template.render(resList=resList,exeTime=exeTime,passCounter=passCounter,failCounter=failCounter,total=total)
        f.write(out)
    return os.path.abspath('.')+os.path.sep+'testResult.html'



if __name__ == "__main__":
    generateHtmlReport(running(jf=json.load(open("config.json",encoding='utf-8'))))
