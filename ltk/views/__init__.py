from django.shortcuts import render
from django.http import HttpResponseRedirect

from .regexp import *
from .detection import *

from ltk.session import get_language, set_language
from ltk.spacy.views import *

def home(request):
    ct = {}
    return render(request, 'home.html', context=ct)

def language_set(request, language_code):
    set_language(request, language_code or '')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
