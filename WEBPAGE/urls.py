
from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.register ,name='register'),
    path('login/',views.login ,name='login'),
    path('logout/',views.logout ,name='logout'),
    path('',views.home ,name='home'),
    path('dashboard/',views.dashboard ,name='dashboard'),
    path('books/',views.books ,name='books'),
    
    path('user/<int:id>/', views.user, name='user'),
]

