from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from bot.models import Account
import uuid


def index(request):
	if request.session.get('Email'):
		return render(request,'web/mainpage.html')
	else:
		return render(request,'web/index.html')
def signin(request):
	if	request.POST:
		return render(request,'web/index.html')

	else:
		return render(request,'web/index.html')
def signup(request):
	if	request.POST:
		utoken = uuid.uuid5(uuid.NAMESPACE_URL, request.POST['upEmail'])
		request.session['Email'] = request.POST['upEmail']
		Account.objects.get_or_create(nickname = request.POST['upNickname'],token = str(utoken), email = request.POST['upEmail'], password = request.POST['upPassword'], mid = '')
		return HttpResponseRedirect(reverse('index'))
		
	else:
		return HttpResponseRedirect(reverse('index'))
def logout(request):
	del request.session['Email']
	return HttpResponseRedirect(reverse('index'))
def checkemail(request):
	email = request.POST['email']
	try:
		Account.objects.get(email=email)
		return HttpResponse("error")
	except :
		return HttpResponse("ok")
def checknickname(request):
	nickname = request.POST['nickname']
	try:
		Account.objects.get(nickname = nickname)
		return HttpResponse("error")
	except :
		return HttpResponse("ok")

# Create your views here.
