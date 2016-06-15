from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from bot.models import Account
import uuid


def index(request):
	
	return render(request,'web/index.html')
def signup(request):
	if	request.POST:
		utoken = uuid.uuid5(uuid.NAMESPACE_URL, request.POST['upEmail'])
		
		Account.objects.get_or_create(nickname = request.POST['upNickname'],token = str(utoken), email = request.POST['upEmail'], password = request.POST['upPassword'], mid = '')
		
		return HttpResponse(Account.objects.get(nickname = request.POST['upNickname']))
	else:
		return HttpResponseRedirect(reverse('index'))

# Create your views here.
