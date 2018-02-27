import json
import spacy
from spacy import displacy
from nltk import Tree

from django.shortcuts import render
from django.views import View
from django.conf import settings

from ltk.session import get_language
from ltk.spacy.models import SPACY_LANGUAGE_MODELS, SPACY_ENTITY_TYPES
from ltk.spacy.forms import SpacyDependencyForm, SpacyNerForm


class SpacyDependency(View):
    form_class = SpacyDependencyForm
    initial = { 'settings': ['collapsePunct', 'collapsePhrase',]}
    template_name = 'spacy_dependency.html'

    def filter_languages(self):
        spacy_language_codes = [code for code,label in SPACY_LANGUAGE_MODELS]
        self.language_codes = [code for code,name in settings.LANGUAGES if code in spacy_language_codes]

    def customize_form(self):
        self.form.fields['language_code'].choices = [item for item in settings.LANGUAGES if item[0] in self.language_codes]

    def parse(self):
        # nlp = spacy.load('custom_parse_model')
        nlp = spacy.load(self.language_code)
        self.doc = nlp(self.text)
        self.print_tree = self.doc.print_tree()

    def node_to_nltk_tree(self, node):
        if node.n_lefts + node.n_rights > 0:
            return Tree(node.orth_, [self.node_to_nltk_tree(child) for child in node.children])
        else:
            return node.orth_

    def tree_to_nltk_tree(self):
        [self.node_to_nltk_tree(sent.root).pretty_print() for sent in self.doc.sents]

    def get(self, request, *args, **kwargs):
        self.filter_languages()
        default_language_code = get_language(request)
        if default_language_code and default_language_code in self.language_codes:
            self.initial['language_code'] = default_language_code
        self.form = self.form_class(initial=self.initial)
        self.customize_form()
        return render(request, self.template_name, {'form': self.form})

    def post(self, request, *args, **kwargs):
        self.filter_languages()
        self.form = self.form_class(request.POST)
        self.doc = None
        self.print_tree = None
        self.markup = ''
        if self.form.is_valid():
            data = self.form.cleaned_data
            self.language_code = data['language_code']
            options = {
                'collapse_punct': 'collapsePunct' in data['settings'],
                'collapse_phrase': 'collapsePhrase' in data['settings']
            }
            self.text = data['text']
            self.parse()
            self.svg_tree = displacy.render(self.doc, style='dep', page=False, minify=False, jupyter=False, options=options, manual=False)
            self.tree_to_nltk_tree()
        self.customize_form()
        return render(request, self.template_name, {'form': self.form, 'doc': self.doc, 'print_tree': json.dumps(self.print_tree), 'svg_tree': self.svg_tree})

class SpacyNer(View):
    form_class = SpacyNerForm
    initial = { 'entity_types': ['PERSON', 'PER', 'ORG', 'LOC', 'DATE',]}
    template_name = 'spacy_ner.html'

    def filter_languages(self):
        spacy_language_codes = [code for code,label in SPACY_LANGUAGE_MODELS]
        self.language_codes = [code for code,name in settings.LANGUAGES if code in spacy_language_codes]

    def customize_form(self):
        self.form.fields['language_code'].choices = [item for item in settings.LANGUAGES if item[0] in self.language_codes]
        self.form.fields['entity_types'].choices = [(code, '{0} ({1})'.format(code, label)) for code,label in SPACY_ENTITY_TYPES]

    def extract_ents(self):
        # nlp = spacy.load('custom_ner_model')
        nlp = spacy.load(self.language_code)
        self.doc = nlp(self.text)
        self.ents = self.doc.ents
            
    def render_ents(self):
        """Render entities in text. (inspired to spacy.displacy.render.py)
        See demo at: https://demos.explosion.ai/displacy-ent/
        """
        markup = ''
        offset = 0
        for ent in self.ents:
            label = ent.label_
            start = ent.start_char
            end = ent.end_char
            entity = self.text[start:end]
            fragments = self.text[offset:start].split('\n')
            for i, fragment in enumerate(fragments):
                markup += fragment
                if len(fragments) > 1 and i != len(fragments)-1:
                    markup += '</br>'
            markup += '<mark data-entity="{0}">{1}</mark>'.format(label.lower(), entity)
            offset = end
        markup += self.text[offset:]
        return markup

    def get(self, request, *args, **kwargs):
        self.filter_languages()
        default_language_code = get_language(request)
        if default_language_code and default_language_code in self.language_codes:
            self.initial['language_code'] = default_language_code
        self.form = self.form_class(initial=self.initial)
        self.customize_form()
        return render(request, self.template_name, {'form': self.form})

    def post(self, request, *args, **kwargs):
        self.filter_languages()
        self.form = self.form_class(request.POST)
        self.doc = None
        self.markup = ''
        if self.form.is_valid():
            data = self.form.cleaned_data
            self.language_code = data['language_code']
            self.text = data['text']
            self.extract_ents()
            self.markup = self.render_ents()
        self.customize_form()
        return render(request, self.template_name, {'form': self.form, 'doc': self.doc, 'markup': self.markup})
