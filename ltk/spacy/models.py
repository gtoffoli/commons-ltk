from django.db import models
from django.utils.translation import ugettext as _
from django.conf import settings


SPACY_LANGUAGE_MODELS = (
    ('de', 'de_core_news_sm (2.0.0)'),
    ('en', 'en_core_web_sm (2.0.0)'),
    ('es', 'es_core_news_sm (2.0.0)'),
    ('fr', 'fr_core_news_sm (2.0.0)'),
    ('it', 'it_core_news_sm (2.0.0)'),
    ('nl', 'nl_core_news_sm (2.0.0)'),
    ('pt', 'pt_core_news_sm (2.0.0)'),
)

SPACY_DEPENDENCY_OPTIONS = (
    ('collapsePunct', _('collapse punctuation')),
    ('collapsePhrase', _('collapse phrases')),
)
    
SPACY_ENTITY_TYPES = (
    ('PERSON', _('People, including fictional')),
    ('PER', _('PER')),
    ('NORP', _('Nationalities or religious or political groups')),
    ('FACILITY', _('Buildings, airports, highways, bridges, etc.')),
    ('ORG', _('Companies, agencies, institutions, etc.')),
    ('GPE', _('Countries, cities, states')),
    ('LOC', _('Non-GPE locations, mountain ranges, bodies of water')),
    ('PRODUCT', _('Objects, vehicles, foods, etc. (not services)')),
    ('EVENT', _('Named hurricanes, battles, wars, sports events, etc.')),
    ('WORK OF ART', _('Titles of books, songs, etc.')),
    ('LANGUAGE', _('Any named language')),
    ('DATE', _('Absolute or relative dates or periods')),
    ('TIME', _('Times smaller than a day')),
    ('PERCENT', _('Percentage, including "%"')),
    ('MONEY', _('Monetary values, including unit')),
    ('QUANTITY', _('Measurements, as of weight or distance')),
    ('ORDINAL', _('"first", "second", etc.')),
    ('CARDINAL', _('Numerals that do not fall under another type')),
)

"""
PERSON    People, including fictional.
NORP    Nationalities or religious or political groups.
FACILITY    Buildings, airports, highways, bridges, etc.
ORG    Companies, agencies, institutions, etc.
GPE    Countries, cities, states.
LOC    Non-GPE locations, mountain ranges, bodies of water.
PRODUCT    Objects, vehicles, foods, etc. (Not services.)
EVENT    Named hurricanes, battles, wars, sports events, etc.
WORK_OF_ART    Titles of books, songs, etc.
LAW    Named documents made into laws.
LANGUAGE    Any named language.
DATE    Absolute or relative dates or periods.
TIME    Times smaller than a day.
PERCENT    Percentage, including "%".
MONEY    Monetary values, including unit.
QUANTITY    Measurements, as of weight or distance.
ORDINAL    "first", "second", etc.
CARDINAL    Numerals that do not fall under another type.
"""
