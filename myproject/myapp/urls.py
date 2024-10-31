from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('data/', views.user_data, name='user_data'),
    path('add/', views.add_data, name='add_data'),
    path('edit/<int:pk>/', views.edit_data, name='edit_data'),
    path('delete/<int:pk>/', views.delete_data, name='delete_data'),
]
