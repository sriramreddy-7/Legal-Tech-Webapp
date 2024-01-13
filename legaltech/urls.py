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
from home import views




urlpatterns = [
    path('admin/', admin.site.urls),
    path("lsp/",include('lsp.urls',namespace='lsp')),
    path("client/",include('client.urls',namespace="client")),
    path("admin_app/",include('admin_app.urls',namespace="admin_app")),
    path("accounts/",include('accounts.urls',namespace="accounts")),
    
    
    path("",views.home,name="home"),
    path("home",views.home,name="home"), 
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path("service",views.service,name="service"),
    path('chat/', views.chat_page, name='chat_page'),
    path('get_messages/', views.get_messages, name='get_messages'),
    path('post_message/', views.post_message, name='post_message'),
    
    
   

    
   
]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
        urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

# urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
# urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)





admin.site.site_header="Legal Tech Web App"
# admin.site.site_title=""
admin.site.index_title="Welcome to the Legal Tech Web App"



 # path("lsp_base",views.lsp_base,name="lsp_base"),
    # path("login",views.login,name="login"),
    # path("admin_base",views.admin_base,name="admin_base"),
    # path("home",include('home.urls',namespace="home")),
    #registration's
   
#    path("user_registration",views.user_registration,name="user_registration"),
    
    # login's
    # path('user_login',views.user_login,name="user_login"),
    # path("logout",views.user_logout,name="logout"),
    # path("user_login",views.user_login,name="user_login"),

    
    #dashboard's