# Create your views here.
from django.http import HttpResponse
from django.template import Context, loader
from django.shortcuts import render_to_response
from lookupapp.models import BingoCard

def index(request):
    return HttpResponse("Allo, World.")

def enter(request):
    id = '1'
    bingocard = BingoCard.objects.get(openid=id)
    
    return render_to_response('lookupapp/enter.html', {'id':id, 'bingocard':bingocard})

def decode(request):
    
    decodedSequence = request.GET['challenge']    


    return render_to_response('lookupapp/enter.html', {'decodedSequence':decodedSequence})

