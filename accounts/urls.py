"""legaltech URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path,include
from accounts import views
from django.conf import settings
from django.conf.urls.static import static

app_name="accounts"

urlpatterns = [
    
    path('client_login',views.client_login,name="client_login"),
    path('user_logout',views.user_logout,name="user_logout"),
    path("client_registration",views.client_registration,name="client_registration"),
    path("lsp_login",views.lsp_login,name="lsp_login"),
    path('lsp_registration',views.lsp_registration,name="lsp_registration"),
    # path("login",views.login,name="login"),
    # path('admin/', admin.site.urls),
    # # path('accounts/',include('accounts.urls')),
    # path("",views.home,name="home"),
    # path("home",views.home2,name="home"), 
    # path('activate/<uidb64>/<token>', views.activate, name='activate'),
    # path("admin_base",views.admin_base,name="admin_base"),
    # path("admin_dashboard",views.admin_dashboard,name="admin_dashboard"),
    # path("lsp_dashboard",views.lsp_dashboard,name="lsp_dashboard"),
    # path("service",views.service,name="service"),
    # path("lsp_base",views.lsp_base,name="lsp_base"),
    # path("lsp_dashboard",views.lsp_dashboard,name="lsp_dashboard"),
   
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)




