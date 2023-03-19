from django.urls import path
from .views import IndexView
urlpatterns = [

    path('', IndexView.as_view(), name='index1'),
    # path('sign-up/', SignUpView.as_view(), name='signup')
]
