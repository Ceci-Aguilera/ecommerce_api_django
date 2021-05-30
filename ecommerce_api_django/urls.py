"""ecommerce_api_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls import url,include
from django.conf import settings
from django.conf.urls.static import static

from ecommerce_backend.views import HomeViewAPI
from ecommerce_accounts_app.views import GetCSRFToken

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', HomeViewAPI, name='home-view-api'),
    url(r'^csrf$', GetCSRFToken.as_view(), name='csrf-api'),
    url(r'^ecommerce-api/', include('ecommerce_backend.urls', namespace='ecommerce-backend-api')),
    url(r'^accounts-api/', include('ecommerce_accounts_app.urls', namespace='ecommerce-accounts-api')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
