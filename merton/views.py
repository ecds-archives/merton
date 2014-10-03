import os
import re
import tempfile, zipfile
from django.core.servers.basehttp import FileWrapper
import mimetypes

from merton_app.models import *
from merton_app.forms import *

from django.conf import settings
from django.http import Http404,HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

import xml.etree.ElementTree as ET

display_xsl = os.path.join('file:///' + settings.BASE_DIR, 'static', 'xsl', 'tei.xsl')

def get_pages():
#    Querying the database this way was taking too long
#    pages = Search.objects.all()
#    Solution: Converted contents into XML file on server, read contents there
#    This solution should be much faster
    tree = ET.parse(os.path.join(settings.STATIC_URL, 'xml', 'contents.xml'))
    root = tree.getroot()
    pages = []
    n = 0
    for item in root:
        pages.append({'id': item.attrib['id'], 'title': item.attrib['text'], 'number': n})
        n = n+1
    return pages

def index(request):
    context = {}
    return render_to_response('index.html',context,context_instance=RequestContext(request))

def about(request):
    context = {}
    return render_to_response('about.html',context,context_instance=RequestContext(request))

def contents(request):
    context = {}
    context['pages'] = get_pages()
    return render_to_response('contents.html', context, context_instance=RequestContext(request))

def display_page(request, doc_id):
    context = {}
    if doc_id == 'credits':
        return render_to_response('credits.html', context, context_instance=RequestContext(request))
    url_params = request.GET
    print 'url_params are' , request.GET
    if 'keyword' in url_params and url_params['keyword']:
        context['keywords'] = re.findall(r'\w+', url_params['keyword'])
        context['keyword_url'] = url_params['keyword']
        filt = {'highlight': url_params['keyword']}
    else:
        filt = {}
    try:
        pages = Search.objects.filter(**filt)
        currentpage = pages.get(id__exact=doc_id)
        allpages = get_pages()
        currentpagenumber = -1
        for i in range(0,len(allpages)): # Locate index of the current page
            if allpages[i]['id'] == currentpage.id:
                currentpagenumber = i
                break
        if currentpagenumber != -1: # Get next and previous pages
            if currentpagenumber-1 >= 0:
                context['prev'] = allpages[currentpagenumber-1]
            if currentpagenumber+1 < len(allpages):
                context['next'] = allpages[currentpagenumber+1]
    except:
        print 'No page found with doc_id=%s' % doc_id
        raise Http404
    formatted = currentpage.xsl_transform(filename=display_xsl) # Put page through XSL doc
    context['page'] = currentpage
    context['format'] = formatted.serialize()
    return render_to_response('display_page.html', context, context_instance=RequestContext(request))

def search(request):
    form = SearchForm(request.GET)
    context = {'searchform':form}
    search_opts = {}
    if form.is_valid():
        kw = '' # Search keyword
        if 'keyword' in form.cleaned_data and form.cleaned_data['keyword']:
            kw = form.cleaned_data['keyword']
            search_opts['fulltext_terms'] = '%s' % form.cleaned_data['keyword']
            search_opts['highlight'] = True # Turn on highlighting
        pagesobj = Search.objects.filter(**search_opts).order_by('-fulltext_score')
        pages = pagesobj.all()
        context['pages'] = pages
        context['keyword'] = kw
        context['keywords'] = re.findall(r'\w+', kw)
    else:
        context['keyword'] = '<empty>'
    return render_to_response('search.html',context,context_instance=RequestContext(request))

def send_file(request):
    filename  = os.path.join(settings.BASE_DIR, 'static', 'txt', 'merton_diary.txt' )
    download_name = 'merton_diary.txt'
    wrapper      = FileWrapper(open(filename))
    content_type = mimetypes.guess_type(filename)[0]
    response     = HttpResponse(wrapper,content_type=content_type)
    response['Content-Length']      = os.path.getsize(filename)    
    response['Content-Disposition'] = "attachment; filename=%s"%download_name
    return response
