from django.urls import path
from .views import RegisterView, LoginView, ResetPasswordRequestView, ResetPasswordView


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("request-reset-password/", ResetPasswordRequestView.as_view()),
    path("reset-password/", ResetPasswordView.as_view()),
]