from django.urls import path
from  . import views
from django.conf import settings
from django.conf.urls.static import static

app_name="client"


urlpatterns=[
     path("client_dashboard",views.client_dashboard,name="client_dashboard"),
     
     
     
    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)