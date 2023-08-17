#from modeltranslation.admin import TranslationAdmin
from pathlib import Path
from django.shortcuts import render
from modeltranslation.models import  FieldTranslation, trans_attr, trans_is_fuzzy_attr, checksum
import modeltranslation
tmp = 'Path'
import os
def module_exists(tmp):

    try:
        __import__(tmp)
        print('ok1')
    except ImportError:
        print('ok2')
        return False
    else:
        print('ok3')
        return True

module_exists('TranslationAdmin')


import pkgutil
# this is the package we are inspecting -- for example 'email' from stdlib
import email
package = email
package = modeltranslation
for importer, modname, ispkg in pkgutil.iter_modules(package.__path__):
    print ("Found submodule %s (is a package: %s)" % (modname, ispkg))