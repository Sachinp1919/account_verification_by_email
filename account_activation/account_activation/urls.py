from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import token_obtain_pair, token_refresh
from auth_employee.views import UserRegisterAPI, UserAccountActivate
urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/', include('employee_app.urls')),
    path('v1/', include('auth_employee.urls')),
    path('v1/account_activate/<token>/',UserRegisterAPI.as_view()),
    path('v1/account_reactive/<token>/', UserAccountActivate.as_view()),
    path('v1/access/', token_obtain_pair),
    path('v1/refresh/', token_refresh)
]
