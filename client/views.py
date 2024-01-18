from django.shortcuts import render ,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from legaltech import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_str
from django.contrib.auth import authenticate, login, logout
from accounts.tokens import generate_token
from accounts.models import Profile,LSP
from django.shortcuts import get_object_or_404
from accounts import views
from accounts.models import LSP



    
def client_dashboard(request):
    return render(request,'client/client_dashboard.html')

def lsp_view(request):
    lsp=LSP.objects.all()
    return render(request,"client/lsp_view.html",{'lsp':lsp})
