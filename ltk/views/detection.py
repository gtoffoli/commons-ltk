from langdetect import detect_langs

from django.views import View
from django.shortcuts import render

from ltk.forms import LanguageDetectionForm


class LanguageDetection(View):
    form_class = LanguageDetectionForm
    initial = {}
    template_name = 'language_detection.html'

    def get(self, request, *args, **kwargs):
        self.form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': self.form})

    def post(self, request, *args, **kwargs):
        self.form = self.form_class(request.POST)
        self.doc = None
        if self.form.is_valid():
            data = self.form.cleaned_data
            text = data['text']
            languages = detect_langs(text)
            languages = [[l.lang, l.prob] for l in languages]
        return render(request, self.template_name, {'form': self.form, 'languages': languages})
