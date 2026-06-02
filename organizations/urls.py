from django.urls import path
from .views import TrialRegistrationView

urlpatterns = [
    path(
        "trial/register/",TrialRegistrationView.as_view(),name="trial-register"),
]