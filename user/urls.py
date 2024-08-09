from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenObtainPairView,
    TokenVerifyView,
)

from user.views import (
    CreateUserView,
    ManageUserView,
    UserListView,
    UserDetailView,
)

app_name = "user"

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="register"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("me/", ManageUserView.as_view(), name="manage_user"),
    path("list/", UserListView.as_view(), name="user_list"),
    path("list/<int:pk>/", UserDetailView.as_view(), name="user_detail"),
]
