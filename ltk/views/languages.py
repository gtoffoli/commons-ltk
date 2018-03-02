from django.shortcuts import render
from django.http import HttpResponseRedirect

from ltk.session import get_language, set_language


def language(request, language_code):
    set_language(request, language_code or '')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
