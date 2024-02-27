from django.urls import path
from .views import UserRegisterAPI, UserAccountActivate


urlpatterns = [
    path('auth/', UserRegisterAPI.as_view(), name='register'),
    path('activate/<uid>/<token>/', UserAccountActivate.as_view(), name='activate')
]