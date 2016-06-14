from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def recvreq(request):
    body = request.body.decode('utf-8')
    print('\nLine Request:\n%s\n' % body)
    return HttpResponse(u"<h1>Hello World</h1>")
