# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext, Context, loader
from django.shortcuts import render_to_response, redirect
from django.utils import simplejson
from lookupapp.models import BingoCard
from django.contrib.auth.decorators import login_required
from django.utils.html import escape
from django_openid_auth.models import UserOpenID
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import auth
import sys
import parseBingoCard


@login_required
def index(request):
    return HttpResponse("Hello,".join(request.user.username))

def login(request):
    return render_to_response('lookupapp/login.html',
                              context_instance=RequestContext(request))
def logout(request):
    auth.logout(request)
    return redirect('/bingocardlookup/') 
#This is ugly...couldn't get it working otherwise

def register(request):
    print request
    return redirect('lookupapp/enter.html')

@login_required
def enter(request):
    userOpenId = UserOpenID.objects.get(user=request.user.id)
    id = userOpenId.claimed_id
    userid = request.user.id
    username = escape(request.user.get_full_name())
    
    try:
       bingocard = BingoCard.objects.get(openid=id)
    except ObjectDoesNotExist: 
       return render_to_response('lookupapp/register.html', {'id':id, 'userid':request.user.id, 'username':username})
    
    return render_to_response('lookupapp/enter.html', {'id':id, 'userid':userid, 'username':username, 'bingocard':bingocard})

def decode(request):
    challenge = request.GET['challenge']    
    id = request.GET['id']
    userDatagrid = eval(BingoCard.objects.get(openid=id).grid)
    decodedSequence = parseBingoCard.decode(challenge, userDatagrid)
    returnString = ",".join(str(decodedSequence)).replace(",","").replace(" ", "").replace("'","")
    return HttpResponse(simplejson.dumps({'response':returnString}))
