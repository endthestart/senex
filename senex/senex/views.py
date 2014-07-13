from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from .forms import ContactForm
from .models import PromoBox
from senex_shop.news.models import Post


# Load Logging
import logging
logger = logging.getLogger("default")


def home(request, template_name='home.html'):
    posts = Post.objects.all()[:3]
    promo_boxes = PromoBox.objects.all()[:4]
    context = {
        'posts': posts,
        'promo_boxes': promo_boxes,
    }
    return render_to_response(template_name, context, RequestContext(request))

def css_test(request, template_name='css_test.html'):
    return render_to_response(template_name, {}, RequestContext(request))


def about(request, template_name='about.html'):
    return render_to_response(template_name, {}, RequestContext(request))


def contact(request, template_name='contact.html'):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            sender_email = form.cleaned_data['sender_email']
            sender_name = form.cleaned_data['sender_name']
            cc_myself = form.cleaned_data['cc_myself']

            recipients = ['info@senexcycling.com']
            if cc_myself:
                recipients.append(sender_email)

            from django.core.mail import send_mail

            email_message = "A new message from: {0}<br /><br />{1}".format(sender_name, message)

            send_mail(subject, email_message, sender_email, recipients)
            return HttpResponseRedirect('/contact/thanks/')

    context = {
        'form': form,
    }

    return render_to_response(template_name, context, RequestContext(request))


def contact_thanks(request, template_name="contact_thanks.html"):
    return render_to_response(template_name, {}, RequestContext(request))


def custom(request, template_name="custom.html"):
    return render_to_response(template_name, {}, RequestContext(request))
