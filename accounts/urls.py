from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
    path("", views.users, name="users"),

    path('<int:user_id>/profile/', views.profile, name='profile'),

    path('<int:user_id>/follow/', views.follow, name='follow'),

    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("signup/", views.signup, name="signup"),
    path("delete/", views.delete, name="delete"),
    path("update/", views.update, name="update"),
    path("password/", views.change_password, name="change_password"),
]