from django.urls import path
from . import views

app_name = 'charter'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('developer/', views.developer_view, name='developer'),
    
    # Auth APIs
    path('api/auth/login/', views.auth_login_api, name='auth_login'),
    path('api/auth/register/', views.auth_register_api, name='auth_register'),
    path('logout/', views.auth_logout_view, name='logout'),
    
    # Operations APIs
    path('api/charter/submit/', views.submit_charter_api, name='submit_charter'),
    path('api/membership/submit/', views.submit_membership_api, name='submit_membership'),
    path('api/route-calculator/', views.route_calculator_api, name='route_calculator'),
    path('api/fleet/', views.fleet_api, name='fleet_api'),
]
