from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('portal/customer/login/', views.CustomerLoginView.as_view(), name='customer_login'),
    path('portal/staff/login/', views.StaffLoginView.as_view(), name='staff_login'),
    path('portal/customer/signup/', views.customer_signup, name='customer_signup'),
    path('portal/staff/signup/', views.staff_signup, name='staff_signup'),
    path('departments/', views.department_list, name='department_list'),
    path('departments/<slug:slug>/', views.department_detail, name='department_detail'),
]

