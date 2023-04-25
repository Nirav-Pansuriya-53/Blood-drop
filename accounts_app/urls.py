from django.urls import path
from accounts_app.views import (
    SignUpView, 
    LoginView, 
    VerifyOtpView, 
    IndexView, 
    AboutView, 
    DonationHistory, 
    LogoutView, 
    UserProfileUpdateView,
    UserProfileDisplayView,
    UserListView,
    BloodRequestCreateView,
    UserLogoUpdateView  )
from .views import CertificateView

urlpatterns = [
    path('sign-up/', SignUpView.as_view(), name='signup'),
    path('sign-in/', LoginView.as_view(), name='login'),
    path("verify-otp/<int:user_id>/", VerifyOtpView.as_view(), name="verify-otp"),
    path("index/", IndexView.as_view(), name="index"),
    path("about/", AboutView.as_view(), name="about"),
    path('certificate/<int:donation_pk>/', CertificateView.as_view(), name='certificate'),
    path('donation-history/<int:pk>/', DonationHistory.as_view(), name='donation_history'),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('update-profile/<int:pk>/', UserProfileUpdateView.as_view(), name="update_profile"),
    path('update-profile/', UserProfileDisplayView.as_view(), name="display_profile"),
    path('user-list/', UserListView.as_view(), name="user_list"),
    path('update-logo/<int:pk>/', UserLogoUpdateView.as_view(), name="update_logo"),
    path('request/', BloodRequestCreateView.as_view(), name="request"),
]