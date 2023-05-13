from django.urls import path
from .views import *


urlpatterns = [
    path('', register, name='register'),
    path('login/', login_view, name='login'),
    path('account_details/', account_details, name='account_details'),
    path('withdraw/', perform_withdraw, name='withdraw'),
    path('deposit/', perform_deposit, name='deposit'),
    path('transfer/', perform_transfer, name='transfer'),
]
