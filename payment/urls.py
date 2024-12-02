from django.urls import path
from .views import ZarinpalPaymentRequest, ZarinpalPaymentVerify

urlpatterns = [
    path('payment-request/', ZarinpalPaymentRequest.as_view(), name='payment-request'),
    path('payment-verify/', ZarinpalPaymentVerify.as_view(), name='payment-verify'),
]
