from django.urls import path
 
# importing views from views..py
from . import views


urlpatterns = [
    path('home', views.home, name='home'),
    path('', views.add_text, name='add_text'),
    path('delete/<int:pk>/', views.delete_text, name='delete_text'),
    path('create', views.create_view ),
]