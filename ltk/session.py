# -*- coding: utf-8 -*-"""

def get_language(request):
    return request.session.get("language", '')

def set_language(request, value):
    request.session["language"] = value
