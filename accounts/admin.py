from django.contrib import admin

from accounts.models import Profile,LSP,Msg,Friend,Fileupload
# Register your models here.

admin.site.register(Profile)
admin.site.register(LSP)

admin.site.register(Msg)
admin.site.register(Friend)
admin.site.register(Fileupload)