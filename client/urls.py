from django.urls import path
from  client import views
from django.conf import settings
from django.conf.urls.static import static
app_name="client"


urlpatterns=[
     path("client_dashboard",views.client_dashboard,name="client_dashboard"),
<<<<<<< HEAD
     path("client_lsp_view",views.client_lsp_view,name="client_lsp_view"),
     path('lsp_profile_view/<str:username>/',views.lsp_profile_view,name="lsp_profile_view"),
=======
     path("lsp_view",views.lsp_view,name="lsp_view"),
     
     
>>>>>>> a9d6ef9258dca79e93d230bedb7f10d419e5cc03
    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)