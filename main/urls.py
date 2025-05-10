from django.urls import path
from .views import custom_login_view, signup_view, dashboard_view
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', custom_login_view, name='login'),    # ← your view here
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('', dashboard_view, name='dashboard'),
]
