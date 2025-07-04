from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.mail import send_mail
import random

@api_view(['POST'])
def send_otp(request):
    email=request.data.get('email')
     
    if not email or "@mits.ac.in" not in email :
        return Response({'message':'Invalid Outlook Email'},status=400)
    otp= str(random.randint(100000,999999))
    request.session['otp']=otp
    request.session['email']=email

    subject="Your Otp Code "
    message= f"Your Otp is :{otp} "

    try:
        send_mail(subject,message,'mrmc3301@outlook.com',[email])
        return Response({'message':'Otp Sent Successfully'})
    except Exception as e:
        return Response({'message':f'Failed to send email {str(e)}'},status=500)