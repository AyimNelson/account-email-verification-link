from django.urls import path  
from . import  views
from django.contrib.auth.views import LogoutView
from .views import CustomLoginView

urlpatterns = [  
    path('', views.home, name = 'home'),  
    path('form/', views.signup, name = 'signup'),  
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',  
        views.activate, name='activate'),
    path ('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path ('login/', CustomLoginView.as_view(), name='login'),
    
    
]