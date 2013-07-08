from django import forms


class ContactForm(forms.Form):
    sender_name = forms.CharField()
    sender_email = forms.EmailField()
    subject = forms.CharField(max_length=100)
    cc_myself = forms.BooleanField(required=False)
    message = forms.CharField(widget=forms.Textarea)
