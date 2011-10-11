# Create your views here.
from django.http import HttpResponse
from django.template import Context, loader
from django.shortcuts import render_to_response
from django.utils import simplejson
from lookupapp.models import BingoCard
import parseBingoCard

def index(request):
    return HttpResponse("Allo, World.")

def enter(request):
    id = '1'
    bingocard = BingoCard.objects.get(openid=id)
    
    return render_to_response('lookupapp/enter.html', {'id':id, 'bingocard':bingocard})

def decode(request):
    challenge = request.GET['challenge']    
    id = '1'
    userDatagrid = eval(BingoCard.objects.get(openid=id).grid)
    decodedSequence = parseBingoCard.decode(challenge, userDatagrid)
    returnString = ",".join(str(decodedSequence)).replace(",","").replace(" ", "").replace("'","")
    return HttpResponse(simplejson.dumps({'response':returnString}))
