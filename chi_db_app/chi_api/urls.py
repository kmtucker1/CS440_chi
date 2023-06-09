from django.urls import path

from . import views

urlpatterns = [
    path("home", views.home_page, name="home"),
    path("vehicles", views.vehicle_list, name='vehicle_list'),
    path("vehicle/<int:id>", views.vehicle, name='vehicle'),
    path("vehicle/<int:id>/update", views.update_vehicle, name='update_vehicle'),
    path("customer_list", views.customer_list, name='customer_list'),
    path("customer/<int:id>", views.customer, name='customer'),
    path("customer-form", views.customer_form, name='customer_form'),
    path('customer/<int:id>/update', views.update_customer, name='update_customer'),
    path('vehicle/<int:id>/add-history', views.add_vehicle_history, name='add_vehicle_history'),
    path('vehicle-form', views.vehicle_form, name='vehicle-form'),
    path("employee-list", views.employee_list, name='employee_list'),
    path("employee/<int:id>", views.employee, name='employee'),
    path("employee/<int:id>/sales-stats", views.employee_sales_stats, name='employee_sales_stats'),
    path("employee-form", views.employee_form, name="employee-form"),
    path('employee/delete/<int:employee_id>/', views.employee_delete, name='employee_delete'),
    path("customer/<int:id>/add_transaction", views.add_transaction, name='add_transaction'),
    path("employee-list/employee-search", views.employee_search, name='employee_search'),
    path("employee/<int:id>/update", views.update_employee, name="update_employee"),
    path('customer/delete/<int:customer_id>/', views.customer_delete, name='customer_delete'),
    path("customer/<int:id>/add_transaction", views.add_transaction, name='add_transaction'),
    path('vehicle/<int:id>/delete/', views.delete_vehicle, name='delete_vehicle')
]