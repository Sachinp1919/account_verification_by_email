from django.urls import path
from .views import EmployeeAPI, EmployeeDetailsAPI


urlpatterns = [
    path('employee/', EmployeeAPI.as_view()),
    path('employee/<int:pk>/', EmployeeDetailsAPI.as_view())
]