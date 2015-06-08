from django.shortcuts import render
from django.template import RequestContext
from django.core.context_processors import csrf
from py_lib.user import login

# Create your views here.
from datetime import datetime
from django.http import HttpResponse
test = ["OH~","suck","your","dick"]

def hello_world(request):
	account = request.POST['account']
	password = request.POST['password']
	test = login(account, password)
	return render(request,
		'hello_world.html',
		{'test': test},
		context_instance = RequestContext(request)
		)
#{'current_time': datetime.now()}
def TGOS(request):
	return render(request,
		'TGOS.html',
		)
def home(request):
	return render(request,
		'home.html'
		)