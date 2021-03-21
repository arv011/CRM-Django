"""crm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import (LoginView, LogoutView, 
PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView)
from leads.views import Signupview

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('leads.urls', namespace='leads')),
    path('login/', LoginView.as_view(), name = 'login'),
    path('signup/', Signupview.as_view(), name = 'signup'),
    path('logout/', LogoutView.as_view(), name = 'logout'),
    path('passwordreset/', PasswordResetView.as_view(), name = 'passwordreset'),
    path('passwordresetdone/', PasswordResetDoneView.as_view(), name = 'password_reset_done'),
    path('passwordresetconfirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name = 'passwordresetconfirm'),
    path('passwordresetcomplete/', PasswordResetCompleteView.as_view(), name = 'password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns+= static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)