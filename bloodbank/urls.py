from django.urls import path
from .views import (
    IndexView, 
    DonorView, 
    BloodBankHistory, 
    LoginView, 
    DonationCreateView, 
    CampScheduleView,
    CampScheduleDeleteView,
    CampScheduleUpdateView,
    CampScheduleDisplayView,
    UserSignupFromBloodbankView,
    SignupView,
    # BloodCountListView,
    LogoutView,
    BloodBankProfileView,
    BloodBankProfileUpdateView,
    BloodBankLogoUpdateView,
    )


urlpatterns = [

    path('index/<int:pk>/', IndexView.as_view(), name='index1'),

    path('donor-detail/', DonorView.as_view(), name='donordetail'),

    path('bloodbank-history/<int:pk>/', BloodBankHistory.as_view(), name='bloodbank_history'),

    path('login/', LoginView.as_view(), name="bloodbank_signin"),

    path('signup/', SignupView.as_view(), name="bloodbank_signup"),

    path('donation/form/', DonationCreateView.as_view(), name='donation_form'),

    path('camp-schedule/form/', CampScheduleView.as_view(), name='camp_form'),

    path('camp-schedule-update/update/<int:pk>/', CampScheduleUpdateView.as_view(), name='camp_update'),

    path('camp-schedule-delete/delete/<int:pk>/', CampScheduleDeleteView.as_view(), name='camp_delete'),

    path('camp-schedule/', CampScheduleDisplayView.as_view(), name='camp_display'),

    path('user-signup-bloodbank/', UserSignupFromBloodbankView.as_view(), name='user_signup_bloodbank'),
    # path('bloodbank-count/<int:pk>/', BloodCountListView.as_view(), name='blood'),
    path('bloodbank-profile/<int:pk>/', BloodBankProfileView.as_view(), name='bloodbank_profile'),
    path('bloodbank-profile-update/<int:pk>/', BloodBankProfileUpdateView.as_view(), name='bloodbank_profile_update'),
    path('bloodbank-logo-update/<int:pk>/', BloodBankLogoUpdateView.as_view(), name='bloodbank_logo_update'),
    path('bloodbank-logout/', LogoutView.as_view(), name='bloodbank_logout'),

]
