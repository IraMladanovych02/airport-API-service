from django.urls import path

from user.views import CreateUserView, LoginUserView, CreateTokenView

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create"),
    path("login/", LoginUserView.as_view(), name="login"),
    path("me/", CreateTokenView.as_view(), name="manage"),
]

app_name = "user"
