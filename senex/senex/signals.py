from django.db.models.signals import post_save
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


def send_registration_email(sender, **kwargs):
    user = kwargs['instance']
    text_template = 'senex_shop/email/user_registration_body.txt'
    subject_template = 'senex_shop/email/user_registration_subject.txt'
    context = {'user': user}
    email_text = render_to_string(text_template, context)
    email_subject = render_to_string(subject_template, context)
    if kwargs['created']:
        send_mail(email_subject, email_text, 'info@senexcycles.com', [user.email])

post_save.connect(send_registration_email, sender=settings.AUTH_USER_MODEL)