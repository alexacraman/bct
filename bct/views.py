from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives, BadHeaderError
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.cache import cache_page

from .forms import ContactForm

@cache_page(60 * 60 * 24 * 365)
def home_page(request):
    return render(request, 'views/home_page.html', {})
@cache_page(60 * 60 * 24 * 365)
def volunteers_needed(request):
    return render(request, 'views/volunteer.html', {})
@cache_page(60 * 60 * 24 * 365)
def customers(request):
    return render(request, 'views/customers.html', {})
@cache_page(60 * 60 * 24 * 365)
def faqs(request):
    return render(request, 'views/faqs.html', {})
@cache_page(60 * 60 * 24 * 365)
def team(request):
    return render(request, 'views/team.html', {})


@login_required
def privacy_policy(request):
    return render(request, 'footer/policy.html', {})
    
@login_required
def tandc_policy(request):
    return render(request, 'footer/terms.html', {})

@login_required
def disclaimer_policy(request):
    return render(request, 'footer/disclaimer.html', {})

@login_required
def cookie_policy(request):
    return render(request, 'footer/cookie.html', {})


def contact_me(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            message = form.cleaned_data.get('message')
            text_content = f'Web form submission from {name}, their email is {email}. There message is {message}'
            html_content =f'<!DOCTYPE html> <html> <head> <meta charset="utf-8"> <title>New Web Form Submission</title> </head> <body> <div style="font-family: Arial, sans-serif; font-size: 14px; line-height: 1.5; margin: 0; padding: 0;"> <h1 style="font-size: 18px; font-weight: normal; margin: 0 0 10px; padding: 0;">New Web Form Submission</h1> <table style="border-collapse: collapse; width: 100%;"> <tr> <td style="padding: 5px 10px; border: 1px solid #ccc;">Name:</td> <td style="padding: 5px 10px; border: 1px solid #ccc;">{ name }</td> </tr> <tr> <td style="padding: 5px 10px; border: 1px solid #ccc;">Email:</td> <td style="padding: 5px 10px; border: 1px solid #ccc;">{ email }</td> </tr> <tr> <td style="padding: 5px 10px; border: 1px solid #ccc;">Phone:</td> <td style="padding: 5px 10px; border: 1px solid #ccc;"></td> </tr> <tr> <td style="padding: 5px 10px; border: 1px solid #ccc;">Message:</td> <td style="padding: 5px 10px; border: 1px solid #ccc;">{message}</td> </tr> </table> <p style="margin-top: 20px;">Thank you for your attention to this matter.</p> <p style="margin-top: 20px;"><br> </p> </div> </body> </html>' 
            company_email = settings.COMPANY_EMAIL
            try:
                emailMessage = EmailMultiAlternatives(
                subject      = "Web Submission",
                body         = text_content,
                from_email   = settings.DEFAULT_FROM_EMAIL,
                to           = [company_email],
                bcc          = ["journeybookingapp@gmail.com"],
                reply_to     = [email]
            )
                emailMessage.attach_alternative(html_content, "text/html")
                emailMessage.send(fail_silently=False)
            except BadHeaderError:
                messages.warning(request,"Invalid header discovered")
            messages.success(request, "Message Sent Sucessfully.")
            return redirect("home_page")             
    else:
        form = ContactForm()
    return render(request, 'views/contact.html', {'form': form})









# def contact_me(request):
#     if request.method == 'POST':
#         form = ContactForm(request.POST)
#         if form.is_valid():
#             recaptcha_response = request.POST.get('g-recaptcha-response')
#             url = 'https://www.google.com/recaptcha/api/siteverify'
#             values = {
#                 'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
#                 'response': recaptcha_response
#             }
#             data        = urllib.parse.urlencode(values).encode()
#             req         = urllib.request.Request(url, data=data)
#             response    = urllib.request.urlopen(req)
#             result      = json.loads(response.read().decode())
#             name        = form.cleaned_data['name']
#             form_email  = form.cleaned_data['email']
#             form_msg    = form.cleaned_data['message']
#             # recipients  =['journeybooking@protonmail.com']
#             if result['success']:
#                 print(result)
#                 text_content = f'Web form submission from {name}, their email is {form_email}. There message is {form_msg}'
#                 html_content =f'<!DOCTYPE html> <html> <head> <meta charset="utf-8"> <title>New Web Form Submission</title> </head> <body> <div style="font-family: Arial, sans-serif; font-size: 14px; line-height: 1.5; margin: 0; padding: 0;"> <h1 style="font-size: 18px; font-weight: normal; margin: 0 0 10px; padding: 0;">New Web Form Submission</h1> <table style="border-collapse: collapse; width: 100%;"> <tr> <td style="padding: 5px 10px; border: 1px solid #ccc;">Name:</td> <td style="padding: 5px 10px; border: 1px solid #ccc;">{ name }</td> </tr> <tr> <td style="padding: 5px 10px; border: 1px solid #ccc;">Email:</td> <td style="padding: 5px 10px; border: 1px solid #ccc;">{ form_email }</td> </tr> <tr> <td style="padding: 5px 10px; border: 1px solid #ccc;">Phone:</td> <td style="padding: 5px 10px; border: 1px solid #ccc;"></td> </tr> <tr> <td style="padding: 5px 10px; border: 1px solid #ccc;">Message:</td> <td style="padding: 5px 10px; border: 1px solid #ccc;">{form_msg}</td> </tr> </table> <p style="margin-top: 20px;">Thank you for your attention to this matter.</p> <p style="margin-top: 20px;"><br> </p> </div> </body> </html>' 
#                 try:
#                     emailMessage = EmailMultiAlternatives(
#                     subject      = "Web Submission",
#                     body         = text_content,
#                     from_email   = settings.DEFAULT_FROM_EMAIL,
#                     to           = ['journeybookingapp@gmail.com'],
#                     reply_to     = [form_email]
#                 )
#                     emailMessage.attach_alternative(html_content, "text/html")
#                     emailMessage.send(fail_silently=False)
#                 except BadHeaderError:
#                     messages.warning(request,"Invalid header discovered")
#                 messages.success(request, "Message Sent Sucessfully.")
#                 return redirect("company:dashboard")             
#     else:
#         form = ContactForm()
#     return render(request, 'views/contact.html', {'form': form})
