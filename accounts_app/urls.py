from django.urls import path
from accounts_app.views import SignUpView, LoginView, VerifyOtpView, IndexView, AboutView
from .views import CertificateView

urlpatterns = [
    path('sign-up/', SignUpView.as_view(), name='signup'),
    path('sign-in/', LoginView.as_view(), name='login'),
    path("verify-otp/<int:user_id>/", VerifyOtpView.as_view(), name="verify-otp"),
    path("index/", IndexView.as_view(), name="index"),
    path("about/", AboutView.as_view(), name="about"),
    path('certificate/', CertificateView.as_view(), name='certificate'),
]