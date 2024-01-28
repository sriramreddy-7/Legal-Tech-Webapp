from django.urls import path
from  . import views
from django.conf import settings
from django.conf.urls.static import static

app_name="client"


urlpatterns=[
     path("client_dashboard",views.client_dashboard,name="client_dashboard"),
     path("client_lsp_view",views.client_lsp_view,name="client_lsp_view"),
     path('client_lsp_profile/<str:username>/',views.client_lsp_profile,name="client_lsp_profile"),
     path('client_contact',views.client_contact,name="client_contact"),
     

    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)