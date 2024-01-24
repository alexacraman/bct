import stripe
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import BadHeaderError, EmailMultiAlternatives
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import Donation

class DonationsListView(LoginRequiredMixin, ListView):
    model = Donation
    template_name = 'donate/donations.html'
    context_object_name = 'donations'
    paginate_by = 4
    ordering = 'timestamp'

def donation_json(request):
    data = {}
    donations = Donation.objects.all()
    for donor in donations:
        donor_data = {
            'donor_name': donor.donor_name,
            'email': donor.email,
            'amount': donor.amount,
            'timestamp': donor.timestamp
        }
        data.append(donor_data)
    return JsonResponse({'data': data})

def receive_donation(request):
    url = "https://donate.stripe.com/test_4gw8y9dVK2D13V6fYY"
    return JsonResponse({'url': url})

def donation_success(request):
    return render(request, 'donate/success.html', {})

@csrf_exempt
def webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)
        print('event', event)
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)
     
    if event.type == 'checkout.session.completed':
        session = event.data.object
        total = session.amount_total / 100
        amount      = total
        donor_name  = session.customer_details.name
        email       = session.customer_details.email
        postcode    = session.customer_details.address.postal_code
        Donation.objects.create(amount=amount, donor_name=donor_name, email=email, postcode=postcode)
        text_content = f'Dear { donor_name },Thank you very much for your kind donation of £{amount}.Yours Sincerely, Team at Billingshurst Community Transport.'
        html_content = f'''
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Donation Confirmation</title>
                    <h1>Thank You</h1>
                        </div>
                        <div class="confirmation-message">
                            <p>Dear { donor_name },</p>
                            <p>Thank you very much for your kind donation of £{amount} </p>
                            <p>Team at Billingshurst Community Transport.</p>
                        </div>
                        
                    </div>
                </body>
                </html>
                '''
        
        try:
            emailMessage = EmailMultiAlternatives(
            subject      = f"Donation to Billingshurst Community Transport.",
            body         = text_content,
            from_email   = settings.DEFAULT_FROM_EMAIL,
            to           = [email],
            reply_to     = [settings.DEFAULT_FROM_EMAIL]
            )
            emailMessage.attach_alternative(html_content, "text/html")
            emailMessage.send(fail_silently=False)
        except BadHeaderError as e:
            raise ValueError(e)
    return HttpResponse(status=200)

#  session {
#   "after_expiration": null,
#   "allow_promotion_codes": false,
#   "amount_subtotal": 1000,
#   "amount_total": 1000,
#   "automatic_tax": {
#     "enabled": false,
#     "status": null
#   },
#   "billing_address_collection": "auto",
#   "cancel_url": "https://stripe.com",
#   "client_reference_id": null,
#   "client_secret": null,
#   "consent": null,
#   "consent_collection": {
#     "payment_method_reuse_agreement": null,
#     "promotions": "none",
#     "terms_of_service": "none"
#   },
#   "created": 1703439184,
#   "currency": "gbp",
#   "currency_conversion": null,
#   "custom_fields": [],
#   "custom_text": {
#     "after_submit": null,
#     "shipping_address": null,
#     "submit": null,
#     "terms_of_service_acceptance": null
#   },
#   "customer": null,
#   "customer_creation": "if_required",
#   "customer_details": {
#     "address": {
#       "city": null,
#       "country": "GB",
#       "line1": null,
#       "line2": null,
#       "postal_code": "RH125YT",
#       "state": null
#     },
#     "email": "Alex@gmail.com",
#     "name": "Alex",
#     "phone": null,
#     "tax_exempt": "none",
#     "tax_ids": []
#   },
#   "customer_email": null,
#   "expires_at": 1703525584,
#   "id": "cs_test_a17FPBAvOnWjwqc0sILUUV2LLeifclpvM47G67UEwOqAnMYlo17LnomuRo",
#   "invoice": null,
#   "invoice_creation": {
#     "enabled": false,
#     "invoice_data": {
#       "account_tax_ids": null,
#       "custom_fields": null,
#       "description": null,
#       "footer": null,
#       "metadata": {},
#       "rendering_options": null
#     }
#   },
#   "livemode": false,
#   "locale": "auto",
#   "metadata": {},
#   "mode": "payment",
#   "object": "checkout.session",
#   "payment_intent": "pi_3OQvYNAr28tIH9rj1DYRkqY0",
#   "payment_link": "plink_1OQrkhAr28tIH9rjLKHuNt6w",
#   "payment_method_collection": "if_required",
#   "payment_method_configuration_details": {
#     "id": "pmc_1OQsGyAr28tIH9rjPcpALPGo",
#     "parent": null
#   },
#   "payment_method_options": {},
#   "payment_method_types": [
#     "card",
#     "link"
#   ],
#   "payment_status": "paid",
#   "phone_number_collection": {
#     "enabled": false
#   },
#   "recovered_from": null,
#   "setup_intent": null,
#   "shipping_address_collection": null,
#   "shipping_cost": null,
#   "shipping_details": null,
#   "shipping_options": [],
#   "status": "complete",
#   "submit_type": "donate",
#   "subscription": null,
#   "success_url": "https://stripe.com",
#   "total_details": {
#     "amount_discount": 0,
#     "amount_shipping": 0,
#     "amount_tax": 0
#   },
#   "ui_mode": "hosted",
#   "url": null
# }