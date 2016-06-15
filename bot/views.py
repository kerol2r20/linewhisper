from django.shortcuts import render
from django.http import HttpResponse
from bot.models import Account
import json

# Create your views here.
def recvreq(request):
    body = request.body.decode('utf-8')
    rawJson = json.loads(body)
    for result in rawJson['result']:
        print('Recv: {}'.format(result['content']['text']))
    return HttpResponse(u"<h1>Hello World</h1>")
