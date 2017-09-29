from django.core.mail import send_mail, BadHeaderError
from django.core.validators import validate_email
from django import forms
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import json
from django.conf import settings
from .forms import ContactForm

@csrf_exempt
def email(request):
    if request.method == 'GET':
        form = ContactForm()
        return HttpResponse("This was a get request.")
    else:
        req_body = json.loads(request.body.decode())
        # validate all fields are not null
        for field_name, field_content in req_body.items():
            if field_content:
                pass
            else:
                return HttpResponseBadRequest("{} cannot be null.")
        # validate email address is in proper format
        try:
            validate_email(req_body['from_email'])
        except forms.ValidationError:
            return HttpResponseBadRequest("Invalid email")
        subject = req_body['subject']
        from_email = req_body['from_email']
        message = "Sender Name: {} {}\nMessage: {}".format(req_body['first_name'], req_body['last_name'], req_body['message'])
        try:
            send_mail(subject, message, from_email, [settings.MALLONEMAIL])
            return HttpResponse('Success! Thank you for your message.', 200)
        except BadHeaderError:
            return HttpResponse('Invalid header found.')