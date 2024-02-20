from django.urls import path

from accounts import views

urlpatterns = [
    path('login/', views.login_attempt, name="login"),
    path('register/', views.Register, name='register'),
    path('otp/', views.otp, name="otp"),
    path('login-otp', views.login_otp, name="login_otp"),
    path('', views.thanku, name="thanku"),
    # logout_view
    path('logout/', views.logout_view, name="logout"),


]
