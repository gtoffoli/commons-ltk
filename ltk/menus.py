from django.conf import settings
from django.utils.translation import ugettext as _, ugettext_lazy
from django.utils.text import capfirst
from menu import Menu, MenuItem

Menu.items = {}
Menu.sorted = {}

def about_children(request):
    children = []
    children.append (MenuItem(
         capfirst(_("the CommonS project")),
         url='/info/about/',
        ))
    children.append (MenuItem(
         capfirst(_("the LTK platform")),
         url='/info/platform/',
         ))
    return children

def start_children(request):
    children = []
    children.append (MenuItem(
         capfirst(_('regular expressions')),
         url='/regexp/'
        ))
    children.append (MenuItem(
         capfirst(_('language detection')),
         url='/detection/'
        ))
    children.append (MenuItem(
         capfirst(_('dependency parsing')),
         url='/dependency/'
        ))
    children.append (MenuItem(
         capfirst(_('named entity recognition')),
         url='/entities/'
        ))
    return children        


def language_children(request, code):
    children = []
    children.append (MenuItem(
         capfirst(_('show')),
         url='/language/%s/info/' % code,
        ))
    children.append (MenuItem(
         capfirst(_('set as default')),
         url='/language/%s/set/' % code,
        ))
    return children        

def languages_children(request):
    children = []
    for code, name in settings.LANGUAGES:
        language_menu = MenuItem(
             name,
             url='/language/%s/set/' % code,
             children=language_children(request, code),
        )
        children.append(language_menu)
    return children        

def my_ltk_children(request):
    children = []
    children.append (MenuItem(
         capfirst(_("my documents")),
         url='/my_documents/'
        ))
    children.append (MenuItem(
         capfirst(_("my resources")),
         url='/my_resources/'
        ))
    return children        

def help_children(request):
    children = []
    children.append (MenuItem(
         capfirst(_("tutorials")),
         url='/help/tutorials/',
        ))
    children.append (MenuItem(
         capfirst(_("registration and authentication")),
         url='/help/register/',
        ))
    children.append (MenuItem(
         capfirst(_("user profile and user roles")),
         url='/help/profile/',
        ))
    children.append (MenuItem(
         capfirst(_("site navigation")),
         url='/help/navigation/',
        ))
    children.append (MenuItem(
         capfirst(_("analytics")),
         url='/help/analytics/',
        ))
    children.append (MenuItem(
         capfirst(_("internationalization")),
         url='/info/i18n/',
        ))
    return children

Menu.add_item("main", MenuItem(capfirst(_("about")),
                               url='/p',
                               weight=30,
                               check=True,
                               children=about_children,
                               separator=True))

Menu.add_item("main", MenuItem(capfirst(_("basic text processing")),
                               url='/',
                               icon='',
                               weight=30,
                               children=start_children,
                               separator=True))     

Menu.add_item("main", MenuItem(capfirst(_("language models")),
                               url='/',
                               icon='',
                               weight=30,
                               children=languages_children,
                               separator=True))     

Menu.add_item("main", MenuItem(capfirst(_("my LTK")),
                               url='/',
                               icon='',
                               weight=30,
                               children=my_ltk_children,
                               separator=True))     

Menu.add_item("main", MenuItem(capfirst(_("help")),
                               url='/p',
                               weight=30,
                               check=True,
                               children=help_children,
                               separator=True))
