import random,time
import os,sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from swaggerjmx.convert import conversion
from swaggerjmx.settings import Settings as ST
import traceback



def swagger2jmeter(url,reportPath):

    #  swagger_url
    try:
        ST.swagger_url = url
        #  report_path
        ST.report_path = reportPath
        # 开始转换
        conversion()
        # print(os.path.abspath(os.path.dirname(__file__))+os.sep+'jmx'+os.sep)

        upperDir = reportPath
        # upperDir=os.path.abspath(os.path.dirname(__file__))+os.sep+'jmx'+os.sep

        for x,y,z in os.walk(upperDir):
            return upperDir+"".join(z)
    except Exception as e:
        print(traceback.format_exc())
        return "switch to jmeter script error"


if __name__=="__main__":
    pass
    # print(swagger2jmeter("http://192.168.118.168:43323/auth/v2/api-docs"))