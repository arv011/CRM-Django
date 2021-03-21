from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
# Create your models here.
class User(AbstractUser):
    is_organiser = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=False)
    

class Userprofile(models.Model):
    user = models.OneToOneField(User,on_delete= models.CASCADE)

    def __str__(self):
        return self.user.username

class Leads(models.Model):
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    age = models.IntegerField(default=0)
    assigned_agent = models.ForeignKey('Agent',blank= True,null=True , on_delete= models.SET_NULL)
    category = models.ForeignKey('Category',blank= True,null=True , on_delete= models.SET_NULL)
    organisation = models.ForeignKey(Userprofile, on_delete= models.CASCADE)
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    
    def __str__(self):
        return f"{self.firstname} {self.lastname}"

class Category(models.Model):
    Name = models.CharField(max_length=30)
    organisation = models.ForeignKey(Userprofile, on_delete= models.CASCADE)
    Number = models.IntegerField(default=0)

    def __str__(self):
        return self.Name

class Agent(models.Model):
    user = models.OneToOneField(User,on_delete= models.CASCADE)
    organisation = models.ForeignKey(Userprofile, on_delete= models.CASCADE)
    
    def __str__(self):
        return self.user.username

def post_user_created_signal(sender, instance, created, **kwargs):
    if created:
        Userprofile.objects.create(user=instance)
post_save.connect(post_user_created_signal, sender = User)