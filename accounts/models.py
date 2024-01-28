from django.db import models
from datetime import datetime
# Create your models here.
from django.contrib.auth.models import AbstractUser,User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone_number = models.CharField(max_length=15,unique=True)
    date_of_birth = models.DateField()
    age = models.IntegerField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
    bio = models.TextField(blank=True)
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    address_line = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state_province = models.CharField(max_length=100, null=True, blank=True)
    zip_code = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    account_creation_date = models.DateTimeField(auto_now_add=True)
    last_login_date = models.DateTimeField(auto_now=True)
    ROLES_CHOICES = [
        ('client', 'Client'),
        ('service_provider', 'Service Provider'),
        ('admin', 'Admin'),
    ]
    account_type = models.CharField(max_length=20, choices=ROLES_CHOICES, default='client')
    is_client = models.BooleanField(default=False)
    is_service_provider = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.user.username)


class LSP(models.Model):
    
    def upload_path(instance,filename):
        new_filename=f"{instance.user}.png"
        return f"LSP/{new_filename}"
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    lsp_type = models.CharField(max_length=100)
    display_picture = models.ImageField(upload_to=upload_path, blank=True)
    signature = models.ImageField(upload_to=upload_path, blank=True)
    enrollment_number = models.CharField(max_length=50, unique=True)
    bar_council_practicing_certificate = models.FileField(upload_to=upload_path, blank=True)
    enrollment_year = models.IntegerField()
    university_llb_completed = models.CharField(max_length=100)
    llb_passout_year = models.IntegerField()
    
    def __str__(self):
        return str(self.user.username)
    
        
class Message(models.Model):
    user_profile = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
   
   
# key = Fernet.generate_key()
# cipher_suite = Fernet(key) 
class Msg(models.Model):
    sender=models.CharField(max_length=120)
    receiver=models.CharField(max_length=120)
    message=models.CharField(max_length=1000000)
    encrypted_message = models.BinaryField(default=b'')
    date=models.DateTimeField(default=datetime.now,blank=True)
    file_status=models.BooleanField(default=False)
    file_name=models.CharField(max_length=1000000,default=None,null=True)

    # def save(self, *args, **kwargs):
    #     # Encrypt the message before saving
    #     encrypted_message = cipher_suite.encrypt(self.message.encode())
    #     self.encrypted_message = encrypted_message
    #     super().save(*args, **kwargs)

    # def __str__(self):
    #     # Decrypt the message when displaying it
    #     decrypted_message = cipher_suite.decrypt(self.encrypted_message).decode()
    #     return f"Sender: {self.sender}, Receiver: {self.receiver}, Message: {decrypted_message}, Date: {self.date}"
    
class Friend(models.Model):
    user=models.CharField(max_length=120)
    friend=models.CharField(max_length=120)
    nickname=models.CharField(max_length=120)

class Fileupload(models.Model):
    file=models.FileField(upload_to='uploaded_files/')



class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.message}'
    
    
class Doubts(models.Model):
    first_name = models.CharField(max_length=100, null=False)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(null=False)
    type_of_doubt = models.CharField(max_length=100, null=False)
    message = models.TextField(null=False)

    def _str_(self):
        return f"{self.first_name} {self.last_name}"