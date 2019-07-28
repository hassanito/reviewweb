from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views
from django.urls import path

app_name = 'accounts'

urlpatterns = [
    url(r"login/$", auth_views.LoginView.as_view(template_name="accounts/login.html"),name='login'),
    url(r"logout/$", auth_views.LogoutView.as_view(), name="logout"),
    url(r"signup/$", views.SignUp.as_view(), name="signup"),
    path('myprofile/', views.UserList.as_view(), name='user-detail'),
    path('profile/<int:pk>',views.UserProfile,name='user-profile'),

]
