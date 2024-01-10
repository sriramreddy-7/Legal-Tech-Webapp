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
from django.urls import path
from accounts import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    
    path('admin/', admin.site.urls),
    path("",views.home,name="home"),
    path("home",views.home2,name="home"), 
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    # path("admin_base",views.admin_base,name="admin_base"),
    
    #registration's
    path("client_registration",views.client_registration,name="client_registration"),
    path("user_registration",views.user_registration,name="user_registration"),
    path('lsp_registration',views.lsp_registration,name="lsp_registration"),
    
    
    # login's
    path('user_login',views.user_login,name="user_login"),
    path("user_login",views.user_login,name="user_login"),
    
    path("logout",views.user_logout,name="logout"),
    
    
    #dashboard's
    path("admin_dashboard",views.admin_dashboard,name="admin_dashboard"),
    
    path('users_list',views.users_list,name="users_list"),
    path("lsp_dashboard",views.lsp_dashboard,name="lsp_dashboard"),
    
    path("service",views.service,name="service"),
    # path("lsp_base",views.lsp_base,name="lsp_base"),
    path("lsp_login",views.lsp_login,name="lsp_login"),
    path("lsp_dashboard",views.lsp_dashboard,name="lsp_dashboard"),
   
    path('admin_lsp_profile/<str:username>/',views.admin_lsp_profile,name="admin_lsp_profile"),
    path('verify_profile/<str:username>/',views.verify_profile,name="verify_profile"),
    
    
    # path("login",views.login,name="login"),
]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
        urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

# urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
# urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)





admin.site.site_header="Legal Tech Web App"
# admin.site.site_title=""
admin.site.index_title="Welcome to the Legal Tech Web App"