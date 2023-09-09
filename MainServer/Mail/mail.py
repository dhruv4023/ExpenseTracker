import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from djangoserver.settings import EMAIL_HOST_USER
import random
MAIL_OTP = {}


@csrf_exempt
def sentOtp(request):
    if request.method == 'POST':
        try:
            to_mail = str(json.loads(request.body).get('email')).strip()
            otp = str(random.randint(100000, 999999))
            send_mail("OTP FOR dhruv4023.vercel.app", "Your OTP is "+otp+"\nThank you for visiting dhruv4023.vercel.app \nhave a nice day !",
                      EMAIL_HOST_USER, [to_mail], fail_silently=False)
            MAIL_OTP[to_mail] = otp
            # print(MAIL_OTP)
            return HttpResponse(json.dumps({"msg": "mail sent", "statusCode": True}), content_type='application/json')
        except json.JSONDecodeError:
            return HttpResponse(json.dumps({"msg": "Invalid JSON data", "statusCode": False}), content_type='application/json')
        except:
            return HttpResponse(json.dumps({"msg": "Server Error", "statusCode": False}), content_type='application/json')

    else:
        return HttpResponse(json.dumps({"msg": "Server Error", "statusCode": False}), content_type='application/json')


@csrf_exempt
def verifyOtp(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            name = body.get('name')
            email = body.get('email')
            otp = body.get('otp')
            if MAIL_OTP[email] == otp:
                MAIL_OTP.pop(email)
                return HttpResponse(json.dumps({"msg": "Verified", "id": id}), content_type='application/json')
            else:
                MAIL_OTP.pop(email)
                return HttpResponse(json.dumps({"msg": "Wrong OTP", "id": False}), content_type='application/json')
        except json.JSONDecodeError:
            return HttpResponse(json.dumps({"msg": "Invalid JSON data"}), content_type='application/json')
        except:
            return HttpResponse(json.dumps({"msg": "resend OTP and try again"}), content_type='application/json')

    else:
        return HttpResponse("Server Error")
