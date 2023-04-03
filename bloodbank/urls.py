from django.urls import path
from .views import IndexView, DonorView, BloodBankHistory, LoginView, DonationCreateView

urlpatterns = [

    path('index/', IndexView.as_view(), name='index1'),
    path('donor-detail/', DonorView.as_view(), name='donordetail'),
    path('bloodbank-history/<int:pk>/', BloodBankHistory.as_view(), name='bloodbank_history'),
    path('login/', LoginView.as_view(), name="login"),
    path('donation/form/', DonationCreateView.as_view(), name='donation_form')

]
