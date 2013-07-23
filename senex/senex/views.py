from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from senex.forms import ContactForm


def home(request, template_name='home.html'):
    return render_to_response(template_name, {}, RequestContext(request))


def about(request, template_name='about.html'):
    return render_to_response(template_name, {}, RequestContext(request))


def contact(request, template_name='contact.html'):
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
    else:
        form = ContactForm()

    return render_to_response(template_name, {'form': form}, RequestContext(request))


def contact_thanks(request, template_name="contact_thanks.html"):
    return render_to_response(template_name, {}, RequestContext(request))

def custom(request, template_name="custom.html"):
    return render_to_response(template_name, {}, RequestContext(request))

def mountain(request, template_name="mountain_index.html"):
    return render_to_response(template_name, {}, RequestContext(request))


def road(request, template_name="road_index.html"):
    return render_to_response(template_name, {}, RequestContext(request))
