from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import json
from .forms import ContactForm

@csrf_exempt
def email(request):
    if request.method == 'GET':
        form = ContactForm()
        return HttpResponse("This was a get request.", 400)
    else:
        req_body = json.loads(request.body.decode())
        print(req_body)
        subject = req_body['subject']
        from_email = req_body['from_email']
        message = req_body['message']
        try:
            send_mail(subject, message, from_email, ['fake@fake.com'])
            return HttpResponse('Success! Thank you for your message.', 200)
        except BadHeaderError:
            return HttpResponse('Invalid header found.')



def success(request):
    return HttpResponse('Success! Thank you for your message.')