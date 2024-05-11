from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import random
import string


#Added by Mohammed Rifad on 14th April 2024
def generate_verification_code():
    alphabet = string.ascii_lowercase
    random_words = [''.join(random.sample(alphabet, 3)) for _ in range(3)]
    random_string = '-'.join(random_words)
    return random_string

# Added by Fidha Naushad on 11th May 2024
def send_otp(email_subject, email_template, recipient_email, context):
    subject = email_subject
    html_message = render_to_string(email_template, context)
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to_email = recipient_email
    send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)