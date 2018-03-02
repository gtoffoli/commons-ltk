from django.shortcuts import render

from .languages import *
from .regexp import *
from .detection import *
from ltk.spacy.views import *

def home(request):
    ct = {}
    return render(request, 'home.html', context=ct)
