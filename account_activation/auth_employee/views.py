from rest_framework.views import APIView
from .serializers import UserSerializer, User
from rest_framework import status
from rest_framework.response import Response
from .tokens import account_activation_token
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from .utils import EmailThread
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.conf import settings


class UserRegisterAPI(APIView):
    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            obj = serializer.save()
            obj.is_active = False
            obj.save()
            domain = get_current_site(request=request).domain
            token = account_activation_token.make_token(obj)
            uid = urlsafe_base64_encode(force_bytes(obj.pk))
            relative_url = reverse('activate', kwargs={'uid':uid, 'token':token})
            absolute_url = f'http://%s'%(domain+relative_url,)
            message = "Hello %s,\n\t Thank you for creating account with us. Please click on the link below to activate your account\n %s"%(obj.username, absolute_url)
            subject = "Account Activation Email"
            EmailThread(subject=subject, message=message, recipient_list=[obj.email], from_email=settings.EMAIL_HOST_USER).start()
            return Response(data={'details':'Please Check your email for account activation mail'}, status=201)
        except Exception as e:
            print(e)
            return Response(data=serializer.errors, status=404)
        

class UserAccountActivate(APIView):
    def get(self, request, uid, token):
        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_id)
        except (TypeError, ValueError, OverflowError, user.DoesNotExist) as e:
            return Response(data={'details':'there is an error'}, status=400)
        if account_activation_token.check_token(user=user, token=token):
            user.is_active = True
            user.save()
            return Response(data={'detail':'Account Activated Successfully'}, status=200)
        return Response(data={'details':'Activate link invalid'}, status=400)
