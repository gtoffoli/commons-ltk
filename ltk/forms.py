import re

from django import forms
from django.utils.translation import ugettext_lazy as _, string_concat

class RegexpForm(forms.Form):
    search_pattern = forms.CharField(
            label=_("search pattern"),
            required=True,
            widget=forms.Textarea(attrs={'class':'form-control', 'rows': 2}))
    replace_pattern = forms.CharField(
            label=_("replacement pattern"),
            required=False,
            widget=forms.TextInput(attrs={'class':'form-control'}))
    text = forms.CharField(
            label=_("source text"),
            required=True,
            widget=forms.Textarea(attrs={'class':'form-control', 'rows': 8}))

    def clean_search_pattern(self):
        pattern = self.cleaned_data['search_pattern']
        try:
            return re.compile(pattern)
        except Exception as e:
            raise forms.ValidationError(_('"{0}" error: at position {1}'.format(e.msg,e.pos)))

    """
    def clean_replace_pattern(self):
        pattern = self.cleaned_data['replace_pattern']
        try:
            return re.compile(pattern)
        except Exception as e:
            raise forms.ValidationError(_('"{0}" error: at position {1}'.format(e.msg,e.pos)))
    """
        