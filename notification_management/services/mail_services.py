from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings

from anymail.message import AnymailMessage

import requests
from requests.exceptions import RequestException

def send_simple_message():
    requests.post(
        "https://api.mailgun.net/v3/sandbox0fcd1f759bdf40eea61c72d5efbf5da0.mailgun.org/messages",
        auth=("api", "3549165238c280369a8f700c6e613255-623e10c8-35186a71"),
        data={
            "from": "Excited User <brad@mg.mailing-service.com>",
            "to": ["berdnika986@gmail.com"],
            "subject": "Hello",
            "text": "Testing some Mailgun awesomeness!"
        }
    )


def send_test_mail(recipient):
    print(recipient)
    mail = AnymailMessage(subject='Hello', body='hello world', from_email=settings.DEFAULT_FROM_EMAIL, to=[recipient])

    mail.send()