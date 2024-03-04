from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

# from django.contrib.auth import get_user_model

# admin.site.register(get_user_model())


urlpatterns = [
    path('', views.index, name='home'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('signout/', auth_views.LogoutView.as_view(), name='signout'),
    path('profile/', views.profile, name= 'profile'),
    path('contact/', views.contactView, name= 'contact')
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)