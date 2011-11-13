# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext, Context, loader
from django.shortcuts import render_to_response, redirect
from django.utils import simplejson
from lookupapp.models import BingoCard
from lookupapp.forms import BingoCardForm
from django.contrib.auth.decorators import login_required
from django.utils.html import escape
from django_openid_auth.models import UserOpenID
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import auth
import sys
import parseBingoCard

def login(request):
    return render_to_response('lookupapp/login.html',
                              context_instance=RequestContext(request))
def logout(request):
    auth.logout(request)
    return redirect('/bingocardlookup/') 
#This is ugly...couldn't get it working otherwise

def register(request):
    if request.method == 'POST':
        form = BingoCardForm(request.POST)
        if(form.is_valid()):
            #print(type(str(form.cleaned_data['grid'])))
	    #print(str(form.cleaned_data['grid']))
            form.save()
            return redirect('/bingocardlookup/enter/')
    else:
        form = BingoCardForm()

    return render_to_response('lookupapp/register.html', { 'form' : form },
                              context_instance=RequestContext(request))

def editcard(request):
    userOpenId = UserOpenID.objects.get(user=request.user.id)
    bingocard = BingoCard.objects.get(openid=userOpenId.claimed_id)

    if request.method == 'POST': 
        form = BingoCardForm(request.POST, instance=bingocard)
        if(form.is_valid()):
            form.save()
            return redirect('/bingocardlookup/enter/')
        else:
            print(str(form.cleaned_data['grid']))
    else:
        return render_to_response('lookupapp/register.html', { 'id' : userOpenId.claimed_id, 'bingocard' : bingocard }, 
                              context_instance=RequestContext(request))
    return render_to_response('lookupapp/register.html', { 'form' : form },
                              context_instance=RequestContext(request))

@login_required
def enter(request):
    userOpenId = UserOpenID.objects.get(user=request.user)
    id = userOpenId.claimed_id
    userid = request.user.id
    username = escape(request.user.get_full_name())
    
    try:
       bingocard = BingoCard.objects.get(openid=id)
    except ObjectDoesNotExist: 
       return render_to_response('lookupapp/register.html', {'id':id, 'userid':request.user.id, 'username':username}, context_instance=RequestContext(request))
        #how to redirect so url changes, while still passing RequestContext?
    return render_to_response('lookupapp/enter.html', {'id':id, 'userid':userid, 'username':username, 'bingocard':bingocard}, context_instance=RequestContext(request))

def decode(request):
    challenge = request.GET['challenge']    
    id = request.GET['id']
    userDatagrid = eval(BingoCard.objects.get(openid=id).grid)
    decodedSequence = parseBingoCard.decode(challenge, userDatagrid)
    returnString = ",".join(str(decodedSequence)).replace(",","").replace(" ", "").replace("'","")
    return HttpResponse(simplejson.dumps({'response':returnString}))
