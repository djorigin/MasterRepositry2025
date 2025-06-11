"""
URL configuration for GaiaDjango project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('systemcore/', include('systemcore.urls')),  # Include URLs from the systemcore app
    path('', include('systemcore.urls')),  # Redirect root URL to systemcore app
    # path('api/', include('api.urls')),  # Uncomment if you have an API app
    # path('auth/', include('auth.urls')),  # Uncomment if you have an authentication app
    # path('games/', include('games.urls')),  # Uncomment if you have a games app
    # path('users/', include('users.urls')),  # Uncomment if you have a users app
    # path('settings/', include('settings.urls')),  # Uncomment if you have a settings app
]
