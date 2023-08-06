#encoding:utf-8
#https://oapi.dingtalk.com/robot/send?access_token=e024afe8a1b7aff5896d5ba9axxxxxxx
import requests
import json

#钉钉告警接口，从钉钉api获取
dingding_url="https://oapi.dingtalk.com/robot/send?access_token=e024afe8a1b7aff5896d5ba9axxxxxxx"
#钉钉告警接口，发送模板
def message_warp(request_url="",response_message=""):
    return {
        "msgtype": "markdown",
        "markdown": {
            "title":"云启业务异常通知",
            "text": "# 重要！！ 云启APP业务错误\n---\n## 发送请求：\n```\n"+request_url+"\n```\n## 返回消息：\n```\n"+response_message+"\n```\n"
        },
    }


#拨测业务数据接口调用
login_data={
    "phoneNum":"1834911xxxx",
    "password":"c03bf628eee907844xxxxxxxxxxxx",
    "businessCode":"xxxxxx-xxxxkit",
    "loginType":"ACCOUNT"
}
login_url="https://xxxxxx.xxxxxx.com/xxxxxx-xxxxkit/homekit/account/login"
login_header={"Content-Type":"application/json","grant_type":"password"}
client=requests.session()
res=client.post(url=login_url,headers=login_header,json=login_data)
login_token=json.loads(res.text)['data']['token']
login_userid=json.loads(res.text)['data']['userId']
if login_token=="":
    client.post(url=dingding_url,json=message_warp(login_url,res.text))
    exit()


query_url="https://xxxxxx.xxxxxx.com/xxxxxx-xxxxkit/homekit/device/query"
query_header={"Content-Type":"application/json","Authorization":login_token}
query_data={"accessToken":login_token,"applicationId":"3f61abxxxx","channelId":"tsl_store","clientId":"0","currenTime":"16285xxxxxx","equipmentId":"","gatewayId":"50294D2246BC","userId":login_userid,"version":"1.0.0"}
res=client.post(url=query_url,headers=query_header,json=query_data)

result_flag=json.loads(res.text.encode('utf-8'))['success']
result_message=json.loads(res.text.encode('utf-8'))['message']
# r=client.post(url=dingding_url,json=message_warp(query_url,res.text))
# print(r.text)
if result_flag!=True or result_message!='成功':
    client.post(url=dingding_url,json=message_warp(query_url,res.text))
    exit()








#语音播放，读取
#coding:utf-8
import pyttsx3
import random
from loguru import logger

story='民国时期，胡八一祖父胡国华因为家道中落和自己吃喝嫖赌抽样样俱全而被迫去盗墓，却被一看风水老先生制止并于百年后传授一本秘书残卷十六字阴阳风水秘术，懂此书可知风水，可观天文，并以此可知隐藏在奇川大山中的琼楼古墓，此书历经磨难最终传到胡八一手上。'
short_words=['革时期','上知','户山','热','得胡八一','之行','期间','Shirley杨']
long_word='陈教授，以四人为主开始梦幻奇绝的探秘之旅。其中以四个大的墓葬为全文脉络，地点分别是沙漠中的精绝古城、陕西的龙岭迷窟、云南虫谷以及西藏昆仑山。故事中用两个小片段交代人物出场、故事背景以及关于盗墓的一些基本常识，高潮则开始于胡八一和胖子跟随考古队，利用秘书残卷中风水秘术来解读天下大川脉搏，寻找一处失落在地下的琼楼宝殿——精绝古城，从而揭开千年部族消失之谜，却在精绝古城中遭遇种种离奇，无论是尸香魔芋的怪异魔力还是关于先知的预言，最终考古队中只有四人从鬼洞中死里逃生。而在龙岭迷窟倒斗的时候，除了遭遇各种匪夷所思的诡异外，还意外地发现从精绝古城的鬼洞死里逃生出来的四个人（另外两个是Shirley杨和陈教授）都染上怪病，需要传说中埋藏在云南古滇国献王墓中的髦尘珠才能救各人性命，但髦尘珠所在地献王墓却隐藏在蛇河虫谷之中，胡八一等为解性命之忧不得已开始云南虫谷之旅。但是如何揭开髦尘珠的秘密，所有线索又指向雪域藏地，此时香港古董商为寻找魔国冰川水晶尸也意欲前往藏地古格王国遗址，从而又开始了一段昆仑神宫的探秘之行，而在异常离奇诡秘的地下世界中，历史的神秘面纱也正一层层地被揭开'
english_chinese=['有些term不好translate','show off 自己的外语level','maybe是刚从国外return，还没有used to 全用中文','Jack，把你提交的代码merge request一下','review一下你的代码，那个工程rebuild一下']

engine=pyttsx3.init()
rate=engine.getProperty('rate')
engine.setProperty('rate',166)
volume = engine.getProperty('volume')   # 获取当前的音量 （默认值）(min=0 and max=1)
#print (volume)                          # 打印当前音量（默认值）
engine.setProperty('volume',1.0)    # 设置一个新的音量（0 < volume < 1）
voices = engine.getProperty('voices')       # 获取当前的音色信息
engine.setProperty('voice', voices[0].id)  # 改变中括号中的值,0为男性,1为女性
engine.setProperty('voice','zh')             #将音色中修改音色的语句替换



def read_phash_07():
    words_list=[]
    f= open('C:\\Users\\oupeng\\Documents\\001TSL-myfile\\项目\\语音转文字SDK测试\\语料.txt','r',encoding='utf-8')
    for one in f.readlines():
        words_list.append(one)
    logger.info(words_list)
    word_len=len(words_list)
    logger.info(word_len)
    sed_int=random.randint(1,10)
    logger.info(sed_int)
    words=""
    for one in range(0,sed_int):
        words=words+words_list[random.randint(0,word_len)]
    logger.info(words)
    engine.say(words)
    # engine.say("你好")
    engine.runAndWait()

def read_story_04():
    logger.info(story)
    engine.say(story)
    engine.runAndWait()

def read_shot_words_03():
    lenth=len(short_words)
    w=short_words[random.randint(0,lenth)]
    logger.info(w)
    engine.say(w)
    engine.runAndWait()

def read_en_ch_06():
    lenth2 = len(english_chinese)
    w = english_chinese[random.randint(0, lenth2)]
    logger.info(w)
    engine.say(w)
    engine.runAndWait()

def read_long_word():
    engine.say(long_word)
    engine.runAndWait()


import pyttsx3
tts = pyttsx3.init()
tts.setProperty('voice', tts.getProperty('voice')[1])
tts.save_to_file("王德发，爱你", "./filename.mp3")
tts.runAndWait()



import getpass
# 自动读取当前用户的名称
user = getpass.getuser()
print("尊敬的",user)
# 以不回显的方式,读取用户的输入
passwd = getpass.getpass("请输入您的密码:")
print("------------->华丽的分割线<----------------")
print("您的密码为:", passwd)


if __name__=='__main__':
    read_long_word()