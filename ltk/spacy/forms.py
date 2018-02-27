from django import forms
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from ltk.spacy.models import SPACY_DEPENDENCY_OPTIONS, SPACY_ENTITY_TYPES


class SpacyDependencyForm(forms.Form):
    language_code = forms.ChoiceField(
        label=_("language code"),
        choices=settings.LANGUAGES,
        widget=forms.Select(attrs={'class':'form-control',}))
    settings = forms.MultipleChoiceField(
        label=_("settings"),
        choices=SPACY_DEPENDENCY_OPTIONS,
        required=False,
        widget=forms.SelectMultiple(attrs={'class':'form-control', 'size': 2,}))
    text = forms.CharField(
        label=_("source text"),
        required=True,
        widget=forms.Textarea(attrs={'class':'form-control', 'rows': 4}))

class SpacyNerForm(forms.Form):
    language_code = forms.ChoiceField(
        label=_("language code"),
        choices=settings.LANGUAGES,
        widget=forms.Select(attrs={'class':'form-control',}))
    entity_types = forms.MultipleChoiceField(
        label=_("entity types"),
        choices=SPACY_ENTITY_TYPES,
        widget=forms.SelectMultiple(attrs={'class':'form-control', 'size': 7,}))
    text = forms.CharField(
        label=_("source text"),
        required=True,
        widget=forms.Textarea(attrs={'class':'form-control', 'rows': 6}))
        