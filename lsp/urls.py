from django.urls import path
from  lsp import views
from django.conf import settings
from django.conf.urls.static import static

app_name="lsp"


urlpatterns=[
    
    path("lsp_dashboard",views.lsp_dashboard,name="lsp_dashboard"),
    # path("lsp_login",views.lsp_login,name="lsp_login"),
    # path('lsp_registration',views.lsp_registration,name="lsp_registration"),
    # path('users_list',views.users_list,name="users_list"),
    # path("lsp_dashboard",views.lsp_dashboard,name="lsp_dashboard"),
    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)