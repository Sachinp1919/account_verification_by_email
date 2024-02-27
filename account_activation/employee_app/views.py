from rest_framework.views import APIView
from .serializers import EmployeeSerializer
from .models import Employee
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
import logging
from .utils import EmailThread
from django.conf import settings



logger = logging.getLogger('mylogger')

class EmployeeAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            employee = Employee.objects.all()
            serializer = EmployeeSerializer(employee, many=True)
            logger.info('Data fetch successfully')
            user_email = request.data.get('email')
            subject = 'test email'
            message = 'users data Fetch'
            if user_email:
                EmailThread(
                    subject = subject,
                    message=message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[user_email]
                ).start()
                return Response(data={'details':'testing email'})
            return Response(data=serializer.data, status=200)
        except:
            logger.error('Data fetching time error')
            return Response(data={'details':'there is an error fetching data'}, status=400)
        
    def post(self, request):
        try:
            serializer = EmployeeSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            logger.info('Data insert successfully')
            user_email = request.data.get('email')
            subject = 'test email'
            message = 'users data Added'
            if user_email:
                EmailThread(
                    subject = subject,
                    message=message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[user_email]
                ).start()
                return Response(data={'details':'testing email'})
            return Response(data=serializer.data, status=201)
        except:
            logger.error('Insertion timing error')
            return Response(data=serializer.errors, status=400)
        
class EmployeeDetailsAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, pk=None):
        try:
            employee = Employee.objects.get(pk=pk)
            serializer = EmployeeSerializer(employee)
            return Response(data=serializer.data, status=200)
        except:
            return Response(data={'details':'Fetching error on details API'}, status=400)
        
    def put(self, request, pk=None):
        try:
            employee = Employee.objects.get(pk=pk)
            serializer = EmployeeSerializer(data=request.data, instance=employee)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            logger.info('updated data')
            user_email = request.data.get('email')
            subject = 'test email'
            message = 'Users data Updating'
            if user_email:
                EmailThread(
                    subject = subject,
                    message=message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[user_email]
                ).start()
                return Response(data={'details': 'User Update successfully'})

            return Response(data=serializer.data, status=205)
        except Employee.DoesNotExist as e:
            logger.error('No matching data found')
            return Response(data={'details':'not found'}, status=404)
        except:
            logger.error('Error On Updating time')
            return Response(data=serializer.errors, status=400)
        
    def delete(self, request, pk=None):
        try:
            employee = Employee.objects.get(pk=pk)
            employee.delete()
            logger.info('Delete Successfully')
            user_email = request.data.get('email')
            subject = 'test email'
            message = 'users data Delete'
            if user_email:
                EmailThread(
                    subject = subject,
                    message=message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[user_email]
                ).start()
                return Response(data={'details':'User Delete succesfully'})
            return Response(data=None, status=204)
        except:
            logger.error('Delete time error')
            return Response(data={'details':'Not found Data'}, status=400)
        
