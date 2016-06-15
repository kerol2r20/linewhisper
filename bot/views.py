from django.shortcuts import render
from django.http import HttpResponse
from bot.models import Account
import json
import re


sendHeader = {'Content-Type':'application/json; charser=UTF-8', 'X-Line-ChannelID':'1467107178', 'X-Line-ChannelSecret':'ee260eb823d4a0c71c54e3a401539acf','X-Line-Trusted-User-With-ACL','u24ba734c4e2a0b5f06be24b80cf479b0'}

def sendMessageBuild(target,content):
    mesg = {'to':target,'toChannel':'1383378250','eventType':'138311608800106203','content':{'contentType':'1','toType':'1','text':content}}
    return mesg

def recvreq(request):
    global sendHeader
    url = 'https://trialbot-api.line.me/v1/events'
    body = request.body.decode('utf-8')
    rawJson = json.loads(body)
    for result in rawJson['result']:
        senderMID = result['content']['from']
        text = result['content']['text']
        if text.startswith("/"):
            command = re.match('^/(\w+)',text).group(1)
            if(command == 'new'):
                result = re.match('^/new\s+([\w-]*)',text)
                if result:
                    token = result.group(1)
                    try:
                        newbie = Account.objects.get(token=token)
                    except DoesNotExist:
                        print("Not exist")
                        MsgBuild = sendMessageBuild([senderMID],'Sorry! Your token may not match any account. Plz try again.')
                        Msg = json.dumps(MsgBuild)
                        requests.post(url,data=Msg,headers=sendHeader)
                        continue
                    newbie.mid = senderMID
                    newbie.save()
                    MsgBuild = sendMessageBuild([senderMID],'Successfully')
                    Msg = json.dumps(MsgBuild)
                    requests.post(url,data=Msg,headers=sendHeader)

        else:
            print('')
    return HttpResponse(u"<h1>Hello World</h1>")
