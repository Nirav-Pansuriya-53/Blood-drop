from django.urls import path
from .views import IndexView, DonationView, DonorView, Donation

urlpatterns = [

    path('index/', IndexView.as_view(), name='index1'),
    path('donor-detail/', DonorView.as_view(), name='donordetail'),
    path('donation/', DonationView.as_view(), name='donation'),
    path('donation1/', Donation.as_view(), name='donation'),

]
