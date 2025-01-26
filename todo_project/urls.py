from django.contrib import admin
from django.urls import path, include
from todo import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/logout/', views.custom_logout, name='logout'),
    path('accounts/logged_out', views.custom_logout, name='logged_out'),
    path('accounts/register/', views.register, name='register'),
    path('', include('todo.urls')),

]
