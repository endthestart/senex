from django.views.generic import TemplateView
from django.shortcuts import render_to_response
from django.template import RequestContext


def home(request, template_name='home.html'):
    return render_to_response(template_name, {}, RequestContext(request))

def about(request, template_name='about.html'):
    return render_to_response(template_name, {}, RequestContext(request))

def contact(request, template_name='contact.html'):
    return render_to_response(template_name, {}, RequestContext(request))