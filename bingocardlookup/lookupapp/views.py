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
import logging

logger = logging.getLogger(__name__)

def login(request):
    logger.debug('login called with request: %s ' % request)
    return render_to_response('lookupapp/login.html',
                              context_instance=RequestContext(request))
def logout(request):
    logger.debug('logout called with request: %s ' % request)
    auth.logout(request)
    return redirect('/bingocardlookup/') 
#This is ugly...couldn't get it working otherwise

@login_required
def editcard(request):
    logger.debug('request.user.id: %s ' % request.user.id)
    logger.debug('request.method: %s' % request.method)
    
    userOpenId = UserOpenID.objects.get(user=request.user.id)
    logger.debug('userOpenId.claimed_id: %s' % userOpenId.claimed_id)

    try:
        bingocard = BingoCard.objects.get(openid=userOpenId.claimed_id)
    except ObjectDoesNotExist:
        logger.debug('bingocard not registered yet')
        bingocard = None

    setup_session(request, userOpenId.claimed_id, bingocard)

    if request.method == 'POST': 
        form = BingoCardForm(request.POST, instance=bingocard)
        logger.debug('form isValid?: %s ' % form.is_valid())
        logger.debug('form: %s ' % form)

        if(form.is_valid()):
            form.save()
            return redirect('/bingocardlookup/enter/')
        else:
            return render_to_response('lookupapp/register.html', { 'form' : form }, context_instance=RequestContext(request))
    else:
	logger.debug('requested GET for editcard, redirecting')
        return render_to_response('lookupapp/register.html', context_instance=RequestContext(request))
    
@login_required
def enter(request):
    logger.debug('request.user: %s' % request.user)
    userOpenId = UserOpenID.objects.get(user=request.user)
    id = userOpenId.claimed_id
    userid = request.user.id
    username = escape(request.user.get_full_name())

    try:
       bingocard = BingoCard.objects.get(openid=id)
    except ObjectDoesNotExist: 
       setup_session(request, id, None)
       return redirect('/bingocardlookup/editcard')
    return render_to_response('lookupapp/enter.html', {'id':id, 'userid':userid, 'username':username, 'bingocard':bingocard}, context_instance=RequestContext(request))

def decode(request):
    challenge = request.GET['challenge']    
    id = request.GET['id']
    userDatagrid = eval(BingoCard.objects.get(openid=id).grid)
    decodedSequence = parseBingoCard.decode(challenge, userDatagrid)
    returnString = ",".join(str(decodedSequence)).replace(",","").replace(" ", "").replace("'","")
    return HttpResponse(simplejson.dumps({'response':returnString}))

def setup_session(request, openid, bingocard):
    logger.debug(request.session.get('id'))
    logger.debug(request.session.get('bingocard'))
    logger.debug('openid to set: %s' % openid)
    logger.debug('bingocard to set: %s' % bingocard)
    if not request.session.get('id'):
        logger.debug('id not set in session, setting now')
        request.session['id'] = openid
    
    if not request.session.get('bingocard'):
        logger.debug('bingocard not set in session, setting now')
        request.session['bingocard'] = bingocard    
