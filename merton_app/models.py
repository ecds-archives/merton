from django.db import models
from django.utils.safestring import mark_safe

from eulexistdb.manager import Manager
from eulexistdb.models import XmlModel

import eulxml
from eulxml import xmlmap
from eulxml.xmlmap.core import XmlObject
from eulxml.xmlmap.dc import DublinCore
from eulxml.xmlmap.fields import StringField, NodeField, StringListField, NodeListField, IntegerField
from eulxml.xmlmap.teimap import Tei, TeiDiv, TEI_NAMESPACE

# Create your models here.

class Fields(XmlObject):
    ROOT_NAMESPACES = {'tei': TEI_NAMESPACE}
    type = StringField('name()')
    text = StringField('text()')
    text_string = StringField('.')
    id = StringField('@xml:id')
    n = StringField('tei:head')
    lang = StringField('@xml:lang')
    target = StringField('@target')
    parent = NodeField('..', 'self') #Gets parent of the current node
    children = NodeListField('tei:div', 'self') #Gets children of the current node

class Bibliography(XmlObject):
    ROOT_NAMESPACES = {'tei' : TEI_NAMESPACE}
    title = StringField('tei:title')
    author = StringListField('tei:author')
    editor = StringListField('tei:editor')
    publisher = StringField('tei:publisher')
    pubplace = StringField('tei:pubPlace')
    date = StringField('tei:date')
    def contents_formatting(self):
    	cit = {
			'title': self.title,
    	 	'author': self.author[0],
    	  	'editors': self.editor[0] + " and " + self.editor[1]
		}
    	return mark_safe('<i>%(title)s</i>, by %(author)s. Edited by %(editors)s.' % cit)
    def formatted_citation(self):
        cit = {
            "author": '',
            "editor": '',
            "title": self.title,
            "pubplace": self.pubplace,
            "publisher":  self.publisher,
            "date": self.date
        }
        if self.author:
			if len(self.author) == 1:
				cit['author'] = '%s. ' % self.author[0]
			elif len(self.author) == 2:
				cit['author'] = '%s and %s. ' % self.author[0], self.author[1]
			else:
				cit['author'] = '%s, et. al. ' % self.author[0]
        if self.editor:
			for ed_name in self.editor:
				cit['editor'] = cit['editor'] + '%s, ' % ed_name
			cit['editor'] = cit['editor'] + 'ed. '

        return mark_safe('%(author)s%(editor)s<i>%(title)s</i>. %(pubplace)s: %(publisher)s, %(date)s.' \
                % cit)

class Page(XmlModel, Tei):
    ROOT_NAMESPACES = {'tei' : TEI_NAMESPACE}
    objects = Manager('//tei:div')
    name = StringField('name()')
    target = StringField('@target')
    dateline = StringListField('tei:dateline/tei:date/text()')
    text_string = StringField('tei:text')

class Search(XmlModel, TeiDiv):
    ROOT_NAMESPACES = {'tei' : TEI_NAMESPACE}
    objects = Manager('//tei:div')

class QuoteFields(XmlObject):
    ROOT_NAMESPACES = {'tei': TEI_NAMESPACE}
    quotation = NodeField('.', Fields)
    author = StringField('../tei:bibl/tei:author/tei:name/tei:choice/tei:sic')
    title = StringField('../tei:bibl/tei:title')

class AllPages(XmlObject):
    ROOT_NAMESPACES = {'tei': TEI_NAMESPACE}
    pages = NodeListField('//tei:div', Fields)
    quotes = NodeListField('//tei:quote', QuoteFields)
    
#For the header bibliography
class MertonBibliography(XmlObject):
	ROOT_NAMESPACES = {'tei': TEI_NAMESPACE}
	bibl = NodeField('//tei:titleStmt', Bibliography)
	def citation(self):
		return self.bibl.contents_formatting()
