from django.http import HttpRequest, JsonResponse

from .mail_services import *

import json

def newsletter_service(request: HttpRequest):
    print(request.POST)
    data = json.load(request)

    send_simple_message()
    #send_test_mail(data['email'])
    
    return JsonResponse(request.POST)