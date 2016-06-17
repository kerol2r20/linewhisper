from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from bot.models import Account
import json
import re
import requests
import random
helpmsg = '註冊 /new token\n密語!name message\ndice /dice'
sendHeader = {'Content-type':'application/json; charset=UTF-8','X-Line-ChannelID':'1467107178','X-Line-ChannelSecret':'ee260eb823d4a0c71c54e3a401539acf','X-Line-Trusted-User-With-ACL':'u24ba734c4e2a0b5f06be24b80cf479b0'}
url = 'https://trialbot-api.line.me/v1/events'
def sendMessageBuild(target,content):
    mesg = {'to':target,'toChannel':'1383378250','eventType':'138311608800106203','content':{'contentType':'1','toType':'1','text':content}}
    return mesg
def sendMessage(target,content):
    mesg = {'to':target,'toChannel':'1383378250','eventType':'138311608800106203','content':{'contentType':'1','toType':'1','text':content}}
    Msg = json.dumps(mesg)
    req = requests.post(url,data=Msg,headers=sendHeader)
    return
def recvreq(request):

    body = request.body.decode('utf-8')
    rawJson = json.loads(body)
    for result in rawJson['result']:
        senderMID = result['content']['from']

        # Text event
        text = result['content']['text']
        if not text == '':
         
            try:
                sender = Account.objects.get(mid=senderMID)
                sender = sender.nickname
                # Command
                if text.startswith("/"):
                    command = re.match('^/(\w+)',text).group(1)
                    if command == 'help':
                        sendMessage([senderMID],helpmsg)
                        continue
                    elif command == 'dice':
                        diceresult = random.randrange(1,7)
                        text = sender + "擲出了" + str(diceresult) + "點!"
                        target = Broadcasttarget()
                        MsgBuild = sendMessageBuild(target,text)
                        Msg = json.dumps(MsgBuild)
                        req = requests.post(url,data=Msg,headers=sendHeader)
                    else:
                        text = "沒有這指令，使用/help來查詢所有指令。"
                        MsgBuild = sendMessageBuild([senderMID],text)
                        Msg = json.dumps(MsgBuild)
                        req = requests.post(url,data=Msg,headers=sendHeader)

                # send message to someone
                elif text.startswith("!"):
                    targetNick = re.match('^!(\w+)\s+(.+)$',text).group(1)
                    text = re.match('^!(\w+)\s+(.+)$',text).group(2)
                    target = Account.objects.filter(nickname=targetNick)
                    if(len(target)!=0):
                    
                        target = target[0].mid
                        text = sender + " 私訊您: " + text
                        MsgBuild = sendMessageBuild([target],text)
                        Msg = json.dumps(MsgBuild)
                        req = requests.post(url,data=Msg,headers=sendHeader)

                # Broadcast
                else:
                    
                    rejectlist = ['']
                    rejectlist.append(senderMID)
                    target = Broadcasttarget(rejectlist)
                    print('即將送出的訊息是:{}'.format(text))
                    text = sender + ": " + text
                    MsgBuild = sendMessageBuild(target,text)
                    Msg = json.dumps(MsgBuild)
                    req = requests.post(url,data=Msg,headers=sendHeader)
            # Not a account
            except:
                # Command
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
                                continue
                    elif command == 'help':

                        MsgBuild = sendMessageBuild([senderMID],helpmsg)
                        Msg = json.dumps(MsgBuild)
                        req = requests.post(url,data=Msg,headers=sendHeader)
                        continue
                MsgBuild = sendMessageBuild([senderMID],'此Line帳號尚未驗證Token，請上 https://linewhisper.herokuapp.com 查看教學')
                Msg = json.dumps(MsgBuild)
                req = requests.post(url,data=Msg,headers=sendHeader)
                continue

        # Add friend event
        addFriendEvent = result['content']['onType']
        if(addFriendEvent=='4'):
            MsgBuild = sendMessageBuild([senderMID],'歡迎使用Linewhisper，請上 https://linewhisper.herokuapp.com 獲取相對應之Token來解鎖服務')
            Msg = json.dumps(MsgBuild)
            req = requests.post(url,data=Msg,headers=sendHeader)


    return HttpResponse(u"<h1>Hello World</h1>")
def Broadcasttarget(rejectlist=['']):
    targetlist = Account.objects.all()
    for mid in rejectlist:
        targetlist = targetlist.exclude(mid = mid)
    targetmid = []
    for recver in targetlist:
        targetmid.append(recver.mid)
    return targetmid