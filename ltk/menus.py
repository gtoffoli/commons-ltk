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
         'Regular expressions',
         url='/regexp/'
        ))
    children.append (MenuItem(
         'Language identification',
         url='/detect/'
        ))
    return children        

def languages_children(request):
    children = []
    for code, name in settings.LANGUAGES:
        children.append (MenuItem(
             name,
             url='/language/%s/set/' % code,
             # selected=lambda code: get_language(request)==code,
            ))
    children.append (MenuItem(
         'none',
         url='/language//set/',
        ))
    return children        

def my_ltk_children(request):
    children = []
    children.append (MenuItem(
         'My documents',
         url='/my_documents/'
        ))
    children.append (MenuItem(
         'My resources',
         url='/my_rrsources/'
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

Menu.add_item("main", MenuItem(capfirst(_("languages")),
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
