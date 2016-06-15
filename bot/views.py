from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from bot.models import Account
import json
import re
import requests



def sendMessageBuild(target,content):
    mesg = {'to':target,'toChannel':'1383378250','eventType':'138311608800106203','content':{'contentType':'1','toType':'1','text':content}}
    return mesg

def recvreq(request):
    sendHeader = {'Content-type':'application/json; charset=UTF-8','X-Line-ChannelID':'1467107178','X-Line-ChannelSecret':'ee260eb823d4a0c71c54e3a401539acf','X-Line-Trusted-User-With-ACL':'u24ba734c4e2a0b5f06be24b80cf479b0'}
    url = 'https://trialbot-api.line.me/v1/events'
    body = request.body.decode('utf-8')
    rawJson = json.loads(body)
    for result in rawJson['result']:
        senderMID = result['content']['from']
        text = result['content']['text']
        if text == '':
            continue
        if text.startswith("/"):
            command = re.match('^/(\w+)',text).group(1)
            if(command == 'new'):
                result = re.match('^/new\s+([\w-]*)',text)
                if result:
                    token = result.group(1)
                    # Test wheather the mid is registed
                    mids = Account.objects.filter(mid=senderMID)
                    if(len(mids)>=1):
                        MsgBuild = sendMessageBuild([senderMID],'此Line帳號已經註冊過')
                        Msg = json.dumps(MsgBuild)
                        req = requests.post(url,data=Msg,headers=sendHeader)
                        continue
                    newbie = Account.objects.filter(token=token)
                    if(len(newbie)==0):
                        print("Not exist")
                        MsgBuild = sendMessageBuild([senderMID],'Token錯誤，請上 https://linewhisper.herokuapp.com 查看教學')
                        Msg = json.dumps(MsgBuild)
                        req = requests.post(url,data=Msg,headers=sendHeader)
                        continue
                    else:
                        newbie[0].mid = senderMID
                        newbie[0].save()
                        MsgBuild = sendMessageBuild([senderMID],'註冊成功')
                        Msg = json.dumps(MsgBuild)
                        req = requests.post(url,data=Msg,headers=sendHeader)

        else:
            target = []
            receivers = Account.objects.all().exclude(mid='').exclude(mid=senderMID)
            for recver in receivers:
                target.append(recver.mid)
            print('即將送出的訊息是:{}'.forat(text))
            MsgBuild = sendMessageBuild(target,text)
            Msg = json.dumps(MsgBuild)
            req = requests.post(url,data=Msg,headers=sendHeader)
    return HttpResponse(u"<h1>Hello World</h1>")
