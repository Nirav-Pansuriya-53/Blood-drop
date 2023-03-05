from django.urls import path
from accounts_app.views import SignUpView,LoginView,VerifyOtpView,IndexView

urlpatterns = [
    path('sign-up/', SignUpView.as_view(), name='signup'),
    path('sign-in/', LoginView.as_view(), name='login'),
    path("verify-otp/", VerifyOtpView.as_view(), name="verify-otp"),
    path("login-successfully/", IndexView.as_view(), name="index"),
]