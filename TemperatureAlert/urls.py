from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('signup', views.signup, name="signup"),
    path('login', views.login_view, name="login_view"),
    path('changeCity', views.changeCity, name="change_city"),
    path('logout', views.logout_view, name="logout")
]
