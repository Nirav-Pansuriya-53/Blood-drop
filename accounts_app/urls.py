from django.urls import path
from accounts_app.views import SignUpView,LoginView

urlpatterns = [
    path('',SignUpView.as_view(),name='signup'),
    path('login/',LoginView.as_view(),name='login_view'),
    path("verify-otp/", LoginView.as_view(), name="")
]