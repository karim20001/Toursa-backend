from django.urls import path
from .views import CombinedHomeAPIView, SearchTourAPIView, SingleTourAPIView, CheckPurchaseAPIView, MyTravelsAPIView

urlpatterns = [
    path('', CombinedHomeAPIView.as_view(), name='home'),
    path('search/', SearchTourAPIView.as_view(), name='search'),
    path('tours/<int:pk>/', SingleTourAPIView.as_view(), name='tour'),
    path('tours/<int:pk>/status/', CheckPurchaseAPIView.as_view(), name='status'),
    path('my-travels/', MyTravelsAPIView.as_view(), name='my_travels'),

]
